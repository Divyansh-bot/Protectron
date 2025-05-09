import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras import regularizers
from sklearn.feature_extraction.text import CountVectorizer

# 📦 Load the dataset
df = pd.read_csv("data/datasets/system_call_dataset.csv")

# 🧠 Extract labels
y = df["is_malicious"]
df = df.drop(columns=["is_malicious"])

# 🧠 Vectorize the system call sequences (BoW)
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(df["syscall_sequence"]).toarray()

# 🔍 Normalize features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_vectorized)

# 🧪 Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 🧠 Build the Autoencoder
input_dim = X_train.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(64, activation='relu', activity_regularizer=regularizers.l1(10e-5))(input_layer)
encoded = Dense(32, activation='relu')(encoded)
decoded = Dense(64, activation='relu')(encoded)
decoded = Dense(input_dim, activation='sigmoid')(decoded)
autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# 🧠 Train the Autoencoder on normal data only
autoencoder.fit(X_train[y_train == 0], X_train[y_train == 0],
                epochs=10, batch_size=32, shuffle=True, validation_split=0.1)

# ⚙️ Generate reconstruction errors for all training samples
reconstructions = autoencoder.predict(X_train)
mse = np.mean(np.power(X_train - reconstructions, 2), axis=1)

# 🌲 Train the Random Forest classifier on reconstruction errors
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(np.expand_dims(mse, axis=1), y_train)

# 💾 Save all models
os.makedirs("models/local_models", exist_ok=True)
autoencoder.save("models/local_models/systemcall_autoencoder.keras")
joblib.dump(rf, "models/local_models/systemcall_rf.pkl")
joblib.dump(scaler, "models/local_models/systemcall_scaler.pkl")
joblib.dump(vectorizer, "models/local_models/systemcall_vectorizer.pkl")

print("✅ System Call Anomaly Detection model trained and saved successfully.")
