"""
=========================================================
Tamil Nadu Private Omni Bus AI Chatbot
Intent Detection Engine
=========================================================
"""

import re

# ==========================================================
# Intent Patterns
# ==========================================================

INTENTS = {

    # ------------------------------------------------------
    # Greetings
    # ------------------------------------------------------

    "greeting": [
        "hi","hello","hey","good morning","good afternoon",
        "good evening","vanakkam","ஹலோ","ஹாய்"
    ],

    # ------------------------------------------------------
    # Route Search
    # ------------------------------------------------------

    "route_search":[
        "from",
        "to",
        "bus from",
        "show buses",
        "available buses",
        "travel from",
        "route",
        "go to",
        "going to",
        "between"
    ],

    # ------------------------------------------------------
    # Cheapest
    # ------------------------------------------------------

    "cheapest":[
        "cheap",
        "cheapest",
        "lowest fare",
        "budget",
        "low cost",
        "minimum fare",
        "under",
        "below",
        "less than"
    ],

    # ------------------------------------------------------
    # Highest Rating
    # ------------------------------------------------------

    "best_rating":[
        "best",
        "highest rated",
        "top rated",
        "rating",
        "good bus",
        "popular",
        "recommended",
        "reviews"
    ],

    # ------------------------------------------------------
    # Bus Type
    # ------------------------------------------------------

    "bus_type":[
        "ac",
        "non ac",
        "sleeper",
        "semi sleeper",
        "luxury",
        "volvo",
        "scania",
        "seater",
        "electric",
        "mini bus"
    ],

    # ------------------------------------------------------
    # Amenities
    # ------------------------------------------------------

    "amenities":[
        "wifi",
        "charging",
        "usb",
        "blanket",
        "pillow",
        "water bottle",
        "reading light",
        "tv",
        "gps",
        "cctv",
        "washroom",
        "ac"
    ],

    # ------------------------------------------------------
    # Timing
    # ------------------------------------------------------

    "timing":[
        "morning",
        "afternoon",
        "evening",
        "night",
        "today",
        "tomorrow",
        "after",
        "before",
        "departure",
        "arrival",
        "early",
        "late"
    ],

    # ------------------------------------------------------
    # Seats
    # ------------------------------------------------------

    "seat":[
        "seat",
        "available seat",
        "window seat",
        "last seat",
        "seat availability",
        "vacant seat"
    ],

    # ------------------------------------------------------
    # Operators
    # ------------------------------------------------------

    "operator":[
        "greenline",
        "srm",
        "kpn",
        "parveen",
        "orange",
        "vrl",
        "ybm",
        "royal",
        "national",
        "sharma"
    ],

    # ------------------------------------------------------
    # Policies
    # ------------------------------------------------------

    "policy":[
        "refund",
        "cancel",
        "cancellation",
        "luggage",
        "pets",
        "policy"
    ],

    # ------------------------------------------------------
    # Help
    # ------------------------------------------------------

    "help":[
        "help",
        "support",
        "how",
        "usage",
        "examples",
        "commands"
    ]
}

# ==========================================================
# Tamil Nadu Cities
# ==========================================================

CITIES = [

"Chennai",
"Madurai",
"Coimbatore",
"Salem",
"Trichy",
"Tirunelveli",
"Erode",
"Vellore",
"Pondicherry",
"Villupuram",
"Karur",
"Namakkal",
"Kumbakonam",
"Thoothukudi",
"Nagercoil",
"Hosur",
"Bengaluru",
"Hyderabad",
"Kochi",
"Trivandrum",
"Mysuru"

]

# lowercase for matching
CITY_LOOKUP = {c.lower(): c for c in CITIES}

# ==========================================================
# Detect Intent
# ==========================================================

def detect_intent(query: str):

    query = query.lower()

    detected = []

    for intent, patterns in INTENTS.items():

        for pattern in patterns:

            if pattern in query:
                detected.append(intent)
                break

    return detected


# ==========================================================
# Detect Cities
# ==========================================================

def detect_cities(query: str):

    query = query.lower()

    found = []

    for city_lower, city_name in CITY_LOOKUP.items():

        if re.search(rf"\b{re.escape(city_lower)}\b", query):
            found.append(city_name)

    return found


# ==========================================================
# Extract Budget
# ==========================================================

def detect_price(query: str):

    nums = re.findall(r"\d+", query)

    if nums:
        return int(nums[0])

    return None


# ==========================================================
# Complete Parser
# ==========================================================

def parse_query(query):

    return {

        "intents": detect_intent(query),

        "cities": detect_cities(query),

        "price": detect_price(query)

    }


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    while True:

        q = input("\nAsk : ")

        if q.lower() == "exit":
            break

        print(parse_query(q))
