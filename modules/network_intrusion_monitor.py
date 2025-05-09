import os
import time
import joblib
import logging
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

# Load models
autoencoder = load_model("models/local_models/network_intrusion_autoencoder.keras")
isoforest = joblib.load("models/local_models/network_intrusion_isoforest.pkl")
scaler = joblib.load("models/local_models/network_preprocessor.pkl")
encoder = joblib.load("models/local_models/network_protocol_encoder.pkl")

# File and expected columns
LIVE_CSV = "temp/network_live.csv"
COLUMNS = [
    'src_ip', 'dest_ip', 'src_port', 'dest_port', 'protocol',
    'duration', 'packet_count', 'byte_count', 'is_malicious'
]

def ensure_csv_exists():
    os.makedirs(os.path.dirname(LIVE_CSV), exist_ok=True)
    if not os.path.exists(LIVE_CSV) or os.stat(LIVE_CSV).st_size == 0:
        pd.DataFrame(columns=COLUMNS).to_csv(LIVE_CSV, index=False)

def start_intrusion_monitor(stop_event):
    logging.info("[Network Intrusion] Monitoring started...")
    ensure_csv_exists()

    while not stop_event.is_set():
        try:
            df = pd.read_csv(LIVE_CSV)
            if df.empty:
                time.sleep(5)
                continue

            df = df[COLUMNS]
            df_clean = df.drop(['src_ip', 'dest_ip', 'is_malicious'], axis=1)
            df_clean['protocol'] = encoder.transform(df_clean['protocol'])

            scaled = scaler.transform(df_clean)
            recon = autoencoder.predict(scaled)
            loss = np.mean(np.square(scaled - recon), axis=1)
            anomaly = isoforest.predict(scaled)

            for i, (l, a) in enumerate(zip(loss, anomaly)):
                if l > 0.05 or a == -1:
                    logging.warning("[Network Intrusion] Suspicious network behavior detected.")
                    alert_malicious_event("Network intrusion attempt")

        except Exception as e:
            logging.error(f"[Network Intrusion] Error during monitoring: {e}")

        time.sleep(5)
