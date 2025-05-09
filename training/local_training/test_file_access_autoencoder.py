import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error

# Load model and scaler
model = load_model("models/local_models/file_access_autoencoder.keras")
scaler = joblib.load("models/local_models/file_access_scaler.pkl")

# Load data to test
test_data = pd.read_csv("data/datasets/file_access_autoencoder_ready.csv")

# Keep a copy of original data if needed for referencing labels
if "is_malicious" in test_data.columns:
    labels = test_data["is_malicious"]
    test_data = test_data.drop(columns=["is_malicious"])
else:
    labels = None

# Scale features
X_scaled = scaler.transform(test_data)

# Get reconstruction from autoencoder
reconstructed = model.predict(X_scaled)

# Calculate reconstruction error
mse = np.mean(np.power(X_scaled - reconstructed, 2), axis=1)

# Set a threshold (you can tune this)
threshold = np.percentile(mse, 95)

# Classify based on error
predictions = (mse > threshold).astype(int)

# Print predictions
for i, pred in enumerate(predictions[:20]):
    status = "🔴 Anomaly" if pred == 1 else "🟢 Normal"
    print(f"[Row {i+1}] → {status} (Reconstruction Error: {mse[i]:.4f})")

# Optional: Evaluate if labels are available
if labels is not None:
    from sklearn.metrics import classification_report
    print("\n📊 Evaluation Report:")
    print(classification_report(labels[:len(predictions)], predictions))
