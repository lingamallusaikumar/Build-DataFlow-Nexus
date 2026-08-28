import re
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
    if not re.search(r"[!@#$%^&*(),.?":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

def generate_totp_secret() -> str:
    """Generates a base32 secret for Authenticator apps."""
    return pyotp.random_base32()

def generate_secure_token(length=32) -> str:
    """Generates a cryptographically secure random token for email verification/resets."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))
