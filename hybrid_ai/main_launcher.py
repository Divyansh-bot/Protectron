import os
import logging
from hybrid_ai.scanner.cnn_scanner import scan_file_with_cnn
from hybrid_ai.scanner.signature_scanner import scan_file_with_signature
from hybrid_ai.fusion_engine.predictor import fuse_predictions
from hybrid_ai.quarantine.quarantine import quarantine_file

def scan_file(file_path):
    """Scan a given file using CNN + Signature-based detection."""
    try:
        # Signature-based detection
        sig_result = scan_file_with_signature(file_path)
        logging.info(f"[Main] Signature detection result: {sig_result}")

        # CNN-based static detection
        cnn_result = scan_file_with_cnn(file_path)
        logging.info(f"[Main] CNN detection result: {cnn_result}")

        # Fuse predictions
        final_result = fuse_predictions(sig_result, cnn_result)
        logging.info(f"[Main] Fused Detection: {final_result}")

        # If malicious, quarantine
        if final_result == "malicious":
            quarantine_file(file_path)
            logging.warning(f"[Main] File {file_path} is malicious and has been quarantined.")
        else:
            logging.info(f"[Main] File {file_path} is safe.")

    except Exception as e:
        logging.error(f"[Main] Error scanning file {file_path}: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

    test_directory = "hybrid_ai/test_samples"

    if not os.path.exists(test_directory):
        logging.warning(f"⚠️ Test directory does not exist: {test_directory}")
    else:
        logging.info(f"🛡️ Scanning files in: {test_directory}")
        for file in os.listdir(test_directory):
            file_path = os.path.join(test_directory, file)
            if os.path.isfile(file_path):
                scan_file(file_path)
