
"""
utils/normalizer.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
Data Normalization Utilities (Version 1.0)
=================================================
"""

import re

# -----------------------------
# Canonical City Names
# -----------------------------
CITY_ALIASES = {
    "bangalore": "bengaluru",
    "blr": "bengaluru",
    "bengaluru": "bengaluru",
    "madras": "chennai",
    "chennai": "chennai",
    "kovai": "coimbatore",
    "coimbatore": "coimbatore",
    "trichy": "trichy",
    "tiruchirappalli": "trichy",
    "pondy": "pondicherry",
    "nellai": "tirunelveli",
}

# -----------------------------
# Amenities
# -----------------------------
AMENITY_ALIASES = {
    "wifi": "wifi",
    "wi-fi": "wifi",
    "wireless": "wifi",
    "internet": "wifi",

    "charging": "charging",
    "usb": "charging",
    "usb charging": "charging",

    "water": "water",
    "water bottle": "water",
    "mineral water": "water",

    "blanket": "blanket",
    "pillow": "pillow",
    "gps": "gps",
    "live tracking": "gps",
    "tv": "tv",
    "ac": "ac",
}

# -----------------------------
# Bus Types
# -----------------------------
BUS_TYPE_ALIASES = {
    "luxury": "luxury sleeper",
    "luxury sleeper": "luxury sleeper",
    "premium": "luxury sleeper",
    "vip": "luxury sleeper",

    "ac sleeper": "ac sleeper",
    "non ac sleeper": "non ac sleeper",
    "semi sleeper": "semi sleeper",
    "ac seater": "ac seater",
    "non ac seater": "non ac seater",
    "volvo": "volvo",
    "bharatbenz": "bharat benz",
    "bharat benz": "bharat benz",
}

def clean_text(text):
    if text is None:
        return ""
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

def normalize_city(city):
    city = clean_text(city)
    return CITY_ALIASES.get(city, city)

def normalize_amenity(value):
    value = clean_text(value)
    return AMENITY_ALIASES.get(value, value)

def normalize_amenities(value):
    if not value:
        return []
    items = [x.strip() for x in str(value).split(",")]
    normalized = []
    for item in items:
        item = normalize_amenity(item)
        if item and item not in normalized:
            normalized.append(item)
    return normalized

def normalize_bus_type(bus_type):
    bus_type = clean_text(bus_type)
    return BUS_TYPE_ALIASES.get(bus_type, bus_type)

def contains_amenity(bus_amenities, requested):
    bus = normalize_amenities(bus_amenities)
    req = normalize_amenity(requested)
    return req in bus

def normalize_record(record: dict):
    """Return a normalized copy of a bus record."""
    data = dict(record)

    data["From_City"] = normalize_city(data.get("From_City"))
    data["To_City"] = normalize_city(data.get("To_City"))
    data["Bus_Type"] = normalize_bus_type(data.get("Bus_Type"))
    data["Amenities"] = normalize_amenities(data.get("Amenities"))

    return data


if __name__ == "__main__":
    sample = {
        "From_City": "Madras",
        "To_City": "Bangalore",
        "Bus_Type": "Luxury",
        "Amenities": "WiFi, Water Bottle, USB Charging"
    }

    print(normalize_record(sample))
