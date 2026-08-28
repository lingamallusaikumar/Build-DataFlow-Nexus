from app.extensions import db
from app.models.base import BaseModel

class Pipeline(BaseModel):
    __tablename__ = 'pipelines'
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    configuration = db.Column(db.JSON, nullable=False, default={}) # Stores the DAG/nodes
    
    project = db.relationship('Project', back_populates='pipelines')
    executions = db.relationship('PipelineExecution', back_populates='pipeline')

class PipelineExecution(BaseModel):
    __tablename__ = 'pipeline_executions'
    pipeline_id = db.Column(db.String(36), db.ForeignKey('pipelines.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending') # pending, running, success, failed
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    logs = db.Column(db.JSON, nullable=True)
    
    pipeline = db.relationship('Pipeline', back_populates='executions')

# Import for alembic migrations
from app.pipelines.versioning import PipelineVersion
