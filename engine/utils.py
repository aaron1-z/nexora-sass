"""
Utility functions for Nexora Intelligence Workbench
"""
import os
import re
import json
import hashlib
import logging
import time
import zipfile
from datetime import datetime, timezone
from typing import List, Dict, Any

# ---------- Core Directories ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("engine")

# ---------- Directory Management ----------
def ensure_dirs() -> None:
    """Ensure all required directories exist"""
    for d in (DATA_DIR, MODELS_DIR, CACHE_DIR):
        os.makedirs(d, exist_ok=True)

# ---------- Text Utilities ----------
def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()

def time_ago(ts: float) -> str:
    """Convert timestamp to human-readable time ago"""
    if not ts:
        return "unknown"
    diff = int(time.time() - ts)
    if diff < 60:
        return f"{diff}s ago"
    if diff < 3600:
        return f"{diff // 60}m ago"
    if diff < 86400:
        return f"{diff // 3600}h ago"
    return f"{diff // 86400}d ago"

def highlight(text: str, keys: List[str]) -> str:
    """Highlight keywords in text with HTML markup"""
    if not text or not keys:
        return text or ""
    highlighted = text
    for key in keys:
        if not key:
            continue
        pattern = re.compile(r"(" + re.escape(key) + r")", re.IGNORECASE)
        highlighted = pattern.sub(r"<mark class='hl'>\1</mark>", highlighted)
    return highlighted

# ---------- File Utilities ----------
def save_zip_bundle(path: str, files: Dict[str, Any]) -> None:
    """Save multiple files into a ZIP bundle"""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            if isinstance(data, str):
                data = data.encode("utf-8")
            z.writestr(name, data)
    log.info(f"Saved ZIP bundle: {path}")

def read_jsonl(path: str) -> List[Dict[str, Any]]:
    """Read JSONL file"""
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows

def append_jsonl(path: str, records: List[Dict[str, Any]]) -> None:
    """Append records to JSONL file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")

# ---------- Data Utilities ----------
def dedupe_by_id(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate rows by id field"""
    seen = set()
    unique = []
    for row in rows:
        rid = row.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            unique.append(row)
        elif not rid:
            unique.append(row)
    return unique

def hash_string(text: str) -> str:
    """Generate hash of string"""
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]

def parse_json_loose(text: str) -> Dict[str, Any]:
    """Parse JSON with fallback for malformed input"""
    if not text:
        return {}
    try:
        return json.loads(text)
    except Exception:
        pass
    # Try to extract JSON object
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return {}
    blob = m.group(0)
    # Try various fixes
    for cand in (blob, blob.replace("'", '"'), re.sub(r",\s*([}\]])", r"\1", blob.replace("'", '"'))):
        try:
            return json.loads(cand)
        except Exception:
            continue
    return {}

# ---------- Cache ----------
_cache: Dict[str, tuple] = {}  # key -> (timestamp, data)

def get_cached(key: str, ttl: int = 300) -> Any:
    """Get cached value if not expired"""
    if key in _cache:
        ts, data = _cache[key]
        if time.time() - ts < ttl:
            return data
    return None

def set_cached(key: str, data: Any) -> None:
    """Set cached value"""
    _cache[key] = (time.time(), data)

def clear_cache() -> None:
    """Clear all cache"""
    _cache.clear()

# ---------- Safe Export ----------
def safe_export_json(obj: Any) -> str:
    """Export object to JSON, handling non-serializable types"""
    def default(o):
        if hasattr(o, '__dict__'):
            return o.__dict__
        return str(o)
    return json.dumps(obj, indent=2, default=default, ensure_ascii=False)
