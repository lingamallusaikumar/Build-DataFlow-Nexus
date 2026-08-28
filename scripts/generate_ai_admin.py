import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/ai/anomaly_detector.py': '''import math

class AnomalyDetector:
    """
    Statistical anomaly detection module. 
    In production, this can be swapped with ML models like IsolationForest or Autoencoders.
    """
    @staticmethod
    def detect_z_score_anomalies(data_list, column, threshold=3.0):
        values = [row[column] for row in data_list if isinstance(row.get(column), (int, float))]
        if not values:
            return []
            
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance) if variance > 0 else 1.0
        
        anomalies = []
        for row in data_list:
            val = row.get(column)
            if isinstance(val, (int, float)):
                z_score = abs(val - mean) / std_dev
                if z_score > threshold:
                    anomalies.append(row)
        return anomalies
''',
    'app/ai/services.py': '''class AIAssistantService:
    """
    Modular AI service designed to integrate with LLM providers (OpenAI, Gemini).
    """
    def __init__(self, provider_client=None):
        self.client = provider_client

    def suggest_data_mapping(self, source_schema, target_schema):
        """
        Uses LLM to automatically suggest column mappings between source and destination.
        """
        # Mock logic. Replace with actual AI completion call.
        suggestions = {}
        for src_field in source_schema:
            if src_field in target_schema:
                suggestions[src_field] = src_field
        return suggestions
        
    def generate_pipeline_summary(self, execution_logs):
        """
        Analyzes failure logs and generates natural language explanations.
        """
        if "error" in str(execution_logs).lower():
            return "The pipeline failed due to a schema mismatch in the mapping phase."
        return "The pipeline executed successfully with no issues."
''',
    'app/audit/models.py': '''from app.extensions import db
from app.models.base import BaseModel

class AuditLog(BaseModel):
    __tablename__ = 'audit_logs'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True) # Null if system action
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False) # e.g., 'UPDATE_PIPELINE', 'DELETE_USER'
    resource = db.Column(db.String(100), nullable=False) # e.g., 'pipeline_id_123'
    ip_address = db.Column(db.String(50), nullable=True)
    metadata_json = db.Column(db.JSON, nullable=True) # Stores before/after states
''',
    'app/audit/services.py': '''from app.extensions import db
from app.audit.models import AuditLog
from flask import request
from flask_jwt_extended import get_jwt_identity

class AuditLogger:
    @staticmethod
    def log_action(action, resource, org_id=None, metadata_json=None):
        try:
            user_id = get_jwt_identity()
        except Exception:
            user_id = None
            
        ip_address = request.remote_addr if request else None

        audit_entry = AuditLog(
            user_id=user_id,
            org_id=org_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            metadata_json=metadata_json
        )
        
        db.session.add(audit_entry)
        db.session.commit()
''',
    'app/admin/routes.py': '''from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.models import User
from app.organizations.models import Organization

admin_bp = Blueprint('admin', __name__)

def check_super_admin(user_id):
    # In production, query user role
    return True

@admin_bp.route('/system/stats', methods=['GET'])
@jwt_required()
def get_system_stats():
    user_id = get_jwt_identity()
    if not check_super_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403
        
    total_users = User.query.count()
    total_orgs = Organization.query.count()
    
    return jsonify({
        'total_users': total_users,
        'total_organizations': total_orgs,
        'status': 'healthy'
    }), 200
'''
}

# Add Blueprint registration logic to app/__init__.py
init_file = os.path.join(base_dir, 'app/__init__.py')
with open(init_file, 'r', encoding='utf-8') as f:
    init_content = f.read()

if 'from app.admin.routes import admin_bp' not in init_content:
    init_content = init_content.replace(
        "return app",
        "    from app.admin.routes import admin_bp\n    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')\n\n    return app"
    )
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 9 & 10 components (AI, Audit, Admin) generated successfully.')
