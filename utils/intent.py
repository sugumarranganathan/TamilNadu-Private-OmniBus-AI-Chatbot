
"""
utils/intent.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Improved Intent Parser (Version 6.0)
=========================================
"""

import re
from typing import Dict, List, Optional

from config import BUS_TYPES, AMENITIES, GREETINGS

# -----------------------------
# Canonical Cities & Aliases
# -----------------------------
CITY_ALIASES = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "blr": "Bengaluru",
    "madras": "Chennai",
    "chennai": "Chennai",
    "trichy": "Trichy",
    "tiruchirappalli": "Trichy",
    "kovai": "Coimbatore",
    "coimbatore": "Coimbatore",
    "pondy": "Pondicherry",
    "pondicherry": "Pondicherry",
    "nellai": "Tirunelveli",
    "tirunelveli": "Tirunelveli",
    "salem": "Salem",
    "madurai": "Madurai",
    "hosur": "Hosur",
    "erode": "Erode",
    "vellore": "Vellore",
    "thanjavur": "Thanjavur",
    "karur": "Karur",
}

OPERATORS = [
    "Parveen", "KPN", "SRS", "YBM",
    "Royal Rider", "Elite Travels",
    "Galaxy Bus", "SkyBus",
    "Happy Journey", "City Link",
    "Comfort Bus", "Smart Coach",
    "Golden Route", "Sunrise Coaches"
]

AMENITY_ALIASES = {
    "wifi": "WiFi",
    "wi-fi": "WiFi",
    "internet": "WiFi",
    "charging": "Charging",
    "usb": "Charging",
    "blanket": "Blanket",
    "water": "Water Bottle",
    "water bottle": "Water Bottle",
    "gps": "GPS",
    "tv": "TV",
}

TIME_KEYWORDS = {
    "morning": "morning",
    "afternoon": "afternoon",
    "evening": "evening",
    "night": "night",
}

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", " ", text)
    return re.sub(r"\s+", " ", text)

def detect_greeting(text: str) -> bool:
    return any(g in text for g in GREETINGS)

def extract_cities(text: str):
    found = []
    for alias, city in CITY_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", text):
            if city not in found:
                found.append(city)

    frm = to = None
    m = re.search(r"from\s+([a-z\s]+?)\s+to\s+([a-z\s]+)", text)
    if m:
        frm = CITY_ALIASES.get(m.group(1).strip(), m.group(1).strip().title())
        to = CITY_ALIASES.get(m.group(2).strip(), m.group(2).strip().title())
    elif "to " in text:
        m = re.search(r"to\s+([a-z\s]+)", text)
        if m:
            to = CITY_ALIASES.get(m.group(1).strip(), m.group(1).strip().title())
            if found:
                frm = found[0]
    elif len(found) >= 2:
        frm, to = found[0], found[1]
    elif len(found) == 1:
        to = found[0]
    return frm, to

def detect_bus_type(text:str)->Optional[str]:
    for bt in sorted(BUS_TYPES,key=len,reverse=True):
        if bt.lower() in text:
            return bt
    return None

def detect_operator(text:str)->Optional[str]:
    for op in OPERATORS:
        if op.lower() in text:
            return op
    return None

def detect_amenities(text:str)->List[str]:
    result=[]
    for alias,canon in AMENITY_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", text):
            if canon not in result:
                result.append(canon)
    return result

def detect_price(text:str):
    info={"min_price":None,"max_price":None}
    patterns=[
        (r"under\s+(\d+)","max"),
        (r"below\s+(\d+)","max"),
        (r"less than\s+(\d+)","max"),
        (r"above\s+(\d+)","min"),
        (r"over\s+(\d+)","min"),
        (r"between\s+(\d+)\s+and\s+(\d+)","between")
    ]
    for p,kind in patterns:
        m=re.search(p,text)
        if not m:
            continue
        if kind=="max":
            info["max_price"]=int(m.group(1))
        elif kind=="min":
            info["min_price"]=int(m.group(1))
        else:
            info["min_price"]=int(m.group(1))
            info["max_price"]=int(m.group(2))
    return info

def detect_time(text:str):
    for k,v in TIME_KEYWORDS.items():
        if k in text:
            return v
    return None

def detect_sort(text:str):
    if "cheapest" in text:
        return "cheapest"
    if "best" in text or "top rated" in text:
        return "rating"
    if "fastest" in text:
        return "duration"
    if "earliest" in text:
        return "departure"
    return None

def analyze_query(query:str)->Dict:
    q=normalize(query)
    frm,to=extract_cities(q)
    price=detect_price(q)
    return {
        "intent":"greeting" if detect_greeting(q) else "search",
        "greeting":detect_greeting(q),
        "from_city":frm,
        "to_city":to,
        "bus_type":detect_bus_type(q),
        "operator":detect_operator(q),
        "amenities":detect_amenities(q),
        "time":detect_time(q),
        "sort":detect_sort(q),
        "min_price":price["min_price"],
        "max_price":price["max_price"],
        "raw_query":query
    }

if __name__=="__main__":
    tests=[
        "Luxury Sleeper bus to Bangalore",
        "Night bus to Salem under 1000 with wifi",
        "Best Volvo bus from Chennai to Madurai",
        "Bus between 800 and 1200"
    ]
    for t in tests:
        print("="*70)
        print(t)
        print(analyze_query(t))
