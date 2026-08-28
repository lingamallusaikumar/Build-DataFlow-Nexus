from flask import Blueprint, request, jsonify
from app.domain_services.dagnode_service import DagNodeService

dagnode_bp = Blueprint('dagnode_api', __name__, url_prefix='/api/v2/dagnodes')

@dagnode_bp.route('/', methods=['GET'])
def list_records():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 100))
    records = DagNodeService.get_all(skip=skip, limit=limit)
    return jsonify([r.to_dict() for r in records]), 200

@dagnode_bp.route('/<record_id>', methods=['GET'])
def get_record(record_id):
    try:
        record = DagNodeService.get_by_id(record_id)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@dagnode_bp.route('/', methods=['POST'])
def create_record():
    try:
        record = DagNodeService.create(request.json)
        return jsonify(record.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@dagnode_bp.route('/<record_id>', methods=['PUT'])
def update_record(record_id):
    try:
        record = DagNodeService.update(record_id, request.json)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@dagnode_bp.route('/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        DagNodeService.delete(record_id)
        return jsonify({'status': 'deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
