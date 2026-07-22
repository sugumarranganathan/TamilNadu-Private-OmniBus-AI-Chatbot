
"""
utils/formatter.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
Response Formatting Utilities (Version 1.0)
=================================================
"""

from statistics import mean


LINE = "━" * 38


def format_currency(value):
    try:
        return f"₹{float(value):,.0f}"
    except Exception:
        return str(value)


def format_rating(value):
    try:
        return f"⭐ {float(value):.1f}"
    except Exception:
        return "⭐ N/A"


def format_bus_card(bus: dict, index: int = None) -> str:
    title = f"🚌 Bus {index}" if index else "🚌 Bus"

    return f"""{LINE}

## {title}

**Operator:** {bus.get("Operator","N/A")}

📍 **Route:** {bus.get("From_City","")} ➜ {bus.get("To_City","")}

🚍 **Bus:** {bus.get("Bus_Name","")} ({bus.get("Bus_Type","")})

🕒 **Departure:** {bus.get("Departure_Time","")}
🕒 **Arrival:** {bus.get("Arrival_Time","")}

💰 **Fare:** {format_currency(bus.get("Fare"))}

⭐ **Rating:** {format_rating(bus.get("Rating"))}

💺 **Available Seats:** {bus.get("Available_Seats","N/A")}

📍 **Boarding:** {bus.get("Boarding_Point","N/A")}
📍 **Dropping:** {bus.get("Dropping_Point","N/A")}

🎁 **Amenities:** {bus.get("Amenities","N/A")}

{LINE}
"""


def format_bus_list(results, limit=5):
    if not results:
        return "❌ No matching buses found."

    output = [f"# ✅ Found {len(results)} Matching Bus(es)\n"]

    for i, bus in enumerate(results[:limit], start=1):
        output.append(format_bus_card(bus, i))

    if len(results) > limit:
        output.append(f"\nShowing first {limit} of {len(results)} buses.")

    return "\n".join(output)


def fare_summary(results):
    if not results:
        return "Fare information is unavailable."

    fares = []
    for bus in results:
        try:
            fares.append(float(bus["Fare"]))
        except Exception:
            pass

    if not fares:
        return "Fare information is unavailable."

    return (
        "# 💰 Fare Summary\n\n"
        f"- Lowest Fare : {format_currency(min(fares))}\n"
        f"- Highest Fare : {format_currency(max(fares))}\n"
        f"- Average Fare : {format_currency(mean(fares))}"
    )


def route_summary(results):
    if not results:
        return "No buses available."

    route = f"{results[0].get('From_City','')} ➜ {results[0].get('To_City','')}"
    operators = len({b.get("Operator") for b in results})

    return (
        "# 📊 Route Summary\n\n"
        f"- Route : {route}\n"
        f"- Total Buses : {len(results)}\n"
        f"- Operators : {operators}"
    )


if __name__ == "__main__":
    sample = [{
        "Operator": "Fast Wheels",
        "From_City": "Chennai",
        "To_City": "Madurai",
        "Bus_Name": "Express",
        "Bus_Type": "AC Sleeper",
        "Departure_Time": "20:30",
        "Arrival_Time": "05:30",
        "Fare": 1250,
        "Rating": 4.7,
        "Available_Seats": 18,
        "Boarding_Point": "Koyambedu",
        "Dropping_Point": "Mattuthavani",
        "Amenities": "WiFi,Charging,Water"
    }]

    print(format_bus_list(sample))
    print()
    print(fare_summary(sample))
    print()
    print(route_summary(sample))
