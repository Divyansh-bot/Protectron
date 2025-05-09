import psutil
import json
import time
from utils.database_handler import MongoDBHandler

db_handler = MongoDBHandler()

def log_network_traffic():
    network_data = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == "ESTABLISHED" and conn.raddr:
            log_entry = {
                "timestamp": time.time(),
                "local_ip": conn.laddr.ip,
                "local_port": conn.laddr.port,
                "remote_ip": conn.raddr.ip,
                "remote_port": conn.raddr.port,
                "status": conn.status
            }
            network_data.append(log_entry)
            db_handler.insert_log("network_traffic_logs", log_entry)

    print(f"✅ Logged Network Traffic: {json.dumps(network_data, indent=4)}")

if __name__ == "__main__":
    while True:
        log_network_traffic()
        time.sleep(30)  # Log every 30 seconds
