import os
import shutil
import logging
from datetime import datetime

QUARANTINE_DIR = "hybrid_ai/quarantine/quarantined_files"

def quarantine_file(file_path):
    """Move a suspicious file to the quarantine directory with a timestamp."""
    try:
        os.makedirs(QUARANTINE_DIR, exist_ok=True)

        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        destination = os.path.join(QUARANTINE_DIR, new_filename)

        shutil.move(file_path, destination)
        logging.info(f"[Quarantine] File moved to quarantine: {destination}")

    except Exception as e:
        logging.error(f"[Quarantine] Error quarantining file: {file_path} - {e}")
