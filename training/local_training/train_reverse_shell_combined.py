import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Dense
from keras.callbacks import EarlyStopping
import joblib

# Load dataset
df = pd.read_csv("data/datasets/reverse_shell_dataset.csv")

# Keep only relevant numeric features
features = ['destination_port', 'bytes_sent', 'bytes_received', 'duration']
label = 'is_malicious'
X = df[features]
y = df[label]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Autoencoder on normal traffic (non-malicious)
X_normal = X_scaled[y == 0]

input_layer = Input(shape=(X_normal.shape[1],))
encoded = Dense(32, activation='relu')(input_layer)
encoded = Dense(16, activation='relu')(encoded)
decoded = Dense(32, activation='relu')(encoded)
output_layer = Dense(X_normal.shape[1], activation='linear')(decoded)

autoencoder = Model(inputs=input_layer, outputs=output_layer)
autoencoder.compile(optimizer='adam', loss='mse')

autoencoder.fit(
    X_normal, X_normal,
    epochs=10,
    batch_size=64,
    validation_split=0.1,
    callbacks=[EarlyStopping(monitor='val_loss', patience=2)],
    verbose=1
)

# Get reconstruction error
X_reconstructed = autoencoder.predict(X_scaled)
reconstruction_error = np.mean(np.square(X_scaled - X_reconstructed), axis=1).reshape(-1, 1)

# Combine with original features
X_combined = np.hstack((X_scaled, reconstruction_error))

# Train Random Forest
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save everything
autoencoder.save("models/local_models/reverse_shell_autoencoder.keras")
joblib.dump(rf_model, "models/local_models/reverse_shell_rf.pkl")
joblib.dump(scaler, "models/local_models/reverse_shell_scaler.pkl")

print("✅ Reverse Shell Detection Models trained and saved successfully.")
