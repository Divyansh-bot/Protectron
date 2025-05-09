import pandas as pd
import numpy as np
import joblib
from keras.models import load_model

# Load trained models
autoencoder = load_model('models/local_models/data_exfiltration_autoencoder.keras')
rf_model = joblib.load('models/local_models/data_exfiltration_random_forest.pkl')
scaler = joblib.load('models/local_models/data_exfiltration_scaler.pkl')

# Load test dataset
df = pd.read_csv('data/datasets/data_exfiltration_dataset.csv')

# Drop irrelevant non-numeric columns
drop_cols = ["timestamp", "source_ip", "destination_ip"]
df = df.drop(columns=[col for col in drop_cols if col in df.columns])

# One-hot encode categorical features (just like in training)
df = pd.get_dummies(df)

# Separate features and labels
X = df.drop(columns=["is_malicious"])
y = df["is_malicious"]

# Align columns to what scaler and model were trained on
# Load saved column structure (from training script, we need to save it there)
expected_columns = joblib.load('models/local_models/data_exfiltration_columns.pkl')

# Add missing columns as 0 and drop extra ones
for col in expected_columns:
    if col not in X.columns:
        X[col] = 0
X = X[expected_columns]

# Scale features
X_scaled = scaler.transform(X)

# AE predictions
reconstructions = autoencoder.predict(X_scaled)
reconstruction_errors = np.mean(np.square(X_scaled - reconstructions), axis=1)

# RF predictions
rf_preds = rf_model.predict(X_scaled)

# Output
for i in range(20):
    ae_label = "Malicious" if reconstruction_errors[i] > 0.01 else "Normal"
    rf_label = "Malicious" if rf_preds[i] == 1 else "Normal"
    verdict = "🔴 Malicious" if ae_label == "Malicious" or rf_label == "Malicious" else "🟢 Normal"
    print(f"[Row {i+1}] → {verdict} (AE Error: {reconstruction_errors[i]:.4f}, RF: {rf_label})")
