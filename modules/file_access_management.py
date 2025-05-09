import os
import time
import joblib
import logging
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

# Load models
autoencoder = load_model("models/local_models/file_access_autoencoder.keras")
scaler = joblib.load("models/local_models/file_access_scaler.pkl")

# CSV path and expected columns
LIVE_CSV = "temp/file_access_live.csv"
COLUMNS = [
    'access_time_sec', 'file_size_kb', 'operation_close', 'operation_delete',
    'operation_encrypt', 'operation_execute', 'operation_exfiltrate', 'operation_open',
    'operation_overwrite', 'operation_ransom_access', 'operation_read', 'operation_write',
    'privilege_level_admin', 'privilege_level_guest', 'privilege_level_user'
]

# Ensure the CSV file exists with proper headers
def ensure_csv_exists():
    os.makedirs(os.path.dirname(LIVE_CSV), exist_ok=True)
    if not os.path.exists(LIVE_CSV) or os.stat(LIVE_CSV).st_size == 0:
        pd.DataFrame(columns=COLUMNS).to_csv(LIVE_CSV, index=False)

# Monitor function
def monitor_file_access(stop_event):
    logging.info("[File Access] Monitoring started...")
    ensure_csv_exists()

    while not stop_event.is_set():
        try:
            df = pd.read_csv(LIVE_CSV)
            if df.empty:
                time.sleep(5)
                continue

            df = df[COLUMNS]  # ensure correct order
            scaled = scaler.transform(df)
            recon = autoencoder.predict(scaled)
            loss = np.mean(np.square(scaled - recon), axis=1)

            for i, score in enumerate(loss):
                if score > 0.05:
                    logging.warning("[File Access] Anomaly detected.")
                    alert_malicious_event("Anomalous file access activity")

        except Exception as e:
            logging.error(f"[File Access] Error in monitoring: {e}")

        time.sleep(5)
