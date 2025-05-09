# Protectron: AI-Enhanced Endpoint Security Tool

⚠️ **This project is currently under active development. Some features may not work as expected.**

Protectron is an advanced AI-driven endpoint security tool designed to detect and mitigate cyber threats in real-time. It leverages AI models for malware detection, phishing prevention, reverse shell identification, and anomaly detection, ensuring robust protection for your system.

## 🚀 Features

### 🔒 **Real-Time Security Monitoring**

- **Network Security:** Monitors incoming and outgoing network traffic, detecting suspicious activities.
- **File Access Management:** Tracks file access patterns to prevent unauthorized changes.
- **Reverse Shell Detection:** Identifies and blocks reverse shell connections.
- **User Behavior Analysis:** Analyzes user activity to detect anomalies.

### 🧠 **AI-Powered Threat Detection**

- **Malware Detection Model** (`malware_classification_model.h5`)
- **Phishing Detection Model** (`phishing_detection_model.h5`)
- **Reverse Shell Detection Model** (`reverse_shell_detection_model.h5`)
- **Advanced Anomaly Detection Model** (`advanced_anomaly_detection_model.h5`)

### 📊 **Dashboard**

- Real-time visualization of network traffic, file activities, and AI-predicted threats.
- Interactive charts for easy security analysis.

### 🔥 **Cross-Platform Compatibility**

- Supports **Windows (netsh)** and **Linux (iptables)** firewall management.
- Detects OS type automatically and applies correct security rules.

---

## 📁 Project Structure

```
Protectron/
│
├── main.py                          # Main entry point (starts Protectron and the dashboard)
├── config.py                        # Configuration settings
├── module_manager.py                # Manages all security modules
│
├── data/                             # Stores logs, raw datasets, and AI inputs
│   ├── network_traffic/              # Network logs and analysis data
│   ├── malware_samples/              # Malware datasets for AI training
│   ├── file_access_logs/             # File access logs
│   ├── permission_logs/              # App permission logs
│   ├── datasets/                     # AI training datasets
│
├── models/                           # AI models
│   ├── local_models/                 # Models trained locally
│   ├── cloud_models/                 # Cloud-trained models
│
├── logs/                             # Security logs
│
├── modules/                          # Security modules
│   ├── network_security.py           # Network security module
│   ├── malware_protection.py         # Malware detection
│   ├── file_access_management.py     # File access monitoring
│   ├── reverse_connection_monitor.py # Reverse shell detection
│   ├── user_behavior.py              # User behavior analysis
│
├── utils/                            # Utility functions
│
├── database/                         # MongoDB for security logs
│
├── training/                         # AI model training scripts
│   ├── local_training/               # Local model training
│   ├── cloud_training/               # Cloud-based training
│
├── frontend/                         # Web-based dashboard
│   ├── static/                       # CSS, JS, Images
│   ├── templates/                    # HTML templates
│   ├── dashboard.py                  # Flask-powered dashboard
│
├── requirements.txt                  # Project dependencies
├── README.md                         # Project documentation
└── LICENSE                           # Project license
```

---

## 📦 Installation

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/yourusername/Protectron.git
cd Protectron
```

### **Step 2: Set Up Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 4: Configure MongoDB**

Ensure MongoDB is installed and running on your system. Update `config.py` with your MongoDB URI.

### **Step 5: Generate AI Training Datasets**

```bash
python training/generate_dataset.py
```

### **Step 6: Train AI Models**

Train models locally:

```bash
python training/local_training/train_malware.py
python training/local_training/train_phishing.py
python training/local_training/train_reverse_shell.py
python training/local_training/train_anomaly.py
```

### **Step 7: Run Protectron**

Launch Protectron's security system and dashboard:

```bash
python main.py
```

Access the dashboard at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📊 Usage

- The **Dashboard** will display real-time security alerts.
- Suspicious IPs detected by AI models will be automatically blocked.
- AI models will continuously learn and adapt to new threats.

---

## 🚨 Contributing

We welcome contributions to enhance Protectron! To contribute:

1. Fork the repo
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push the branch (`git push origin feature-xyz`)
5. Open a pull request

---

## 🔐 License

Protectron is licensed under the MIT License. See `LICENSE` for details.

---

## 📧 Contact

For questions or suggestions:

- **Email:** [your-email@example.com](mailto\:your-email@example.com)
- **GitHub:** [yourusername](https://github.com/yourusername)

---

🚀 **Stay secure with Protectron!** 🔥

