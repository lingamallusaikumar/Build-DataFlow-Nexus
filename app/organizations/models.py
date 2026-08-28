from app.extensions import db
from app.models.base import BaseModel

class Organization(BaseModel):
    __tablename__ = 'organizations'
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    billing_plan = db.Column(db.String(50), default='free')
    is_active = db.Column(db.Boolean, default=True)

    teams = db.relationship('Team', back_populates='organization', cascade='all, delete-orphan')
    workspaces = db.relationship('Workspace', back_populates='organization', cascade='all, delete-orphan')

class OrganizationMember(BaseModel):
    __tablename__ = 'organization_members'
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False) # e.g., owner, admin, developer
