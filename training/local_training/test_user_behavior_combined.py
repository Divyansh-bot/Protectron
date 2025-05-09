import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load the data
df = pd.read_csv("data/datasets/user_behavior_dataset.csv")

# Drop irrelevant or non-numeric columns if they exist
columns_to_drop = ["timestamp", "username", "file_path"]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Separate label
y = df["is_malicious"]
df = df.drop(columns=["is_malicious"])

# Load encoders
encoder = joblib.load("models/local_models/user_behavior_encoder.pkl")
scaler = joblib.load("models/local_models/user_behavior_scaler.pkl")
autoencoder = load_model("models/local_models/user_behavior_autoencoder.keras")
rf = joblib.load("models/local_models/user_behavior_rf.pkl")

# Handle categorical and numeric
categorical_cols = [col for col in df.columns if df[col].dtype == "object"]
numerical_cols = [col for col in df.columns if col not in categorical_cols]

X_cat = encoder.transform(df[categorical_cols]) if categorical_cols else np.empty((len(df), 0))
X_num = df[numerical_cols].to_numpy()

X_full = np.concatenate([X_cat, X_num], axis=1)
X_scaled = scaler.transform(X_full)

# Autoencoder predictions
X_reconstructed = autoencoder.predict(X_scaled)
reconstruction_errors = np.mean(np.square(X_scaled - X_reconstructed), axis=1)

# Random Forest predictions
rf_preds = rf.predict(X_scaled)

# Print results
for i in range(min(20, len(X_scaled))):
    ae_score = reconstruction_errors[i]
    rf_label = rf_preds[i]
    status = "🔴 Malicious" if rf_label == 1 or ae_score > 0.5 else "🟢 Normal"
    print(f"[Row {i+1}] → {status} (AE Error: {ae_score:.4f}, RF: {'Malicious' if rf_label else 'Normal'})")
