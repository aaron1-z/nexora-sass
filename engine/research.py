from typing import List, Dict, Any, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

from .utils import clean_text, domain_of

def _texts(items: List[Dict[str, Any]]) -> List[str]:
    out = []
    for it in items:
        out.append(clean_text(f"{it.get('title','')}. {it.get('summary','')}"))
    return out

def cluster_topics(items: List[Dict[str, Any]], k: int = 6) -> List[Dict[str, Any]]:
    if not items: return []
    texts = _texts(items)
    vec = TfidfVectorizer(max_features=2000, ngram_range=(1,2), stop_words="english")
    X = vec.fit_transform(texts)
    model = KMeans(n_clusters=min(k, len(items)), n_init="auto", random_state=42)
    labels = model.fit_predict(X)
    terms = vec.get_feature_names_out()

    clusters: List[Dict[str, Any]] = []
    for cid in sorted(set(labels)):
        idxs = [i for i, l in enumerate(labels) if l == cid]
        sub = [items[i] for i in idxs]
        # top terms for cluster centroid
        center = model.cluster_centers_[cid]
        top_ids = center.argsort()[-8:][::-1]
        top_terms = [terms[i] for i in top_ids]
        clusters.append({
            "cluster": int(cid),
            "count": len(sub),
            "top_terms": top_terms,
            "items": sub[:12],  # keep concise
        })
    clusters.sort(key=lambda x: x["count"], reverse=True)
    return clusters

def source_heatmap(items: List[Dict[str, Any]]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame(columns=["source","count"])
    hosts = [domain_of(it.get("link","")) for it in items]
    cnt = Counter(h for h in hosts if h)
    df = pd.DataFrame(cnt.items(), columns=["source","count"]).sort_values("count", ascending=False)
    return df
