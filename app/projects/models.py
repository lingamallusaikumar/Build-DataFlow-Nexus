from app.extensions import db
from app.models.base import BaseModel

class Project(BaseModel):
    __tablename__ = 'projects'
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    workspace_id = db.Column(db.String(36), db.ForeignKey('workspaces.id'), nullable=False)
    
    workspace = db.relationship('Workspace', back_populates='projects')
    pipelines = db.relationship('Pipeline', back_populates='project', cascade='all, delete-orphan')
