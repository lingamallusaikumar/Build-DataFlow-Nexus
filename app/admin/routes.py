from flask import Blueprint, jsonify
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
