import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
import os

# Load dataset
df = pd.read_csv("data/datasets/data_exfiltration_dataset.csv")

# Drop irrelevant or sensitive columns
df = df.drop(columns=["timestamp", "source_ip", "destination_ip",
                      "process_id", "parent_process", "child_process", "command_executed", "protocol"], errors="ignore")

# Separate labels
y = df["is_malicious"]
X = df.drop(columns=["is_malicious"], errors="ignore")

# One-hot encode categorical features
X = pd.get_dummies(X)

# Save column structure for real-time detection
os.makedirs("models/local_models", exist_ok=True)
joblib.dump(X.columns.tolist(), "models/local_models/data_exfiltration_columns.pkl")

# Normalize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, "models/local_models/data_exfiltration_scaler.pkl")

# Split for evaluation
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Autoencoder
input_dim = X_train.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(64, activation='relu')(input_layer)
encoded = Dense(32, activation='relu')(encoded)
decoded = Dense(64, activation='relu')(encoded)
decoded = Dense(input_dim, activation='linear')(decoded)

autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
autoencoder.fit(X_train, X_train, epochs=10, batch_size=64, shuffle=True, validation_split=0.1)

# Save autoencoder model
autoencoder.save("models/local_models/data_exfiltration_autoencoder.keras")

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
joblib.dump(rf, "models/local_models/data_exfiltration_random_forest.pkl")

print("✅ Training completed. Models saved and ready for real-time use.")
