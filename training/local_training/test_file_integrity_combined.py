import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("data/datasets/file_integrity_dataset.csv")

# Drop non-numeric (object) columns
df = df.select_dtypes(include=[np.number])

# Separate features and labels
X = df.drop(columns=["is_malicious"])
y = df["is_malicious"]

# Load models
autoencoder = load_model("models/local_models/file_integrity_autoencoder.keras")
rf = joblib.load("models/local_models/file_integrity_rf.pkl")
scaler = joblib.load("models/local_models/file_integrity_scaler.pkl")

# Scale input
X_scaled = scaler.transform(X)

# Get reconstruction errors from Autoencoder
reconstructions = autoencoder.predict(X_scaled)
mse = np.mean(np.power(X_scaled - reconstructions, 2), axis=1)

# Get RF predictions
rf_preds = rf.predict(X_scaled)

# Threshold for visualization (not used for detection, only display)
THRESHOLD = 0.01

# Display results
for i in range(20):  # Show first 20 rows
    status_ae = "🔴 Malicious" if mse[i] > THRESHOLD else "🟢 Normal"
    status_rf = "Malicious" if rf_preds[i] == 1 else "Normal"
    print(f"[Row {i+1}] → {status_ae} (AE Error: {mse[i]:.4f}, RF: {status_rf})")
