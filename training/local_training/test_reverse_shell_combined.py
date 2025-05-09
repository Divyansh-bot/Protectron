# training/local_training/test_reverse_shell_combined.py
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load data and models
df = pd.read_csv("data/datasets/reverse_shell_dataset.csv")

features = ['destination_port', 'bytes_sent', 'bytes_received', 'duration']
X = df[features]

# Load scaler and models
scaler = joblib.load("models/local_models/reverse_shell_scaler.pkl")
autoencoder = load_model("models/local_models/reverse_shell_autoencoder.keras")
rf_model = joblib.load("models/local_models/reverse_shell_rf.pkl")

# Normalize data
X_scaled = scaler.transform(X)

# Autoencoder reconstruction error
reconstructed = autoencoder.predict(X_scaled)
reconstruction_error = np.mean(np.power(X_scaled - reconstructed, 2), axis=1)

# Combine features with reconstruction error for RF prediction
X_combined = pd.DataFrame(X_scaled, columns=features)
X_combined["recon_error"] = reconstruction_error

# Predict
predictions = rf_model.predict(X_combined)

# Display results
for i in range(20):
    status = "🔴 Malicious" if predictions[i] == 1 else "🟢 Normal"
    print(f"[Row {i+1}] → {status} (Reconstruction Error: {reconstruction_error[i]:.4f})")
