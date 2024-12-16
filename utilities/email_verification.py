from flask import Flask, jsonify
from  redis import redis_client
from bcrypt import jwt
import datetime
from models import db, User, Doctor

SECRET_KEY = 'mysecretkey'

def generate_verification_token(email, role):
    payload = {
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_email(token):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload["email"]
        role = payload["role"]

        # Retrieve data from Redis
        user_data = redis_client.get(email)
        if not user_data:
            return jsonify({"error": "Invalid or expired token"}), 400

        # Convert JSON string back to dictionary
        user_data = eval(user_data.decode("utf-8"))

        # Persist data to the appropriate table
        if role == "user":
            new_user = User(**user_data)
            db.session.add(new_user)
        elif role == "doctor":
            new_doctor = Doctor(**user_data)
            db.session.add(new_doctor)

        db.session.commit()
        redis_client.delete(email)

        return jsonify({"message": f"{role.capitalize()} verified and registered successfully"}), 201

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
