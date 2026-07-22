
"""
chatbot_v6.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Professional Chatbot Layer (Version 6.0)
=========================================
"""

from search_engine import BusSearchEngine
from utils.intent import analyze_query


class BusChatbot:
    def __init__(self):
        self.engine = BusSearchEngine()

    def greeting(self):
        return (
            "# 👋 Welcome to Tamil Nadu Private OmniBus AI Chatbot\n\n"
            "Try asking:\n"
            "- Show buses from Chennai to Madurai\n"
            "- Night Luxury Sleeper to Bangalore\n"
            "- Bus under 1000 with WiFi\n"
            "- Cheapest Volvo bus\n"
            "- Best rated buses"
        )

    def _card(self, bus: dict, index: int) -> str:
        return f"""## 🚌 Bus {index}

**Operator:** {bus.get('Operator','N/A')}

📍 **Route:** {bus.get('From_City','')} ➜ {bus.get('To_City','')}

🚍 **Bus:** {bus.get('Bus_Name','')} ({bus.get('Bus_Type','')})

🕒 **Departure:** {bus.get('Departure_Time','')}  
🕒 **Arrival:** {bus.get('Arrival_Time','')}

💰 **Fare:** ₹{bus.get('Fare','')}

⭐ **Rating:** {bus.get('Rating','')}

💺 **Available Seats:** {bus.get('Available_Seats','')}

📍 **Boarding:** {bus.get('Boarding_Point','')}

📍 **Dropping:** {bus.get('Dropping_Point','')}

🎁 **Amenities:** {bus.get('Amenities','')}
"""

    def no_results(self, intent):
        tips = []
        if intent.get("max_price"):
            tips.append("• Increase the maximum fare.")
        if intent.get("amenities"):
            tips.append("• Remove one or more amenity filters.")
        if intent.get("bus_type"):
            tips.append("• Try a different bus type.")
        tips.append("• Check the city names or try a nearby city.")

        return (
            "## ❌ No matching buses found.\n\n"
            "### Suggestions\n" +
            "\n".join(tips)
        )

    def reply(self, query: str) -> str:
        query = (query or "").strip()

        if not query:
            return "Please enter a search query."

        intent = analyze_query(query)

        if intent.get("greeting"):
            return self.greeting()

        buses = self.engine.search(query)

        if not buses:
            return self.no_results(intent)

        header = f"# ✅ Found {len(buses)} Matching Bus(es)\n"
        cards = [self._card(bus, i) for i, bus in enumerate(buses[:5], start=1)]

        footer = ""
        if len(buses) > 5:
            footer = f"\n---\nShowing first 5 of {len(buses)} buses."

        return header + "\n\n---\n\n".join(cards) + footer


if __name__ == "__main__":
    bot = BusChatbot()

    print("=" * 60)
    print("Tamil Nadu Private OmniBus AI Chatbot V6")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        q = input("\nYou: ")
        if q.lower() == "exit":
            break

        print("\nAssistant:\n")
        print(bot.reply(q))
