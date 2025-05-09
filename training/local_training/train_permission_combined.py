import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping

# Load dataset
df = pd.read_csv('data/datasets/app_permission_dataset.csv')

# Split features and target
X = df.drop(columns=['is_malicious'])
y = df['is_malicious']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, 'models/local_models/permission_scaler.pkl')

# ------------------- Autoencoder -------------------
autoencoder = Sequential([
    Dense(12, activation='relu', input_shape=(X.shape[1],)),
    Dense(8, activation='relu'),
    Dense(12, activation='relu'),
    Dense(X.shape[1], activation='sigmoid')
])

autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(X_scaled[y == 0], X_scaled[y == 0],
                epochs=10,
                batch_size=256,
                shuffle=True,
                validation_split=0.2,
                callbacks=[EarlyStopping(patience=3, restore_best_weights=True)])

autoencoder.save('models/local_models/permission_autoencoder.keras')

# ------------------- Random Forest -------------------
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_scaled, y)

# Save Random Forest
joblib.dump(rf, 'models/local_models/permission_rf.pkl')

print("✅ Permission anomaly model trained and saved successfully.")
