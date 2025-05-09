import os
import logging
import numpy as np
from hybrid_ai.utils.hash_utils import is_file_malicious
from hybrid_ai.fusion_engine.predictor import cnn_predict
from hybrid_ai.config.config import QUARANTINE_DIR

def move_to_quarantine(file_path):
    """Move a suspicious file to the quarantine directory."""
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    try:
        base_name = os.path.basename(file_path)
        quarantine_path = os.path.join(QUARANTINE_DIR, base_name)
        os.rename(file_path, quarantine_path)
        logging.warning(f"[QUARANTINE] Moved file to: {quarantine_path}")
    except Exception as e:
        logging.error(f"[ERROR] Failed to move to quarantine: {e}")

def scan_file(file_path):
    """Scan a file for malware using hybrid AI detection."""
    if not os.path.exists(file_path):
        logging.error(f"[ERROR] File not found: {file_path}")
        return

    # 1. Signature-based Detection
    is_malicious, signature_name = is_file_malicious(file_path)
    if is_malicious:
        logging.warning(f"[SIGNATURE] Detected malicious file: {file_path} (Signature: {signature_name})")
        move_to_quarantine(file_path)
        return

    # 2. CNN-based Detection
    prediction = cnn_predict(file_path)
    if prediction == 1:
        logging.warning(f"[AI-DETECTION] AI flagged {file_path} as MALICIOUS.")
        move_to_quarantine(file_path)
    else:
        logging.info(f"[SCAN] {file_path} is clean.")
