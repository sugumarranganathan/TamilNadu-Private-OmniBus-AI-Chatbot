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


# ==========================================================
# Filter By Amenities
# ==========================================================

def filter_amenities(df, amenities):

    if not amenities:
        return df

    filtered = df.copy()

    for amenity in amenities:

        filtered = filtered[
            filtered["Amenities"].str.contains(
                amenity,
                case=False,
                na=False
            )
        ]

    return filtered


# ==========================================================
# Filter By Operator
# ==========================================================

def filter_operator(df, operator):

    if operator is None:
        return df

    return df[
        df["Operator"].str.contains(
            operator,
            case=False,
            na=False
        )
    ]


# ==========================================================
# Filter By Rating
# ==========================================================

def filter_rating(df, rating_intent):

    if not rating_intent:
        return df

    return df.sort_values(
        by="Rating",
        ascending=False
    )


# ==========================================================
# Filter By Seats
# ==========================================================

def filter_seats(df, seat_intent):

    if not seat_intent:
        return df

    return df[df["Available_Seats"] > 0]


# ==========================================================
# Filter By Time
# ==========================================================

def filter_time(df, time_keywords):

    if not time_keywords:
        return df

    filtered = df.copy()

    for keyword in time_keywords:

        keyword = keyword.lower()

        if keyword == "morning":

            filtered = filtered[
                filtered["Departure_Time"].str[:2].astype(int).between(5, 11)
            ]

        elif keyword == "afternoon":

            filtered = filtered[
                filtered["Departure_Time"].str[:2].astype(int).between(12, 16)
            ]

        elif keyword == "evening":

            filtered = filtered[
                filtered["Departure_Time"].str[:2].astype(int).between(17, 21)
            ]

        elif keyword == "night":

            hour = filtered["Departure_Time"].str[:2].astype(int)

            filtered = filtered[
                (hour >= 22) | (hour <= 4)
            ]

    return filtered


# ==========================================================
# Semantic Search Using FAISS
# ==========================================================

def semantic_search(query, top_k=TOP_K):

    embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        embedding.astype(np.float32),
        top_k
    )

    rows = []

    for score, idx in zip(distances[0], indices[0]):

        if idx >= len(bus_df):
            continue

        bus = bus_df.iloc[idx].to_dict()

        bus["Confidence"] = round(float(score), 3)

        rows.append(bus)

    return rows


# ==========================================================
# Apply Structured Filters
# ==========================================================

def apply_filters(df, parsed):

    df = filter_route(
        df,
        parsed["route"]
    )

    df = filter_price(
        df,
        parsed["price"]
    )

    df = filter_bus_type(
        df,
        parsed["bus_type"]
    )

    df = filter_amenities(
        df,
        parsed["amenities"]
    )

    df = filter_operator(
        df,
        parsed["operator"]
    )

    df = filter_seats(
        df,
        parsed["seat_intent"]
    )

    df = filter_rating(
        df,
        parsed["rating_intent"]
    )

    df = filter_time(
        df,
        parsed["time"]
    )

    return df


# ==========================================================
# Search Buses
# ==========================================================

def search_buses(query):

    # -----------------------------------------------
    # Analyze User Query
    # -----------------------------------------------

    parsed = analyze_query(query)

    # -----------------------------------------------
    # Structured Search
    # -----------------------------------------------

    filtered_df = apply_filters(
        bus_df.copy(),
        parsed
    )

    structured_results = []

    if len(filtered_df) > 0:

        structured_results = filtered_df.to_dict(
            orient="records"
        )

    # -----------------------------------------------
    # FAISS Semantic Search
    # -----------------------------------------------

    semantic_results = semantic_search(query)

    # -----------------------------------------------
    # Merge Results
    # -----------------------------------------------

    merged = []

    seen = set()

    for row in structured_results + semantic_results:

        bus_id = row["Bus_ID"]

        if bus_id not in seen:

            seen.add(bus_id)

            merged.append(row)

    # -----------------------------------------------
    # Sort by Rating
    # -----------------------------------------------

    merged.sort(

        key=lambda x: (
            float(x.get("Rating", 0)),
            int(x.get("Available_Seats", 0))
        ),

        reverse=True

    )

    return merged[:TOP_K]


# ==========================================================
# Pretty Print
# ==========================================================

def print_results(results):

    if len(results) == 0:

        print("\nNo buses found.\n")

        return

    print("\n" + "=" * 70)

    print(f"Found {len(results)} Bus(es)")

    print("=" * 70)

    for i, bus in enumerate(results, start=1):

        print(f"\n{i}")

        print("-" * 70)

        print("Operator :", bus.get("Operator"))

        print("Bus Name :", bus.get("Bus_Name"))

        print("Route    :", bus.get("From_City"),
              "→",
              bus.get("To_City"))

        print("Bus Type :", bus.get("Bus_Type"))

        print("Departure:", bus.get("Departure_Time"))

        print("Arrival  :", bus.get("Arrival_Time"))

        print("Duration :", bus.get("Duration"))

        print("Fare     : ₹", bus.get("Fare"))

        print("Seats    :", bus.get("Available_Seats"))

        print("Rating   :", bus.get("Rating"))

        print("Amenities:", bus.get("Amenities"))

        if "Confidence" in bus:

            print("Semantic Score:", bus["Confidence"])


# ==========================================================
# Test Mode
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)

    print("Tamil Nadu Private Omni Bus AI Chatbot")

    print("Search Engine V1")

    print("=" * 70)

    while True:

        query = input("\nSearch Bus : ")

        if query.lower() == "exit":

            break

        buses = search_buses(query)

        print_results(buses)


# ==========================================================
# Sample Queries
# ==========================================================

"""
Try these queries:

hi

Show buses from Chennai to Madurai

Bus from Salem to Trichy

Cheapest bus

Bus under 900

Bus below 700

Budget bus

Luxury Sleeper

Volvo bus

AC Sleeper bus

Non AC bus

Bus with WiFi

Bus with Charging

Bus with GPS

Night bus

Morning bus

Best rated bus

Window seat

Available seats

SRM bus

KPN bus

Refund policy

Cancellation

Chennai la irundhu Madurai bus

Madurai bus venum

1000 ku keela bus

WiFi iruka

Volvo bus kaatu

"""
