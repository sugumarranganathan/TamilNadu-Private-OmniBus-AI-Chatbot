"""
chatbot.py
===========

Chatbot layer for TamilNadu-Private-OmniBus-AI-Chatbot.

Works with:
    - search_engine.py
    - utils.intent.analyze_query
"""

from typing import Dict, List

from search_engine import search_buses
from utils.intent import analyze_query


WELCOME_MESSAGE = """
🚌 Welcome to Tamil Nadu Private OmniBus AI Chatbot!

Ask questions like:

• Show buses from Chennai to Madurai
• Cheapest bus to Coimbatore
• Luxury Sleeper buses
• Bus with WiFi
• Night buses
• AC Sleeper under ₹1000
""".strip()


def format_bus(bus: Dict) -> str:
    amenities = str(bus.get("Amenities", "")).replace(",", " • ")

    return f"""
🚌 {bus.get("Operator")}

🚏 Route:
{bus.get("From_City")} ➜ {bus.get("To_City")}

🛏 Bus:
{bus.get("Bus_Name")}

🚌 Type:
{bus.get("Bus_Type")}

🕒 Departure:
{bus.get("Departure_Time")}

🕒 Arrival:
{bus.get("Arrival_Time")}

⏳ Duration:
{bus.get("Duration")}

💰 Fare:
₹{bus.get("Fare")}

💺 Seats:
{bus.get("Available_Seats")} / {bus.get("Seats")}

📍 Boarding:
{bus.get("Boarding_Point")}

📍 Dropping:
{bus.get("Dropping_Point")}

⭐ Rating:
{bus.get("Rating")}

✨ Amenities:
{amenities}
""".strip()


def build_filters(intent: Dict) -> Dict:
    return {
        "from_city": intent.get("from_city"),
        "to_city": intent.get("to_city"),
        "bus_type": intent.get("bus_type"),
        "operator": intent.get("operator"),
        "max_price": intent.get("max_price"),
    }


def chatbot_response(user_query: str) -> str:
    if not user_query.strip():
        return "Please enter a bus search query."

    intent = analyze_query(user_query)
    filters = build_filters(intent)

    buses = search_buses(user_query, filters)

    if not buses:
        return (
            "❌ No matching buses found.\n\n"
            "Try another route, operator, fare or bus type."
        )

    reply: List[str] = [
        f"✅ Found {len(buses)} matching buses\n"
    ]

    for bus in buses[:10]:
        reply.append(format_bus(bus))
        reply.append("-" * 50)

    return "\n\n".join(reply)


if __name__ == "__main__":
    print(WELCOME_MESSAGE)
    print()
    while True:
        q = input("You: ")
        if q.lower() in ("exit", "quit"):
            break
        print()
        print(chatbot_response(q))
        print()
