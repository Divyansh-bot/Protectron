import hashlib
import json
import os
from hybrid_ai.config.config import SIGNATURE_DB

def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[ERROR] Failed to calculate hash: {e}")
        return None

def is_file_malicious(file_path):
    """Check if the file's hash matches any known malware signatures."""
    file_hash = calculate_sha256(file_path)
    if not file_hash:
        return False, None

    if not os.path.exists(SIGNATURE_DB):
        return False, None

    with open(SIGNATURE_DB, 'r') as f:
        signatures = json.load(f)

    if file_hash in signatures:
        return True, signatures[file_hash]

    return False, None
