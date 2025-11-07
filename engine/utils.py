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
