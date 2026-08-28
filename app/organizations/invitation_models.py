from app.extensions import db
from app.models.base import BaseModel
from datetime import datetime, timedelta

class OrganizationInvitation(BaseModel):
    __tablename__ = 'organization_invitations'
    
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    role = db.Column(db.String(50), nullable=False, default='developer')
    expires_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=7))
    is_accepted = db.Column(db.Boolean, default=False)
    
    organization = db.relationship('Organization')
