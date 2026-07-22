
"""
memory.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
Conversation Memory (Version 1.0)
=================================================
"""

from copy import deepcopy


class ConversationMemory:
    """
    Stores the latest search context so follow-up
    queries can reuse missing information.
    """

    FIELDS = (
        "from_city",
        "to_city",
        "bus_type",
        "operator",
        "amenities",
        "time",
        "min_price",
        "max_price",
        "sort",
    )

    def __init__(self):
        self.clear()

    def clear(self):
        self._context = {k: None for k in self.FIELDS}
        self._context["amenities"] = []

    def get_context(self):
        return deepcopy(self._context)

    def update(self, intent: dict):
        """
        Save non-empty values from the latest intent.
        """
        for key in self.FIELDS:
            if key not in intent:
                continue

            value = intent[key]

            if key == "amenities":
                if value:
                    self._context[key] = list(value)
            else:
                if value not in (None, "", []):
                    self._context[key] = value

    def merge(self, intent: dict):
        """
        Fill missing intent fields using stored context.
        """
        merged = deepcopy(intent)

        for key in self.FIELDS:
            if key == "amenities":
                if not merged.get(key):
                    merged[key] = list(self._context.get(key, []))
            else:
                if merged.get(key) in (None, "", []):
                    merged[key] = self._context.get(key)

        return merged

    def process(self, intent: dict):
        """
        Merge previous context into the current intent,
        then update memory.
        """
        merged = self.merge(intent)
        self.update(merged)
        return merged


# Global memory instance
memory = ConversationMemory()


if __name__ == "__main__":

    q1 = {
        "from_city": "Chennai",
        "to_city": "Madurai",
        "amenities": [],
        "bus_type": None,
        "operator": None,
        "time": None,
        "min_price": None,
        "max_price": None,
        "sort": None,
    }

    print("Query 1")
    print(memory.process(q1))

    q2 = {
        "from_city": None,
        "to_city": None,
        "amenities": ["wifi"],
        "bus_type": None,
        "operator": None,
        "time": None,
        "min_price": None,
        "max_price": None,
        "sort": None,
    }

    print("\nQuery 2 (follow-up)")
    print(memory.process(q2))

    print("\nCurrent Context")
    print(memory.get_context())
