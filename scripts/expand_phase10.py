import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/audit/diff_engine.py': '''class AuditDiffEngine:
    """
    Computes the exact changes between two JSON states to store in the Audit Log.
    """
    @staticmethod
    def calculate_diff(old_state: dict, new_state: dict) -> dict:
        diff = {
            'added': {},
            'removed': {},
            'modified': {}
        }
        
        old_keys = set(old_state.keys()) if old_state else set()
        new_keys = set(new_state.keys()) if new_state else set()
        
        # Added keys
        for key in new_keys - old_keys:
            diff['added'][key] = new_state[key]
            
        # Removed keys
        for key in old_keys - new_keys:
            diff['removed'][key] = old_state[key]
            
        # Modified keys
        for key in old_keys.intersection(new_keys):
            if old_state[key] != new_state[key]:
                diff['modified'][key] = {
                    'from': old_state[key],
                    'to': new_state[key]
                }
                
        return diff
''',
    'app/admin/health.py': '''from flask import Blueprint, jsonify
from app.extensions import db
from app.config.settings import config
import redis
import logging

logger = logging.getLogger(__name__)
health_bp = Blueprint('health', __name__)

@health_bp.route('/liveness', methods=['GET'])
def liveness_probe():
    """Kubernetes Liveness Probe: Checks if the application is running."""
    return jsonify({"status": "alive"}), 200

@health_bp.route('/readiness', methods=['GET'])
def readiness_probe():
    """Kubernetes Readiness Probe: Checks if the application can accept traffic (DB & Redis up)."""
    checks = {"database": "down", "redis": "down"}
    status_code = 503
    
    try:
        # Check Database
        db.session.execute('SELECT 1')
        checks['database'] = "up"
        
        # Check Redis
        redis_client = redis.from_url(config['default'].REDIS_URL)
        if redis_client.ping():
            checks['redis'] = "up"
            
        if checks['database'] == "up" and checks['redis'] == "up":
            status_code = 200
            
    except Exception as e:
        logger.error(f"Readiness probe failed: {e}")
        
    return jsonify({"status": "ready" if status_code == 200 else "unready", "checks": checks}), status_code
''',
    'app/common/error_handlers.py': '''from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """
    Registers global error handlers to prevent stack traces from leaking to the client.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized", "message": "Authentication required."}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden", "message": "You do not have permission to access this resource."}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal Server Error: {error}")
        return jsonify({
            "error": "Internal Server Error", 
            "message": "An unexpected error occurred. Please try again later."
        }), 500
''',
    'tests/test_admin_audit.py': '''from app.audit.diff_engine import AuditDiffEngine

def test_audit_diff_engine():
    old_state = {"name": "Test", "status": "active", "old_key": "exists"}
    new_state = {"name": "Test Modified", "status": "active", "new_key": "added"}
    
    diff = AuditDiffEngine.calculate_diff(old_state, new_state)
    
    assert "new_key" in diff['added']
    assert "old_key" in diff['removed']
    assert "name" in diff['modified']
    assert diff['modified']['name']['from'] == "Test"
    assert diff['modified']['name']['to'] == "Test Modified"
    
def test_liveness_probe(client):
    response = client.get('/health/liveness')
    assert response.status_code == 200
    assert response.json['status'] == 'alive'
'''
}

# Update app/__init__.py to register error handlers and health probes
init_file = os.path.join(base_dir, 'app/__init__.py')
with open(init_file, 'r', encoding='utf-8') as f:
    init_content = f.read()

if 'from app.common.error_handlers import register_error_handlers' not in init_content:
    init_content = init_content.replace(
        "    from app.admin.routes import admin_bp",
        "    from app.admin.routes import admin_bp\n    from app.admin.health import health_bp\n    app.register_blueprint(health_bp, url_prefix='/health')\n    \n    from app.common.error_handlers import register_error_handlers\n    register_error_handlers(app)\n"
    )
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 10 Deep Dive components generated successfully.')
