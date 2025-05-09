import hashlib
import os
import mimetypes
import logging

def compute_file_hash(file_path):
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def is_executable(file_path):
    """Check if a file is an executable based on MIME type."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type in ['application/x-dosexec', 'application/x-executable']

def list_files_recursively(directory, extensions=None):
    """Yield all file paths in a directory recursively, filtering by extensions."""
    for root, _, files in os.walk(directory):
        for file in files:
            if extensions:
                if any(file.lower().endswith(ext.lower()) for ext in extensions):
                    yield os.path.join(root, file)
            else:
                yield os.path.join(root, file)

def load_signature_db(file_path):
    """Load the signature DB from a text file into a Python set."""
    try:
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f.readlines())
    except Exception as e:
        logging.error(f"Failed to load signature DB: {e}")
        return set()
