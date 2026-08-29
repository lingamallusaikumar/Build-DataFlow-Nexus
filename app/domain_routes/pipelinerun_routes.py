from flask import Blueprint, request, jsonify
from app.domain_services.pipelinerun_service import PipelineRunService

pipelinerun_bp = Blueprint('pipelinerun_api', __name__, url_prefix='/api/v2/pipelineruns')

@pipelinerun_bp.route('/', methods=['GET'])
def list_records():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 100))
    records = PipelineRunService.get_all(skip=skip, limit=limit)
    return jsonify([r.to_dict() for r in records]), 200

@pipelinerun_bp.route('/<record_id>', methods=['GET'])
def get_record(record_id):
    try:
        record = PipelineRunService.get_by_id(record_id)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@pipelinerun_bp.route('/', methods=['POST'])
def create_record():
    try:
        record = PipelineRunService.create(request.json)
        return jsonify(record.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@pipelinerun_bp.route('/<record_id>', methods=['PUT'])
def update_record(record_id):
    try:
        record = PipelineRunService.update(record_id, request.json)
        return jsonify(record.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@pipelinerun_bp.route('/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        PipelineRunService.delete(record_id)
        return jsonify({'status': 'deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
