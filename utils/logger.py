import datetime
import os

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "protectron_log.txt")

def log_threat(module_name, message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] [{module_name}] {message}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    print(log_line.strip())  # Optional: output to console as well

def log_event(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    print(log_line.strip())
