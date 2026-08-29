from flask import Blueprint, request, jsonify

from app.auth.schemas import UserRegistrationSchema, UserLoginSchema
from app.auth.services import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = UserRegistrationSchema(**request.get_json())
    except Exception as e:
        return jsonify({"errors": e.errors()}), 400

    user, error = AuthService.register_user(data)
    if error:
        return jsonify({"error": error}), 409

    return jsonify({"message": "User created successfully", "user_id": user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = UserLoginSchema(**request.get_json())
    except Exception as e:
        return jsonify({"errors": e.errors()}), 400

    tokens, error = AuthService.authenticate_user(data.email, data.password)
    if error:
        return jsonify({"error": error}), 401

    return jsonify(tokens), 200

