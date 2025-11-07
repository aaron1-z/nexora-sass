"""
Async RSS fetcher for Google News with multi-term expansion
"""
import asyncio
import feedparser
import time
import random
from typing import List, Dict, Any
from datetime import datetime, timezone

from .utils import log, hash_string, clean_text, get_cached, set_cached


def expand_terms(q: str) -> List[str]:
    """Lightweight term expansion with synonyms and adjacencies"""
    terms = [q]
    words = q.lower().split()
    
    # Industry adjacencies
    expansions = {
        "ai": ["artificial intelligence", "machine learning"],
        "chip": ["semiconductor", "processor"],
        "market": ["industry", "sector"],
        "ban": ["restriction", "regulation"],
        "export": ["trade", "supply"],
    }
    
    for word in words:
        if word in expansions:
            terms.extend(expansions[word])
    
    # Return unique terms, limit to avoid overload
    return list(dict.fromkeys(terms))[:3]


def _build_feed_url(query: str) -> str:
    """Build Google News RSS URL for query"""
    q = query.replace(" ", "+")
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"


async def _fetch_feed_async(url: str) -> List[Dict[str, Any]]:
    """Fetch and parse RSS feed asynchronously"""
    def _parse():
        try:
            return feedparser.parse(url)
        except Exception as e:
            log.error(f"Feed parse error: {e}")
            return None
    
    # Run feedparser in thread executor to avoid blocking
    loop = asyncio.get_event_loop()
    parsed = await loop.run_in_executor(None, _parse)
    
    if not parsed or not hasattr(parsed, 'entries'):
        return []
    
    entries = []
    for e in parsed.entries[:30]:
        try:
            link = getattr(e, "link", "")
            if not link:
                continue
            
            title = getattr(e, "title", "")
            
            # Try to get published time
            pub_time = time.time()
            if hasattr(e, "published_parsed") and e.published_parsed:
                try:
                    dt = datetime(*e.published_parsed[:6], tzinfo=timezone.utc)
                    pub_time = dt.timestamp()
                except Exception:
                    pass
            
            # Extract source
            source = "News"
            if hasattr(e, "source") and e.source:
                if isinstance(e.source, dict):
                    source = e.source.get("title", "News")
                else:
                    source = str(e.source)
            
            entries.append({
                "id": hash_string(link),
                "title": title,
                "summary": getattr(e, "summary", "")[:200],
                "source": source,
                "link": link,
                "timestamp": pub_time,
                "sentiment": random.uniform(-0.3, 0.3),  # Random proxy
                "credibility": 0.9,
                "catalysts": ["RSS", "Headline"],
                "entities": [],
            })
        except Exception as e:
            log.debug(f"Entry parse error: {e}")
            continue
    
    return entries


async def fetch_live_news(limit: int = 20, query: str = "", expand: bool = True) -> List[Dict[str, Any]]:
    """
    Fetch live news from Google News RSS
    
    Args:
        limit: Maximum number of items to return
        query: Search query
        expand: Whether to expand query with related terms
        
    Returns:
        List of headline dictionaries
    """
    if not query:
        query = "technology news"
    
    # Check cache
    cache_key = f"news:{query}:{expand}"
    cached = get_cached(cache_key, ttl=300)  # 5 min TTL
    if cached:
        log.info(f"Cache hit for query: {query}")
        return cached[:limit]
    
    # Expand query if requested
    queries = [query]
    if expand:
        queries = expand_terms(query)
        log.info(f"Expanded query to: {queries}")
    
    # Fetch all feeds concurrently
    all_entries = []
    tasks = []
    
    for q in queries:
        url = _build_feed_url(q)
        tasks.append(_fetch_feed_async(url))
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_entries.extend(result)
            elif isinstance(result, Exception):
                log.warning(f"Feed fetch error: {result}")
    except Exception as e:
        log.error(f"Failed to fetch news: {e}")
        return []
    
    # Deduplicate by id
    seen = set()
    unique = []
    for entry in all_entries:
        eid = entry.get("id")
        if eid not in seen:
            seen.add(eid)
            unique.append(entry)
    
    # Sort by timestamp (most recent first)
    unique.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    
    # Limit results
    result = unique[:limit]
    
    # Cache result
    set_cached(cache_key, result)
    
    log.info(f"Fetched {len(result)} news items for query: {query}")
    return result
