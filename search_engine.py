
"""
search_engine.py
Production-ready foundation for TamilNadu-Private-OmniBus-AI-Chatbot
"""

import os
import pickle
import re
from typing import Dict, List, Optional

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import (
    BUS_CSV,
    DOCUMENTS_FILE,
    FAISS_INDEX,
    EMBEDDING_MODEL,
    TOP_K,
)

_model = None
_index = None
_documents = None
_df = None
_lookup = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def load_csv():
    global _df, _lookup
    if _df is None:
        _df = pd.read_csv(BUS_CSV)
        _lookup = {str(r["Bus_ID"]): r.to_dict() for _, r in _df.iterrows()}
    return _df


def load_documents():
    global _documents
    if _documents is None:
        with open(DOCUMENTS_FILE, "rb") as f:
            _documents = pickle.load(f)
    return _documents


def load_index():
    global _index
    if _index is None:
        _index = faiss.read_index(FAISS_INDEX)
    return _index


def _extract_bus_id(text: str) -> Optional[str]:
    m = re.search(r"Bus ID:\s*([A-Za-z0-9_-]+)", text)
    return m.group(1) if m else None


def semantic_search(query: str, top_k: int = TOP_K) -> List[Dict]:
    load_csv()
    docs = load_documents()
    idx = load_index()
    model = get_model()

    emb = model.encode([query], normalize_embeddings=True)
    scores, ids = idx.search(np.asarray(emb, dtype=np.float32), top_k)

    results = []

    for score, i in zip(scores[0], ids[0]):
        if i < 0:
            continue

        bus_id = _extract_bus_id(docs[i])
        if not bus_id:
            continue

        row = _lookup.get(bus_id)
        if row:
            item = dict(row)
            item["confidence"] = float(score)
            results.append(item)

    return results


def apply_filters(
    results: List[Dict],
    from_city=None,
    to_city=None,
    bus_type=None,
    operator=None,
    max_price=None,
):
    out = []

    for r in results:
        if from_city and str(r["From_City"]).lower() != from_city.lower():
            continue
        if to_city and str(r["To_City"]).lower() != to_city.lower():
            continue
        if bus_type and bus_type.lower() not in str(r["Bus_Type"]).lower():
            continue
        if operator and operator.lower() not in str(r["Operator"]).lower():
            continue
        if max_price is not None and float(r["Fare"]) > max_price:
            continue
        out.append(r)

    return out


def search_buses(query: str, filters: Optional[Dict] = None):
    filters = filters or {}

    results = semantic_search(query)

    results = apply_filters(
        results,
        from_city=filters.get("from_city"),
        to_city=filters.get("to_city"),
        bus_type=filters.get("bus_type"),
        operator=filters.get("operator"),
        max_price=filters.get("max_price"),
    )

    results.sort(
        key=lambda x: (
            x.get("confidence", 0),
            x.get("Rating", 0),
            x.get("Available_Seats", 0),
        ),
        reverse=True,
    )

    return results


if __name__ == "__main__":
    buses = search_buses("Luxury Sleeper bus from Bengaluru to Chennai")
    for bus in buses:
        print(
            f"{bus['Operator']} | "
            f"{bus['From_City']} -> {bus['To_City']} | "
            f"₹{bus['Fare']} | "
            f"⭐ {bus['Rating']}"
        )
