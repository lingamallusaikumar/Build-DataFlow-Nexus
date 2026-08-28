from app.extensions import db
from app.models.base import BaseModel

class AuditLog(BaseModel):
    __tablename__ = 'audit_logs'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True) # Null if system action
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False) # e.g., 'UPDATE_PIPELINE', 'DELETE_USER'
    resource = db.Column(db.String(100), nullable=False) # e.g., 'pipeline_id_123'
    ip_address = db.Column(db.String(50), nullable=True)
    metadata_json = db.Column(db.JSON, nullable=True) # Stores before/after states
