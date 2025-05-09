import os
import time
import joblib
import logging
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

# Load models
autoencoder = load_model("models/local_models/file_integrity_autoencoder.keras")
rf_model = joblib.load("models/local_models/file_integrity_rf.pkl")
scaler = joblib.load("models/local_models/file_integrity_scaler.pkl")

# File and expected columns
LIVE_CSV = "temp/file_integrity_live.csv"
COLUMNS = ['filename', 'file_exists', 'hash_mismatch', 'modified', 'is_malicious']

def ensure_csv_exists():
    os.makedirs(os.path.dirname(LIVE_CSV), exist_ok=True)
    if not os.path.exists(LIVE_CSV) or os.stat(LIVE_CSV).st_size == 0:
        pd.DataFrame(columns=COLUMNS).to_csv(LIVE_CSV, index=False)

def monitor_file_integrity(stop_event):
    logging.info("[File Integrity] Monitor started...")
    ensure_csv_exists()

    while not stop_event.is_set():
        try:
            df = pd.read_csv(LIVE_CSV)
            if df.empty:
                time.sleep(5)
                continue

            df = df[COLUMNS]
            df_clean = df.drop(['filename', 'is_malicious'], axis=1)

            scaled = scaler.transform(df_clean)
            recon = autoencoder.predict(scaled)
            loss = np.mean(np.square(scaled - recon), axis=1)
            pred = rf_model.predict(scaled)

            for i, (l, p) in enumerate(zip(loss, pred)):
                if l > 0.05 or p == 1:
                    logging.warning("[File Integrity] Malicious file behavior detected.")
                    alert_malicious_event("File integrity anomaly")

        except Exception as e:
            logging.error(f"[File Integrity] Error: {e}")

        time.sleep(5)
