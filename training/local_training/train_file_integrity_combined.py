import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
import joblib
import os

# Load dataset
df = pd.read_csv("data/datasets/file_integrity_dataset.csv")

# Drop all non-numeric columns (like file_name, file_path, hash)
df = df.select_dtypes(include=[np.number])

# Separate features and label
X = df.drop(columns=["is_malicious"])
y = df["is_malicious"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the scaler
os.makedirs("models/local_models", exist_ok=True)
joblib.dump(scaler, "models/local_models/file_integrity_scaler.pkl")

# Build Autoencoder
input_dim = X_scaled.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(32, activation='relu')(input_layer)
encoded = Dense(16, activation='relu')(encoded)
decoded = Dense(32, activation='relu')(encoded)
decoded = Dense(input_dim, activation='linear')(encoded)

autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer=Adam(0.001), loss='mse')

# Train Autoencoder on normal data only
X_normal = X_scaled[y == 0]
autoencoder.fit(X_normal, X_normal, epochs=10, batch_size=64, shuffle=True)

# Save the Autoencoder
autoencoder.save("models/local_models/file_integrity_autoencoder.keras")

# Train Random Forest on entire data
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_scaled, y)

# Save Random Forest
joblib.dump(rf, "models/local_models/file_integrity_rf.pkl")

print("✅ File Integrity Monitoring model trained and saved.")
