# Simple in-memory blocklist for JWT Revocation.
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
