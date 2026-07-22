"""
==============================================================
Tamil Nadu Private Omni Bus AI Chatbot
search_engine.py

Version : 1.0

Part 1 / 3

Loads:

✔ CSV
✔ FAISS Index
✔ Documents
✔ Embedding Model

==============================================================
"""

import os
import pickle
import faiss
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer

from utils.intent import analyze_query

# ==========================================================
# Configuration
# ==========================================================

DATA_FOLDER = "data"

CSV_FILE = os.path.join(DATA_FOLDER, "bus_services.csv")

DOCUMENT_FILE = os.path.join(DATA_FOLDER, "documents.pkl")

INDEX_FILE = os.path.join(DATA_FOLDER, "bus_index.faiss")

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 10

# ==========================================================
# Load Embedding Model
# ==========================================================

print("=" * 60)
print("Loading Sentence Transformer...")
print("=" * 60)

model = SentenceTransformer(MODEL_NAME)

# ==========================================================
# Load CSV
# ==========================================================

print("Loading Bus Database...")

bus_df = pd.read_csv(CSV_FILE)

bus_df.columns = bus_df.columns.str.strip()

print(f"Loaded {len(bus_df)} Bus Records")

# ==========================================================
# Load Documents
# ==========================================================

print("Loading Documents...")

with open(DOCUMENT_FILE, "rb") as f:

    documents = pickle.load(f)

print(f"Loaded {len(documents)} Documents")

# ==========================================================
# Load FAISS
# ==========================================================

print("Loading FAISS Index...")

index = faiss.read_index(INDEX_FILE)

print("FAISS Loaded Successfully")

print("=" * 60)

# ==========================================================
# Helper Functions
# ==========================================================

def normalize_text(text):

    if pd.isna(text):

        return ""

    return str(text).strip().lower()


def contains_word(text, word):

    return word.lower() in normalize_text(text)


# ==========================================================
# Filter By Route
# ==========================================================

def filter_route(df, route):

    source = route["source"]

    destination = route["destination"]

    filtered = df.copy()

    if source:

        filtered = filtered[
            filtered["From_City"].str.lower() == source.lower()
        ]

    if destination:

        filtered = filtered[
            filtered["To_City"].str.lower() == destination.lower()
        ]

    return filtered


# ==========================================================
# Filter By Price
# ==========================================================

def filter_price(df, price):

    if price is None:

        return df

    return df[df["Fare"] <= price]


# ==========================================================
# Filter Bus Type
# ==========================================================

def filter_bus_type(df, bus_type):

    if bus_type is None:

        return df

    return df[
        df["Bus_Type"].str.contains(
            bus_type,
            case=False,
            na=False
        )
    ]
