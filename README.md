# 🚨 Real-Time Intrusion Detection System (IDS)

A real-time intrusion detection system that leverages Snort for packet sniffing and deep learning models (DNN + LightGBM) to detect cyberattacks. Alerts are sent via email and SMS. The system features a full-stack web interface with user authentication, dashboards, and visualization tools.

---

## 📌 Table of Contents

- [🚀 Features](#-features)
- [🛠️ Tech Stack](#%ef%b8%8f-tech-stack)
- [📦 Directory Structure](#-directory-structure)
- [📊 Model Performance](#-model-performance)
- [📚 Dataset Used](#-dataset-used)
- [🧠 Model Training](#-model-training)
- [🖥️ Frontend Features](#%ef%b8%8f-frontend-features)
- [🔐 Backend Services](#-backend-services)
- [⚠️ Alerts & Notifications](#%ef%b8%8f-alerts--notifications)
- [💡 How It Works](#-how-it-works)
- [🚀 Deployment Instructions](#-deployment-instructions)
- [📜 License](#-license)

---

## 🚀 Features

- 🔐 User Signup/Login with OTP email verification
- 📈 Real-time intrusion detection using Snort
- 📩 Instant alerts via Email & SMS
- 🌐 Live dashboard for alerts, geolocation, and system status
- 🧠 DNN and LightGBM models trained on real network data
- 📊 LIME for explainable ML predictions
- 🌎 IP geolocation and risk-level scoring
- ⚙️ Admin pages for safeguards, profile settings, etc.

---

## 🛠️ Tech Stack

### 💻 Frontend

- React.js
- JavaScript, CSS
- Axios, React Toastify
- Responsive UI with Dark/Light mode

### 🧪 Backend

- Flask (Python)
- MySQL
- TensorFlow (DNN model)
- LightGBM
- Snort (Packet monitoring)
- Twilio (SMS), SMTP (Emails)
- LIME (Model interpretability)

### 🛠️ Development Tools

- Google Colab (Training models)
- Google Drive (Model storage)
- Postman (API Testing)
- Git & GitHub

---

## 📦 Directory Structure

```
📂 Real-Time-IDS/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── database/
│   │   ├── db_connection.py
│   │   └── models.py
│   ├── auth/
│   │   ├── signup.py
│   │   └── login.py
│   ├── model/
│   │   ├── inference.py
│   │   └── saved_models/
│   │       ├── dnn_ids_model.h5
│   │       └── lgbm_ids_model.txt
│   ├── snort/
│   │   └── snort_monitor.py
│   └── utils/
│       ├── email_alerts.py
│       └── sms_alerts.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│
├── model_training/
│   └── train_ids_models.ipynb   # Complete notebook for DNN & LightGBM training
│
├── .gitignore
└── README.md
```

---

## 📊 Model Performance

| Class         | Precision                | Recall      | F1-Score    | Support |
| ------------- | ------------------------ | ----------- | ----------- | ------- |
| Normal (0)    | 0.90 (DNN) / 0.87 (LGBM) | 0.90 / 0.95 | 0.90 / 0.91 | 18613   |
| Intrusion (1) | 0.94 / 0.97              | 0.94 / 0.92 | 0.94 / 0.95 | 32922   |
| Accuracy      | **0.9267 (DNN)**         | —           | —           | 51535   |
|               | **0.9321 (LGBM)**        | —           | —           | 51535   |

---

## 📚 Dataset Used

- **UNSW-NB15 Dataset** from the Australian Centre for Cyber Security (ACCS)
- Used for binary classification (normal vs intrusion)
- Top 20 features selected using **Random Forest**

---

## 🧠 Model Training

### 📁 `model_training/train_ids_models.ipynb` includes:
- Full training pipeline for both **DNN** and **LightGBM**.
- **Preprocessing** with label encoding, SMOTE for class balance, and feature selection using Random Forest.
- **DNN Training** using Keras with Keras Tuner for hyperparameter optimization.
- **LightGBM Training** using Optuna for hyperparameter tuning.
- Saves models (`dnn_ids_model_1.h5`, `lgbm_ids_model_1.txt`) to Google Drive for use in backend.

### ✅ Key Highlights:
- Dataset: UNSW-NB15
- Feature Selection: Top 20 via RandomForestClassifier
- Balancing: SMOTE
- DNN:
  - Framework: TensorFlow/Keras
  - Tuning: Keras Tuner
  - Accuracy: **92.67%**
- LightGBM:
  - Tuning: Optuna
  - Accuracy: **93.21%**

---

## 🖥️ Frontend Features

- ✅ **Signup** with OTP (Email)
- 🔐 **Login**
- 📈 **Dashboard**: Traffic summary, alerts, geolocation
- 🔔 **Alerts Page**: Display only malicious events
- 🛡️ **Safeguards Page**: Security tips for users
- ⚙️ **Settings/Profile Page**: Update details, upload profile image

---

## 🔐 Backend Services

- 📡 **Snort** monitors packets in real-time
- ↻ Flask APIs classify each flow using ML models
- 📁 Alerts saved to MySQL only if classified as intrusion
- 📩 **SMTP** & 📱 **Twilio** used for sending alerts
- 🔍 LIME gives insight into why a packet was flagged

---

## ⚠️ Alerts & Notifications

- ⛔ Real-time detection of malicious flows
- 📧 Email: timestamp, type, source/destination IP
- 📱 SMS: quick summary to mobile
- 🧠 Risk labels: Minimal, Low, Medium, High

---

## 💡 How It Works

```
Snort ➞ Packet Info ➞ Flow Extractor ➞ ML Model ➞ Classification ➞ DB + Alerts ➞ UI
```

---

## 🚀 Deployment Instructions

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Real-Time-IDS.git

# 2. Backend Setup
cd backend
pip install -r requirements.txt
python app.py

# 3. Frontend Setup
cd ../frontend
npm install
npm start
```

---

## 📜 License

This project was developed by **Pavan Kumar Kollipara and team** for academic and educational purposes. 
You are welcome to explore, learn from, and adapt the code for personal or academic use.  

© 2025 Pavan Kumar Kollipara. All rights reserved.

