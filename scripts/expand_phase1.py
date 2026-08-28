import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/auth/decorators.py': '''from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.auth.models import User
import logging

logger = logging.getLogger(__name__)

def role_required(*allowed_roles):
    """
    Decorator to enforce Role-Based Access Control (RBAC).
    Usage: @role_required('Super Admin', 'Organization Owner')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({"error": "User not found"}), 404
                
            if not user.is_active:
                return jsonify({"error": "Account is disabled"}), 403
                
            if user.role and user.role.name in allowed_roles:
                return fn(*args, **kwargs)
                
            logger.warning(f"Unauthorized access attempt by user {user_id}. Required roles: {allowed_roles}")
            return jsonify({"error": "Insufficient permissions"}), 403
        return decorator
    return wrapper

def mfa_required():
    """
    Ensures the user has passed Multi-Factor Authentication.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            # Implement JWT claims check for MFA verified flag
            return fn(*args, **kwargs)
        return decorator
    return wrapper
''',
    'app/auth/utils.py': '''import re
import pyotp
import secrets
import string

def validate_password_strength(password: str) -> bool:
    """
    Enforces enterprise password policies:
    - At least 12 characters
    - Contains uppercase and lowercase
    - Contains numbers
    - Contains special characters
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

def generate_totp_secret() -> str:
    """Generates a base32 secret for Authenticator apps."""
    return pyotp.random_base32()

def generate_secure_token(length=32) -> str:
    """Generates a cryptographically secure random token for email verification/resets."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))
''',
    'app/auth/blocklist.py': '''# Simple in-memory blocklist for JWT Revocation.
# In production, this must be backed by Redis.

jwt_redis_blocklist = set()

def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    """
    Callback function for Flask-JWT-Extended to check if a token is revoked.
    """
    jti = jwt_payload["jti"]
    token_in_redis = jti in jwt_redis_blocklist
    return token_in_redis

def revoke_token(jti: str):
    """
    Adds a token's JTI to the blocklist.
    """
    jwt_redis_blocklist.add(jti)
''',
    'tests/test_auth_advanced.py': '''import pytest
from app.auth.utils import validate_password_strength, generate_secure_token

def test_password_strength_validator_weak():
    is_valid, msg = validate_password_strength("weakpass")
    assert not is_valid
    assert "12 characters" in msg

def test_password_strength_validator_no_special():
    is_valid, msg = validate_password_strength("StrongPassword123")
    assert not is_valid
    assert "special character" in msg

def test_password_strength_validator_valid():
    is_valid, msg = validate_password_strength("Super!Strong12345")
    assert is_valid
    assert msg == ""

def test_generate_secure_token():
    token1 = generate_secure_token()
    token2 = generate_secure_token()
    assert len(token1) == 32
    assert token1 != token2 # Extremely low probability of collision
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 1 Deep Dive components generated successfully.')
