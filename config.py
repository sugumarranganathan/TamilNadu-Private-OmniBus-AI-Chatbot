"""
==========================================================
Tamil Nadu Private Omni Bus AI Chatbot
Configuration File
==========================================================
"""

# ==========================================================
# Application
# ==========================================================

APP_TITLE = "🚌 Tamil Nadu Private Omni Bus AI Chatbot"
APP_SUBTITLE = "Find the Best Private Omni Buses Using AI"

# ==========================================================
# Data Files
# ==========================================================

CSV_FILE = "data/bus_services.csv"
DOCUMENTS_FILE = "data/documents.pkl"
FAISS_INDEX_FILE = "data/bus_index.faiss"

# ==========================================================
# AI Model
# ==========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==========================================================
# Search Settings
# ==========================================================

TOP_K = 5
CONFIDENCE_THRESHOLD = 0.30

# ==========================================================
# UI Settings
# ==========================================================

CHATBOT_HEIGHT = 650
THEME = "soft"

# ==========================================================
# Colors
# ==========================================================

PRIMARY_COLOR = "#2563EB"
SUCCESS_COLOR = "#22C55E"
WARNING_COLOR = "#F59E0B"

BACKGROUND_COLOR = "#0F172A"
SIDEBAR_COLOR = "#111827"
CARD_COLOR = "#1E293B"

TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#CBD5E1"

# ==========================================================
# Quick Suggestions
# ==========================================================

QUICK_QUESTIONS = [
    "Show buses from Chennai to Madurai",
    "Show buses from Chennai to Coimbatore",
    "Cheapest bus",
    "Luxury Sleeper bus",
    "AC Sleeper",
    "Volvo bus",
    "Night bus",
    "Morning bus",
    "Bus with WiFi",
    "Bus with Charging",
    "Bus under ₹1000",
    "Best rated bus"
]
