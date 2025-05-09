import pandas as pd
import joblib
import numpy as np
from tensorflow.keras.models import load_model

# Load test data
df = pd.read_csv("data/datasets/usb_security_dataset.csv")

# Drop identifier columns
X = df.drop(columns=["is_malicious", "device_id", "manufacturer_id"], errors="ignore")
y = df["is_malicious"]

# Load saved preprocessor, models
preprocessor = joblib.load("models/local_models/usb_preprocessor.pkl")
rf_model = joblib.load("models/local_models/usb_rf.pkl")
autoencoder = load_model("models/local_models/usb_autoencoder.keras")

# Transform input
X_processed = preprocessor.transform(X)

# Get predictions
X_reconstructed = autoencoder.predict(X_processed)
reconstruction_errors = np.mean(np.square(X_processed - X_reconstructed), axis=1)
rf_predictions = rf_model.predict(X_processed)

# Output results
for i in range(20):
    ae_err = reconstruction_errors[i]
    rf_label = rf_predictions[i]
    result = "🔴 Malicious" if rf_label == 1 else "🟢 Normal"
    print(f"[Row {i+1}] → {result} (AE Error: {ae_err:.4f}, RF: {'Malicious' if rf_label == 1 else 'Normal'})")
