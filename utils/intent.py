"""
==============================================================
Tamil Nadu Private Omni Bus AI Chatbot
intent.py

Version : 1.0
Author  : Sugumar R Project

Part 1 / 3

Intent Detection Engine

This file detects:

✔ Greetings
✔ Routes
✔ Cities
✔ Fare
✔ Bus Type
✔ Amenities
✔ Timings
✔ Seats
✔ Ratings
✔ Operators
✔ Policies

==============================================================
"""

import re

# ==============================================================
# Greeting Patterns
# ==============================================================

GREETINGS = [

    "hi",
    "hello",
    "hey",
    "hai",
    "helo",
    "good morning",
    "good afternoon",
    "good evening",
    "good night",
    "welcome",
    "vanakkam",
    "greetings",
    "help",
    "start",
    "open",
    "chat",
    "what can you do",
    "how are you",
    "ஹாய்",
    "ஹலோ",
    "வணக்கம்"

]

# ==============================================================
# Fare Keywords
# ==============================================================

FARE_KEYWORDS = [

    "fare",
    "price",
    "ticket",
    "cost",
    "amount",
    "cheap",
    "cheapest",
    "budget",
    "discount",
    "offer",
    "low fare",
    "low price",
    "lowest fare",
    "under",
    "below",
    "less than",
    "within",
    "around",
    "economy",
    "affordable",
    "best price"

]

# ==============================================================
# Bus Types
# ==============================================================

BUS_TYPES = [

    "ac",
    "non ac",
    "sleeper",
    "semi sleeper",
    "seater",
    "volvo",
    "scania",
    "luxury",
    "premium",
    "deluxe",
    "mini bus",
    "electric",
    "multi axle"

]

# ==============================================================
# Amenities
# ==============================================================

AMENITIES = [

    "wifi",
    "internet",
    "charging",
    "usb",
    "mobile charging",
    "gps",
    "tracking",
    "live tracking",
    "blanket",
    "pillow",
    "water bottle",
    "reading light",
    "tv",
    "television",
    "cctv",
    "camera",
    "air conditioning",
    "washroom",
    "toilet"

]

# ==============================================================
# Time Keywords
# ==============================================================

TIME_KEYWORDS = [

    "today",
    "tomorrow",
    "morning",
    "afternoon",
    "evening",
    "night",
    "late night",
    "early morning",
    "departure",
    "arrival",
    "after",
    "before",
    "first bus",
    "last bus"

]

# ==============================================================
# Seat Keywords
# ==============================================================

SEAT_KEYWORDS = [

    "seat",
    "window seat",
    "available seat",
    "available seats",
    "vacant",
    "empty",
    "last seat",
    "book seat",
    "reserve"

]

# ==============================================================
# Rating Keywords
# ==============================================================

RATING_KEYWORDS = [

    "rating",
    "ratings",
    "review",
    "reviews",
    "best",
    "top",
    "highest rated",
    "recommended",
    "popular"

]

# ==============================================================
# Policy Keywords
# ==============================================================

POLICY_KEYWORDS = [

    "refund",
    "cancellation",
    "cancel",
    "policy",
    "insurance",
    "luggage",
    "baggage",
    "pets"

]

# ==============================================================
# Bus Operators
# ==============================================================

OPERATORS = [

    "srm",
    "kpn",
    "parveen",
    "greenline",
    "orange",
    "vrl",
    "national",
    "royal",
    "ybm",
    "sharma",
    "srs",
    "kallada",
    "intrcity"

]

# ==============================================================
# Cities
# ==============================================================

CITIES = [

    # Tamil Nadu

    "Chennai",
    "Madurai",
    "Coimbatore",
    "Salem",
    "Trichy",
    "Tirunelveli",
    "Erode",
    "Karur",
    "Namakkal",
    "Vellore",
    "Villupuram",
    "Cuddalore",
    "Kumbakonam",
    "Thanjavur",
    "Thoothukudi",
    "Nagercoil",
    "Dindigul",
    "Hosur",
    "Tiruppur",
    "Pudukkottai",
    "Dharmapuri",
    "Krishnagiri",
    "Mayiladuthurai",
    "Nagapattinam",
    "Ariyalur",
    "Perambalur",
    "Sivagangai",
    "Virudhunagar",
    "Ramanathapuram",
    "Pollachi",
    "Palani",
    "Ooty",
    "Coonoor",
    "Tenkasi",
    "Sankarankovil",
    "Kovilpatti",
    "Chidambaram",
    "Karaikudi",
    "Avinashi",
    "Gobichettipalayam",
    "Mettupalayam",

    # Karnataka

    "Bengaluru",
    "Mysuru",
    "Mangalore",
    "Hubli",
    "Belgaum",

    # Kerala

    "Kochi",
    "Thrissur",
    "Trivandrum",
    "Kollam",
    "Kannur",
    "Palakkad",
    "Kozhikode",

    # Andhra Pradesh

    "Hyderabad",
    "Vijayawada",
    "Visakhapatnam",
    "Tirupati",
    "Kurnool",
    "Nellore",
    "Guntur",

    # Pondicherry

    "Pondicherry"

]

# ==============================================================
# Lookup Dictionary
# ==============================================================

CITY_LOOKUP = {

    city.lower(): city

    for city in CITIES

}

# ==============================================================
# Greeting Response
# ==============================================================

GREETING_RESPONSE = """
👋 Welcome to Tamil Nadu Private Omni Bus AI Chatbot!

I can help you with:

✅ Find buses between cities
✅ Cheapest buses
✅ Luxury / Volvo buses
✅ AC / Non AC buses
✅ Sleeper buses
✅ Bus timings
✅ Fare details
✅ Seat availability
✅ Amenities
✅ Ratings
✅ Operators

Examples:

• Show buses from Chennai to Madurai
• Cheapest bus
• Bus under 1000
• AC Sleeper bus
• Night bus
• Bus with WiFi
"""

# ==============================================================
# Greeting Detection
# ==============================================================

def is_greeting(query):

    query = query.lower().strip()

    for word in GREETINGS:

        if word in query:

            return True

    return False


# ==============================================================
# Detect Cities
# ==============================================================

def detect_cities(query):

    query = query.lower()

    found = []

    for city_lower, city_name in CITY_LOOKUP.items():

        if re.search(rf"\b{re.escape(city_lower)}\b", query):

            found.append(city_name)

    return found


# ==============================================================
# Detect Route
# ==============================================================

def detect_route(query):

    cities = detect_cities(query)

    if len(cities) >= 2:

        return {

            "source": cities[0],

            "destination": cities[1]

        }

    elif len(cities) == 1:

        return {

            "source": None,

            "destination": cities[0]

        }

    return {

        "source": None,

        "destination": None

    }


# ==============================================================
# Detect Price
# ==============================================================

def detect_price(query):

    numbers = re.findall(r"\d+", query)

    if numbers:

        return int(numbers[0])

    return None


# ==============================================================
# Fare Intent
# ==============================================================

def detect_fare_intent(query):

    query = query.lower()

    for keyword in FARE_KEYWORDS:

        if keyword in query:

            return True

    return False


# ==============================================================
# Detect Bus Type
# ==============================================================

def detect_bus_type(query):

    query = query.lower()

    for bus_type in BUS_TYPES:

        if bus_type in query:

            return bus_type.title()

    return None


# ==============================================================
# Detect Amenities
# ==============================================================

def detect_amenities(query):

    query = query.lower()

    found = []

    for amenity in AMENITIES:

        if amenity in query:

            found.append(amenity.title())

    return found


# ==============================================================
# Detect Time Keywords
# ==============================================================

def detect_time(query):

    query = query.lower()

    found = []

    for keyword in TIME_KEYWORDS:

        if keyword in query:

            found.append(keyword.title())

    return found


# ==============================================================
# Detect Seat Intent
# ==============================================================

def detect_seat(query):

    query = query.lower()

    for seat in SEAT_KEYWORDS:

        if seat in query:

            return True

    return False


# ==============================================================
# Detect Rating Intent
# ==============================================================

def detect_rating(query):

    query = query.lower()

    for rating in RATING_KEYWORDS:

        if rating in query:

            return True

    return False


# ==============================================================
# Detect Operator
# ==============================================================

def detect_operator(query):

    query = query.lower()

    for operator in OPERATORS:

        if operator in query:

            return operator.upper()

    return None


# ==============================================================
# Detect Policy Intent
# ==============================================================

def detect_policy(query):

    query = query.lower()

    for keyword in POLICY_KEYWORDS:

        if keyword in query:

            return True

    return False


# ==============================================================
# Tamil / Tanglish Support
# ==============================================================

TAMIL_WORDS = {

    "iruka": "available",

    "venum": "need",

    "kaatu": "show",

    "ku": "under",

    "keela": "below",

    "bus venum": "bus",

    "la irundhu": "from",

    "pogum": "to",

    "irunthu": "from",

    "vara": "to"

}


def normalize_tamil(query):

    text = query.lower()

    for tamil, english in TAMIL_WORDS.items():

        text = text.replace(tamil, english)

    return text

# ==============================================================
# Parse Query
# ==============================================================

def parse_query(query):
    """
    Parse a user query and return all detected intents.
    """

    # Normalize Tamil/Tanglish before processing
    normalized_query = normalize_tamil(query)

    result = {

        "original_query": query,

        "normalized_query": normalized_query,

        "is_greeting": is_greeting(normalized_query),

        "route": detect_route(normalized_query),

        "fare_intent": detect_fare_intent(normalized_query),

        "price": detect_price(normalized_query),

        "bus_type": detect_bus_type(normalized_query),

        "amenities": detect_amenities(normalized_query),

        "time": detect_time(normalized_query),

        "seat_intent": detect_seat(normalized_query),

        "rating_intent": detect_rating(normalized_query),

        "operator": detect_operator(normalized_query),

        "policy_intent": detect_policy(normalized_query)

    }

    return result


# ==============================================================
# Intent Name
# ==============================================================

def detect_primary_intent(parsed):

    if parsed["is_greeting"]:
        return "greeting"

    if parsed["route"]["destination"] is not None:
        return "route_search"

    if parsed["fare_intent"]:
        return "fare_search"

    if parsed["bus_type"] is not None:
        return "bus_type"

    if len(parsed["amenities"]) > 0:
        return "amenities"

    if len(parsed["time"]) > 0:
        return "timing"

    if parsed["seat_intent"]:
        return "seat"

    if parsed["rating_intent"]:
        return "rating"

    if parsed["operator"] is not None:
        return "operator"

    if parsed["policy_intent"]:
        return "policy"

    return "general"


# ==============================================================
# Chatbot Helper
# ==============================================================

def analyze_query(query):
    """
    Returns complete analysis including primary intent.
    """

    parsed = parse_query(query)

    parsed["intent"] = detect_primary_intent(parsed)

    return parsed


# ==============================================================
# Test Mode
# ==============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Tamil Nadu Private Omni Bus AI Chatbot")
    print("Intent Engine V1")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        query = input("\nAsk : ")

        if query.lower() == "exit":
            break

        result = analyze_query(query)

        print("\nDetected Information")
        print("-" * 60)

        for key, value in result.items():
            print(f"{key:20}: {value}")

        if result["is_greeting"]:
            print("\n" + GREETING_RESPONSE)


# ==============================================================
# Example Queries
# ==============================================================

"""
Try:

hi

hello

vanakkam

show buses from Chennai to Madurai

bus from Salem to Trichy

cheapest bus

budget bus under 900

AC Sleeper bus

Volvo bus

bus with wifi

bus with charging

night bus

morning bus

available seats

window seat

best rated bus

SRM bus

KPN bus

refund policy

cancellation

Chennai la irundhu Madurai bus

Madurai bus venum

1000 ku keela bus

wifi iruka

AC sleeper bus venum

Volvo bus kaatu
"""

