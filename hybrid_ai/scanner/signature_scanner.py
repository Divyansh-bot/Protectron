import hashlib
import logging
import json
from hybrid_ai.config.paths import SIGNATURE_DB_PATH

def calculate_file_hash(file_path):
    """Generate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logging.error(f"[Signature Scanner] Failed to hash file: {e}")
        return None

def scan_file_with_signature(file_path):
    """Check if a file matches any known malicious hash signatures."""
    try:
        file_hash = calculate_file_hash(file_path)
        if not file_hash:
            return "error"

        # Load known malicious signatures
        with open(SIGNATURE_DB_PATH, "r") as f:
            signature_db = json.load(f)

        if file_hash in signature_db.get("malicious_hashes", []):
            logging.warning(f"[Signature Scanner] Match found: {file_path}")
            return "malicious"
        else:
            return "benign"

    except FileNotFoundError:
        logging.error(f"[Signature Scanner] Signature DB not found at: {SIGNATURE_DB_PATH}")
        return "error"
    except Exception as e:
        logging.error(f"[Signature Scanner] Error: {e}")
        return "error"
