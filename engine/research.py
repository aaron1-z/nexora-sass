"""
Topic clustering and source analytics
"""
from typing import List, Dict, Any
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from .utils import log, clean_text


def cluster_topics(flash: List[Dict[str, Any]], k: int = 6) -> List[Dict[str, Any]]:
    """
    Cluster topics using TF-IDF + KMeans
    
    Args:
        flash: List of headlines
        k: Number of clusters
        
    Returns:
        List of cluster dicts with: cluster, count, top_terms, items
    """
    if not flash or len(flash) < k:
        return []
    
    try:
        # Build text corpus
        texts = []
        for it in flash:
            text = clean_text(f"{it.get('title', '')} {it.get('summary', '')}")
            texts.append(text if text else "empty")
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words="english",
            max_df=0.8,
            min_df=2
        )
        X = vectorizer.fit_transform(texts)
        
        # KMeans clustering
        n_clusters = min(k, len(flash))
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
        labels = kmeans.fit_predict(X)
        
        # Get feature names
        feature_names = vectorizer.get_feature_names_out()
        
        # Build cluster summaries
        clusters = []
        for cid in range(n_clusters):
            indices = [i for i, label in enumerate(labels) if label == cid]
            if not indices:
                continue
            
            # Get top terms for this cluster
            centroid = kmeans.cluster_centers_[cid]
            top_idx = centroid.argsort()[-8:][::-1]
            top_terms = [feature_names[i] for i in top_idx]
            
            # Get items in this cluster
            cluster_items = [flash[i] for i in indices]
            
            clusters.append({
                "cluster": int(cid),
                "count": len(indices),
                "top_terms": top_terms,
                "items": cluster_items[:12],  # Limit to 12 items
            })
        
        # Sort by count
        clusters.sort(key=lambda x: x["count"], reverse=True)
        
        log.info(f"Clustered {len(flash)} items into {len(clusters)} clusters")
        return clusters
        
    except Exception as e:
        log.error(f"Clustering failed: {e}")
        # Return single cluster as fallback
        return [{
            "cluster": 0,
            "count": len(flash),
            "top_terms": ["news", "update", "market"],
            "items": flash[:12],
        }]


def source_heatmap(flash: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Generate source distribution heatmap data
    
    Returns:
        DataFrame with columns: source, count
    """
    if not flash:
        return pd.DataFrame(columns=["source", "count"])
    
    sources = [it.get("source", "Unknown") for it in flash if it.get("source")]
    source_counts = Counter(sources)
    
    df = pd.DataFrame(source_counts.most_common(15), columns=["source", "count"])
    return df
