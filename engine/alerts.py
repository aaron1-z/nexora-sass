from typing import List, Dict, Any, Tuple
from collections import Counter
from .utils import clean_text
from .sentiment import score_sentiment

def calculate_urgency(sentiment: float, catalyst_count: int, trigger_count: int) -> str:
    """Calculate urgency level: High, Medium, Low."""
    score = abs(sentiment) * 2 + catalyst_count * 0.5 + trigger_count
    if score >= 4.0:
        return "High"
    elif score >= 2.0:
        return "Medium"
    else:
        return "Low"

def find_correlations(items: List[Dict[str, Any]], min_cooccurrence: int = 3) -> List[Tuple[str, str, int]]:
    """Find frequently co-occurring catalyst pairs."""
    pairs = Counter()
    for it in items:
        cats = it.get("catalysts", [])
        if len(cats) >= 2:
            for i, c1 in enumerate(cats):
                for c2 in cats[i+1:]:
                    pair = tuple(sorted([c1, c2]))
                    pairs[pair] += 1
    
    correlations = [(c1, c2, count) for (c1, c2), count in pairs.items() if count >= min_cooccurrence]
    correlations.sort(key=lambda x: x[2], reverse=True)
    return correlations[:10]

def generate_alerts(items: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
    alerts = []
    keys = [k.lower() for k in keywords if k]
    for it in items:
        text = " ".join([it.get("title",""), clean_text(", ".join(it.get("catalysts", [])))])
        trig = [k for k in keys if k in text.lower()]
        s = float(it.get("sentiment", 0.0))
        cat_count = len(it.get("catalysts", []))
        
        if trig or abs(s) >= 0.6 or cat_count >= 3:
            urgency = calculate_urgency(s, cat_count, len(trig))
            alerts.append({
                "title": it.get("title"),
                "link": it.get("link"),
                "source": it.get("source"),
                "triggers": trig,
                "sentiment": s,
                "catalysts": it.get("catalysts", []),
                "urgency": urgency,
                "timestamp": it.get("timestamp", 0),
            })
    
    # prioritize strongest signals
    urgency_map = {"High": 3, "Medium": 2, "Low": 1}
    alerts.sort(key=lambda x: (urgency_map.get(x["urgency"], 0), len(x["triggers"]), abs(x["sentiment"]), len(x["catalysts"])), reverse=True)
    return alerts[:15]
