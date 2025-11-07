import os, json, time
from typing import List, Dict, Any
from .utils import DATA_DIR, safe_filename

WATCH_DIR = os.path.join(DATA_DIR, "watchlists")
ALERTS_PATH = os.path.join(DATA_DIR, "alerts_history.json")

os.makedirs(WATCH_DIR, exist_ok=True)

def save_watchlist(name: str, keywords: List[str]) -> None:
    path = os.path.join(WATCH_DIR, f"{safe_filename(name)}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"name": name, "keywords": keywords, "saved_at": time.time()}, f)

def load_watchlists() -> List[Dict[str, Any]]:
    items = []
    for fn in os.listdir(WATCH_DIR):
        if fn.endswith(".json"):
            try:
                with open(os.path.join(WATCH_DIR, fn), "r", encoding="utf-8") as f:
                    items.append(json.load(f))
            except Exception:
                pass
    return items

def save_alert_history(alerts: List[Dict[str, Any]]) -> None:
    try:
        with open(ALERTS_PATH, "w", encoding="utf-8") as f:
            json.dump({"time": time.time(), "alerts": alerts}, f)
    except Exception:
        pass

def load_alert_history() -> List[Dict[str, Any]]:
    try:
        with open(ALERTS_PATH, "r", encoding="utf-8") as f:
            p = json.load(f)
            return p.get("alerts", [])
    except Exception:
        return []
