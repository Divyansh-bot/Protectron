import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the models and scaler
autoencoder = load_model('models/local_models/permission_autoencoder.keras')
rf_model = joblib.load('models/local_models/permission_rf.pkl')
scaler = joblib.load('models/local_models/permission_scaler.pkl')

# Load the dataset
df = pd.read_csv('data/datasets/app_permission_dataset.csv')

# Separate features and target
X = df.drop(columns=["is_malicious"])
y = df["is_malicious"]

# Scale features
X_scaled = scaler.transform(X)

# Autoencoder predictions (reconstruction error)
X_reconstructed = autoencoder.predict(X_scaled)
reconstruction_errors = np.mean(np.square(X_scaled - X_reconstructed), axis=1)

# Random Forest predictions
rf_predictions = rf_model.predict(X_scaled)

# Thresholds (customizable if needed)
recon_threshold = 0.0015  # adjust this based on validation

# Output predictions
for idx in range(min(20, len(X))):
    ae_score = reconstruction_errors[idx]
    rf_pred = rf_predictions[idx]

    ae_label = "Malicious" if ae_score > recon_threshold else "Normal"
    rf_label = "Malicious" if rf_pred == 1 else "Normal"

    final_label = "🔴 Malicious" if ae_label == "Malicious" or rf_label == "Malicious" else "🟢 Normal"

    print(f"[Row {idx+1}] → {final_label} (AE Error: {ae_score:.4f}, RF: {rf_label})")
