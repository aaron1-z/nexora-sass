import asyncio, aiohttp, feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from .utils import clean_text, normalize_url, hash_string, log

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120 Safari/537.36"
)
_CONCURRENCY = 8

def _build_feed_urls(query: str) -> List[str]:
    q = query.replace(" ", "+")
    return [
        f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en",
        f"https://news.google.com/rss/search?q={q}%20site:reuters.com&hl=en-US&gl=US&ceid=US:en",
        f"https://news.google.com/rss/search?q={q}%20site:bloomberg.com&hl=en-US&gl=US&ceid=US:en",
    ]

async def _fetch(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status != 200: return ""
            return await resp.text(errors="ignore")
    except Exception:
        return ""

def _extract_text(html: str) -> str:
    if not html: return ""
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script","style","noscript","header","footer","svg"]): t.decompose()
    container = soup.find("article") or soup.find("main") or soup
    ps = [p.get_text(" ", strip=True) for p in container.find_all(["p","li"])][:220]
    return clean_text(" ".join(ps))

@asynccontextmanager
async def _session():
    async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as s:
        yield s

async def _fetch_bodies(session, items):
    sem = asyncio.Semaphore(_CONCURRENCY)
    async def job(it):
        async with sem:
            html = await _fetch(session, it["link"])
            it["text"] = _extract_text(html)
            return it
    return await asyncio.gather(*[job(i) for i in items])

async def ingest_query(query: str, max_items: int = 20) -> List[Dict[str, Any]]:
    urls = _build_feed_urls(query)
    entries = []
    seen = set()
    for u in urls:
        try:
            parsed = feedparser.parse(u)
            for e in parsed.entries:
                link = normalize_url(getattr(e, "link", ""))
                if not link: continue
                uid = hash_string(link)
                if uid in seen: continue
                seen.add(uid)
                title = getattr(e, "title", "")
                try:
                    published_at = (
                        datetime(*e.published_parsed[:6], tzinfo=timezone.utc).isoformat()
                        if getattr(e, "published_parsed", None) else None
                    )
                except Exception:
                    published_at = None
                entries.append({
                    "id": uid,
                    "title": title,
                    "link": link,
                    "source": getattr(e, "source", {}).get("title") if getattr(e, "source", None) else getattr(e, "source", None),
                    "published_at": published_at,
                })
        except Exception as ex:
            log.debug(f"Feed parse error: {ex}")
        if len(entries) >= max_items: break
    entries = entries[:max_items]
    async with _session() as s:
        full = await _fetch_bodies(s, entries)
    for it in full:
        it["text"] = it.get("text", "")
    return full
