import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'
files = {
    'app/models/base.py': '''import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
''',
    'app/auth/models.py': '''from app.extensions import db
from app.models.base import BaseModel
import bcrypt

class Role(BaseModel):
    __tablename__ = 'roles'
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    users = db.relationship('User', back_populates='role')

class User(BaseModel):
    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id'), nullable=True)

    role = db.relationship('Role', back_populates='users')

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
''',
    'app/auth/schemas.py': '''from pydantic import BaseModel, EmailStr, constr

class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    first_name: str = None
    last_name: str = None

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
''',
    'app/auth/services.py': '''from app.extensions import db
from app.auth.models import User
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:
    @staticmethod
    def register_user(data):
        if User.query.filter_by(email=data.email).first():
            return None, "User already exists."
        
        new_user = User(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name
        )
        new_user.set_password(data.password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, None

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return {
                "access_token": create_access_token(identity=user.id),
                "refresh_token": create_refresh_token(identity=user.id)
            }, None
        return None, "Invalid email or password"
''',
    'app/auth/routes.py': '''from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.auth.schemas import UserRegistrationSchema, UserLoginSchema
from app.auth.services import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = UserRegistrationSchema(**request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    user, error = AuthService.register_user(data)
    if error:
        return jsonify({"error": error}), 409

    return jsonify({"message": "User created successfully", "user_id": user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = UserLoginSchema(**request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    tokens, error = AuthService.authenticate_user(data.email, data.password)
    if error:
        return jsonify({"error": error}), 401

    return jsonify(tokens), 200
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Auth models, schemas, routes, and services created.')
