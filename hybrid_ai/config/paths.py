import os

# Base directory for the hybrid AI system
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# CNN model path (updated to .keras format)
CNN_MODEL_PATH = os.path.join(BASE_DIR, "models", "cnn_malware_detector.keras")

# Signature DB path
SIGNATURE_DB_PATH = os.path.join(BASE_DIR, "signature_db", "malware_hashes.txt")

# Quarantine folder
QUARANTINE_DIR = os.path.join(BASE_DIR, "quarantine")

# Log file path
LOG_FILE = os.path.join(BASE_DIR, "logs", "detection.log")
