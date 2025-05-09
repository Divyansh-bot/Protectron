import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv1D, MaxPooling1D, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint
import os

# Load dataset
df = pd.read_csv("data/datasets/malware_dataset.csv")

# Separate features and label
X = df.drop("label", axis=1).values
y = df["label"].values

# Reshape for CNN input (samples, time_steps, features)
X = X.reshape((X.shape[0], X.shape[1], 1))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build CNN Model
model = Sequential([
    Conv1D(32, 3, activation='relu', input_shape=(X.shape[1], 1)),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),
    Conv1D(64, 3, activation='relu'),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Save model on improvement
os.makedirs("hybrid_ai/models", exist_ok=True)
checkpoint = ModelCheckpoint("hybrid_ai/models/cnn_malware_detector.keras", save_best_only=True, monitor='val_accuracy', mode='max')

# Train
model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_test, y_test), callbacks=[checkpoint])

print("✅ Model training complete and saved to: cnn_malware_detector.h5")
