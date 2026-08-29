from flask import Blueprint, request, jsonify
from app.domain_services.connector_service import ConnectorService

connector_bp = Blueprint('connector_api', __name__, url_prefix='/api/v2/connectors')

@connector_bp.route('/', methods=['GET'])
def list_records():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 100))
    records = ConnectorService.get_all(skip=skip, limit=limit)
    return jsonify([r.to_dict() for r in records]), 200

@connector_bp.route('/<record_id>', methods=['GET'])
def get_record(record_id):
    try:
        record = ConnectorService.get_by_id(record_id)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@connector_bp.route('/', methods=['POST'])
def create_record():
    try:
        record = ConnectorService.create(request.json)
        return jsonify(record.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@connector_bp.route('/<record_id>', methods=['PUT'])
def update_record(record_id):
    try:
        record = ConnectorService.update(record_id, request.json)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@connector_bp.route('/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        ConnectorService.delete(record_id)
        return jsonify({'status': 'deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
