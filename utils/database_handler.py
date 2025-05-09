from pymongo import MongoClient
from datetime import datetime

class MongoDBHandler:
    def __init__(self):
        """Initialize MongoDB connection."""
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["protectron"]
            print("✅ Connected to MongoDB")
        except Exception as e:
            print(f"❌ MongoDB Connection Error: {e}")

    def insert_log(self, collection_name, log_data):
        """Insert log data into MongoDB and print confirmation."""
        try:
            log_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db[collection_name].insert_one(log_data)
            print(f"📝 Log saved to MongoDB → {collection_name}: {log_data}")
        except Exception as e:
            print(f"❌ Failed to insert log into {collection_name}: {e}")

    def get_latest_logs(self, collection_name, limit=10):
        """Retrieve the latest logs from MongoDB."""
        try:
            logs = list(self.db[collection_name].find({}, {"_id": 0}).sort("_id", -1).limit(limit))
            return logs
        except Exception as e:
            print(f"❌ Failed to retrieve logs from {collection_name}: {e}")
            return []

    def clear_logs(self, collection_name):
        """Clear all logs from a specified collection."""
        try:
            self.db[collection_name].delete_many({})
            print(f"🗑️ Cleared all logs in {collection_name}")
        except Exception as e:
            print(f"❌ Failed to clear logs from {collection_name}: {e}")

if __name__ == "__main__":
    # ✅ Test MongoDB connection & logging
    db_handler = MongoDBHandler()
    
    # Insert test logs
    db_handler.insert_log("network_security", {"source_ip": "192.168.1.1", "destination_ip": "10.0.0.2", "threat": "Port Scan"})
    db_handler.insert_log("file_access", {"file": "/etc/passwd", "action": "read", "user": "root"})
    db_handler.insert_log("user_behavior", {"event": "Unusual login attempt", "user": "admin"})

    # Retrieve logs
    print("📡 Latest Network Security Logs:", db_handler.get_latest_logs("network_security"))
    print("📡 Latest File Access Logs:", db_handler.get_latest_logs("file_access"))
    print("📡 Latest User Behavior Logs:", db_handler.get_latest_logs("user_behavior"))

    # Clear logs (for testing)
    # db_handler.clear_logs("network_security")
    # db_handler.clear_logs("file_access")
    # db_handler.clear_logs("user_behavior")
