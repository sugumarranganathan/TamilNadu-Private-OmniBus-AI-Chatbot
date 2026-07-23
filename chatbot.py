"""
chatbot.py
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
Gemini + FAISS RAG Version
Version 10.0
=========================================================
"""

from search_engine import BusSearchEngine
from memory import memory

from llm import generate_answer

from utils.intent import analyze_query
from utils.formatter import (
    format_bus_list,
    fare_summary,
    route_summary,
)


class BusChatbot:
    """
    Tamil Nadu Private OmniBus AI Chatbot

    Workflow

    User
        │
        ▼
    Intent Detection
        │
        ▼
    FAISS Semantic Search
        │
        ▼
    Context Formatting
        │
        ▼
    Gemini
        │
        ▼
    Final AI Response
    """

    def __init__(self):
        self.engine = BusSearchEngine()

    def reply(self, query: str) -> str:

        query = query.strip()

        if not query:
            return "Please enter your question."

        # Save user query
        memory.add_user(query)

        # Detect intent
        intent = analyze_query(query)

        try:

            # --------------------------------------------------
            # Bus Search
            # --------------------------------------------------

            if intent == "bus_search":

                buses = self.engine.search(query)

                if not buses:
                    answer = (
                        "Sorry, I couldn't find any matching buses "
                        "for your request."
                    )

                else:

                    context = format_bus_list(buses)

                    answer = generate_answer(
                        question=query,
                        context=context,
                    )

            # --------------------------------------------------
            # Fare
            # --------------------------------------------------

            elif intent == "fare":

                buses = self.engine.search(query)

                if not buses:
                    answer = "Fare information not available."

                else:

                    context = fare_summary(buses)

                    answer = generate_answer(
                        question=query,
                        context=context,
                    )

            # --------------------------------------------------
            # Route
            # --------------------------------------------------

            elif intent == "route":

                buses = self.engine.search(query)

                if not buses:
                    answer = "Route information not available."

                else:

                    context = route_summary(buses)

                    answer = generate_answer(
                        question=query,
                        context=context,
                    )

            # --------------------------------------------------
            # General
            # --------------------------------------------------

            else:

                buses = self.engine.search(query)

                if buses:

                    context = format_bus_list(buses)

                    answer = generate_answer(
                        question=query,
                        context=context,
                    )

                else:

                    answer = (
                        "Sorry, I couldn't find any relevant "
                        "information in the bus database."
                    )

        except Exception as e:

            answer = f"❌ Error: {e}"

        memory.add_bot(answer)

        return answer
