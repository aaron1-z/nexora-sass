from typing import List, Dict, Any
from .utils import clean_text
from .sentiment import score_sentiment

def generate_alerts(items: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
    alerts = []
    keys = [k.lower() for k in keywords if k]
    for it in items:
        text = " ".join([it.get("title",""), clean_text(", ".join(it.get("catalysts", [])))])
        trig = [k for k in keys if k in text.lower()]
        s = float(it.get("sentiment", 0.0))
        if trig or abs(s) >= 0.6 or len(it.get("catalysts", [])) >= 3:
            alerts.append({
                "title": it.get("title"),
                "link": it.get("link"),
                "source": it.get("source"),
                "triggers": trig,
                "sentiment": s,
                "catalysts": it.get("catalysts", []),
            })
    # prioritize strongest signals
    alerts.sort(key=lambda x: (len(x["triggers"]), abs(x["sentiment"]), len(x["catalysts"])), reverse=True)
    return alerts[:12]
