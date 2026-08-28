import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'
files = {
    'app/organizations/models.py': '''from app.extensions import db
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
''',
    'app/teams/models.py': '''from app.extensions import db
from app.models.base import BaseModel

class Team(BaseModel):
    __tablename__ = 'teams'
    name = db.Column(db.String(100), nullable=False)
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    
    organization = db.relationship('Organization', back_populates='teams')
''',
    'app/workspaces/models.py': '''from app.extensions import db
from app.models.base import BaseModel

class Workspace(BaseModel):
    __tablename__ = 'workspaces'
    name = db.Column(db.String(100), nullable=False)
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    
    organization = db.relationship('Organization', back_populates='workspaces')
    projects = db.relationship('Project', back_populates='workspace', cascade='all, delete-orphan')
''',
    'app/projects/models.py': '''from app.extensions import db
from app.models.base import BaseModel

class Project(BaseModel):
    __tablename__ = 'projects'
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    workspace_id = db.Column(db.String(36), db.ForeignKey('workspaces.id'), nullable=False)
    
    workspace = db.relationship('Workspace', back_populates='projects')
    pipelines = db.relationship('Pipeline', back_populates='project', cascade='all, delete-orphan')
''',
    'app/pipelines/models.py': '''from app.extensions import db
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
''',
    'app/connectors/models.py': '''from app.extensions import db
from app.models.base import BaseModel

class Connector(BaseModel):
    __tablename__ = 'connectors'
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., postgres, rest_api, mongodb
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    config = db.Column(db.JSON, nullable=False) # Credentials/Host configs (encrypted in real scenario)
    is_active = db.Column(db.Boolean, default=True)
'''
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 2, 3, and 4 models created.')
