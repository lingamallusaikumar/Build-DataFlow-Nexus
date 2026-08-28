from app.extensions import db
from app.api_management.models import APIKey
import hashlib

class APIKeyService:
    @staticmethod
    def create_api_key(name, org_id, expires_at=None):
        raw_key, prefix = APIKey.generate_key()
        
        # Hash the key for storage
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        api_key = APIKey(
            org_id=org_id,
            name=name,
            key_hash=key_hash,
            prefix=prefix,
            expires_at=expires_at
        )
        
        db.session.add(api_key)
        db.session.commit()
        
        # We only return the raw key once upon creation
        return api_key, raw_key

    @staticmethod
    def verify_key(raw_key):
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        return APIKey.query.filter_by(key_hash=key_hash, is_active=True).first()
