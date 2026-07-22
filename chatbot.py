"""
chatbot.py
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
Professional Chatbot Controller
Version 7.0
Part 1 / 2
=========================================================
"""

import re

from search_engine import BusSearchEngine
from memory import memory

from utils.intent import analyze_query

from utils.formatter import (
    format_bus_list,
    fare_summary,
    route_summary,
)


class BusChatbot:
    """
    Professional Chatbot Controller

    Responsibilities
    ----------------
    ✓ Greeting detection
    ✓ Intent parsing
    ✓ Conversation memory
    ✓ Analytics requests
    ✓ Search requests
    ✓ Response formatting
    """

    def __init__(self):

        self.engine = BusSearchEngine()

        self.analytics_keywords = {

            "statistics",
            "stats",
            "analytics",
            "summary",
            "dataset",

            "total buses",
            "total routes",
            "operators",

            "average fare",
            "average rating",

            "top operators",
        }

    # ----------------------------------------------------
    # Greeting
    # ----------------------------------------------------

    def greeting(self):

        return (
            "# 🚌 Tamil Nadu Private OmniBus AI Chatbot\n\n"
            "Welcome!\n\n"
            "You can ask naturally.\n\n"

            "### Examples\n\n"

            "• Chennai to Madurai\n"
            "• Luxury Sleeper bus\n"
            "• Cheapest bus under 1000\n"
            "• Night bus with WiFi\n"
            "• Best rated Volvo bus\n"
            "• Bus fare Chennai Madurai\n"
            "• Average fare\n"
            "• Dataset statistics\n"
        )

    # ----------------------------------------------------
    # Empty Query
    # ----------------------------------------------------

    def empty_query(self):

        return (
            "Please enter a bus search query.\n\n"
            "Example:\n"
            "- Chennai to Madurai\n"
            "- WiFi bus\n"
        )

    # ----------------------------------------------------
    # No Results
    # ----------------------------------------------------

    def no_results(self, intent):

        tips = []

        if intent.get("max_price"):
            tips.append("• Increase the maximum fare.")

        if intent.get("amenities"):
            tips.append("• Remove one or more amenity filters.")

        if intent.get("bus_type"):
            tips.append("• Try another bus type.")

        if intent.get("operator"):
            tips.append("• Try another operator.")

        if intent.get("time"):
            tips.append("• Remove the time filter.")

        tips.append("• Check spelling of city names.")

        return (
            "# ❌ No matching buses found.\n\n"
            "## Suggestions\n\n"
            + "\n".join(tips)
        )

    # ----------------------------------------------------
    # Analytics Detection
    # ----------------------------------------------------

    def is_analytics_query(self, query):

        q = query.lower()

        for word in self.analytics_keywords:

            if word in q:
                return True

        return False

    # ----------------------------------------------------
    # Analytics Response
    # ----------------------------------------------------

    def analytics_response(self):

        stats = self.engine.analytics()

        response = "# 📊 Dataset Analytics\n\n"

        response += (
            f"🚌 Total Buses : {stats['Total Buses']}\n\n"
            f"🛣 Total Routes : {stats['Total Routes']}\n\n"
            f"🏢 Total Operators : {stats['Total Operators']}\n\n"
            f"💰 Average Fare : ₹{stats['Average Fare']}\n\n"
            f"⭐ Average Rating : {stats['Average Rating']}\n\n"
            f"💵 Fare Range : {stats['Fare Range']}\n\n"
        )

        response += "## 🏆 Top Operators\n\n"

        for operator, count in stats["Top Operators"]:

            response += f"• {operator} ({count} buses)\n"

        return response

    # ----------------------------------------------------
    # Fare Question
    # ----------------------------------------------------

    def is_fare_question(self, query):

        q = query.lower()

        patterns = [

            "fare",

            "ticket price",

            "price",

            "cost",

            "how much",

        ]

        return any(p in q for p in patterns)

    # ----------------------------------------------------
    # Route Summary Question
    # ----------------------------------------------------

    def is_route_summary(self, query):

        q = query.lower()

        patterns = [

            "how many buses",

            "total buses",

            "available buses",

        ]

        return any(p in q for p in patterns)

    # ----------------------------------------------------
    # Main Reply Function
    # ----------------------------------------------------

    def reply(self, query: str) -> str:
        """
        Main chatbot entry point.
        """

        query = (query or "").strip()

        # ---------------- Empty ----------------

        if not query:
            return self.empty_query()

        # ---------------- Intent ----------------

        intent = analyze_query(query)

        # ---------------- Greeting ----------------

        if intent.get("greeting"):
            return self.greeting()

        # ---------------- Conversation Memory ----------------

        intent = memory.process(intent)

        # ---------------- Analytics ----------------

        if self.is_analytics_query(query):
            return self.analytics_response()

        # ---------------- Search ----------------

        buses = self.engine.search(
            query=query,
            intent=intent,
        )

        # ---------------- No Results ----------------

        if not buses:
            return self.no_results(intent)

        # ---------------- Fare Questions ----------------

        if self.is_fare_question(query):
            return fare_summary(buses)

        # ---------------- Route Summary ----------------

        if self.is_route_summary(query):
            return route_summary(buses)

        # ---------------- Normal Bus Results ----------------

        return format_bus_list(
            buses,
            limit=5,
        )


# ==========================================================
# Command Line Testing
# ==========================================================

if __name__ == "__main__":

    chatbot = BusChatbot()

    print("=" * 70)
    print("Tamil Nadu Private OmniBus AI Chatbot")
    print("Version 7.0")
    print("=" * 70)

    print("\nExamples")
    print("----------------------------")
    print("Chennai to Madurai")
    print("Luxury Sleeper")
    print("Bus under 1000")
    print("Night bus with WiFi")
    print("Average Fare")
    print("Dataset Statistics")
    print("exit")
    print("----------------------------")

    while True:

        query = input("\nYou : ")

        if query.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        print("\nAssistant:\n")

        try:
            response = chatbot.reply(query)
            print(response)

        except Exception as e:

            print("\nUnexpected Error")
            print(e)

