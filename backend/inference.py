import numpy as np
from datetime import datetime
from flask import g  # For potential user context
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
from model.load_model import load_dnn_model, load_lgbm_model
from database.db_connection import create_connection
from utils.email_alerts import send_email_alert
from utils.sms_alerts import send_sms_alert

# Load models once
dnn_model = load_dnn_model()
lgbm_model = load_lgbm_model()

# Helper to get latest user's contact info
def get_user_contact_details():
    try:
        connection = create_connection()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT email, phone FROM users ORDER BY id DESC LIMIT 1")
                user = cursor.fetchone()
            connection.close()
            return user
    except Exception as e:
        print("Error fetching user contact:", e)
    return None

# Store alert in MySQL
def store_alert_in_db(message):
    try:
        connection = create_connection()
        if connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO alerts (message, timestamp) VALUES (%s, %s)"
                cursor.execute(query, (message, datetime.now()))
                connection.commit()
            connection.close()
    except Exception as e:
        print("Database Insertion Error:", e)

# Alert logic
def send_alerts_if_needed(dnn_result, lgbm_result):
    if "Intrusion Detected" in [dnn_result, lgbm_result]:
        alert_message = f"🚨 Intrusion Detected!\nDNN: {dnn_result}\nLightGBM: {lgbm_result}"
        user = get_user_contact_details()
        if user:
            if user.get("email"):
                send_email_alert(user["email"], alert_message)
            if user.get("phone"):
                send_sms_alert(user["phone"], alert_message)
        else:
            print("❌ No user contact info available")

# Main inference
def predict_intrusion(features):
    if dnn_model is None or lgbm_model is None:
        return {"error": "Models not loaded properly"}

    features = np.array(features).reshape(1, -1)
    print(f"Processed Features: {features.shape}")

    try:
        dnn_pred = dnn_model.predict(features)
        dnn_result = "Intrusion Detected" if dnn_pred[0][0] > 0.5 else "Normal Traffic"
    except Exception as e:
        print("❌ DNN Prediction Error:", e)
        dnn_result = "Error"

    try:
        lgbm_pred = lgbm_model.predict(features)
        lgbm_result = "Intrusion Detected" if lgbm_pred[0] > 0.5 else "Normal Traffic"
    except Exception as e:
        print("❌ LightGBM Prediction Error:", e)
        lgbm_result = "Error"

    message = f"DNN: {dnn_result}, LightGBM: {lgbm_result}"
    store_alert_in_db(message)
    send_alerts_if_needed(dnn_result, lgbm_result)

    return {
        "DNN": dnn_result,
        "LightGBM": lgbm_result,
        "Message": message
    }

# For manual test
if __name__ == "__main__":
    sample_features = np.random.rand(20).tolist()
    result = predict_intrusion(sample_features)
    print(result)
