"""
==============================================================
Tamil Nadu Private Omni Bus AI Chatbot
config.py

Central Configuration File

All project settings should be defined here.

==============================================================
"""

import os

# ==========================================================
# Project Information
# ==========================================================

APP_NAME = "Tamil Nadu Private Omni Bus AI Chatbot"

APP_VERSION = "1.0"

APP_DESCRIPTION = (
    "AI-powered chatbot for searching Tamil Nadu Private Omni Buses"
)

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ==========================================================
# Data Files
# ==========================================================

BUS_CSV = os.path.join(DATA_DIR, "bus_services.csv")

DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.pkl")

FAISS_INDEX = os.path.join(DATA_DIR, "bus_index.faiss")

# ==========================================================
# AI Model
# ==========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==========================================================
# Search Settings
# ==========================================================

TOP_K = 10

MAX_RESULTS = 5

MIN_AVAILABLE_SEATS = 1

# ==========================================================
# Gradio UI
# ==========================================================

PAGE_TITLE = "🚌 Tamil Nadu Private Omni Bus AI Chatbot"

CHATBOT_HEIGHT = 650

SHOW_FOOTER = True

SHOW_COPYRIGHT = True

# ==========================================================
# Theme
# ==========================================================

PRIMARY_COLOR = "#2563EB"

SECONDARY_COLOR = "#0F172A"

SUCCESS_COLOR = "#16A34A"

WARNING_COLOR = "#F59E0B"

ERROR_COLOR = "#DC2626"

BACKGROUND_COLOR = "#0B1120"

CARD_COLOR = "#1E293B"

TEXT_COLOR = "#FFFFFF"

# ==========================================================
# Default Messages
# ==========================================================

WELCOME_MESSAGE = """
👋 Welcome!

I can help you find the best Private Omni Buses in Tamil Nadu.

Try asking:

• Chennai to Madurai
• Cheapest bus
• Luxury Sleeper
• Bus with WiFi
• Night bus
"""

NO_RESULT_MESSAGE = """
😔 Sorry!

No buses were found.

Try:

• Another route
• Different budget
• Another bus type
"""

ERROR_MESSAGE = """
❌ Something went wrong.

Please try again.
"""

# ==========================================================
# Quick Questions
# ==========================================================

QUICK_QUESTIONS = [

    "Show buses from Chennai to Madurai",

    "Cheapest bus",

    "Luxury Sleeper",

    "Bus under 1000",

    "Bus with WiFi",

    "Bus with Charging",

    "Night bus",

    "Morning bus",

    "Best rated bus",

    "SRM bus"

]

# ==========================================================
# Supported Bus Types
# ==========================================================

SUPPORTED_BUS_TYPES = [

    "AC",

    "Non AC",

    "Sleeper",

    "Semi Sleeper",

    "Volvo",

    "Scania",

    "Luxury",

    "Premium"

]

# ==========================================================
# Supported Amenities
# ==========================================================

SUPPORTED_AMENITIES = [

    "WiFi",

    "Charging",

    "GPS",

    "Blanket",

    "Pillow",

    "Reading Light",

    "CCTV",

    "Water Bottle"

]
