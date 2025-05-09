import os
import time
import joblib
import logging
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

# Load models
autoencoder = load_model("models/local_models/data_exfiltration_autoencoder.keras")
rf_model = joblib.load("models/local_models/data_exfiltration_random_forest.pkl")
scaler = joblib.load("models/local_models/data_exfiltration_scaler.pkl")
columns = joblib.load("models/local_models/data_exfiltration_columns.pkl")  # This is a list

# File and expected columns
LIVE_CSV = "temp/data_exfiltration_live.csv"

def ensure_csv_exists():
    os.makedirs(os.path.dirname(LIVE_CSV), exist_ok=True)
    if not os.path.exists(LIVE_CSV) or os.stat(LIVE_CSV).st_size == 0:
        pd.DataFrame(columns=columns).to_csv(LIVE_CSV, index=False)

def monitor_data_exfiltration(stop_event):
    logging.info("📤 Data Exfiltration Monitoring Started...")
    ensure_csv_exists()

    while not stop_event.is_set():
        try:
            df = pd.read_csv(LIVE_CSV)
            if df.empty:
                time.sleep(5)
                continue

            data = df[columns].drop(['is_malicious'], axis=1)
            scaled = scaler.transform(data)

            recon = autoencoder.predict(scaled)
            loss = np.mean(np.square(scaled - recon), axis=1)
            pred = rf_model.predict(scaled)

            for i, (l, p) in enumerate(zip(loss, pred)):
                if l > 0.05 or p == 1:
                    logging.warning("[Data Exfiltration] Suspicious exfiltration detected.")
                    alert_malicious_event("Possible data exfiltration")

        except Exception as e:
            logging.error(f"[Data Exfiltration] Error in monitoring: {e}")

        time.sleep(5)
