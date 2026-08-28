import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/organizations/services.py': '''from app.extensions import db
from app.organizations.models import Organization, OrganizationMember
from sqlalchemy.exc import IntegrityError

class OrganizationService:
    @staticmethod
    def create_organization(name, slug, user_id):
        try:
            org = Organization(name=name, slug=slug)
            db.session.add(org)
            db.session.flush() # Get ID without committing

            member = OrganizationMember(org_id=org.id, user_id=user_id, role='owner')
            db.session.add(member)
            db.session.commit()
            return org, None
        except IntegrityError:
            db.session.rollback()
            return None, "Organization slug already exists."

    @staticmethod
    def get_user_organizations(user_id):
        memberships = OrganizationMember.query.filter_by(user_id=user_id).all()
        return [Organization.query.get(m.org_id) for m in memberships]
''',
    'app/organizations/routes.py': '''from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.organizations.services import OrganizationService

org_bp = Blueprint('organizations', __name__)

@org_bp.route('/', methods=['POST'])
@jwt_required()
def create_org():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not 'name' in data or not 'slug' in data:
        return jsonify({'error': 'Name and slug are required'}), 400
        
    org, error = OrganizationService.create_organization(data['name'], data['slug'], user_id)
    if error:
        return jsonify({'error': error}), 409
        
    return jsonify({'message': 'Organization created', 'org_id': org.id}), 201

@org_bp.route('/', methods=['GET'])
@jwt_required()
def list_orgs():
    user_id = get_jwt_identity()
    orgs = OrganizationService.get_user_organizations(user_id)
    return jsonify([{'id': o.id, 'name': o.name, 'slug': o.slug} for o in orgs]), 200
''',
    'app/workspaces/services.py': '''from app.extensions import db
from app.workspaces.models import Workspace

class WorkspaceService:
    @staticmethod
    def create_workspace(name, org_id):
        workspace = Workspace(name=name, org_id=org_id)
        db.session.add(workspace)
        db.session.commit()
        return workspace

    @staticmethod
    def get_workspaces_by_org(org_id):
        return Workspace.query.filter_by(org_id=org_id).all()
''',
    'app/projects/services.py': '''from app.extensions import db
from app.projects.models import Project

class ProjectService:
    @staticmethod
    def create_project(name, description, workspace_id):
        project = Project(name=name, description=description, workspace_id=workspace_id)
        db.session.add(project)
        db.session.commit()
        return project
''',
    'app/connectors/base/connector_interface.py': '''from abc import ABC, abstractmethod

class BaseConnector(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def push_data(self, data):
        pass
        
    @abstractmethod
    def test_connection(self) -> bool:
        pass
''',
    'app/connectors/base/postgres_connector.py': '''from app.connectors.base.connector_interface import BaseConnector
import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresConnector(BaseConnector):
    def connect(self):
        return psycopg2.connect(
            host=self.config.get('host'),
            database=self.config.get('database'),
            user=self.config.get('user'),
            password=self.config.get('password'),
            port=self.config.get('port', 5432)
        )

    def test_connection(self):
        try:
            conn = self.connect()
            conn.close()
            return True
        except Exception:
            return False

    def fetch_data(self, query):
        conn = self.connect()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                return cur.fetchall()
        finally:
            conn.close()

    def push_data(self, data):
        pass # Implemented in specific destinations
''',
    'app/executor/tasks.py': '''from app.extensions import celery_app, db
from app.pipelines.models import Pipeline, PipelineExecution
import time
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def execute_pipeline_task(self, execution_id):
    """
    Celery task to run a pipeline asynchronously.
    """
    # Requires app context for DB access if running in a separate worker
    # In a real setup, Celery needs Flask app context pushed here.
    logger.info(f"Starting pipeline execution: {execution_id}")
    try:
        # Simulate execution logic
        time.sleep(2)
        logger.info(f"Pipeline {execution_id} completed successfully.")
        return {"status": "success", "execution_id": execution_id}
    except Exception as exc:
        logger.error(f"Pipeline execution failed: {exc}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
''',
    'app/data_quality/validators.py': '''class DataValidator:
    def __init__(self, rules):
        self.rules = rules

    def validate_record(self, record):
        errors = []
        for field, rule in self.rules.items():
            value = record.get(field)
            if rule.get('required') and value is None:
                errors.append(f"{field} is required.")
            if rule.get('type') and value is not None:
                if type(value).__name__ != rule['type']:
                    errors.append(f"{field} must be of type {rule['type']}.")
        
        return len(errors) == 0, errors
'''
}

# Add Blueprint registration logic to app/__init__.py
init_file = os.path.join(base_dir, 'app/__init__.py')
with open(init_file, 'r', encoding='utf-8') as f:
    init_content = f.read()

if 'from app.organizations.routes import org_bp' not in init_content:
    init_content = init_content.replace(
        "app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')",
        "app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')\n    from app.organizations.routes import org_bp\n    app.register_blueprint(org_bp, url_prefix='/api/v1/organizations')"
    )
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 5 components, Connectors, and Organization routes generated successfully.')
