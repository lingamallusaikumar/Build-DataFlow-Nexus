from app.extensions import db
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
