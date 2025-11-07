import os, re, json, hashlib, logging, time
from datetime import datetime, timezone
from typing import List, Dict, Any, Iterable

# ---------- Core Directories ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# ---------- Logging ----------
_LOG_LEVEL = os.environ.get("NEXORA_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, _LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("engine")

# ---------- Directory Management ----------
def ensure_dirs() -> None:
    for d in (DATA_DIR, MODELS_DIR, CACHE_DIR):
        os.makedirs(d, exist_ok=True)

# ---------- Utility ----------
def safe_filename(name: str, max_len: int = 128) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name)[:max_len]

def normalize_url(url: str) -> str:
    return (url or "").split("?")[0].rstrip("/")

def domain_of(url: str) -> str:
    try:
        host = re.sub(r"^https?://", "", url).split("/")[0]
        return host.lower()
    except Exception:
        return ""

def hash_string(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def short_hash(text: str, length: int = 8) -> str:
    return hash_string(text)[:length]

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def clean_text(text: str) -> str:
    if not text: return ""
    return re.sub(r"\s+", " ", str(text)).strip()

def chunk_text(text: str, max_tokens: int = 900, overlap: int = 100):
    words = (text or "").split()
    if not words: return []
    out, i = [], 0
    while i < len(words):
        j = min(i + max_tokens, len(words))
        out.append(" ".join(words[i:j]))
        if j == len(words): break
        i = max(0, j - overlap)
    return out

# ---------- File IO ----------
def read_jsonl(path: str):
    if not os.path.exists(path): return []
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try: rows.append(json.loads(line))
            except Exception: pass
    return rows

def append_jsonl(path: str, records: Iterable[Dict[str, Any]]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

# ---------- JSON ----------
def parse_json_loose(text: str) -> Dict[str, Any]:
    if not text: return {}
    try: return json.loads(text)
    except Exception: pass
    m = re.search(r"\{[\s\S]*\}", text)
    if not m: return {}
    blob = m.group(0)
    for cand in (blob, blob.replace("'", '"'), re.sub(r",\s*([}\]])", r"\1", blob.replace("'", '"'))):
        try: return json.loads(cand)
        except Exception: continue
    return {}

# ---------- Confidence & Rate Limit ----------
def score_confidence(num_matches: int, catalyst_overlap: int) -> str:
    s = 0
    s += 2 if num_matches >= 5 else 1 if num_matches >= 3 else 0
    s += 2 if catalyst_overlap >= 2 else 1 if catalyst_overlap >= 1 else 0
    return "High" if s >= 3 else "Medium" if s == 2 else "Low"

def rate_limit_key(key: str, seconds: int = 30) -> bool:
    p = os.path.join(DATA_DIR, f"rl_{safe_filename(key)}.stamp")
    now = time.time()
    try:
        if os.path.exists(p) and (now - os.path.getmtime(p)) < seconds:
            return False
    except Exception:
        pass
    try:
        with open(p, "w") as f: f.write(str(now))
    except Exception:
        pass
    return True

# ---------- Cache ----------
def cache_result(key: str, data: Any) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{hash_string(key)}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"time": time.time(), "data": data}, f)
    except Exception as e:
        log.warning(f"Cache write failed: {e}")

def get_cached(key: str, ttl: int = 300):
    path = os.path.join(CACHE_DIR, f"{hash_string(key)}.json")
    try:
        if not os.path.exists(path): return None
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if time.time() - payload["time"] < ttl:
            return payload["data"]
    except Exception:
        pass
    return None

def format_time_ago(ts: float) -> str:
    diff = int(time.time() - (ts or time.time()))
    if diff < 60: return f"{diff}s ago"
    if diff < 3600: return f"{diff // 60}m ago"
    if diff < 86400: return f"{diff // 3600}h ago"
    return f"{diff // 86400}d ago"

# ---------- Enhanced Analytics ----------
def calculate_sentiment_drift(items: List[Dict[str, Any]], window: int = 5) -> float:
    """Calculate sentiment drift between recent and older items."""
    if len(items) < window * 2:
        return 0.0
    sents = [float(it.get("sentiment", 0.0)) for it in items]
    recent = sum(sents[:window]) / window if len(sents) >= window else 0.0
    older = sum(sents[window:window*2]) / window if len(sents) >= window*2 else recent
    return recent - older

def calculate_volatility(items: List[Dict[str, Any]]) -> float:
    """Calculate sentiment volatility (standard deviation)."""
    sents = [float(it.get("sentiment", 0.0)) for it in items]
    if len(sents) < 2:
        return 0.0
    mean_sent = sum(sents) / len(sents)
    variance = sum((s - mean_sent) ** 2 for s in sents) / len(sents)
    return variance ** 0.5

def get_ai_signal(sentiment_avg: float, drift: float, volatility: float) -> str:
    """Determine AI signal based on metrics."""
    if sentiment_avg > 0.2 and drift > 0.1:
        return "⬆ Bullish"
    elif sentiment_avg < -0.2 and drift < -0.1:
        return "⬇ Bearish"
    elif volatility > 0.4:
        return "⚡ Volatile"
    else:
        return "⚖ Neutral"

def highlight_keywords(text: str, keywords: List[str]) -> str:
    """Highlight keywords in text with HTML markup."""
    if not keywords or not text:
        return text
    import re
    highlighted = text
    for kw in keywords:
        if not kw:
            continue
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        highlighted = pattern.sub(f'<mark style="background:#ffd700;color:#000;padding:2px 4px;border-radius:3px;">{kw}</mark>', highlighted)
    return highlighted

def generate_forecast_data(sentiment_avg: float, volatility: float, days: int = 30):
    """Generate simple forecast data for visualization."""
    import random
    random.seed(42)  # For consistency
    data = []
    current = sentiment_avg
    for i in range(days):
        # Random walk with mean reversion
        change = random.gauss(0, volatility * 0.3) + (sentiment_avg - current) * 0.1
        current = max(-1.0, min(1.0, current + change))
        data.append({"day": i + 1, "sentiment": round(current, 3)})
    return data
