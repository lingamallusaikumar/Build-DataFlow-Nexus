import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verifies SHA256 HMAC signature of incoming webhook payloads."""
    if not signature or not secret:
        return False
    
    expected_hash = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Secure comparison to prevent timing attacks
    return hmac.compare_digest(f"sha256={expected_hash}", signature)
