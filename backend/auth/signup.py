from flask import Blueprint, request, jsonify
import random
import string
import time
import mysql.connector
import bcrypt
from werkzeug.security import generate_password_hash
from utils.email_alerts import send_email_alert

signup_bp = Blueprint("signup", __name__)

# 🔹 Temporary in-memory OTP storage (suggest Redis for production)
otp_storage = {}

# ✅ MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add if password is set
        database="ids_db",
        pool_name="mypool",
        pool_size=5
    )

# ✅ OTP generator
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# ✅ Send OTP to user email
@signup_bp.route('/signup', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {
        "otp": otp,
        "timestamp": time.time()
    }

    print(f"🔐 DEBUG: Generated OTP for {email}: {otp}")  # Debug only

    if send_email_alert(email, f"Your OTP code is: {otp}"):
        return jsonify({"message": "OTP sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send OTP"}), 500


# 🔹 Register new user after OTP verification
@signup_bp.route('/register', methods=['POST'])
def register_user():
   data = request.json
   first_name = data.get("first_name")
   last_name = data.get("last_name")
   email = data.get("email")
   phone = data.get("phone")
   password = data.get("password")
   otp = data.get("otp")
   if not all([first_name, last_name, email, phone, password, otp]):
        return jsonify({"error": "All fields are required!"}), 400
   otp_data = otp_storage.get(email)
   if not otp_data:
        return jsonify({"error": "OTP not found or expired"}), 400

    # Optional: OTP Expiry Check (5 minutes)
   if time.time() - otp_data["timestamp"] > 300:
        del otp_storage[email]
        return jsonify({"error": "OTP expired!"}), 400

    # Match the OTP
   if otp_data["otp"] != otp:
        return jsonify({"error": "Invalid OTP"}), 400
   try:
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO users (first_name, last_name, email, phone, password_hash)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, phone, hashed_password))
        conn.commit()

        print("✅ User inserted into database")

        cursor.close()
        conn.close()
        del otp_storage[email]

        return jsonify({"message": "User registered successfully!"}), 201
   except mysql.connector.Error as err:
        print(f"❌ MySQL error occurred: {err}")
        return jsonify({"error": "Database error", "details": str(err)}), 500