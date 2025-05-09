import os
import hashlib
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from utils.hash_utils import compute_sha256
from utils.logger import log_detection
from hybrid_ai.config.paths import SIGNATURE_DB_PATH, CNN_MODEL_PATH

# Load signature database and CNN model
with open(SIGNATURE_DB_PATH, "r") as f:
    known_signatures = set(line.strip() for line in f.readlines())

cnn_model = load_model(CNN_MODEL_PATH)

def extract_features(file_path):
    """Basic static binary feature extraction (for demo purposes)."""
    with open(file_path, 'rb') as f:
        byte_data = f.read(200000)  # Limit size for consistency
    byte_array = np.frombuffer(byte_data, dtype=np.uint8)
    byte_array = np.pad(byte_array, (0, max(0, 200000 - len(byte_array))), 'constant')
    normalized = byte_array / 255.0
    return normalized.reshape(1, 200000)

def fusion_scan(file_path):
    file_hash = compute_sha256(file_path)

    # 1. Signature Match
    if file_hash in known_signatures:
        verdict = "malicious"
        log_detection(file_path, verdict, method="signature")
        return verdict

    # 2. CNN Prediction
    features = extract_features(file_path)
    prediction = cnn_model.predict(features)
    is_malicious = prediction[0][0] > 0.5

    verdict = "malicious" if is_malicious else "safe"
    log_detection(file_path, verdict, method="cnn" if is_malicious else "clean")
    return verdict
