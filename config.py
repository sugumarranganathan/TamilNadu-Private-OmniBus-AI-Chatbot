"""
config.py
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
Production Configuration
Version 8.0
=========================================================
"""

from pathlib import Path

# =========================================================
# Application
# =========================================================

APP_NAME = "Tamil Nadu Private OmniBus AI Chatbot"
APP_VERSION = "8.0.0"
AUTHOR = "Sugumar R"

# =========================================================
# Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
UTILS_DIR = BASE_DIR / "utils"

# =========================================================
# Dataset Files
# =========================================================

CSV_FILE = DATA_DIR / "bus_services.csv"
INDEX_FILE = DATA_DIR / "bus_index.faiss"
DOCUMENTS_FILE = DATA_DIR / "documents.pkl"

# Legacy aliases (backward compatibility)
BUS_CSV = CSV_FILE
FAISS_INDEX = INDEX_FILE

# =========================================================
# Embedding Model
# =========================================================

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_MODEL = MODEL_NAME

# =========================================================
# Search
# =========================================================

TOP_K = 20
MIN_CONFIDENCE = 0.30
MAX_RESULTS = 10

# =========================================================
# UI
# =========================================================

TITLE = "🚌 Tamil Nadu Private OmniBus AI Chatbot"
CHAT_HEIGHT = 600
STYLE_FILE = ASSETS_DIR / "style.css"

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
    "AC", "Non AC", "Sleeper", "Semi Sleeper",
    "Luxury Sleeper", "Seater", "Volvo", "Bharat Benz",
]

AMENITIES = [
    "AC", "WiFi", "Charging", "Blanket",
    "Water Bottle", "GPS", "TV", "Emergency Exit",
]

TIME_SLOTS = {
    "morning": (5, 11),
    "afternoon": (12, 16),
    "evening": (17, 20),
    "night": (21, 4),
}

GREETINGS = [
    "hi", "hello", "hey",
    "good morning", "good afternoon", "good evening",
]

# =========================================================
# Validation
# =========================================================

REQUIRED_FILES = [
    CSV_FILE,
    INDEX_FILE,
    DOCUMENTS_FILE,
]

def validate_project():
    """Raise an error if required project files are missing."""
    missing = [str(p) for p in REQUIRED_FILES if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required project files:\\n- " + "\\n- ".join(missing)
        )
    return True

def get_paths():
    """Return project paths as strings for libraries that do not support Path."""
    return {
        "csv": str(CSV_FILE),
        "index": str(INDEX_FILE),
        "documents": str(DOCUMENTS_FILE),
        "style": str(STYLE_FILE),
    }
