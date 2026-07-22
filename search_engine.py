"""
===========================================================
Tamil Nadu Private OmniBus AI Chatbot
search_engine.py (Version 2.0 - Part 1)
===========================================================
"""

import os
import pickle
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


# ==========================================================
# Globals (Lazy Loading)
# ==========================================================

_model = None
_bus_df = None
_faiss_index = None
_documents = None


# ==========================================================
# Expected CSV Columns
# ==========================================================

REQUIRED_COLUMNS = [
    "Bus_ID",
    "Operator",
    "Route_ID",
    "From_City",
    "To_City",
    "Bus_Name",
    "Bus_Type",
    "Departure_Time",
    "Arrival_Time",
    "Duration",
    "Distance_KM",
    "Fare",
    "Boarding_Point",
    "Dropping_Point",
    "Seats",
    "Available_Seats",
    "Amenities",
    "Running_Days",
    "Rating",
]


# ==========================================================
# Load Embedding Model (Lazy)
# ==========================================================

def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(EMBEDDING_MODEL)

    return _model


# ==========================================================
# Load CSV
# ==========================================================

def load_bus_data() -> pd.DataFrame:
    global _bus_df

    if _bus_df is not None:
        return _bus_df

    if not os.path.exists(BUS_CSV):
        raise FileNotFoundError(f"CSV not found: {BUS_CSV}")

    df = pd.read_csv(BUS_CSV)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(
            f"Missing columns in CSV:\n{missing}"
        )

    df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce").fillna(0)

    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    ).fillna(0)

    df["Available_Seats"] = pd.to_numeric(
        df["Available_Seats"],
        errors="coerce"
    ).fillna(0)

    df["Seats"] = pd.to_numeric(
        df["Seats"],
        errors="coerce"
    ).fillna(0)

    df = df.fillna("")

    _bus_df = df

    print(f"Loaded {len(df)} buses")

    return _bus_df


# ==========================================================
# Load FAISS
# ==========================================================

def load_faiss_index():

    global _faiss_index

    if _faiss_index is not None:
        return _faiss_index

    if not os.path.exists(FAISS_INDEX):
        raise FileNotFoundError(
            f"FAISS index not found: {FAISS_INDEX}"
        )

    _faiss_index = faiss.read_index(FAISS_INDEX)

    print("FAISS index loaded")

    return _faiss_index


# ==========================================================
# Load Documents
# ==========================================================

def load_documents():

    global _documents

    if _documents is not None:
        return _documents

    if not os.path.exists(DOCUMENTS_FILE):
        raise FileNotFoundError(
            f"documents.pkl not found: {DOCUMENTS_FILE}"
        )

    with open(DOCUMENTS_FILE, "rb") as f:
        _documents = pickle.load(f)

    print(f"Loaded {len(_documents)} documents")

    return _documents


# ==========================================================
# Route Filter
# ==========================================================

def filter_route(
    df: pd.DataFrame,
    from_city: Optional[str],
    to_city: Optional[str],
) -> pd.DataFrame:

    if from_city:
        df = df[
            df["From_City"].str.lower()
            == from_city.lower()
        ]

    if to_city:
        df = df[
            df["To_City"].str.lower()
            == to_city.lower()
        ]

    return df


# ==========================================================
# Fare Filter
# ==========================================================

def filter_fare(
    df: pd.DataFrame,
    max_price: Optional[int],
) -> pd.DataFrame:

    if max_price is None:
        return df

    return df[df["Fare"] <= max_price]


# ==========================================================
# Bus Type Filter
# ==========================================================

def filter_bus_type(
    df: pd.DataFrame,
    bus_type: Optional[str],
) -> pd.DataFrame:

    if not bus_type:
        return df

    return df[
        df["Bus_Type"]
        .str.lower()
        .str.contains(bus_type.lower(), na=False)
    ]


# ==========================================================
# Operator Filter
# ==========================================================

def filter_operator(
    df: pd.DataFrame,
    operator: Optional[str],
) -> pd.DataFrame:

    if not operator:
        return df

    return df[
        df["Operator"]
        .str.lower()
        .str.contains(operator.lower(), na=False)
    ]


# ==========================================================
# Amenities Filter
# ==========================================================

def filter_amenities(
    df: pd.DataFrame,
    amenities: List[str],
) -> pd.DataFrame:

    if not amenities:
        return df

    filtered = df.copy()

    for amenity in amenities:
        filtered = filtered[
            filtered["Amenities"]
            .str.lower()
            .str.contains(amenity.lower(), na=False)
        ]

    return filtered


# ==========================================================
# Seats Filter
# ==========================================================

def filter_available_seats(
    df: pd.DataFrame,
    minimum: int = 1,
) -> pd.DataFrame:

    return df[df["Available_Seats"] >= minimum]


# ==========================================================
# Time Filter
# ==========================================================

def filter_time(
    df: pd.DataFrame,
    keyword: Optional[str],
) -> pd.DataFrame:

    if not keyword:
        return df

    dep = df["Departure_Time"].astype(str)

    if keyword == "morning":
        return df[dep.str[:2].astype(int).between(5, 11)]

    if keyword == "afternoon":
        return df[dep.str[:2].astype(int).between(12, 16)]

    if keyword == "evening":
        return df[dep.str[:2].astype(int).between(17, 20)]

    if keyword == "night":
        return df[
            (dep.str[:2].astype(int) >= 21)
            | (dep.str[:2].astype(int) <= 4)
        ]

    return df

    
