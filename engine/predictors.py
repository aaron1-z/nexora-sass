from typing import List, Dict, Any, Tuple
import pandas as pd
from collections import defaultdict

def _rolling_mean(series: List[float], n: int) -> float:
    if not series: return 0.0
    if len(series) < n: n = len(series)
    if n <= 0: return 0.0
    return float(sum(series[-n:]) / n)

def momentum_report(items: List[Dict[str, Any]], window_short: int = 5, window_long: int = 12) -> Dict[str, Any]:
    """
    Compute momentum (short vs long) for entities & catalysts, plus burst detection.
    """
    if not items: return {"entity_momentum": [], "catalyst_momentum": [], "bursts": []}

    # group sentiment by entity / catalyst in arrival order
    ent_series = defaultdict(list)
    cat_series = defaultdict(list)

    for it in items:
        sent = float(it.get("sentiment", 0.0))
        ents = it.get("entities") or []
        cats = it.get("catalysts") or []
        for e in ents: ent_series[e].append(sent)
        for c in cats: cat_series[c].append(sent)

    def calc_momentum(series_map):
        rows: List[Tuple[str, float, float, float]] = []
        for name, sers in series_map.items():
            short = _rolling_mean(sers, window_short)
            long  = _rolling_mean(sers, window_long)
            delta = short - long
            rows.append((name, short, long, delta))
        rows.sort(key=lambda x: x[3], reverse=True)
        return rows[:10]

    entity_mom = calc_momentum(ent_series)
    catalyst_mom = calc_momentum(cat_series)

    # burst = many mentions recently (frequency spike)
    freq_map = defaultdict(int)
    for it in items:
        for c in it.get("catalysts") or []:
            freq_map[c] += 1
        for e in it.get("entities") or []:
            freq_map[e] += 1
    bursts = sorted(freq_map.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "entity_momentum": entity_mom,
        "catalyst_momentum": catalyst_mom,
        "bursts": bursts,
    }
