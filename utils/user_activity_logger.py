import time
import json
from datetime import datetime
from utils.database_handler import MongoDBHandler

db_handler = MongoDBHandler()

def log_user_activity():
    user_activity = {
        "timestamp": datetime.now(),
        "user": "Divyansh",
        "login_time": time.time(),
        "access_patterns": ["opened_notepad", "executed_python_script"]
    }
    db_handler.insert_log("user_behavior_logs", user_activity)
    print(f"✅ Logged User Activity: {json.dumps(user_activity, indent=4)}")

if __name__ == "__main__":
    while True:
        log_user_activity()
        time.sleep(30)  # Log every 30 seconds

