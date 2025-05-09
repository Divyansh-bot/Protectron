import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Directory paths
MODEL_DIR = os.path.join(BASE_DIR, 'models')
SIGNATURE_DB = os.path.join(BASE_DIR, 'signature_db', 'malware_hashes.json')
QUARANTINE_DIR = os.path.join(BASE_DIR, 'quarantine')
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'hybrid_ai.log')

# Scanning settings
SCAN_EXTENSIONS = ['.exe', '.dll', '.js', '.vbs', '.bat', '.py', '.jar']
MAX_FILE_SIZE_MB = 50  # Skip files larger than this

# CNN model file
CNN_MODEL_PATH = os.path.join(MODEL_DIR, 'malware_cnn_model.keras')

# Metadata
VERSION = '1.0'
