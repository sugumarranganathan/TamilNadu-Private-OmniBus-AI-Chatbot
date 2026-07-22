
"""
utils/intent.py
====================================
Tamil Nadu Private OmniBus AI Chatbot
Intent Parser (Version 4.0)
====================================
"""

import re
from typing import Dict, List

from config import BUS_TYPES, AMENITIES, GREETINGS

# --------------------------------------------------
# Supported Cities
# --------------------------------------------------

CITIES = [
    "Chennai","Madurai","Coimbatore","Salem","Trichy","Tirunelveli",
    "Erode","Vellore","Kanchipuram","Thanjavur","Karur","Hosur",
    "Bengaluru","Mysuru","Pondicherry"
]

OPERATORS = [
    "GreenLine Travels",
    "Parveen",
    "KPN",
    "SRS",
    "YBM",
]

PRICE_PATTERNS = [
    r"under\s+(\d+)",
    r"below\s+(\d+)",
    r"less\s+than\s+(\d+)",
]

TIME_WORDS = ["morning", "afternoon", "evening", "night"]


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def detect_greeting(text: str) -> bool:
    return any(g in text for g in GREETINGS)


def detect_route(text: str):
    found = [c for c in CITIES if c.lower() in text]

    if " from " in text and " to " in text:
        m = re.search(r"from\s+(.+?)\s+to\s+(.+)", text)
        if m:
            f = m.group(1).strip().title()
            t = m.group(2).strip().title()
            return f, t

    if len(found) >= 2:
        return found[0], found[1]

    return None, None


def detect_bus_type(text: str):
    for b in sorted(BUS_TYPES, key=len, reverse=True):
        if b.lower() in text:
            return b
    return None


def detect_operator(text: str):
    for op in OPERATORS:
        if op.lower() in text:
            return op
    return None


def detect_amenities(text: str) -> List[str]:
    return [a for a in AMENITIES if a.lower() in text]


def detect_price(text: str):
    for p in PRICE_PATTERNS:
        m = re.search(p, text)
        if m:
            return int(m.group(1))
    return None


def detect_time(text: str):
    for t in TIME_WORDS:
        if t in text:
            return t
    return None


def detect_sort(text: str):
    if "cheapest" in text:
        return "cheapest"
    if "best" in text or "top rated" in text:
        return "rating"
    return None


def analyze_query(query: str) -> Dict:
    q = normalize(query)

    from_city, to_city = detect_route(q)

    return {
        "intent": "greeting" if detect_greeting(q) else "search",
        "greeting": detect_greeting(q),
        "from_city": from_city,
        "to_city": to_city,
        "bus_type": detect_bus_type(q),
        "operator": detect_operator(q),
        "amenities": detect_amenities(q),
        "max_price": detect_price(q),
        "time": detect_time(q),
        "sort": detect_sort(q),
    }


if __name__ == "__main__":
    tests = [
        "Show Luxury Sleeper bus from Chennai to Madurai under 1000 with WiFi",
        "Cheapest bus to Coimbatore",
        "Night Volvo bus",
        "Hello",
    ]

    for t in tests:
        print("=" * 60)
        print(t)
        print(analyze_query(t))
