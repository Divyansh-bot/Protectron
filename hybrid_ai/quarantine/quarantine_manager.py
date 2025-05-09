import os
import shutil
import hashlib
import logging
from datetime import datetime
from hybrid_ai.config.config import QUARANTINE_DIRECTORY

def hash_file(file_path):
    """Generate SHA256 hash for the file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def quarantine_file(file_path, reason="Suspicious activity"):
    """Move the file to quarantine with metadata."""
    try:
        if not os.path.exists(QUARANTINE_DIRECTORY):
            os.makedirs(QUARANTINE_DIRECTORY)

        base_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_val = hash_file(file_path)
        new_name = f"{base_name}_{timestamp}_{hash_val[:8]}.quarantine"

        target_path = os.path.join(QUARANTINE_DIRECTORY, new_name)
        shutil.move(file_path, target_path)

        logging.warning(f"[QUARANTINE] {file_path} moved to quarantine due to: {reason}")
        logging.info(f"[QUARANTINE] Saved as: {target_path}")
        return target_path
    except Exception as e:
        logging.error(f"[QUARANTINE] Failed to quarantine file: {e}")
        return None
