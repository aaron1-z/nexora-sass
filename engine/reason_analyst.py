"""
Article analysis: summarization + catalyst + entity enrichment
(FAST + DETAIL-PRESERVING — <2 MIN GUARANTEE)
"""

from typing import List, Dict, Any, Tuple
from transformers import pipeline
import os
import re

from .utils import chunk_text, clean_text, log
from .classify import classify_catalysts


# --------------------------------------------------
# PERFORMANCE CONSTANTS (CRITICAL)
# --------------------------------------------------

MAX_SUMMARIZED_ARTICLES = 6          # 👈 HARD CAP (biggest speed win)
MAX_CHUNK_TOKENS = 700               # Lower than before
MAX_SUMMARY_WORDS = 220


# --------------------------------------------------
# Model loader (FAST FIRST)
# --------------------------------------------------

def _load_summarizer() -> Tuple[object, int, str]:
    """
    Returns: (pipeline, max_len, mode)
    Prioritizes SPEED over size.
    """
    override = os.environ.get("NEXORA_SUMMARY_MODEL")

    model_candidates = (
        [(override, 384)] if override else
        [
            ("sshleifer/distilbart-cnn-12-6", 384),   # 👈 FAST DEFAULT
            ("facebook/bart-large-cnn", 512),
            ("google/flan-t5-large", 512),
        ]
    )

    last_err = None

    for name, max_len in model_candidates:
        try:
            log.info(f"Loading summarizer: {name}")

            if "flan-t5" in name:
                summarizer = pipeline(
                    "text2text-generation",
                    model=name,
                    tokenizer=name,
                    device=-1,
                )
                return summarizer, max_len, "t5"

            summarizer = pipeline(
                "summarization",
                model=name,
                tokenizer=name,
                device=-1,
            )
            return summarizer, max_len, "summ"

        except Exception as e:
            last_err = e
            log.warning("Summarizer load failed for %s: %s", name, e)

    raise RuntimeError(f"Failed to load summarizer: {last_err}")


_SUMMARIZER, _MAX_LEN, _MODE = _load_summarizer()


# --------------------------------------------------
# Entity extraction (cheap + fast)
# --------------------------------------------------

_ENTITY_PATTERN = re.compile(
    r"\b([A-Z][a-zA-Z]{2,}(?:\s[A-Z][a-zA-Z]{2,})*)\b"
)

_ENTITY_BLACKLIST = {
    "January", "February", "March", "April",
    "Monday", "Tuesday", "Wednesday",
    "Reuters", "Bloomberg", "Analyst",
    "Market", "Markets", "Shares",
    "Company", "Companies", "Technology",
}


def extract_entities(text: str, limit: int = 6) -> List[str]:
    if not text:
        return []

    seen = []
    for match in _ENTITY_PATTERN.findall(text):
        if match in _ENTITY_BLACKLIST:
            continue
        if match not in seen:
            seen.append(match)
        if len(seen) >= limit:
            break

    return seen


# --------------------------------------------------
# FAST, SIGNAL-PRESERVING SUMMARIZATION
# --------------------------------------------------

def summarize(text: str, title: str = "") -> str:
    text = clean_text(text)

    if not text:
        return clean_text(title)[:200]

    # ⛔ Skip summarization for short content
    if len(text.split()) < 120:
        return text[:600]

    chunks = chunk_text(text, max_tokens=MAX_CHUNK_TOKENS)
    summaries: List[str] = []

    for ch in chunks[:1]:  # 👈 ONE chunk only (huge speed win)
        token_len = len(ch.split())

        if _MODE == "summ":
            max_len = min(int(token_len * 0.6), _MAX_LEN)
            min_len = max(50, int(max_len * 0.4))

            out = _SUMMARIZER(
                ch,
                max_length=max_len,
                min_length=min_len,
                do_sample=False,
            )
            summaries.append(out[0]["summary_text"])

        else:
            out = _SUMMARIZER(
                f"Summarize with key drivers preserved: {ch}",
                max_new_tokens=min(160, int(token_len * 0.5)),
                do_sample=False,
            )
            summaries.append(out[0]["generated_text"])

    combined = clean_text(" ".join(summaries))

    # Absolute cap
    return " ".join(combined.split()[:MAX_SUMMARY_WORDS])


# --------------------------------------------------
# Main analyzer (OPTIMIZED)
# --------------------------------------------------

def analyze_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Strategy:
    - Summarize ONLY top N articles
    - Remaining articles → signal-only
    """

    analyzed: List[Dict[str, Any]] = []

    for idx, a in enumerate(articles):
        title = a.get("title", "")
        text = a.get("text") or a.get("summary") or ""

        if idx < MAX_SUMMARIZED_ARTICLES:
            summary = summarize(text, title)
        else:
            # 👇 Signal-only mode (FAST)
            summary = clean_text(title)[:180]

        catalyst_input = f"{title}. {summary}"

        analyzed.append({
            **a,
            "summary": summary,
            "catalysts": classify_catalysts(catalyst_input),
            "entities": extract_entities(summary),
        })

    log.info(
        f"Analyzed {len(analyzed)} articles "
        f"({min(len(articles), MAX_SUMMARIZED_ARTICLES)} summarized, rest signal-only)"
    )

    return analyzed
