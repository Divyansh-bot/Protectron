from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["protectron"]

@app.route("/api/logs/network")
def get_network_logs():
    logs = list(db["network_security"].find({}, {"_id": 0}).sort("_id", -1).limit(10))
    return jsonify(logs)

@app.route("/api/logs/file_access")
def get_file_logs():
    logs = list(db["file_access"].find({}, {"_id": 0}).sort("_id", -1).limit(10))
    return jsonify(logs)

@app.route("/api/logs/user_behavior")
def get_user_behavior_logs():
    logs = list(db["user_behavior"].find({}, {"_id": 0}).sort("_id", -1).limit(10))
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
