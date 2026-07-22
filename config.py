"""
config.py
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
Production Configuration
Version 7.0
=========================================================
"""

from pathlib import Path

# =========================================================
# Application
# =========================================================

APP_NAME = "Tamil Nadu Private OmniBus AI Chatbot"
APP_VERSION = "7.0.0"
AUTHOR = "Sugumar R"

# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
UTILS_DIR = BASE_DIR / "utils"
ASSETS_DIR = BASE_DIR / "assets"

# =========================================================
# Dataset Files
# =========================================================

CSV_FILE = DATA_DIR / "bus_services.csv"
INDEX_FILE = DATA_DIR / "bus_index.faiss"
DOCUMENTS_FILE = DATA_DIR / "documents.pkl"

# Backward-compatible aliases
BUS_CSV = CSV_FILE
FAISS_INDEX = INDEX_FILE

# =========================================================
# Embedding Model
# =========================================================

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_MODEL = MODEL_NAME

# =========================================================
# Search Configuration
# =========================================================

TOP_K = 20
MIN_CONFIDENCE = 0.30

# =========================================================
# UI Configuration
# =========================================================

STYLE_FILE = ASSETS_DIR / "style.css"

TITLE = "🚌 Tamil Nadu Private OmniBus AI Chatbot"
CHAT_HEIGHT = 600

EXAMPLE_QUERIES = [
    "Show buses from Chennai to Madurai",
    "Cheapest bus",
    "Luxury Sleeper bus",
    "Bus under 1000",
    "Bus with WiFi",
    "Night bus",
    "Volvo bus",
    "Best rated bus",
    "AC Sleeper bus",
    "Bus after 10 PM",
]

# =========================================================
# Domain Constants
# =========================================================

BUS_TYPES = [
    "AC",
    "Non AC",
    "Sleeper",
    "Semi Sleeper",
    "Luxury Sleeper",
    "Seater",
    "Volvo",
    "Bharat Benz",
]

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

TIME_SLOTS = {
    "morning": (5, 11),
    "afternoon": (12, 16),
    "evening": (17, 20),
    "night": (21, 4),
}

GREETINGS = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
]

# =========================================================
# Validation
# =========================================================

REQUIRED_FILES = [
    CSV_FILE,
    INDEX_FILE,
    DOCUMENTS_FILE,
]

def validate_project() -> bool:
    """Validate required project files exist."""
    missing = [str(f) for f in REQUIRED_FILES if not f.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required project files:\n- " + "\n- ".join(missing)
        )
    return True
