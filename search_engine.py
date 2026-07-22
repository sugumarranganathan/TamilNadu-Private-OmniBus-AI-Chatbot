"""
=========================================================
Tamil Nadu Private Omni Bus AI Chatbot
Search Engine
=========================================================
"""

import pickle
import faiss
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer

from config import (
    CSV_FILE,
    DOCUMENTS_FILE,
    FAISS_INDEX_FILE,
    EMBEDDING_MODEL,
    TOP_K,
    CONFIDENCE_THRESHOLD
)

# ==========================================================
# Load CSV
# ==========================================================

print("Loading bus dataset...")

bus_df = pd.read_csv(CSV_FILE)

print(f"Loaded {len(bus_df)} bus records.")

# ==========================================================
# Load Documents
# ==========================================================

print("Loading documents...")

with open(DOCUMENTS_FILE, "rb") as f:
    documents = pickle.load(f)

print(f"Loaded {len(documents)} documents.")

# ==========================================================
# Load FAISS Index
# ==========================================================

print("Loading FAISS index...")

index = faiss.read_index(FAISS_INDEX_FILE)

print("FAISS index loaded successfully.")

# ==========================================================
# Load Embedding Model
# ==========================================================

print("Loading Sentence Transformer...")

model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding model loaded.")

# ==========================================================
# Search Function
# ==========================================================

def search_buses(query):

    """
    Search buses using semantic search.
    """

    embedding = model.encode([query])

    distances, indices = index.search(
        np.array(embedding).astype("float32"),
        TOP_K
    )

    results = []

    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        confidence = 1 / (1 + score)

        if confidence < CONFIDENCE_THRESHOLD:
            continue

        row = bus_df.iloc[idx]

        results.append({

            "Bus_ID": row.get("Bus_ID", ""),

            "Operator": row.get("Operator", ""),

            "Bus_Name": row.get("Bus_Name", ""),

            "Source": row.get("Source", ""),

            "Destination": row.get("Destination", ""),

            "Bus_Type": row.get("Bus_Type", ""),

            "Departure_Time": row.get("Departure_Time", ""),

            "Arrival_Time": row.get("Arrival_Time", ""),

            "Fare": row.get("Fare", ""),

            "Rating": row.get("Rating", ""),

            "Available_Seats": row.get("Available_Seats", ""),

            "AC": row.get("AC", ""),

            "WiFi": row.get("WiFi", ""),

            "Charging": row.get("Charging", ""),

            "GPS": row.get("GPS", ""),

            "CCTV": row.get("CCTV", ""),

            "Confidence": round(confidence, 2)

        })

    return results

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    while True:

        query = input("\nAsk: ")

        if query.lower() == "exit":
            break

        buses = search_buses(query)

        print()

        for i, bus in enumerate(buses, start=1):

            print("=" * 50)

            print(f"{i}. {bus['Operator']}")

            print(bus["Bus_Name"])

            print(f"{bus['Source']} -> {bus['Destination']}")

            print(f"Fare : ₹{bus['Fare']}")

            print(f"Rating : {bus['Rating']}")

            print(f"Confidence : {bus['Confidence']}")

            print("=" * 50)
