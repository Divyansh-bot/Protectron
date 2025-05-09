import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from hybrid_ai.fusion_engine.predictor import hybrid_predict
from hybrid_ai.quarantine.quarantine import quarantine_file

MONITOR_PATH = "C:/Users/Divyansh/Downloads"  # 👈 Change as needed

class MalwareDetectionHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        logging.info(f"[Scanner] New file detected: {file_path}")

        result = hybrid_predict(file_path)
        logging.info(f"[Scanner] Detection Result: {result}")

        if result == "malicious":
            quarantine_file(file_path)
            logging.warning(f"[Scanner] File quarantined: {file_path}")

def start_realtime_scanner():
    logging.info("[Scanner] 🔍 Starting real-time malware scanner...")
    os.makedirs(MONITOR_PATH, exist_ok=True)

    event_handler = MalwareDetectionHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITOR_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
