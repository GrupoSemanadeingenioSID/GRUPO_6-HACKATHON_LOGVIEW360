"""
Configuration settings for the LogView360 analysis module.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Paths Configuration
LOG_DIR = os.getenv("LOG_DIR", "logs")
DATA_DIR = os.getenv("DATA_DIR", "data")
MODEL_DIR = os.getenv("MODEL_DIR", "models")

# Processing Configuration
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

# Anomaly Detection Configuration
LATENCY_THRESHOLD = float(os.getenv("LATENCY_THRESHOLD", "5.0"))  # seconds
ANOMALY_SCORE_THRESHOLD = float(os.getenv("ANOMALY_SCORE_THRESHOLD", "0.95")) 