"""
==============================================================
Tamil Nadu Private Omni Bus AI Chatbot
chatbot.py

Version : 1.0
Part : 1 / 2

This module:

✔ Receives user query
✔ Calls Search Engine
✔ Formats beautiful responses
✔ Handles greeting messages

==============================================================
"""

from utils.intent import analyze_query, GREETING_RESPONSE
from search_engine import search_buses

# ==========================================================
# Constants
# ==========================================================

MAX_RESULTS = 5

DIVIDER = "\n" + "─" * 55 + "\n"

# ==========================================================
# Emoji Icons
# ==========================================================

ICONS = {
    "bus": "🚌",
    "route": "📍",
    "departure": "🕘",
    "arrival": "🕗",
    "fare": "💰",
    "seat": "💺",
    "rating": "⭐",
    "amenity": "✨",
    "operator": "🏢",
    "type": "🚍"
}

# ==========================================================
# Greeting
# ==========================================================

def greeting_message():
    return GREETING_RESPONSE

# ==========================================================
# No Result Message
# ==========================================================

def no_result_message():

    return """
😔 Sorry!

No matching buses were found.

Try asking:

• Chennai to Madurai
• Cheapest bus
• Luxury Sleeper
• Bus under 1000
• Bus with WiFi
• Night bus
"""

# ==========================================================
# Format Amenities
# ==========================================================

def format_amenities(amenities):

    if amenities is None:
        return "N/A"

    if str(amenities).strip() == "":
        return "N/A"

    return amenities

# ==========================================================
# Format Single Bus Card
# ==========================================================

def format_bus(bus):

    operator = bus.get("Operator", "Unknown")

    bus_name = bus.get("Bus_Name", "")

    source = bus.get("From_City", "")

    destination = bus.get("To_City", "")

    departure = bus.get("Departure_Time", "")

    arrival = bus.get("Arrival_Time", "")

    duration = bus.get("Duration", "")

    fare = bus.get("Fare", "")

    seats = bus.get("Available_Seats", "")

    rating = bus.get("Rating", "")

    bus_type = bus.get("Bus_Type", "")

    amenities = format_amenities(
        bus.get("Amenities", "")
    )

    response = f"""
{ICONS["bus"]} **{operator}**

**{bus_name}**

{ICONS["route"]} Route
{source} ➜ {destination}

{ICONS["type"]} Bus Type
{bus_type}

{ICONS["departure"]} Departure
{departure}

{ICONS["arrival"]} Arrival
{arrival}

⏳ Duration
{duration}

{ICONS["fare"]} Fare
₹ {fare}

{ICONS["seat"]} Available Seats
{seats}

{ICONS["rating"]} Rating
⭐ {rating}

{ICONS["amenity"]} Amenities
{amenities}
"""

    if "Confidence" in bus:

        response += f"\n🤖 AI Match Score : {bus['Confidence']}"

    return response

# ==========================================================
# Format Multiple Results
# ==========================================================

def format_results(results):

    if len(results) == 0:

        return no_result_message()

    response = f"""
## 🚌 Found {len(results)} Bus Result(s)

"""

    count = 0

    for bus in results:

        count += 1

        if count > MAX_RESULTS:
            break

        response += DIVIDER

        response += format_bus(bus)

    return response

# ==========================================================
# Chatbot Response
# ==========================================================

def chatbot_response(query):

    try:

        # -----------------------------------------
        # Validate Input
        # -----------------------------------------

        if query is None:
            return "❌ Please enter a question."

        query = query.strip()

        if len(query) == 0:
            return "❌ Please enter a question."

        # -----------------------------------------
        # Analyze Intent
        # -----------------------------------------

        parsed = analyze_query(query)

        # -----------------------------------------
        # Greeting
        # -----------------------------------------

        if parsed["is_greeting"]:
            return greeting_message()

        # -----------------------------------------
        # Search
        # -----------------------------------------

        buses = search_buses(query)

        if len(buses) == 0:
            return no_result_message()

        # -----------------------------------------
        # Header
        # -----------------------------------------

        response = f"""
# 🚌 Tamil Nadu Private Omni Bus AI Chatbot

You asked:

> {query}

"""

        # Route Information
        if parsed["route"]["destination"]:

            source = parsed["route"]["source"]
            destination = parsed["route"]["destination"]

            if source:

                response += f"""
📍 **Route:** {source} ➜ {destination}

"""

            else:

                response += f"""
📍 **Destination:** {destination}

"""

        # Budget Information
        if parsed["price"]:

            response += f"""
💰 **Budget:** Under ₹{parsed['price']}

"""

        # Bus Type
        if parsed["bus_type"]:

            response += f"""
🚌 **Bus Type:** {parsed['bus_type']}

"""

        # Amenities
        if parsed["amenities"]:

            response += f"""
✨ **Amenities:** {", ".join(parsed["amenities"])}

"""

        response += "\n---\n"

        # -----------------------------------------
        # Bus Results
        # -----------------------------------------

        response += format_results(buses)

        return response

    except Exception as e:

        return f"""
❌ Something went wrong.

Error:

{str(e)}

Please try another query.
"""


# ==========================================================
# Test Mode
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("Tamil Nadu Private Omni Bus AI Chatbot")
    print("Chatbot Engine V1")
    print("=" * 70)

    while True:

        q = input("\nYou : ")

        if q.lower() == "exit":
            break

        answer = chatbot_response(q)

        print("\nBot:\n")
        print(answer)


# ==========================================================
# Sample Queries
# ==========================================================

"""
Try:

hi

hello

vanakkam

show buses from Chennai to Madurai

Madurai bus

Cheapest bus

Bus under 900

Luxury Sleeper

Volvo bus

AC bus

Bus with WiFi

Bus with Charging

Night bus

Morning bus

Window seat

Available seats

Best rated bus

SRM bus

KPN bus

Refund policy

Cancellation policy

Chennai la irundhu Madurai bus

Madurai bus venum

1000 ku keela bus

WiFi iruka

Volvo bus kaatu

"""
