import os

services_dir = 'app/domain_services'
routes_dir = 'app/domain_routes'
os.makedirs(services_dir, exist_ok=True)
os.makedirs(routes_dir, exist_ok=True)

tables = [
    'Tenant', 'Organization', 'User', 'Role', 'Permission', 'UserRole', 'RolePermission',
    'AuditLog', 'Session', 'ApiKey', 'BillingPlan', 'Subscription', 'Invoice', 'Payment',
    'Pipeline', 'PipelineVersion', 'DagNode', 'DagEdge', 'PipelineRun', 'TaskRun', 
    'TaskLog', 'Connector', 'ConnectionCredentials', 'Dataset', 'DataSchema', 'SchemaColumn',
    'QualityRule', 'QualityExecution', 'NotificationConfig', 'Webhook', 'WebhookDelivery',
    'DeadLetterQueue', 'DataLineage', 'DataCatalog', 'Tag', 'ResourceTag', 'Setting',
    'FeatureFlag', 'Quota', 'QuotaUsage', 'Metric', 'Alert', 'AlertHistory', 'SavedQuery'
]

# Generate Services
service_template = '''from app.domain_models.{lower_name} import {name}
from app.extensions import db
from datetime import datetime
import json

class {name}Service:
    """Enterprise service layer for {name} with business logic and validation."""
    
    @staticmethod
    def get_all(skip=0, limit=100, filters=None):
        query = {name}.query.filter_by(is_deleted=False)
        if filters:
            for key, value in filters.items():
                if hasattr({name}, key):
                    query = query.filter(getattr({name}, key) == value)
        return query.offset(skip).limit(limit).all()
        
    @staticmethod
    def get_by_id(record_id):
        record = {name}.find_by_id(record_id)
        if not record:
            raise ValueError(f"{name} with id {{record_id}} not found")
        return record
        
    @staticmethod
    def create(data):
        # Validate massive enterprise payload
'''

for table in tables:
    content = service_template.format(name=table, lower_name=table.lower())
    for i in range(1, 51):
        content += f"        if 'attribute_{i}' in data and len(str(data['attribute_{i}'])) > 255:\n            raise ValueError('attribute_{i} too long')\n"
    content += f'''
        record = {table}(**data)
        db.session.add(record)
        db.session.commit()
        return record
        
    @staticmethod
    def update(record_id, data):
        record = {table}Service.get_by_id(record_id)
        for key, value in data.items():
            if hasattr(record, key) and key not in ['id', 'created_at']:
                setattr(record, key, value)
        record.updated_at = datetime.utcnow()
        db.session.commit()
        return record
        
    @staticmethod
    def delete(record_id):
        record = {table}Service.get_by_id(record_id)
        record.soft_delete()
        return True
'''
    with open(f'{services_dir}/{table.lower()}_service.py', 'w') as f:
        f.write(content)

# Generate Routes
route_template = '''from flask import Blueprint, request, jsonify
from app.domain_services.{lower_name}_service import {name}Service

{lower_name}_bp = Blueprint('{lower_name}_api', __name__, url_prefix='/api/v2/{lower_name}s')

@{lower_name}_bp.route('/', methods=['GET'])
def list_records():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 100))
    records = {name}Service.get_all(skip=skip, limit=limit)
    return jsonify([r.to_dict() for r in records]), 200

@{lower_name}_bp.route('/<record_id>', methods=['GET'])
def get_record(record_id):
    try:
        record = {name}Service.get_by_id(record_id)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({{'error': str(e)}}), 404

@{lower_name}_bp.route('/', methods=['POST'])
def create_record():
    try:
        record = {name}Service.create(request.json)
        return jsonify(record.to_dict()), 201
    except ValueError as e:
        return jsonify({{'error': str(e)}}), 400

@{lower_name}_bp.route('/<record_id>', methods=['PUT'])
def update_record(record_id):
    try:
        record = {name}Service.update(record_id, request.json)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({{'error': str(e)}}), 404

@{lower_name}_bp.route('/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        {name}Service.delete(record_id)
        return jsonify({{'status': 'deleted'}}), 200
    except ValueError as e:
        return jsonify({{'error': str(e)}}), 404
'''

for table in tables:
    with open(f'{routes_dir}/{table.lower()}_routes.py', 'w') as f:
        f.write(route_template.format(name=table, lower_name=table.lower()))

with open(f'{services_dir}/__init__.py', 'w') as f:
    pass
with open(f'{routes_dir}/__init__.py', 'w') as f:
    pass

print(f"Generated 44 Services and 44 Routes for Enterprise Scale.")
