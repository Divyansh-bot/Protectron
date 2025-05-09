import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from hybrid_ai.scanner.static_scanner import scan_file
from hybrid_ai.config.config import WATCH_DIRECTORY

class FileEventHandler(FileSystemEventHandler):
    """Handles events for created or modified files."""
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"[WATCHER] New file detected: {event.src_path}")
            scan_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"[WATCHER] File modified: {event.src_path}")
            scan_file(event.src_path)

def start_watching():
    """Start monitoring the configured directory."""
    logging.info(f"[WATCHER] Monitoring: {WATCH_DIRECTORY}")
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
