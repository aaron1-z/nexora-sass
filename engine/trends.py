from collections import Counter
import pandas as pd
from typing import List, Dict, Any
from .utils import short_hash, format_time_ago, calculate_volatility

def _entities_from_title(title: str) -> List[str]:
    if not title: return []
    words = [w.strip(",.:;()[]") for w in title.split()]
    caps = [w for w in words if (w.isupper() and 2 <= len(w) <= 6)]
    proper = [w for w in words if len(w) > 2 and w[0].isupper() and w[1:].islower()]
    ents = list(dict.fromkeys(caps + proper))
    return ents[:8]

def build_trends(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not items:
        return {"top_entities": [], "top_catalysts": [], "sentiment_avg": 0.0,
                "table": pd.DataFrame(columns=["Title","Source","Sentiment","catalysts","time","link"])}

    df = pd.DataFrame(items)
    # normalize columns
    if "catalysts" not in df: df["catalysts"] = [[]]
    df["catalysts"] = df["catalysts"].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))
    df["sentiment"] = pd.to_numeric(df.get("sentiment", 0.0), errors="coerce").fillna(0.0)
    df["entities"]  = df["title"].map(_entities_from_title)

    cat_counts = Counter(c for lst in df["catalysts"].tolist() for c in lst if c)
    ent_counts = Counter(e for lst in df["entities"].tolist()  for e in lst if e)

    top_catalysts = cat_counts.most_common(10)
    top_entities  = ent_counts.most_common(12)
    sentiment_avg = float(df["sentiment"].mean())

    # display table
    df["time"] = df["timestamp"].apply(format_time_ago) if "timestamp" in df else ""
    df.rename(columns={"title":"Title","source":"Source"}, inplace=True)
    df["Sentiment"] = df["sentiment"].round(2)
    df["id"] = df["Title"].apply(short_hash)

    table = df[["id","Title","Source","Sentiment","catalysts","time","link"]]

    # Calculate volatility index
    volatility = calculate_volatility(items)
    
    return {
        "top_entities": top_entities,
        "top_catalysts": top_catalysts,
        "sentiment_avg": sentiment_avg,
        "volatility": volatility,
        "table": table,
    }

def sentiment_evolution(items: List[Dict[str, Any]]) -> pd.DataFrame:
    """Track sentiment evolution over time for key entities."""
    if not items:
        return pd.DataFrame(columns=["timestamp", "entity", "sentiment"])
    
    rows = []
    for it in items:
        ts = it.get("timestamp", 0)
        sent = float(it.get("sentiment", 0.0))
        entities = it.get("entities") or _entities_from_title(it.get("title", ""))
        for ent in entities[:3]:  # Top 3 entities per item
            rows.append({"timestamp": ts, "entity": ent, "sentiment": sent})
    
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    
    # Aggregate by entity and time buckets
    df["time_bucket"] = pd.to_datetime(df["timestamp"], unit="s").dt.floor("5min")
    grouped = df.groupby(["time_bucket", "entity"])["sentiment"].mean().reset_index()
    return grouped.sort_values("time_bucket")
