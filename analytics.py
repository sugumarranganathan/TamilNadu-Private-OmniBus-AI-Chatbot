
"""
analytics.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
Analytics Module (Version 1.0)
=================================================
"""

from collections import Counter
from statistics import mean


class BusAnalytics:

    def __init__(self, buses):
        self.buses = buses or []

    def total_buses(self):
        return len(self.buses)

    def total_routes(self):
        return len({
            (b.get("From_City"), b.get("To_City"))
            for b in self.buses
        })

    def total_operators(self):
        return len({
            b.get("Operator")
            for b in self.buses
        })

    def average_fare(self):
        fares = [float(b["Fare"]) for b in self.buses if b.get("Fare") not in (None, "")]
        return round(mean(fares), 2) if fares else 0

    def average_rating(self):
        ratings = [float(b["Rating"]) for b in self.buses if b.get("Rating") not in (None, "")]
        return round(mean(ratings), 2) if ratings else 0

    def bus_type_distribution(self):
        return Counter(b.get("Bus_Type", "Unknown") for b in self.buses)

    def operator_distribution(self):
        return Counter(b.get("Operator", "Unknown") for b in self.buses)

    def route_distribution(self):
        return Counter(
            f'{b.get("From_City")} ➜ {b.get("To_City")}'
            for b in self.buses
        )

    def top_operators(self, limit=5):
        return self.operator_distribution().most_common(limit)

    def fare_range(self):
        fares = [float(b["Fare"]) for b in self.buses if b.get("Fare") not in (None, "")]
        if not fares:
            return (0, 0)
        return (min(fares), max(fares))

    def summary(self):
        low, high = self.fare_range()
        return {
            "Total Buses": self.total_buses(),
            "Total Routes": self.total_routes(),
            "Total Operators": self.total_operators(),
            "Average Fare": self.average_fare(),
            "Fare Range": f"₹{low:.0f} - ₹{high:.0f}",
            "Average Rating": self.average_rating(),
            "Top Operators": self.top_operators()
        }

    def markdown_report(self):
        s = self.summary()

        lines = [
            "# 📊 OmniBus Analytics Report",
            "",
            f"**🚌 Total Buses:** {s['Total Buses']}",
            f"**🛣 Total Routes:** {s['Total Routes']}",
            f"**🏢 Total Operators:** {s['Total Operators']}",
            f"**💰 Average Fare:** ₹{s['Average Fare']:.2f}",
            f"**💵 Fare Range:** {s['Fare Range']}",
            f"**⭐ Average Rating:** {s['Average Rating']}",
            "",
            "## 🏆 Top Operators"
        ]

        for op, count in s["Top Operators"]:
            lines.append(f"- {op}: {count} bus(es)")

        return "\n".join(lines)


if __name__ == "__main__":
    sample = [
        {"Operator":"SkyBus","From_City":"Chennai","To_City":"Madurai","Fare":1400,"Rating":4.8,"Bus_Type":"AC Sleeper"},
        {"Operator":"SkyBus","From_City":"Chennai","To_City":"Salem","Fare":950,"Rating":4.4,"Bus_Type":"Semi Sleeper"},
        {"Operator":"Fast Wheels","From_City":"Chennai","To_City":"Madurai","Fare":1250,"Rating":4.2,"Bus_Type":"AC Sleeper"},
    ]

    analytics = BusAnalytics(sample)
    print(analytics.markdown_report())
