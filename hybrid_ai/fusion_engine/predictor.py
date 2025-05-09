import logging
from hybrid_ai.scanner.cnn_scanner import scan_file_with_cnn
from hybrid_ai.signature_db.signature_checker import check_file_signature

def cnn_predict(file_path):
    """
    Combines CNN-based static analysis and signature hash checking.

    Returns:
        {
            "cnn_result": "malicious" or "benign",
            "signature_result": "malicious" or "benign" or "unknown",
            "final_decision": "malicious" or "benign"
        }
    """
    logging.info(f"[Fusion Engine] Running combined prediction for {file_path}")

    # Step 1: CNN-based analysis
    cnn_result = predict_with_cnn(file_path)
    logging.info(f"[Fusion Engine] CNN result: {cnn_result}")

    # Step 2: Signature-based detection
    signature_result = check_file_signature(file_path)
    logging.info(f"[Fusion Engine] Signature result: {signature_result}")

    # Step 3: Fusion Logic (You can enhance this logic if needed)
    if signature_result == "malicious" or cnn_result == "malicious":
        final_decision = "malicious"
    else:
        final_decision = "benign"

    return {
        "cnn_result": cnn_result,
        "signature_result": signature_result,
        "final_decision": final_decision
    }
