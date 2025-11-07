import feedparser, time
from typing import List, Dict, Any
from .utils import clean_text, normalize_url, hash_string, rate_limit_key, log
from .sentiment import score_sentiment
from .classify import classify_catalysts
from .credibility import score_credibility

FLASH_SOURCES = [
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
]

def fetch_live_news(limit: int = 25) -> List[Dict[str, Any]]:
    """Fast RSS flash feed with sentiment, catalysts, credibility."""
    if not rate_limit_key("flash_feed", seconds=8):
        return []

    all_items: List[Dict[str, Any]] = []
    try:
        for src in FLASH_SOURCES:
            parsed = feedparser.parse(src)
            for e in parsed.entries:
                link = normalize_url(getattr(e, "link", ""))
                title = clean_text(getattr(e, "title", ""))
                if not link or not title: continue
                summary = clean_text(getattr(e, "summary", ""))
                ts = time.time()
                it = {
                    "id": hash_string(link),
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "source": clean_text(getattr(e, "source", {}).get("title") if getattr(e, "source", None) else getattr(e, "source", "")),
                    "published_at": getattr(e, "published", "") or getattr(e, "updated", ""),
                    "timestamp": ts,
                }
                text = f"{title}. {summary}"
                it["sentiment"] = score_sentiment(text)
                it["catalysts"] = classify_catalysts(text)
                it["credibility"] = score_credibility(link)
                all_items.append(it)
    except Exception as ex:
        log.warning(f"Flash feed error: {ex}")

    # prioritize by impact (catalysts + sentiment + credibility)
    all_items.sort(key=lambda x: (len(x.get("catalysts", [])), abs(x.get("sentiment", 0.0)), x.get("credibility", 0.6)), reverse=True)
    uniq, seen = [], set()
    for it in all_items:
        if it["id"] in seen: continue
        seen.add(it["id"])
        uniq.append(it)
        if len(uniq) >= limit: break
    return uniq
