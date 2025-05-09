
# 🛡️ Protectron – AI-Based Endpoint Security System

Protectron is an advanced endpoint security solution designed to provide real-time protection against a wide array of digital threats. It leverages artificial intelligence and traditional security mechanisms to detect anomalies, malware, unauthorized access, and system-level intrusions on a user’s machine.

---

## 🚀 Key Features

- 🔒 Real-Time Threat Detection
- 🧠 AI-Powered Security Modules
  - User Behavior Analysis
  - File Access Anomaly Detection
  - Network Intrusion Detection
  - Reverse Shell Detection
  - USB Device Threat Monitoring
  - App Permission Abuse Detection
  - System Call Monitoring
  - File Integrity Checking
- ⚙️ Hybrid Malware Detection Engine
  - CNN-Based Static Malware Classifier
  - Signature-Based Matching
  - Fusion Verdict System
- 🖥️ GUI Dashboard for Monitoring and Control
- 🔔 Real-Time Alerts and Logging

---

## 🧠 Architecture Overview

```
        ┌────────────────────┐
        │ Real-Time Monitors │
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │   AI Detection     │
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ Hybrid Malware     │
        │ Detection Engine   │
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ GUI + Notifications│
        └────────────────────┘
```

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/Protectron.git
cd Protectron
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Protectron/
├── modules/                  # All real-time monitoring scripts
├── models/local_models/      # Trained model files
├── hybrid_ai/                # Malware detection engine
│   ├── models/
│   ├── scanner/
│   ├── fusion_engine/
│   ├── signature_db/
│   ├── quarantine/
│   ├── utils/
│   └── config/
├── training/                 # Scripts for training models
├── utils/                    # Logging & alert functions
├── temp/                     # Live data buffers (CSV)
├── protectron_gui.py         # GUI application
├── protectron_app.py         # Main engine launcher
└── README.md
```

---

## ✅ How to Run

```bash
python protectron_gui.py
```

- Launches GUI dashboard
- Click "Start Protectron" to activate real-time monitoring
- Logs and alerts will appear live in the console

---

## 📊 Detection Techniques Used

| Module                | AI Techniques Used                 |
|-----------------------|------------------------------------|
| User Behavior         | Autoencoder + Random Forest        |
| File Access           | Autoencoder                        |
| Network Intrusion     | Autoencoder + Isolation Forest     |
| Reverse Shell         | Autoencoder + Random Forest        |
| USB Monitoring        | Autoencoder + Random Forest        |
| Permission Abuse      | Autoencoder + Random Forest        |
| System Calls          | Vectorizer + Autoencoder           |
| File Integrity        | Autoencoder + Random Forest        |
| Malware Detection     | CNN + Signature Matching + Fusion  |

---

## 📌 Dependencies

- Python 3.8+
- TensorFlow / Keras
- scikit-learn
- pandas, numpy
- watchdog
- psutil
- plyer (for desktop notifications)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🧩 Contribution

Contributions, feature requests, and issues are welcome. Please open an issue or submit a pull request to participate in improving Protectron.

---
