"""
Async RSS fetcher for Google News with multi-term expansion
(FAST + SIGNAL-ENRICHED + SAFE)
"""

import asyncio
import feedparser
import time
import re
from typing import List, Dict, Any
from datetime import datetime, timezone

from .utils import log, hash_string, clean_text, get_cached, set_cached


# --------------------------------------------------
# Query expansion (bounded, signal-first)
# --------------------------------------------------

def expand_terms(q: str) -> List[str]:
    base = q.strip()
    terms = [base]
    ql = base.lower()

    expansions = {
        "tesla": ["Tesla earnings", "EV market", "electric vehicles"],
        "nvidia": ["Nvidia earnings", "AI chips", "data center demand"],
        "copper": ["copper prices", "industrial metals", "mining supply"],
        "quantum": ["quantum computing", "quantum hardware"],
        "ai": ["artificial intelligence", "AI regulation"],
        "semiconductor": ["chip industry", "fab capacity"],
    }

    for key, exps in expansions.items():
        if key in ql:
            terms.extend(exps)

    return list(dict.fromkeys(terms))[:4]


# --------------------------------------------------
# Feed URL
# --------------------------------------------------

def _build_feed_url(query: str) -> str:
    q = query.replace(" ", "+")
    return (
        "https://news.google.com/rss/search"
        f"?q={q}&hl=en-US&gl=US&ceid=US:en"
    )


# --------------------------------------------------
# Deterministic sentiment heuristic
# --------------------------------------------------

_POS = re.compile(r"\b(growth|surge|beat|record|strong|rally|expansion)\b", re.I)
_NEG = re.compile(r"\b(drop|decline|risk|cut|miss|pressure|slowdown)\b", re.I)

def estimate_sentiment(text: str) -> float:
    if not text:
        return 0.0

    t = text[:400]  # 👈 prevent regex overwork
    pos = len(_POS.findall(t))
    neg = len(_NEG.findall(t))

    if pos == 0 and neg == 0:
        return 0.0

    score = (pos - neg) / max(pos + neg, 1)
    return max(-0.5, min(0.5, score))


# --------------------------------------------------
# RSS fetch (timeout-safe)
# --------------------------------------------------

async def _fetch_feed_async(url: str) -> List[Dict[str, Any]]:
    def _parse():
        try:
            return feedparser.parse(url)
        except Exception as e:
            log.error(f"Feed parse error: {e}")
            return None

    try:
        loop = asyncio.get_running_loop()
        parsed = await asyncio.wait_for(
            loop.run_in_executor(None, _parse),
            timeout=4.0,   # 👈 HARD STOP
        )
    except asyncio.TimeoutError:
        log.warning("RSS fetch timed out")
        return []

    if not parsed or not hasattr(parsed, "entries"):
        return []

    entries: List[Dict[str, Any]] = []

    for e in parsed.entries[:25]:  # 👈 CAP
        try:
            link = getattr(e, "link", "")
            if not link:
                continue

            title = clean_text(getattr(e, "title", ""))
            summary = clean_text(getattr(e, "summary", ""))

            pub_ts = time.time()
            if getattr(e, "published_parsed", None):
                try:
                    dt = datetime(*e.published_parsed[:6], tzinfo=timezone.utc)
                    pub_ts = dt.timestamp()
                except Exception:
                    pass

            source = "News"
            if getattr(e, "source", None):
                source = (
                    e.source.get("title")
                    if isinstance(e.source, dict)
                    else str(e.source)
                )

            combined = f"{title}. {summary}"
            sentiment = estimate_sentiment(combined)

            entries.append({
                "id": hash_string(link),
                "title": title,
                "summary": summary[:600],
                "source": source,
                "link": link,
                "timestamp": pub_ts,
                "sentiment": sentiment,
                "credibility": 0.9,
                "catalysts": ["Headline"],
                "entities": [],
            })

        except Exception as e:
            log.debug(f"Entry parse error: {e}")

    return entries


# --------------------------------------------------
# Public API
# --------------------------------------------------

async def fetch_live_news(
    limit: int = 20,
    query: str = "",
    expand: bool = True,
) -> List[Dict[str, Any]]:

    if not query:
        query = "technology"

    cache_key = f"news:{query}:{expand}"
    cached = get_cached(cache_key, ttl=300)
    if cached:
        log.info(f"Cache hit for query: {query}")
        return cached[:limit]

    queries = expand_terms(query) if expand else [query]
    log.info(f"Expanded query to: {queries}")

    tasks = [
        _fetch_feed_async(_build_feed_url(q))
        for q in queries
    ]

    all_entries: List[Dict[str, Any]] = []

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if isinstance(r, list):
            all_entries.extend(r)

    seen = set()
    unique: List[Dict[str, Any]] = []
    for item in all_entries:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique.append(item)

    unique.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

    result = unique[:limit]
    set_cached(cache_key, result)

    log.info(f"Fetched {len(result)} enriched news items for query: {query}")
    return result
