import os
import time
import joblib
import logging
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

# Load models
autoencoder = load_model("models/local_models/user_behavior_autoencoder.keras")
encoder = joblib.load("models/local_models/user_behavior_encoder.pkl")
rf_model = joblib.load("models/local_models/user_behavior_rf.pkl")
scaler = joblib.load("models/local_models/user_behavior_scaler.pkl")

# CSV path and required columns
LIVE_CSV = "temp/user_behavior_live.csv"
COLUMNS = [
    'timestamp', 'cpu_usage', 'memory_usage', 'network_connections', 'process_count',
    'file_accessed', 'access_level', 'external_connection', 'executed_command', 'is_malicious'
]

# Ensure CSV exists with proper columns
def ensure_csv_exists():
    os.makedirs(os.path.dirname(LIVE_CSV), exist_ok=True)
    if not os.path.exists(LIVE_CSV) or os.stat(LIVE_CSV).st_size == 0:
        pd.DataFrame(columns=COLUMNS).to_csv(LIVE_CSV, index=False)

# Monitor function
def monitor_user_behavior(stop_event):
    logging.info("🧠 User Behavior Monitoring Started...")
    ensure_csv_exists()

    while not stop_event.is_set():
        try:
            df = pd.read_csv(LIVE_CSV)
            if df.empty:
                time.sleep(5)
                continue

            df = df[COLUMNS[:-1]]  # exclude is_malicious for prediction
            encoded = encoder.transform(df)
            scaled = scaler.transform(encoded)
            recon = autoencoder.predict(scaled)
            loss = np.mean(np.square(scaled - recon), axis=1)
            pred = rf_model.predict(scaled)

            for i in range(len(df)):
                if loss[i] > 0.05 or pred[i] == 1:
                    logging.warning("[User Behavior] Suspicious activity detected.")
                    alert_malicious_event("Suspicious user behavior detected.")

        except Exception as e:
            logging.error(f"[User Behavior] Monitoring error: {e}")

        time.sleep(5)
