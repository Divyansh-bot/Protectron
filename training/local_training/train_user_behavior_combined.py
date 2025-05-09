import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import joblib
import os

# Load dataset
df = pd.read_csv("data/datasets/user_behavior_dataset.csv")

# Drop only if columns exist
columns_to_drop = ["timestamp", "username", "file_path"]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Separate label
y = df["is_malicious"]
df = df.drop(columns=["is_malicious"])

# Handle categorical and numerical
categorical_cols = [col for col in df.columns if df[col].dtype == "object"]
numerical_cols = [col for col in df.columns if col not in categorical_cols]

# Encode categorical columns
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_cat = encoder.fit_transform(df[categorical_cols]) if categorical_cols else np.empty((len(df), 0))
joblib.dump(encoder, "models/local_models/user_behavior_encoder.pkl")

# Handle numerical columns
X_num = df[numerical_cols].to_numpy()
X_full = np.concatenate([X_cat, X_num], axis=1)

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_full)
joblib.dump(scaler, "models/local_models/user_behavior_scaler.pkl")

# Train Autoencoder
X_train, _, y_train, _ = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
input_dim = X_train.shape[1]

input_layer = Input(shape=(input_dim,))
encoded = Dense(14, activation="relu")(input_layer)
decoded = Dense(input_dim, activation="linear")(encoded)

autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss="mse")
autoencoder.fit(X_train, X_train, epochs=10, batch_size=64, shuffle=True)
autoencoder.save("models/local_models/user_behavior_autoencoder.keras")

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_scaled, y)
joblib.dump(rf, "models/local_models/user_behavior_rf.pkl")

print("✅ User behavior model retrained and saved successfully.")
