from flask import Blueprint, request, jsonify
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
