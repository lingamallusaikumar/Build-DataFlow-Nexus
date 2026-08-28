from app.extensions import db
from app.models.base import BaseModel

class PipelineVersion(BaseModel):
    __tablename__ = 'pipeline_versions'
    
    pipeline_id = db.Column(db.String(36), db.ForeignKey('pipelines.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    configuration = db.Column(db.JSON, nullable=False)
    commit_message = db.Column(db.String(255), nullable=True)
    
    pipeline = db.relationship('Pipeline', backref=db.backref('versions', lazy='dynamic', cascade='all, delete-orphan'))
