import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/transformations/engine.py': '''class TransformationEngine:
    """
    Registry for data transformations. Follows the Strategy pattern.
    """
    def __init__(self):
        self.registry = {
            'rename_field': RenameFieldTransformation,
            'drop_field': DropFieldTransformation,
            'cast_type': CastTypeTransformation
        }

    def apply_transformations(self, data, transformations_config):
        """
        Applies a list of transformation configs to the data payload.
        """
        transformed_data = data
        for config in transformations_config:
            transform_type = config.get('type')
            if transform_type in self.registry:
                transformer = self.registry[transform_type](config)
                transformed_data = transformer.apply(transformed_data)
        return transformed_data


class BaseTransformation:
    def __init__(self, config):
        self.config = config

    def apply(self, data):
        raise NotImplementedError("Transformation subclasses must implement 'apply'")


class RenameFieldTransformation(BaseTransformation):
    def apply(self, data):
        old_name = self.config.get('old_name')
        new_name = self.config.get('new_name')
        if old_name in data:
            data[new_name] = data.pop(old_name)
        return data


class DropFieldTransformation(BaseTransformation):
    def apply(self, data):
        field = self.config.get('field')
        if field in data:
            del data[field]
        return data


class CastTypeTransformation(BaseTransformation):
    def apply(self, data):
        field = self.config.get('field')
        target_type = self.config.get('target_type')
        if field in data:
            try:
                if target_type == 'int':
                    data[field] = int(data[field])
                elif target_type == 'float':
                    data[field] = float(data[field])
                elif target_type == 'string':
                    data[field] = str(data[field])
            except (ValueError, TypeError):
                pass # In a real engine, we might log this or route to a dead-letter queue
        return data
''',
    'app/monitoring/sockets.py': '''from flask_socketio import emit, join_room, leave_room
from flask import request
from app.extensions import socketio
import logging

logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    # In production, validate JWT token from request.args before allowing connection
    logger.info(f"Client connected: {request.sid}")
    emit('system_status', {'status': 'connected', 'message': 'Welcome to DataFlow Nexus Real-Time Engine'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('subscribe_pipeline')
def handle_subscribe_pipeline(data):
    """
    Allows a client to subscribe to real-time events for a specific pipeline execution.
    """
    pipeline_id = data.get('pipeline_id')
    if pipeline_id:
        join_room(f"pipeline_{pipeline_id}")
        logger.info(f"Client {request.sid} subscribed to pipeline {pipeline_id}")
        emit('subscription_success', {'pipeline_id': pipeline_id})

@socketio.on('unsubscribe_pipeline')
def handle_unsubscribe_pipeline(data):
    pipeline_id = data.get('pipeline_id')
    if pipeline_id:
        leave_room(f"pipeline_{pipeline_id}")
        logger.info(f"Client {request.sid} unsubscribed from pipeline {pipeline_id}")
''',
    'app/notifications/models.py': '''from app.extensions import db
from app.models.base import BaseModel

class Notification(BaseModel):
    __tablename__ = 'notifications'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., 'pipeline_success', 'pipeline_failure', 'alert'
    is_read = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
''',
    'app/api_management/models.py': '''from app.extensions import db
from app.models.base import BaseModel
import secrets

class APIKey(BaseModel):
    __tablename__ = 'api_keys'
    
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    key_hash = db.Column(db.String(255), nullable=False, unique=True)
    prefix = db.Column(db.String(10), nullable=False) # Store first few chars for display
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    @staticmethod
    def generate_key():
        raw_key = secrets.token_urlsafe(32)
        return raw_key, f"df_{raw_key[:6]}"
''',
    'app/api_management/services.py': '''from app.extensions import db
from app.api_management.models import APIKey
import hashlib

class APIKeyService:
    @staticmethod
    def create_api_key(name, org_id, expires_at=None):
        raw_key, prefix = APIKey.generate_key()
        
        # Hash the key for storage
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        api_key = APIKey(
            org_id=org_id,
            name=name,
            key_hash=key_hash,
            prefix=prefix,
            expires_at=expires_at
        )
        
        db.session.add(api_key)
        db.session.commit()
        
        # We only return the raw key once upon creation
        return api_key, raw_key

    @staticmethod
    def verify_key(raw_key):
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        return APIKey.query.filter_by(key_hash=key_hash, is_active=True).first()
'''
}

# Update app/__init__.py to import sockets so they register with socketio
init_file = os.path.join(base_dir, 'app/__init__.py')
with open(init_file, 'r', encoding='utf-8') as f:
    init_content = f.read()

if 'import app.monitoring.sockets' not in init_content:
    init_content = init_content.replace(
        "return app",
        "    # Import socket events\n    import app.monitoring.sockets\n\n    return app"
    )
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)


for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Transformation, Monitoring, Notifications, and API Management modules generated.')
