import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.database_handler import MongoDBHandler

db_handler = MongoDBHandler()

class FileAccessHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            log_entry = {"file": event.src_path, "event": "modified", "timestamp": time.time()}
            db_handler.insert_log("file_access_logs", log_entry)
            print(f"⚠️ File Modified: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            log_entry = {"file": event.src_path, "event": "deleted", "timestamp": time.time()}
            db_handler.insert_log("file_access_logs", log_entry)
            print(f"⚠️ File Deleted: {event.src_path}")

def log_file_access(path="data/file_access_logs"):
    observer = Observer()
    event_handler = FileAccessHandler()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    log_file_access()

