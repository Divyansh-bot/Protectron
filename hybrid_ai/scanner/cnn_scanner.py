import numpy as np
import logging
from tensorflow.keras.models import load_model
from hybrid_ai.config.paths import CNN_MODEL_PATH

# Load model once at import
cnn_model = load_model(CNN_MODEL_PATH)

def preprocess_file(file_path, max_len=2000):
    """
    Reads a binary file and converts to a fixed-size normalized array for CNN.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read(max_len)
        byte_arr = np.frombuffer(content, dtype=np.uint8)
        # Pad with zeros if needed
        if len(byte_arr) < max_len:
            byte_arr = np.pad(byte_arr, (0, max_len - len(byte_arr)))
        byte_arr = byte_arr / 255.0  # Normalize
        return byte_arr.reshape((1, max_len, 1))
    except Exception as e:
        logging.error(f"[CNN Scanner] Error preprocessing file: {e}")
        return None

def scan_file_with_cnn(file_path):
    """
    Predicts whether a file is malicious or benign using the CNN model.
    """
    logging.info(f"[CNN Scanner] Predicting with CNN for {file_path}")
    features = preprocess_file(file_path)
    if features is None:
        return "unknown"

    prediction = cnn_model.predict(features)[0][0]
    return "malicious" if prediction > 0.5 else "benign"
