
"""
search_engine.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Semantic Search Engine (Version 4.0)
=========================================
"""

import pickle
from pathlib import Path

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import (
    BUS_CSV,
    DOCUMENTS_FILE,
    EMBEDDING_MODEL,
    FAISS_INDEX,
    TOP_K,
    validate_project,
)
from utils.intent import analyze_query


class BusSearchEngine:
    def __init__(self):
        validate_project()

        self.df = pd.read_csv(BUS_CSV)
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        with open(DOCUMENTS_FILE, "rb") as f:
            self.documents = pickle.load(f)

        self.index = faiss.read_index(str(FAISS_INDEX))

    def semantic_search(self, query: str, top_k: int = TOP_K):
        embedding = self.model.encode([query], convert_to_numpy=True)
        scores, ids = self.index.search(embedding, top_k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0 or idx >= len(self.df):
                continue
            row = self.df.iloc[int(idx)].to_dict()
            row["score"] = float(score)
            results.append(row)
        return results

    def apply_filters(self, results, intent):
        filtered = []

        for bus in results:
            if intent["from_city"] and str(bus.get("From_City", "")).lower() != intent["from_city"].lower():
                continue

            if intent["to_city"] and str(bus.get("To_City", "")).lower() != intent["to_city"].lower():
                continue

            if intent["bus_type"]:
                if intent["bus_type"].lower() not in str(bus.get("Bus_Type", "")).lower():
                    continue

            if intent["operator"]:
                if intent["operator"].lower() not in str(bus.get("Operator", "")).lower():
                    continue

            if intent["max_price"] is not None:
                try:
                    if float(bus.get("Fare", 0)) > intent["max_price"]:
                        continue
                except Exception:
                    pass

            amenities = str(bus.get("Amenities", "")).lower()
            if any(a.lower() not in amenities for a in intent["amenities"]):
                continue

            filtered.append(bus)

        if intent["sort"] == "cheapest":
            filtered.sort(key=lambda x: float(x.get("Fare", 0)))

        elif intent["sort"] == "rating":
            filtered.sort(key=lambda x: float(x.get("Rating", 0)), reverse=True)

        return filtered

    def search(self, query: str):
        intent = analyze_query(query)
        semantic = self.semantic_search(query)
        return self.apply_filters(semantic, intent)


if __name__ == "__main__":
    engine = BusSearchEngine()

    while True:
        q = input("\nAsk (or 'exit'): ")
        if q.lower() == "exit":
            break

        buses = engine.search(q)

        print(f"\nFound {len(buses)} bus(es)\n")

        for bus in buses[:5]:
            print(
                f"{bus['Operator']} | "
                f"{bus['From_City']} -> {bus['To_City']} | "
                f"{bus['Bus_Type']} | "
                f"₹{bus['Fare']} | "
                f"⭐ {bus['Rating']}"
            )
