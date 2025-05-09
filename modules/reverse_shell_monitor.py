import os
import time
import logging
import joblib
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

LIVE_CSV = "temp/reverse_shell_live.csv"

# Required columns during training
COLUMNS = [
    'timestamp', 'process_id', 'parent_process', 'child_process',
    'source_ip', 'destination_ip', 'destination_port', 'protocol',
    'bytes_sent', 'bytes_received', 'duration', 'command_executed', 'is_malicious'
]

# Load models
scaler = joblib.load("models/local_models/reverse_shell_scaler.pkl")
autoencoder = load_model("models/local_models/reverse_shell_autoencoder.keras")
classifier = joblib.load("models/local_models/reverse_shell_rf.pkl")

def monitor_reverse_shell(stop_event):
    logging.info("[Reverse Shell] Monitoring started...")

    # Ensure CSV exists
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
            data = df.drop(['is_malicious'], axis=1)

            # Scale and predict
            scaled = scaler.transform(data)
            recon = autoencoder.predict(scaled)
            loss = np.mean(np.square(scaled - recon), axis=1)
            prediction = classifier.predict(scaled)

            for i in range(len(df)):
                if loss[i] > 0.1 or prediction[i] == 1:
                    logging.warning("[Reverse Shell] Reverse shell behavior detected.")
                    alert_malicious_event("Potential Reverse Shell Activity")

        except Exception as e:
            logging.error(f"[Reverse Shell] Error in monitoring: {e}")

        time.sleep(3)
