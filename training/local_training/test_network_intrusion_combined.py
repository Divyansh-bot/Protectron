import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load trained models and scaler
autoencoder = load_model("models/local_models/network_intrusion_autoencoder.keras")
iso_model = joblib.load("models/local_models/network_intrusion_isoforest.pkl")
preprocessor = joblib.load("models/local_models/network_preprocessor.pkl")

# Load dataset
df = pd.read_csv("data/datasets/network_intrusion_combined.csv")

# Drop columns not used for training
X = df.drop(columns=["is_malicious", "src_ip", "dest_ip"])
y_true = df["is_malicious"].values

# Transform the data
X_scaled = preprocessor.transform(X)

# Autoencoder predictions
reconstructed = autoencoder.predict(X_scaled)
reconstruction_errors = np.mean(np.square(X_scaled - reconstructed), axis=1)
threshold = np.percentile(reconstruction_errors, 95)
ae_preds = (reconstruction_errors > threshold).astype(int)

# Isolation Forest predictions
iso_preds = iso_model.predict(X_scaled)
iso_preds = np.where(iso_preds == -1, 1, 0)

# Combine predictions (AND logic)
combined_preds = (ae_preds + iso_preds) > 1

# Display test results
for i in range(20):
    status = "🔴 Malicious" if combined_preds[i] else "🟢 Normal"
    print(f"[Row {i+1}] → {status} (AE Error: {reconstruction_errors[i]:.4f}, ISO: {'Malicious' if iso_preds[i] else 'Normal'})")
