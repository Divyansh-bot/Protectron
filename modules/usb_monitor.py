import os
import time
import logging
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

LIVE_CSV = "temp/usb_live.csv"

# Required columns
COLUMNS = [
    'device_id', 'device_type', 'file_accessed', 'action', 'port_used',
    'manufacturer_id', 'access_duration_sec', 'file_size_kb', 'os_alert_flag',
    'is_encrypted', 'is_malicious'
]

# Load models
preprocessor = joblib.load("models/local_models/usb_security_preprocessor.pkl")
autoencoder = load_model("models/local_models/usb_autoencoder.keras")
classifier = joblib.load("models/local_models/usb_rf.pkl")

def monitor_usb_security(stop_event):
    logging.info("[USB Security] Monitoring started...")

    # Ensure the temp directory and CSV file exist
    if not os.path.exists(LIVE_CSV):
        os.makedirs("temp", exist_ok=True)
        pd.DataFrame(columns=COLUMNS).to_csv(LIVE_CSV, index=False)

    while not stop_event.is_set():
        try:
            df = pd.read_csv(LIVE_CSV)
            if df.empty:
                time.sleep(3)
                continue

            df = df[COLUMNS]
            X = df.drop('is_malicious', axis=1)

            # Preprocessing
            processed = preprocessor.transform(X)
            recon = autoencoder.predict(processed)
            loss = np.mean(np.square(processed - recon), axis=1)
            prediction = classifier.predict(processed)

            for i in range(len(df)):
                if loss[i] > 0.05 or prediction[i] == 1:
                    logging.warning("[USB Security] Suspicious USB activity detected.")
                    alert_malicious_event("USB-based threat detected")

        except Exception as e:
            logging.error(f"[USB Security] Error: {e}")

        time.sleep(3)
