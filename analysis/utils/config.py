"""
Configuration settings for the LogView360 application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_HOST = "0.0.0.0"  # Listen on all interfaces
API_PORT = 8000       # Default FastAPI port

# Paths Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_DIR = os.path.join(BASE_DIR, "source")
OUTPUT_DIR = os.path.join(BASE_DIR, "analysis", "output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Processing Configuration
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

# Anomaly Detection Configuration
LATENCY_THRESHOLD = 5.0  # seconds
ANOMALY_SCORE_THRESHOLD = float(os.getenv("ANOMALY_SCORE_THRESHOLD", "0.95"))

# Analysis settings
CACHE_DURATION = 300  # 5 minutes
MIN_STAGES = 2 