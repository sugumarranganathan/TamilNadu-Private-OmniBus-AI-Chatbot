
"""
utils/ranking.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
Ranking Utilities (Version 1.0)
=================================================
"""

from typing import Dict, List


def calculate_score(bus: Dict, intent: Dict) -> float:
    """
    Calculate a relevance score for a bus record.
    Higher score = better match.
    """
    score = 0.0

    # Route
    if intent.get("from_city") and str(bus.get("From_City","")).lower() == intent["from_city"].lower():
        score += 40

    if intent.get("to_city") and str(bus.get("To_City","")).lower() == intent["to_city"].lower():
        score += 40

    # Bus type
    if intent.get("bus_type"):
        if intent["bus_type"].lower() in str(bus.get("Bus_Type","")).lower():
            score += 20

    # Operator
    if intent.get("operator"):
        if intent["operator"].lower() in str(bus.get("Operator","")).lower():
            score += 15

    # Amenities
    requested = intent.get("amenities", [])
    amenities = str(bus.get("Amenities","")).lower()

    for amenity in requested:
        if amenity.lower() in amenities:
            score += 10

    # Fare
    fare = float(bus.get("Fare", 0))

    if intent.get("max_price") is not None and fare <= intent["max_price"]:
        score += 10

    if intent.get("min_price") is not None and fare >= intent["min_price"]:
        score += 10

    # Rating bonus
    try:
        score += float(bus.get("Rating", 0)) * 2
    except Exception:
        pass

    # Seat availability bonus
    try:
        seats = int(bus.get("Available_Seats", 0))
        score += min(seats, 30) / 3
    except Exception:
        pass

    return round(score, 2)


def rank_results(results: List[Dict], intent: Dict) -> List[Dict]:
    """
    Rank search results from best to worst.
    """
    ranked = []

    for bus in results:
        item = dict(bus)
        item["Score"] = calculate_score(item, intent)
        ranked.append(item)

    ranked.sort(key=lambda x: x["Score"], reverse=True)
    return ranked


def remove_duplicates(results: List[Dict]) -> List[Dict]:
    """
    Remove duplicate buses based on operator, route,
    departure time, and bus name.
    """
    unique = []
    seen = set()

    for bus in results:
        key = (
            bus.get("Operator"),
            bus.get("Bus_Name"),
            bus.get("From_City"),
            bus.get("To_City"),
            bus.get("Departure_Time")
        )

        if key not in seen:
            seen.add(key)
            unique.append(bus)

    return unique


def top_results(results: List[Dict], limit: int = 5) -> List[Dict]:
    return results[:limit]


if __name__ == "__main__":
    sample_intent = {
        "from_city": "Chennai",
        "to_city": "Madurai",
        "amenities": ["WiFi"],
        "bus_type": "AC Sleeper",
        "operator": None,
        "min_price": None,
        "max_price": 1500
    }

    sample_results = [
        {
            "Operator": "SkyBus",
            "Bus_Name": "SkyBus Express",
            "From_City": "Chennai",
            "To_City": "Madurai",
            "Bus_Type": "AC Sleeper",
            "Amenities": "WiFi,Charging,Water",
            "Fare": 1400,
            "Rating": 4.9,
            "Available_Seats": 18,
            "Departure_Time": "20:30"
        },
        {
            "Operator": "Fast Wheels",
            "Bus_Name": "Fast Wheels Express",
            "From_City": "Chennai",
            "To_City": "Salem",
            "Bus_Type": "Semi Sleeper",
            "Amenities": "AC",
            "Fare": 900,
            "Rating": 4.0,
            "Available_Seats": 28,
            "Departure_Time": "18:00"
        }
    ]

    ranked = rank_results(sample_results, sample_intent)
    for bus in ranked:
        print(bus["Operator"], bus["Score"])
