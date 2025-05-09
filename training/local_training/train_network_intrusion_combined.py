import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
import joblib
import os

# Load dataset
df = pd.read_csv("data/datasets/network_intrusion_dataset.csv")

# Drop IP columns if they exist
df.drop(columns=[col for col in ["src_ip", "dest_ip"] if col in df.columns], inplace=True)

# Encode 'protocol' column
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
protocol_encoded = encoder.fit_transform(df[["protocol"]])
protocol_encoded_df = pd.DataFrame(protocol_encoded, columns=encoder.get_feature_names_out(["protocol"]))

# Drop and concatenate encoded protocol
df.drop(columns=["protocol"], inplace=True)
df = pd.concat([df.reset_index(drop=True), protocol_encoded_df.reset_index(drop=True)], axis=1)

# Scale data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Train/Test split
X_train, X_test = train_test_split(scaled_data, test_size=0.2, random_state=42)

# Build autoencoder model
input_dim = X_train.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(32, activation="relu")(input_layer)
encoded = Dense(16, activation="relu")(encoded)
decoded = Dense(32, activation="relu")(encoded)
decoded = Dense(input_dim, activation="linear")(decoded)
autoencoder = Model(inputs=input_layer, outputs=decoded)

autoencoder.compile(optimizer="adam", loss="mse")
early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

# Train autoencoder
autoencoder.fit(
    X_train,
    X_train,
    epochs=50,
    batch_size=32,
    shuffle=True,
    validation_data=(X_test, X_test),
    callbacks=[early_stop],
    verbose=1,
)

# Generate embeddings for Isolation Forest
encoder_model = Model(inputs=autoencoder.input, outputs=autoencoder.layers[1].output)
X_train_embed = encoder_model.predict(X_train)

# Train Isolation Forest
isoforest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
isoforest.fit(X_train_embed)

# Save all models and processors
os.makedirs("models/local_models", exist_ok=True)
autoencoder.save("models/local_models/network_intrusion_autoencoder.keras")
joblib.dump(isoforest, "models/local_models/network_intrusion_isoforest.pkl")
joblib.dump(scaler, "models/local_models/network_preprocessor.pkl")
joblib.dump(encoder, "models/local_models/network_protocol_encoder.pkl")

print("[✅] Network intrusion model training complete and saved.")
