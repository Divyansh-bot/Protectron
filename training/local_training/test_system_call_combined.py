import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load dataset
df = pd.read_csv("data/datasets/system_call_dataset.csv")

# Separate labels
y = df["is_malicious"]
X_raw = df["syscall_sequence"]

# Load models and tools
vectorizer = joblib.load("models/local_models/systemcall_vectorizer.pkl")
scaler = joblib.load("models/local_models/systemcall_scaler.pkl")
rf = joblib.load("models/local_models/systemcall_rf.pkl")
autoencoder = load_model("models/local_models/systemcall_autoencoder.keras")

# Preprocess input
X_vectorized = vectorizer.transform(X_raw).toarray()
X_scaled = scaler.transform(X_vectorized)

# Autoencoder reconstruction errors
reconstructions = autoencoder.predict(X_scaled)
reconstruction_errors = np.mean(np.power(X_scaled - reconstructions, 2), axis=1)

# Random Forest predictions
rf_preds = rf.predict(np.expand_dims(reconstruction_errors, axis=1))

# Output prediction results
for i in range(min(20, len(X_raw))):
    ae_error = reconstruction_errors[i]
    rf_label = rf_preds[i]
    label = "🔴 Malicious" if rf_label == 1 else "🟢 Normal"
    print(f"[Row {i+1}] → {label} (AE Error: {ae_error:.4f}, RF: {'Malicious' if rf_label == 1 else 'Normal'})")
