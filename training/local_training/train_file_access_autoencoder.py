import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
import os

# Load dataset
data_path = "data/datasets/file_access_autoencoder_ready.csv"
df = pd.read_csv(data_path)

# Drop non-numeric or ID columns if any exist
if "is_malicious" in df.columns:
    df = df.drop(columns=["is_malicious"])

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Autoencoder architecture
input_dim = X_scaled.shape[1]
encoding_dim = 10

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='linear')(encoded)

autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# Train the autoencoder
autoencoder.fit(X_scaled, X_scaled, epochs=50, batch_size=64, shuffle=True, validation_split=0.1)

# Save the model in recommended format
model_path = "models/local_models/file_access_autoencoder.keras"
autoencoder.save(model_path)

# Save the scaler
import joblib
scaler_path = "models/local_models/file_access_scaler.pkl"
joblib.dump(scaler, scaler_path)

print(f"✅ Autoencoder and scaler saved to:\n- {model_path}\n- {scaler_path}")
