import pytest
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
