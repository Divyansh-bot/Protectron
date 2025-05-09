import datetime
import os
from plyer import notification

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "protectron_log.txt")

def log_threat(module_name, message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] [{module_name}] {message}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    print(log_line.strip())

def log_event(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    print(log_line.strip())

def raise_alert(title="Protectron Alert", message="A threat was detected."):
    """Display a desktop notification for a threat."""
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )
    except Exception as e:
        print(f"[Alert Error] {e}")

def alert_malicious_event(module_name, description):
    """Specialized alert for malicious events with module context."""
    title = f"🚨 Threat Detected in {module_name}"
    message = description
    raise_alert(title, message)
