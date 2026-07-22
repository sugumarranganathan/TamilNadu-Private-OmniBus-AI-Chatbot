"""
=========================================================
Tamil Nadu Private OmniBus AI Chatbot

Utility Package

Contains:
- intent.py
- normalizer.py
- formatter.py
- ranking.py
- helpers.py
=========================================================
"""

from .intent import analyze_query

from .normalizer import (
    normalize_city,
    normalize_bus_type,
    normalize_amenities,
)

from .formatter import (
    format_bus_list,
    fare_summary,
    route_summary,
)

from .ranking import (
    rank_results,
    remove_duplicates,
)

from .helpers import (
    safe_int,
    safe_float,
)

__all__ = [
    "analyze_query",

    "normalize_city",
    "normalize_bus_type",
    "normalize_amenities",

    "format_bus_list",
    "fare_summary",
    "route_summary",

    "rank_results",
    "remove_duplicates",

    "safe_int",
    "safe_float",
]
