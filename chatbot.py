
"""
chatbot.py
Version 3.0
Compatible with Gradio 6.x architecture.
"""

from typing import Dict, List

from search_engine import search_buses
from utils.intent import analyze_query


WELCOME_MESSAGE = (
    "🚌 Welcome to Tamil Nadu Private OmniBus AI Chatbot!\n\n"
    "Try:\n"
    "- Show buses from Chennai to Madurai\n"
    "- Luxury Sleeper buses\n"
    "- Bus under 1000\n"
    "- Bus with WiFi"
)


def _format_bus(bus: Dict) -> str:
    amenities = str(bus.get("Amenities", "")).replace(",", " • ")
    return (
        f"🚌 **{bus.get('Operator','')}**\n\n"
        f"**Route:** {bus.get('From_City','')} ➜ {bus.get('To_City','')}\n"
        f"**Bus:** {bus.get('Bus_Name','')}\n"
        f"**Type:** {bus.get('Bus_Type','')}\n"
        f"**Departure:** {bus.get('Departure_Time','')}\n"
        f"**Arrival:** {bus.get('Arrival_Time','')}\n"
        f"**Duration:** {bus.get('Duration','')}\n"
        f"**Fare:** ₹{bus.get('Fare','')}\n"
        f"**Seats:** {bus.get('Available_Seats','')} / {bus.get('Seats','')}\n"
        f"**Boarding:** {bus.get('Boarding_Point','')}\n"
        f"**Dropping:** {bus.get('Dropping_Point','')}\n"
        f"**Rating:** ⭐ {bus.get('Rating','')}\n"
        f"**Amenities:** {amenities}"
    )


def build_filters(intent: Dict) -> Dict:
    return {
        "from_city": intent.get("from_city"),
        "to_city": intent.get("to_city"),
        "bus_type": intent.get("bus_type"),
        "operator": intent.get("operator"),
        "max_price": intent.get("max_price"),
    }


def chatbot_response(user_query: str) -> str:
    """Return a plain text/Markdown response."""
    query = (user_query or "").strip()

    if not query:
        return "Please enter a bus search query."

    try:
        intent = analyze_query(query)
    except Exception:
        intent = {}

    try:
        buses = search_buses(query, build_filters(intent))
    except Exception as e:
        return f"❌ Search error:\n\n{e}"

    if not buses:
        return (
            "❌ No matching buses found.\n\n"
            "Try changing the route, fare, bus type or operator."
        )

    reply: List[str] = [f"### ✅ Found {len(buses)} matching bus(es)\n"]

    for i, bus in enumerate(buses[:10], start=1):
        reply.append(f"#### {i}. Result\n{_format_bus(bus)}")

    return "\n\n---\n\n".join(reply)


if __name__ == "__main__":
    print(WELCOME_MESSAGE)
    while True:
        q = input("\nYou: ")
        if q.lower() in {"exit", "quit"}:
            break
        print(chatbot_response(q))
