import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from hybrid_ai.scanner.cnn_scanner import scan_file_with_cnn
from hybrid_ai.scanner.signature_scanner import scan_file_with_signature
from hybrid_ai.fusion_engine.predictor import cnn_predict
from hybrid_ai.quarantine.quarantine import quarantine_file
from hybrid_ai.utils.logger import setup_logger

# Setup logger
logger = setup_logger("hybrid_scanner")

# ✅ Folder to monitor
WATCH_FOLDER = os.path.join("data", "malware_samples")

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.handle_event(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.handle_event(event.src_path)

    def handle_event(self, file_path):
        try:
            logger.info(f"[Hybrid Scanner] Detected file event: {file_path}")

            # Scan using signature method
            sig_result = scan_file_with_signature(file_path)

            # Scan using CNN method
            cnn_result = scan_file_with_cnn(file_path)

            # Fusion decision
            final_verdict = cnn_predict(sig_result, cnn_result)

            if final_verdict:
                logger.warning(f"[Hybrid Scanner] Malicious file detected: {file_path}")
                quarantine_file(file_path)
            else:
                logger.info(f"[Hybrid Scanner] File is clean: {file_path}")

        except Exception as e:
            logger.error(f"[Hybrid Scanner] Error scanning {file_path}: {str(e)}")

def start_hybrid_scanner(stop_event=None):
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)

    logger.info(f"[Hybrid Scanner] Monitoring folder: {WATCH_FOLDER}")

    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    observer.start()

    try:
        while not stop_event.is_set() if stop_event else True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("[Hybrid Scanner] Stopped monitoring due to interrupt.")

    observer.stop()
    observer.join()


if __name__ == "__main__":
    start_hybrid_scanner(WATCH_FOLDER)
