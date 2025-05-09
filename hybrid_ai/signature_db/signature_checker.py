import hashlib
import json
import os
from hybrid_ai.config.paths import SIGNATURE_DB_PATH
import logging

def compute_file_hash(filepath):
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except Exception as e:
        logging.error(f"[Signature] Error reading file for hashing: {filepath} -> {e}")
        return None
    return sha256_hash.hexdigest()

def load_signature_db():
    """Load malware signature database from JSON file."""
    if not os.path.exists(SIGNATURE_DB_PATH):
        logging.warning("[Signature] Signature DB not found, returning empty DB.")
        return {}
    with open(SIGNATURE_DB_PATH, "r") as f:
        return json.load(f)

def is_hash_malicious(file_hash):
    """Check if a file hash exists in the malware signature DB."""
    db = load_signature_db()
    return db.get(file_hash, "benign") == "malicious"

def check_file_signature(filepath):
    """Complete check: compute hash and check against DB."""
    file_hash = compute_file_hash(filepath)
    if not file_hash:
        return "unknown"
    return "malicious" if is_hash_malicious(file_hash) else "benign"
