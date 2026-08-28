from app.extensions import db
from app.models.base import BaseModel

class Team(BaseModel):
    __tablename__ = 'teams'
    name = db.Column(db.String(100), nullable=False)
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    
    organization = db.relationship('Organization', back_populates='teams')
