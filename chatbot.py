
"""
chatbot.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Chatbot Response Layer (Version 4.0)
=========================================
"""

from search_engine import BusSearchEngine
from utils.intent import analyze_query


class BusChatbot:
    def __init__(self):
        self.engine = BusSearchEngine()

    def _format_bus(self, bus: dict) -> str:
        return (
            f"🚌 **{bus.get('Operator','N/A')}**\n"
            f"**Route:** {bus.get('From_City')} → {bus.get('To_City')}\n"
            f"**Bus:** {bus.get('Bus_Name','')} ({bus.get('Bus_Type','')})\n"
            f"**Departure:** {bus.get('Departure_Time','')} | "
            f"**Arrival:** {bus.get('Arrival_Time','')}\n"
            f"**Fare:** ₹{bus.get('Fare','N/A')}\n"
            f"**Seats Available:** {bus.get('Available_Seats','N/A')}\n"
            f"**Amenities:** {bus.get('Amenities','N/A')}\n"
            f"**Rating:** ⭐ {bus.get('Rating','N/A')}"
        )

    def _greeting(self) -> str:
        return (
            "👋 Hello! I'm your Tamil Nadu Private OmniBus AI Assistant.\n\n"
            "You can ask questions like:\n"
            "- Show buses from Chennai to Madurai\n"
            "- Cheapest bus to Coimbatore\n"
            "- Luxury Sleeper bus under 1000\n"
            "- Night bus with WiFi"
        )

    def reply(self, query: str) -> str:
        query = (query or "").strip()
        if not query:
            return "Please enter a bus search query."

        intent = analyze_query(query)

        if intent.get("greeting"):
            return self._greeting()

        results = self.engine.search(query)

        if not results:
            return (
                "❌ No matching buses found.\n\n"
                "Try changing the city, bus type, fare limit, or amenities."
            )

        response = [f"### Found {len(results)} matching bus(es)\n"]

        for i, bus in enumerate(results[:5], start=1):
            response.append(f"## {i}\n{self._format_bus(bus)}")

        if len(results) > 5:
            response.append(
                f"\nShowing first 5 of {len(results)} matching buses."
            )

        return "\n\n---\n\n".join(response)


if __name__ == "__main__":
    bot = BusChatbot()

    print("=" * 60)
    print("Tamil Nadu Private OmniBus AI Chatbot")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        q = input("\nYou: ")
        if q.lower() == "exit":
            break

        print("\nAssistant:\n")
        print(bot.reply(q))
