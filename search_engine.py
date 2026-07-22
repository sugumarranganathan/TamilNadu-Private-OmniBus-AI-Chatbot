"""
search_engine.py
==========================================================
Tamil Nadu Private OmniBus AI Chatbot
Production Search Engine (Version 7.0)
Part 1 / 3
==========================================================
"""

import os
import pickle
import warnings

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import (
    MODEL_NAME,
    INDEX_FILE,
    DOCUMENTS_FILE,
    CSV_FILE,
    TOP_K,
)

from utils.normalizer import normalize_record
from utils.ranking import (
    rank_results,
    remove_duplicates,
)
from utils.helpers import (
    safe_float,
    safe_int,
    is_night_bus,
    is_morning_bus,
    is_afternoon_bus,
    is_evening_bus,
)

warnings.filterwarnings("ignore")


class BusSearchEngine:
    """
    Production Search Engine

    Responsibilities

    ✓ Load FAISS
    ✓ Load Sentence Transformer
    ✓ Load CSV
    ✓ Semantic Search
    ✓ Filtering
    ✓ Ranking
    """

    def __init__(self):

        print("=" * 60)
        print("Loading Tamil Nadu OmniBus AI Search Engine")
        print("=" * 60)

        self._load_model()
        self._load_documents()
        self._load_csv()
        self._load_index()

        print("Search Engine Ready.")
        print("=" * 60)

    # -----------------------------------------------------
    # Load Embedding Model
    # -----------------------------------------------------

    def _load_model(self):

        print("Loading SentenceTransformer...")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Model Loaded.")

    # -----------------------------------------------------
    # Load CSV
    # -----------------------------------------------------

    def _load_csv(self):

        print("Loading Bus Dataset...")

        self.df = pd.read_csv(CSV_FILE)

        print(f"Loaded {len(self.df)} Bus Records.")

    # -----------------------------------------------------
    # Load Documents
    # -----------------------------------------------------

    def _load_documents(self):

        print("Loading Semantic Documents...")

        with open(DOCUMENTS_FILE, "rb") as f:
            self.documents = pickle.load(f)

        print(f"Loaded {len(self.documents)} Documents.")

    # -----------------------------------------------------
    # Load FAISS Index
    # -----------------------------------------------------

    def _load_index(self):

        print("Loading FAISS Index...")

        self.index = faiss.read_index(INDEX_FILE)

        print(
            f"FAISS Index Loaded "
            f"({self.index.ntotal} vectors)"
        )

    # -----------------------------------------------------
    # Encode Query
    # -----------------------------------------------------

    def _embed_query(self, query: str):

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.astype("float32")

    # -----------------------------------------------------
    # Retrieve Candidates
    # -----------------------------------------------------

    def _semantic_candidates(
        self,
        query: str,
        top_k: int = TOP_K,
    ):
        """
        Return semantic candidate rows.

        Returns
        -------
        list[dict]
        """

        embedding = self._embed_query(query)

        scores, indices = self.index.search(
            embedding,
            top_k,
        )

        candidates = []

        for score, idx in zip(scores[0], indices[0]):

            if idx < 0:
                continue

            if idx >= len(self.df):
                continue

            row = self.df.iloc[idx].to_dict()

            row["SemanticScore"] = float(score)

            candidates.append(row)

        return candidates

    # -----------------------------------------------------
    # Normalize Results
    # -----------------------------------------------------

    def _normalize_results(
        self,
        candidates,
    ):

        normalized = []

        for row in candidates:
            normalized.append(
                normalize_record(row)
            )

        return normalized

    # -----------------------------------------------------
    # Apply Intent Filters
    # -----------------------------------------------------

    def _apply_filters(self, buses, intent):
        """
        Apply structured filters extracted from intent.
        """

        filtered = []

        for bus in buses:

            # ---------------- Route ----------------
            if intent.get("from_city"):
                if str(bus.get("From_City", "")).lower() != intent["from_city"].lower():
                    continue

            if intent.get("to_city"):
                if str(bus.get("To_City", "")).lower() != intent["to_city"].lower():
                    continue

            # ---------------- Bus Type ----------------
            if intent.get("bus_type"):
                if intent["bus_type"].lower() not in str(
                    bus.get("Bus_Type", "")
                ).lower():
                    continue

            # ---------------- Operator ----------------
            if intent.get("operator"):
                if intent["operator"].lower() not in str(
                    bus.get("Operator", "")
                ).lower():
                    continue

            # ---------------- Amenities ----------------
            requested = intent.get("amenities", [])

            if requested:

                amenities = [
                    x.strip().lower()
                    for x in str(bus.get("Amenities", "")).split(",")
                ]

                ok = True

                for item in requested:
                    if item.lower() not in amenities:
                        ok = False
                        break

                if not ok:
                    continue

            # ---------------- Fare ----------------
            fare = safe_float(bus.get("Fare"))

            if (
                intent.get("min_price") is not None
                and fare < intent["min_price"]
            ):
                continue

            if (
                intent.get("max_price") is not None
                and fare > intent["max_price"]
            ):
                continue

            # ---------------- Seats ----------------
            if intent.get("min_seats") is not None:
                seats = safe_int(bus.get("Available_Seats"))

                if seats < intent["min_seats"]:
                    continue

            # ---------------- Rating ----------------
            if intent.get("min_rating") is not None:

                rating = safe_float(bus.get("Rating"))

                if rating < intent["min_rating"]:
                    continue

            # ---------------- Time ----------------
            if intent.get("time"):

                departure = str(bus.get("Departure_Time", ""))

                if intent["time"] == "night":
                    if not is_night_bus(departure):
                        continue

                elif intent["time"] == "morning":
                    if not is_morning_bus(departure):
                        continue

                elif intent["time"] == "afternoon":
                    if not is_afternoon_bus(departure):
                        continue

                elif intent["time"] == "evening":
                    if not is_evening_bus(departure):
                        continue

            filtered.append(bus)

        return filtered

    # -----------------------------------------------------
    # Rank Results
    # -----------------------------------------------------

    def _rank_results(self, buses, intent):
        """
        Apply ranking algorithm.
        """

        buses = remove_duplicates(buses)

        buses = rank_results(
            buses,
            intent,
        )

        return buses

    # -----------------------------------------------------
    # Sorting
    # -----------------------------------------------------

    def _sort_results(self, buses, intent):
        """
        Optional sorting.
        """

        if not buses:
            return buses

        mode = intent.get("sort")

        if mode == "cheapest":

            buses.sort(
                key=lambda x: safe_float(
                    x.get("Fare")
                )
            )

        elif mode == "rating":

            buses.sort(
                key=lambda x: safe_float(
                    x.get("Rating")
                ),
                reverse=True,
            )

        elif mode == "duration":

            buses.sort(
                key=lambda x: safe_float(
                    x.get("Duration")
                )
            )

        return buses

    # -----------------------------------------------------
    # Pipeline
    # -----------------------------------------------------

    def _process_candidates(
        self,
        query,
        intent,
    ):
        """
        Complete search pipeline.

        FAISS
            ↓
        Normalize
            ↓
        Filter
            ↓
        Rank
            ↓
        Sort
        """

        candidates = self._semantic_candidates(
            query=query,
            top_k=TOP_K,
        )

        candidates = self._normalize_results(
            candidates
        )

        candidates = self._apply_filters(
            candidates,
            intent,
        )

        candidates = self._rank_results(
            candidates,
            intent,
        )

        candidates = self._sort_results(
            candidates,
            intent,
        )

        return candidates

    # -----------------------------------------------------
    # Public Search API
    # -----------------------------------------------------

    def search(self, query: str, intent: dict):
        """
        Main Search Function

        Parameters
        ----------
        query : str
            Original user query

        intent : dict
            Parsed intent from intent.py

        Returns
        -------
        list[dict]
        """

        if not query:
            return []

        results = self._process_candidates(
            query=query,
            intent=intent,
        )

        return results

    # -----------------------------------------------------
    # Analytics
    # -----------------------------------------------------

    def analytics(self):
        """
        Dataset analytics.
        """

        from analytics import BusAnalytics

        analytics = BusAnalytics(
            self.df.to_dict("records")
        )

        return analytics.summary()

    # -----------------------------------------------------
    # Dataset Info
    # -----------------------------------------------------

    def dataset_info(self):

        return {
            "records": len(self.df),
            "documents": len(self.documents),
            "vectors": self.index.ntotal,
        }

    # -----------------------------------------------------
    # Reload
    # -----------------------------------------------------

    def reload(self):

        self._load_csv()
        self._load_documents()
        self._load_index()

        return True

# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from utils.intent import analyze_query

    engine = BusSearchEngine()

    print("\n")
    print("=" * 70)
    print("Tamil Nadu Private OmniBus AI Search Engine")
    print("=" * 70)

    while True:

        query = input("\nSearch Bus > ")

        if query.lower() in ["exit", "quit"]:
            break

        intent = analyze_query(query)

        results = engine.search(
            query,
            intent,
        )

        print("\n")
        print("=" * 70)
        print(f"Results Found : {len(results)}")
        print("=" * 70)

        for i, bus in enumerate(results[:5], start=1):

            print(
                f"""
{i}.

Operator  : {bus['Operator']}
Route     : {bus['From_City']} -> {bus['To_City']}
Bus       : {bus['Bus_Name']}
Type      : {bus['Bus_Type']}
Departure : {bus['Departure_Time']}
Arrival   : {bus['Arrival_Time']}
Fare      : ₹{bus['Fare']}
Rating    : {bus['Rating']}
Seats     : {bus['Available_Seats']}
Amenities : {bus['Amenities']}
Score     : {bus.get('Score',0)}
"""
            )

        if not results:
            print("No matching buses found.")

