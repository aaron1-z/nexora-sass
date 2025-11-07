import os
import json
import sqlite3
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from .utils import DATA_DIR, MODELS_DIR, ensure_dirs, append_jsonl, read_jsonl, hash_string, clean_text, log

MEMORY_JSONL = os.path.join(DATA_DIR, "memory.jsonl")
FAISS_PATH = os.path.join(DATA_DIR, "embeddings.faiss")
SQLITE_PATH = os.path.join(DATA_DIR, "articles.db")

class MemoryStore:
    """FAISS + JSONL + SQLite-backed memory for analyzed news/events."""

    def __init__(self) -> None:
        ensure_dirs()
        self.model_name = os.environ.get("NEXORA_EMBEDDER", "sentence-transformers/all-MiniLM-L6-v2")
        self.embedder: SentenceTransformer = self._load_embedder()
        self.dim = self.embedder.get_sentence_embedding_dimension()
        self.index = self._load_faiss_index()
        self.ids: List[str] = []
        self.meta: Dict[str, Dict[str, Any]] = {}
        self._load_memory_meta()
        self._ensure_sqlite()

    def _load_embedder(self) -> SentenceTransformer:
        try:
            return SentenceTransformer(self.model_name, cache_folder=MODELS_DIR)
        except Exception as e:
            log.warning("Falling back embedder due to: %s", e)
            return SentenceTransformer("all-MiniLM-L6-v2", cache_folder=MODELS_DIR)

    def _load_faiss_index(self):
        if os.path.exists(FAISS_PATH):
            try:
                return faiss.read_index(FAISS_PATH)
            except Exception as e:
                log.warning("Failed to load FAISS index, creating a new one: %s", e)
        return faiss.IndexFlatIP(self.dim)

    def _load_memory_meta(self) -> None:
        for r in read_jsonl(MEMORY_JSONL):
            rid = r.get("id")
            if not rid:
                continue
            self.ids.append(rid)
            self.meta[rid] = r

    def _ensure_sqlite(self) -> None:
        os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
        with sqlite3.connect(SQLITE_PATH) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                  id TEXT PRIMARY KEY,
                  url TEXT,
                  title TEXT,
                  source TEXT,
                  published_at TEXT,
                  text TEXT
                )
                """
            )
            conn.commit()

    def _persist_faiss(self) -> None:
        faiss.write_index(self.index, FAISS_PATH)

    def _persist_meta(self, new_records: List[Dict[str, Any]]) -> None:
        append_jsonl(MEMORY_JSONL, new_records)

    def add_documents(self, docs: List[Dict[str, Any]]) -> List[str]:
        """Add analyzed docs. Expected keys: id, title, text, link, source, published_at, summary, catalysts"""
        to_index: List[Tuple[str, str]] = []
        to_store_meta: List[Dict[str, Any]] = []

        for d in docs:
            rid = d.get("id") or hash_string(d.get("link", "") or d.get("title", ""))
            if rid in self.meta:
                continue
            text = clean_text(d.get("summary") or d.get("text") or d.get("title") or "")
            if not text:
                continue
            to_index.append((rid, text))
            to_store_meta.append({
                "id": rid,
                "title": d.get("title"),
                "url": d.get("link"),
                "source": d.get("source"),
                "published_at": d.get("published_at"),
                "summary": d.get("summary"),
                "catalysts": d.get("catalysts", []),
                "added_at": datetime.utcnow().isoformat(),
            })

        if not to_index:
            return []

        embeddings = self.embedder.encode([t for _, t in to_index], normalize_embeddings=True, show_progress_bar=False)
        emb = np.asarray(embeddings, dtype="float32")
        self.index.add(emb)

        for (rid, _), meta_row in zip(to_index, to_store_meta):
            self.ids.append(rid)
            self.meta[rid] = meta_row

        self._persist_faiss()
        self._persist_meta(to_store_meta)

        # Store raw docs in sqlite for traceability
        with sqlite3.connect(SQLITE_PATH) as conn:
            for d in docs:
                rid = d.get("id") or hash_string(d.get("link", "") or d.get("title", ""))
                try:
                    conn.execute(
                        "INSERT OR IGNORE INTO articles(id, url, title, source, published_at, text) VALUES (?, ?, ?, ?, ?, ?)",
                        (rid, d.get("link"), d.get("title"), d.get("source"), d.get("published_at"), d.get("text")),
                    )
                except Exception:
                    pass
            conn.commit()

        return [rid for rid, _ in to_index]

    def similarity_search(self, query: str, k: int = 3, lookback_days: int = 30) -> List[Dict[str, Any]]:
        if self.index.ntotal == 0 or not self.meta:
            return []
        q_emb = self.embedder.encode([query], normalize_embeddings=True)[0].astype("float32")[None, :]
        scores, idxs = self.index.search(q_emb, min(k, len(self.ids)))
        results: List[Dict[str, Any]] = []
        cutoff = datetime.utcnow() - timedelta(days=lookback_days)

        for score, idx in zip(scores[0], idxs[0]):
            if idx < 0 or idx >= len(self.ids):
                continue
            rid = self.ids[idx]
            m = self.meta.get(rid)
            if not m:
                continue
            pub = m.get("published_at")
            try:
                if pub:
                    dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                    if dt < cutoff:
                        continue
            except Exception:
                pass
            results.append({**m, "similarity": float(score)})
        return results[:k]
