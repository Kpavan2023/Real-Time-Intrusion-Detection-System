from flask import Blueprint, request, jsonify
import mysql.connector
from werkzeug.security import check_password_hash
import jwt
import datetime
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

login_bp = Blueprint("login", __name__)

# ✅ Use the secret key from .env
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("❌ Secret key is missing! Set FLASK_SECRET_KEY in .env")

def get_db_connection():
    """Establishes a database connection with connection pooling"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ids_db",
        pool_name="mypool",
        pool_size=5  # 🔹 Enables connection pooling
    )

@login_bp.route('/login', methods=['POST'])
def login():
    """Handles user login authentication"""
    data = request.json
    email, password = data.get("email"), data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid email or password"}), 401

        token = jwt.encode(
            {"user_id": user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY, algorithm="HS256"
        )

        return jsonify({"message": "Login successful!", "token": token}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
