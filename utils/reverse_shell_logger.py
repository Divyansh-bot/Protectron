import psutil
import json
import time
from utils.database_handler import MongoDBHandler

db_handler = MongoDBHandler()

def log_reverse_shell_activity():
    shell_activity = []
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'ESTABLISHED' and conn.raddr:
            remote_ip, remote_port = conn.raddr
            if remote_port > 50000:
                log_entry = {
                    "timestamp": time.time(),
                    "process": conn.pid,
                    "remote_ip": remote_ip,
                    "remote_port": remote_port,
                    "details": "Potential reverse shell connection detected"
                }
                shell_activity.append(log_entry)
                db_handler.insert_log("reverse_shell_logs", log_entry)

    print(f"✅ Logged Reverse Shell Activity: {json.dumps(shell_activity, indent=4)}")

if __name__ == "__main__":
    while True:
        log_reverse_shell_activity()
        time.sleep(30)  # Log every 30 seconds
