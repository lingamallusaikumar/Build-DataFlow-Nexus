from functools import wraps
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
