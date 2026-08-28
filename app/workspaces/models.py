from app.extensions import db
from app.models.base import BaseModel

class Workspace(BaseModel):
    __tablename__ = 'workspaces'
    name = db.Column(db.String(100), nullable=False)
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    
    organization = db.relationship('Organization', back_populates='workspaces')
    projects = db.relationship('Project', back_populates='workspace', cascade='all, delete-orphan')
