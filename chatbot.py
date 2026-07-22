"""
==========================================================
Tamil Nadu Private Omni Bus AI Chatbot
Chatbot Logic
==========================================================
"""

from search_engine import search_buses


def chatbot_response(user_query: str) -> str:
    """
    Main chatbot function.
    """

    if not user_query.strip():
        return "⚠️ Please enter your question."

    try:
        buses = search_buses(user_query)

        if not buses:
            return (
                "❌ No matching buses found.\n\n"
                "Try asking:\n"
                "- Show buses from Chennai to Madurai\n"
                "- Cheapest bus\n"
                "- AC Sleeper\n"
                "- Bus with WiFi"
            )

        response = f"## 🚌 Found {len(buses)} Matching Bus(es)\n\n"

        for i, bus in enumerate(buses, start=1):

            response += f"""
### {i}. {bus['Operator']}

**🚌 Bus Name:** {bus['Bus_Name']}

📍 **Route:** {bus['Source']} ➜ {bus['Destination']}

🛏 **Type:** {bus['Bus_Type']}

💰 **Fare:** ₹{bus['Fare']}

⭐ **Rating:** {bus['Rating']}

🕒 **Departure:** {bus['Departure_Time']}

🕕 **Arrival:** {bus['Arrival_Time']}

💺 **Available Seats:** {bus['Available_Seats']}

📶 **Amenities**

- AC : {bus['AC']}
- WiFi : {bus['WiFi']}
- Charging : {bus['Charging']}
- GPS : {bus['GPS']}
- CCTV : {bus['CCTV']}

---
"""

        return response

    except Exception as e:
        return f"❌ Error: {str(e)}"
