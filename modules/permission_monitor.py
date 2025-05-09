import os
import time
import logging
import pandas as pd
import numpy as np
import joblib
import psutil
from keras.models import load_model
from plyer import notification
from utils.alert import alert_malicious_event

# Load models
scaler = joblib.load("models/local_models/permission_scaler.pkl")
autoencoder = load_model("models/local_models/permission_autoencoder.keras")
classifier = joblib.load("models/local_models/permission_rf.pkl")

COLUMNS = [
    'camera', 'microphone', 'location', 'sms', 'contacts', 'call_logs',
    'storage', 'calendar', 'phone', 'background_activity', 'bluetooth',
    'nfc', 'internet', 'system_alert_window', 'vibration'
]

# Suspicious process simulation
SUSPICIOUS_PROCESS_MAP = {
    "camera": ["zoom.exe", "obs64.exe"],
    "microphone": ["zoom.exe", "audiodg.exe"],
    "location": ["chrome.exe"],
    "sms": [],  # mobile specific
    "contacts": [],
    "call_logs": [],
    "storage": ["powershell.exe", "cmd.exe"],
    "calendar": [],
    "phone": [],
    "background_activity": [],
    "bluetooth": [],
    "nfc": [],
    "internet": ["chrome.exe", "firefox.exe"],
    "system_alert_window": [],
    "vibration": []
}

def notify_user(title, message):
    try:
        notification.notify(title=title, message=message, timeout=5)
    except Exception as e:
        logging.warning(f"[Permission Abuse] Notification error: {e}")

def extract_live_permission_features():
    data = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info['name'].lower()
            row = [1 if pname in [p.lower() for p in SUSPICIOUS_PROCESS_MAP[col]] else 0 for col in COLUMNS]
            if sum(row) > 0:
                data.append((pname, row))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return data

def monitor_app_permissions(stop_event):
    logging.info("[Permission Abuse] Monitoring started...")

    while not stop_event.is_set():
        try:
            rows = extract_live_permission_features()
            if not rows:
                time.sleep(5)
                continue

            for pname, feats in rows:
                df = pd.DataFrame([feats], columns=COLUMNS)
                scaled = scaler.transform(df)
                recon = autoencoder.predict(scaled)
                loss = np.mean(np.square(scaled - recon), axis=1)
                prediction = classifier.predict(scaled)

                if loss[0] > 0.05 or prediction[0] == 1:
                    msg = f"⚠️ Suspicious permissions in: {pname}"
                    logging.warning(f"[Permission Abuse] {msg}")
                    notify_user("Permission Abuse Detected", msg)
                    alert_malicious_event("Permission Abuse", msg)

        except Exception as e:
            logging.error(f"[Permission Abuse] Error: {str(e)}")

        time.sleep(10)

    logging.info("[Permission Abuse] Monitoring stopped.")
