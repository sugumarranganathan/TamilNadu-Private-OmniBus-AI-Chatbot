"""
config.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Production Configuration (Version 4.0)
=========================================
"""

from pathlib import Path

APP_NAME = "Tamil Nadu Private OmniBus AI Chatbot"
APP_VERSION = "4.0.0"
AUTHOR = "Sugumar R"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UTILS_DIR = BASE_DIR / "utils"

BUS_CSV = DATA_DIR / "bus_services.csv"
FAISS_INDEX = DATA_DIR / "bus_index.faiss"
DOCUMENTS_FILE = DATA_DIR / "documents.pkl"
STYLE_FILE = BASE_DIR / "style.css"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 10
MIN_CONFIDENCE = 0.30

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

EXAMPLE_QUERIES = [
    "Show buses from Chennai to Madurai",
    "Luxury Sleeper bus",
    "Bus under 1000",
    "Bus with WiFi",
    "Night bus to Salem",
    "Best rated bus",
]

TITLE = "🚌 Tamil Nadu Private OmniBus AI Chatbot"
CHAT_HEIGHT = 550

REQUIRED_FILES = [BUS_CSV, FAISS_INDEX, DOCUMENTS_FILE]

def validate_project():
    missing = [str(f) for f in REQUIRED_FILES if not f.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required project files:\n- " + "\n- ".join(missing)
        )
    return True
