from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import jwt
from functools import wraps

# Load environment variables
load_dotenv()

from database.db_connection import create_connection
from auth.signup import signup_bp
from auth.login import login_bp
from inference import predict_intrusion  # inference.py is in the backend folder
from snort.snort_monitor import capture_traffic  # Run separately if needed
from utils.email_alerts import send_email_alert
from utils.sms_alerts import send_sms_alert

# Initialize Flask app
app = Flask(__name__)

# Proper CORS setup for React frontend (port 3000)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")

# Register authentication blueprints
app.register_blueprint(signup_bp, url_prefix='/auth')
app.register_blueprint(login_bp, url_prefix='/auth')

# Path to the Snort alerts file (if you want to use file-based alerts)
LOG_FILE = "C:/Snort/log/alert.ids"

# Middleware to require a valid token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403
        try:
            token = token.split(" ")[1]  # Extract token from "Bearer <token>"
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = decoded_token["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 403
        return f(current_user, *args, **kwargs)
    return decorated_function

# Function to get the latest user's contact details (email and phone number)
def get_user_contact_details():
    try:
        connection = create_connection()
        if connection is None:
            return None
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT email, phone FROM users ORDER BY id DESC LIMIT 1")
            user = cursor.fetchone()
        connection.close()
        return user
    except Exception as e:
        print("❌ Database error:", e)
        return None

@app.route('/')
def home():
    return jsonify({"message": "🚀 Intrusion Detection System is Running!"}), 200

@app.route('/detect', methods=['POST'])
@token_required
def detect_intrusion(current_user):
    """
    Detects network intrusions using the trained AI models.
    If traffic features are provided in the JSON payload, they are used for prediction.
    Otherwise, it returns an error since snort_monitor.py should run separately.
    """
    try:
        data = request.json
        traffic_data = data.get("features")
        source_ip = data.get("source_ip", "0.0.0.0")
        destination_ip = data.get("destination_ip", "0.0.0.0")

        if not traffic_data:
            return jsonify({"error": "No network traffic data provided."}), 400

        # Predict intrusion using the AI model
        try:
            prediction = predict_intrusion(traffic_data, current_user, source_ip, destination_ip)
        except Exception as e:
            return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

        intrusion_detected = (
            prediction.get("DNN") == "Intrusion Detected" or
            prediction.get("LightGBM") == "Intrusion Detected"
        )

        alert_message = "🚨 Intrusion detected in your network!" if intrusion_detected else "✅ No intrusion detected."

        # If an intrusion is detected, store the alert in the database and send notifications
        if intrusion_detected:
            connection = create_connection()
            if connection:
                with connection.cursor() as cursor:
                    query = "INSERT INTO alerts (user_email, source_ip, destination_ip, is_intrusion) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (current_user, source_ip, destination_ip, "Intrusion Detected"))
                    connection.commit()
                connection.close()

            user = get_user_contact_details()
            if user:
                send_email_alert(user["email"], alert_message)
                send_sms_alert(user["phone"], alert_message)

        return jsonify({
            "intrusion_detected": intrusion_detected,
            "message": alert_message,
            "prediction": prediction
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """
    ✅ Fetches alerts from MySQL instead of alert.ids
    """
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"alerts": []})

        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, message, timestamp FROM alerts ORDER BY timestamp DESC")
            alerts = cursor.fetchall()

        connection.close()
        return jsonify({"alerts": alerts})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profile/<email>', methods=['GET'])
@token_required  # Protect the route with token validation
def get_profile(current_user, email):
    """
    Fetches the profile details of a user based on their email. This route is protected.
    """
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT first_name, last_name, email, phone, profile_image FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

        connection.close()
        if user:
            return jsonify({"profile": user}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profile/update', methods=['POST'])
@token_required  # Protect this route too
def update_profile(current_user):
    """
    Updates the profile details of a user.
    """
    try:
        data = request.json
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        profile_image = data.get("profile_image")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        with connection.cursor() as cursor:
            query = "UPDATE users SET first_name = %s, last_name = %s, phone = %s, profile_image = %s WHERE email = %s"
            cursor.execute(query, (first_name, last_name, phone, profile_image, email))
            connection.commit()

        connection.close()
        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/safeguards', methods=['GET'])
@token_required  # Protect the safeguards page
def get_safeguards(current_user):
    """
    Returns the security safeguards and guidelines. This route is protected.
    """
    return jsonify({
        "safeguards": [
            "🔒 Keep your OS updated regularly.",
            "🔑 Use strong passwords and change them frequently.",
            "🚫 Avoid suspicious links and attachments.",
            "🔍 Monitor your network traffic for unusual activities."
        ]
    })

if __name__ == '__main__':
    # Running the app on port 5000 with debug mode enabled
    app.run(debug=True, port=5000)
