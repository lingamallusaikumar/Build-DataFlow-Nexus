from flask import Blueprint, request, jsonify
from app.domain_services.role_service import RoleService

role_bp = Blueprint('role_api', __name__, url_prefix='/api/v2/roles')

@role_bp.route('/', methods=['GET'])
def list_records():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 100))
    records = RoleService.get_all(skip=skip, limit=limit)
    return jsonify([r.to_dict() for r in records]), 200

@role_bp.route('/<record_id>', methods=['GET'])
def get_record(record_id):
    try:
        record = RoleService.get_by_id(record_id)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@role_bp.route('/', methods=['POST'])
def create_record():
    try:
        record = RoleService.create(request.json)
        return jsonify(record.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@role_bp.route('/<record_id>', methods=['PUT'])
def update_record(record_id):
    try:
        record = RoleService.update(record_id, request.json)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@role_bp.route('/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        RoleService.delete(record_id)
        return jsonify({'status': 'deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
