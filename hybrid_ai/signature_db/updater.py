import json
import hashlib
import os
from hybrid_ai.config.config import SIGNATURE_DB

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    hash_func = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"[ERROR] Could not hash file: {file_path} - {e}")
        return None

def update_signature_db(file_path, malware_name):
    """Add new hash entry to the signature DB."""
    file_hash = calculate_file_hash(file_path)
    if not file_hash:
        return

    if not os.path.exists(SIGNATURE_DB):
        with open(SIGNATURE_DB, 'w') as f:
            json.dump({}, f)

    with open(SIGNATURE_DB, 'r') as f:
        signatures = json.load(f)

    signatures[file_hash] = malware_name

    with open(SIGNATURE_DB, 'w') as f:
        json.dump(signatures, f, indent=4)

    print(f"[+] Added hash for {malware_name}: {file_hash}")

# Example usage (for manual updates):
if __name__ == "__main__":
    test_file = "sample_malware.exe"
    malware_label = "Trojan.Generic"
    update_signature_db(test_file, malware_label)
