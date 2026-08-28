from flask import Blueprint, jsonify
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
