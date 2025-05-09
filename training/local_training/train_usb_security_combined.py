import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from keras.models import Sequential
from keras.layers import Dense
import joblib
import os

# Load data
df = pd.read_csv("data/datasets/usb_security_dataset.csv")

# Drop unneeded identifiers
X = df.drop(columns=["is_malicious", "device_id", "manufacturer_id"], errors="ignore")
y = df["is_malicious"]

# Identify categorical and numeric columns
categorical_cols = ["device_type", "file_accessed", "action", "port_used"]
numerical_cols = [col for col in X.columns if col not in categorical_cols]

# Preprocessing
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
    ("num", StandardScaler(), numerical_cols)
])

# Apply transformations
X_processed = preprocessor.fit_transform(X)

# Save preprocessor
os.makedirs("models/local_models", exist_ok=True)
joblib.dump(preprocessor, "models/local_models/usb_preprocessor.pkl")

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
joblib.dump(rf, "models/local_models/usb_rf.pkl")

# Autoencoder (Only normal samples)
X_normal = X_processed[y == 0]
input_dim = X_normal.shape[1]

autoencoder = Sequential([
    Dense(128, activation='relu', input_shape=(input_dim,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(64, activation='relu'),
    Dense(128, activation='relu'),
    Dense(input_dim, activation='linear')
])
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(X_normal, X_normal, epochs=10, batch_size=64, shuffle=True)
autoencoder.save("models/local_models/usb_autoencoder.keras")

print("✅ USB Security Model training complete and saved.")
