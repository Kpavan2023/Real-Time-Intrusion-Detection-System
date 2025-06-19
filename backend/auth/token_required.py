from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = 'your_secret_key_here'  # Replace with your actual secret key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if Authorization header is present
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]  # Extract token from "Bearer <token>"

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_email = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403

        # You can also fetch and pass the user from DB if needed
        return f(current_user_email, *args, **kwargs)

    return decorated
