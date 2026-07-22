
"""
utils/helpers.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
General Helper Functions (Version 1.0)
=================================================
"""

from datetime import datetime
import re


def clean_text(text):
    """
    Clean and normalize input text.
    """
    if text is None:
        return ""

    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def safe_int(value, default=0):
    """
    Safely convert a value to int.
    """
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    """
    Safely convert a value to float.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_time(time_str):
    """
    Convert HH:MM to datetime.time.
    """
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except Exception:
        return None


def time_in_range(bus_time, start_time, end_time):
    """
    Check whether a bus departure time falls within a range.
    """
    bus = parse_time(bus_time)
    start = parse_time(start_time)
    end = parse_time(end_time)

    if not (bus and start and end):
        return False

    return start <= bus <= end


def is_night_bus(time_str):
    """
    Night = 18:00 to 05:59
    """
    t = parse_time(time_str)
    if t is None:
        return False

    return t.hour >= 18 or t.hour < 6


def is_morning_bus(time_str):
    t = parse_time(time_str)
    return t is not None and 5 <= t.hour < 12


def is_afternoon_bus(time_str):
    t = parse_time(time_str)
    return t is not None and 12 <= t.hour < 17


def is_evening_bus(time_str):
    t = parse_time(time_str)
    return t is not None and 17 <= t.hour < 21


def format_duration(hours):
    """
    Convert decimal hours to 'Xh Ym'.
    """
    try:
        total_minutes = int(float(hours) * 60)
        h = total_minutes // 60
        m = total_minutes % 60
        return f"{h}h {m}m"
    except Exception:
        return str(hours)


def unique_results(results):
    """
    Remove duplicate bus records.
    """
    unique = []
    seen = set()

    for bus in results:
        key = (
            bus.get("Operator"),
            bus.get("Bus_Name"),
            bus.get("From_City"),
            bus.get("To_City"),
            bus.get("Departure_Time"),
        )

        if key not in seen:
            seen.add(key)
            unique.append(bus)

    return unique


def sort_by_fare(results, ascending=True):
    return sorted(
        results,
        key=lambda x: safe_float(x.get("Fare")),
        reverse=not ascending
    )


def sort_by_rating(results):
    return sorted(
        results,
        key=lambda x: safe_float(x.get("Rating")),
        reverse=True
    )


def sort_by_departure(results):
    return sorted(
        results,
        key=lambda x: parse_time(x.get("Departure_Time", "23:59")) or datetime.max.time()
    )


if __name__ == "__main__":
    print(clean_text("  Chennai TO Madurai  "))
    print(safe_int("123"))
    print(safe_float("4.5"))
    print(is_night_bus("20:15"))
    print(format_duration(8.5))
