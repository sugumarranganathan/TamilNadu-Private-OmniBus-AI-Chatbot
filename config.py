"""
config.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Production Configuration (Version 4.0)
=========================================
"""

from pathlib import Path

# ==========================================================
# Project Information
# ==========================================================

APP_NAME = "Tamil Nadu Private OmniBus AI Chatbot"
APP_VERSION = "4.0.0"
AUTHOR = "Sugumar R"

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
UTILS_DIR = BASE_DIR / "utils"

BUS_CSV = DATA_DIR / "bus_services.csv"
FAISS_INDEX = DATA_DIR / "bus_index.faiss"
DOCUMENTS_FILE = DATA_DIR / "documents.pkl"

STYLE_FILE = BASE_DIR / "style.css"

# ==========================================================
# AI Configuration
# ==========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 10

MIN_CONFIDENCE = 0.30

# ==========================================================
# Supported Bus Types
# ==========================================================

BUS_TYPES = [
    "AC",
    "Non AC",
    "Sleeper",
    "Seater",
    "Semi Sleeper",
    "Luxury Sleeper",
    "Volvo",
    "Bharat Benz",
]

# ==========================================================
# Supported Amenities
# ==========================================================

AMENITIES = [
    "AC",
    "WiFi",
    "Charging",
    "Blanket",
    "Water Bottle",
    "GPS",
    "TV",
    "Emergency Exit",
]

# ==========================================================
# Supported Time Slots
# ==========================================================

TIME_SLOTS = {
    "morning": (5, 11),
    "afternoon": (12, 16),
    "evening": (17, 20),
    "night": (21, 4),
}

# ==========================================================
# Greetings
# ==========================================================

GREETINGS = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
]

# ==========================================================
# Example Questions
# ==========================================================

EXAMPLE_QUERIES = [
    "Show buses from Chennai to Madurai",
    "Luxury Sleeper buses",
    "Bus under 1000",
    "Cheapest bus to Coimbatore",
    "Night bus to Salem",
    "Bus with WiFi",
    "Best rated bus",
    "Volvo bus",
    "AC Sleeper bus",
]

# ==========================================================
# UI
# ==========================================================

TITLE = "🚌 Tamil Nadu Private OmniBus AI Chatbot"
CHAT_HEIGHT = 550

# ==========================================================
# Validation
# ==========================================================

REQUIRED_FILES = [
    BUS_CSV,
    FAISS_INDEX,
    DOCUMENTS_FILE,
]


def validate_project():
    """Raise FileNotFoundError if required data files are missing."""
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required project files:\n- " + "\n- ".join(missing)
        )
    return True
