from typing import List, Dict, Any, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import networkx as nx
from pyvis.network import Network
import tempfile
import os

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

def build_network_graph(items: List[Dict[str, Any]], max_nodes: int = 50) -> str:
    """Build an interactive network graph showing relationships between entities and catalysts.
    Returns HTML string for embedding."""
    if not items:
        return "<p>No data for network graph.</p>"
    
    # Build network
    G = nx.Graph()
    
    # Extract entities and catalysts
    entity_counts = Counter()
    catalyst_counts = Counter()
    edges = []
    
    for it in items:
        title = it.get("title", "")
        words = title.split()
        # Simple entity extraction (uppercase words)
        entities = [w.strip(",.;:()[]") for w in words if w.isupper() and 2 <= len(w) <= 6][:3]
        catalysts = it.get("catalysts", [])
        
        for ent in entities:
            entity_counts[ent] += 1
        for cat in catalysts:
            catalyst_counts[cat] += 1
        
        # Connect entities to catalysts
        for ent in entities:
            for cat in catalysts:
                edges.append((ent, cat))
    
    # Add top nodes
    top_entities = [e for e, _ in entity_counts.most_common(15)]
    top_catalysts = [c for c, _ in catalyst_counts.most_common(10)]
    
    for ent in top_entities:
        G.add_node(ent, size=entity_counts[ent]*3, color="#4CAF50", title=f"Entity: {ent}")
    
    for cat in top_catalysts:
        G.add_node(cat, size=catalyst_counts[cat]*5, color="#FF9800", title=f"Catalyst: {cat}")
    
    # Add edges
    edge_counts = Counter(edges)
    for (n1, n2), weight in edge_counts.items():
        if n1 in G.nodes and n2 in G.nodes:
            G.add_edge(n1, n2, weight=weight)
    
    if len(G.nodes) == 0:
        return "<p>No network data available.</p>"
    
    # Create pyvis network
    net = Network(height="500px", width="100%", bgcolor="#0e1117", font_color="white")
    net.from_nx(G)
    net.toggle_physics(True)
    
    # Generate HTML
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
            net.save_graph(f.name)
            with open(f.name, 'r') as hf:
                html = hf.read()
            os.unlink(f.name)
        return html
    except Exception as e:
        return f"<p>Error generating network: {e}</p>"
