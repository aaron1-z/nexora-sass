from typing import List, Dict, Any, Tuple
from transformers import pipeline
import os

from .utils import MODELS_DIR, chunk_text, clean_text, log
from .classify import classify_catalysts

def _load_summarizer() -> Tuple[object, int, str]:
    """
    Returns: (pipeline, max_len, mode)
    mode ∈ {"summ", "t5"}
    """
    # Allow override via env
    override = os.environ.get("NEXORA_SUMMARY_MODEL")
    model_candidates = (
        [(override, 512)] if override else
        [("facebook/bart-large-cnn", 512),
         ("sshleifer/distilbart-cnn-12-6", 512),
         ("google/flan-t5-large", 512)]
    )
    last_err = None
    for name, max_len in model_candidates:
        if not name:
            continue
        try:
            if "flan-t5" in name:
                summarizer = pipeline(
                    "text2text-generation", model=name, tokenizer=name,
                    device_map="auto", cache_dir=MODELS_DIR,
                )
                return summarizer, max_len, "t5"
            else:
                summarizer = pipeline(
                    "summarization", model=name, tokenizer=name,
                    device_map="auto", cache_dir=MODELS_DIR,
                )
                return summarizer, max_len, "summ"
        except Exception as e:
            last_err = e
            log.warning("Summarizer load failed for %s: %s", name, e)
    raise RuntimeError(f"Failed to load summarizer: {last_err}")

_SUMMARIZER, _MAX_LEN, _MODE = _load_summarizer()

def summarize(text: str, title: str = "") -> str:
    text = clean_text(text)
    if not text:
        return clean_text(title)[:256]
    chunks = chunk_text(text, max_tokens=900)
    summaries: List[str] = []
    for ch in chunks or [text]:
        if _MODE == "summ":
            out = _SUMMARIZER(ch, max_length=min(180, _MAX_LEN), min_length=50, do_sample=False)
            summaries.append(out[0]["summary_text"])
        else:
            out = _SUMMARIZER(f"Summarize briefly: {ch}", max_new_tokens=160, do_sample=False)
            summaries.append(out[0]["generated_text"])
    combined = " ".join(summaries)
    if len(combined.split()) > 240:
        if _MODE == "summ":
            out = _SUMMARIZER(combined, max_length=200, min_length=80, do_sample=False)
            combined = out[0]["summary_text"]
        else:
            out = _SUMMARIZER(f"Summarize concisely for an executive: {combined}", max_new_tokens=160, do_sample=False)
            combined = out[0]["generated_text"]
    return clean_text(combined)

def analyze_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    analyzed: List[Dict[str, Any]] = []
    for a in articles:
        s = summarize(a.get("text") or "", a.get("title") or "")
        cats = classify_catalysts(" ".join([a.get("title", ""), s]))
        analyzed.append({**a, "summary": s, "catalysts": cats})
    return analyzed
