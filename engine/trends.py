"""
Sentiment/momentum analytics, co-occurrence, anomalies
"""
from typing import List, Dict, Any
from collections import Counter
import pandas as pd
import numpy as np

from .utils import log


def _extract_entities(title: str) -> List[str]:
    """Simple entity extraction from title"""
    if not title:
        return []
    words = title.split()
    # Capitals 2-6 chars or TitleCase words
    entities = []
    for w in words:
        w_clean = w.strip(",.;:()[]")
        if w_clean.isupper() and 2 <= len(w_clean) <= 6:
            entities.append(w_clean)
        elif len(w_clean) > 2 and w_clean[0].isupper() and w_clean[1:].islower():
            entities.append(w_clean)
    return entities[:5]


def build_trends(flash: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build trend summary from flash data
    
    Returns:
        Dict with sentiment_avg, top_entities, top_catalysts, volatility, table (DataFrame)
    """
    if not flash:
        return {
            "sentiment_avg": 0.0,
            "top_entities": [],
            "top_catalysts": [],
            "volatility": 0.0,
            "table": pd.DataFrame(),
        }
    
    df = pd.DataFrame(flash)
    
    # Ensure list columns
    if "catalysts" not in df:
        df["catalysts"] = [[] for _ in range(len(df))]
    else:
        df["catalysts"] = df["catalysts"].apply(lambda x: x if isinstance(x, list) else [])
    
    if "entities" not in df:
        df["entities"] = df["title"].apply(_extract_entities)
    else:
        df["entities"] = df["entities"].apply(lambda x: x if isinstance(x, list) else [])
    
    # Sentiment avg
    df["sentiment"] = pd.to_numeric(df.get("sentiment", 0.0), errors="coerce").fillna(0.0)
    sentiment_avg = float(df["sentiment"].mean())
    
    # Volatility (stddev)
    volatility = float(df["sentiment"].std()) if len(df) > 1 else 0.0
    
    # Top catalysts and entities
    all_catalysts = [c for lst in df["catalysts"] for c in lst if c]
    all_entities = [e for lst in df["entities"] for e in lst if e]
    
    top_catalysts = Counter(all_catalysts).most_common(10)
    top_entities = Counter(all_entities).most_common(10)
    
    return {
        "sentiment_avg": sentiment_avg,
        "top_entities": top_entities,
        "top_catalysts": top_catalysts,
        "volatility": volatility,
        "table": df,
    }


def momentum_report(flash: List[Dict[str, Any]], short_window: int = 5, long_window: int = 12) -> Dict[str, Any]:
    """
    Calculate momentum (short vs long term sentiment)
    
    Returns:
        Dict with entity_momentum, catalyst_momentum, bursts
    """
    if len(flash) < short_window:
        return {
            "entity_momentum": [],
            "catalyst_momentum": [],
            "bursts": [],
        }
    
    # Sort by timestamp (most recent first)
    sorted_flash = sorted(flash, key=lambda x: x.get("timestamp", 0), reverse=True)
    
    # Entity momentum
    entity_sents = {}
    for it in sorted_flash:
        sent = it.get("sentiment", 0.0)
        entities = it.get("entities") or _extract_entities(it.get("title", ""))
        for e in entities:
            if e not in entity_sents:
                entity_sents[e] = []
            entity_sents[e].append(sent)
    
    entity_momentum = []
    for entity, sents in entity_sents.items():
        if len(sents) >= short_window:
            short_avg = np.mean(sents[:short_window])
            long_avg = np.mean(sents[:long_window]) if len(sents) >= long_window else short_avg
            delta = short_avg - long_avg
            entity_momentum.append((entity, round(short_avg, 3), round(long_avg, 3), round(delta, 3)))
    
    entity_momentum.sort(key=lambda x: abs(x[3]), reverse=True)
    
    # Catalyst momentum
    catalyst_sents = {}
    for it in sorted_flash:
        sent = it.get("sentiment", 0.0)
        catalysts = it.get("catalysts") or []
        for c in catalysts:
            if c not in catalyst_sents:
                catalyst_sents[c] = []
            catalyst_sents[c].append(sent)
    
    catalyst_momentum = []
    for catalyst, sents in catalyst_sents.items():
        if len(sents) >= short_window:
            short_avg = np.mean(sents[:short_window])
            long_avg = np.mean(sents[:long_window]) if len(sents) >= long_window else short_avg
            delta = short_avg - long_avg
            catalyst_momentum.append((catalyst, round(short_avg, 3), round(long_avg, 3), round(delta, 3)))
    
    catalyst_momentum.sort(key=lambda x: abs(x[3]), reverse=True)
    
    # Burst detection (recent mentions)
    entity_counts = Counter()
    for it in sorted_flash[:short_window]:
        entities = it.get("entities") or _extract_entities(it.get("title", ""))
        entity_counts.update(entities)
    
    bursts = entity_counts.most_common(10)
    
    return {
        "entity_momentum": entity_momentum[:10],
        "catalyst_momentum": catalyst_momentum[:10],
        "bursts": bursts,
    }
