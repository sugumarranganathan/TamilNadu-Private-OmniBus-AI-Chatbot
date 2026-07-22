
"""
utils/intent_v7.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
Intent Parser Version 7.0
=================================================
"""

import re
from typing import Dict, List

from config import BUS_TYPES, AMENITIES, GREETINGS

# -------------------------------------------------
# City aliases
# -------------------------------------------------
CITY_ALIASES = {
    "bangalore": "Bengaluru",
    "blr": "Bengaluru",
    "bengaluru": "Bengaluru",
    "madras": "Chennai",
    "chennai": "Chennai",
    "madurai": "Madurai",
    "salem": "Salem",
    "trichy": "Trichy",
    "tiruchirappalli": "Trichy",
    "coimbatore": "Coimbatore",
    "kovai": "Coimbatore",
    "erode": "Erode",
    "hosur": "Hosur",
    "tirunelveli": "Tirunelveli",
    "nellai": "Tirunelveli",
    "pondy": "Pondicherry",
    "pondicherry": "Pondicherry",
    "vellore": "Vellore",
    "karur": "Karur",
    "thanjavur": "Thanjavur",
}

FILLER_WORDS = {
    "bus","buses","list","show","find","search","available",
    "please","me","need","want","services","service"
}

AMENITY_ALIASES = {
    "wifi":"WiFi",
    "wi-fi":"WiFi",
    "internet":"WiFi",
    "wireless":"WiFi",
    "charging":"Charging",
    "usb":"Charging",
    "blanket":"Blanket",
    "water":"Water Bottle",
    "gps":"GPS",
    "tv":"TV",
}

OPERATORS = [
    "Parveen","KPN","SRS","YBM","Royal Rider","Elite Travels",
    "Galaxy Bus","SkyBus","Happy Journey","City Link",
    "Comfort Bus","Golden Route","Sunrise Coaches","Smart Coach"
]

TIME_WORDS = ("morning","afternoon","evening","night")


def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("→", " to ").replace("-", " ")
    text = re.sub(r"[^\w\s]", " ", text)
    words = [w for w in text.split() if w not in FILLER_WORDS]
    return " ".join(words)


def detect_greeting(text: str) -> bool:
    return any(g in text for g in GREETINGS)


def extract_route(text: str):
    words = text.split()
    cities = []

    for w in words:
        if w in CITY_ALIASES:
            city = CITY_ALIASES[w]
            if city not in cities:
                cities.append(city)

    m = re.search(r"from\s+(\w+)\s+to\s+(\w+)", text)
    if m:
        return (
            CITY_ALIASES.get(m.group(1), m.group(1).title()),
            CITY_ALIASES.get(m.group(2), m.group(2).title())
        )

    m = re.search(r"(\w+)\s+to\s+(\w+)", text)
    if m:
        a = CITY_ALIASES.get(m.group(1), m.group(1).title())
        b = CITY_ALIASES.get(m.group(2), m.group(2).title())
        return a, b

    if len(cities) >= 2:
        return cities[0], cities[1]
    if len(cities) == 1:
        return None, cities[0]
    return None, None


def detect_bus_type(text):
    for b in sorted(BUS_TYPES, key=len, reverse=True):
        if b.lower() in text:
            return b
    return None


def detect_operator(text):
    for op in OPERATORS:
        if op.lower() in text:
            return op
    return None


def detect_amenities(text) -> List[str]:
    found = []
    for alias, canonical in AMENITY_ALIASES.items():
        if alias in text and canonical not in found:
            found.append(canonical)
    return found


def detect_price(text):
    result = {"min_price": None, "max_price": None}
    if m := re.search(r"under\s+(\d+)", text):
        result["max_price"] = int(m.group(1))
    elif m := re.search(r"below\s+(\d+)", text):
        result["max_price"] = int(m.group(1))
    elif m := re.search(r"above\s+(\d+)", text):
        result["min_price"] = int(m.group(1))
    elif m := re.search(r"between\s+(\d+)\s+and\s+(\d+)", text):
        result["min_price"] = int(m.group(1))
        result["max_price"] = int(m.group(2))
    return result


def detect_time(text):
    return next((t for t in TIME_WORDS if t in text), None)


def detect_sort(text):
    if "cheapest" in text:
        return "cheapest"
    if "best" in text or "top rated" in text:
        return "rating"
    if "fastest" in text:
        return "duration"
    return None


def analyze_query(query: str) -> Dict:
    q = normalize(query)
    frm, to = extract_route(q)
    price = detect_price(q)

    return {
        "intent": "greeting" if detect_greeting(q) else "search",
        "greeting": detect_greeting(q),
        "from_city": frm,
        "to_city": to,
        "bus_type": detect_bus_type(q),
        "operator": detect_operator(q),
        "amenities": detect_amenities(q),
        "time": detect_time(q),
        "sort": detect_sort(q),
        "min_price": price["min_price"],
        "max_price": price["max_price"],
        "raw_query": query,
        "normalized_query": q,
    }


if __name__ == "__main__":
    tests = [
        "Chennai to madurai wifi bus list",
        "Luxury Sleeper bus to Bangalore",
        "Night bus under 1000",
        "Best Volvo bus with charging"
    ]
    for t in tests:
        print("=" * 70)
        print(t)
        print(analyze_query(t))
