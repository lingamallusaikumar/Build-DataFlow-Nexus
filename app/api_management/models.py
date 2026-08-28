from app.extensions import db
from app.models.base import BaseModel
import secrets

class APIKey(BaseModel):
    __tablename__ = 'api_keys'
    
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    key_hash = db.Column(db.String(255), nullable=False, unique=True)
    prefix = db.Column(db.String(10), nullable=False) # Store first few chars for display
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    @staticmethod
    def generate_key():
        raw_key = secrets.token_urlsafe(32)
        return raw_key, f"df_{raw_key[:6]}"
