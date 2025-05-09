import os
import time
import logging
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from utils.alert import alert_malicious_event

LIVE_CSV = "temp/systemcall_live.csv"

# Required columns
COLUMNS = ['syscall_sequence', 'is_malicious']

# Load models
scaler = joblib.load("models/local_models/systemcall_scaler.pkl")
vectorizer = joblib.load("models/local_models/systemcall_vectorizer.pkl")
autoencoder = load_model("models/local_models/systemcall_autoencoder.keras")
classifier = joblib.load("models/local_models/systemcall_rf.pkl")

def monitor_system_calls(stop_event):
    logging.info("[System Calls] Monitoring started...")

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
            X = df['syscall_sequence'].astype(str)
            y = df['is_malicious']

            # Vectorize syscall sequence
            vectorized = vectorizer.transform(X)
            scaled = scaler.transform(vectorized.toarray())
            recon = autoencoder.predict(scaled)
            loss = np.mean(np.square(scaled - recon), axis=1)
            prediction = classifier.predict(scaled)

            for i in range(len(df)):
                if loss[i] > 0.05 or prediction[i] == 1:
                    logging.warning("[System Calls] Malicious system call sequence detected.")
                    alert_malicious_event("Suspicious system call behavior")

        except Exception as e:
            logging.error(f"[System Calls] Error: {e}")

        time.sleep(3)
