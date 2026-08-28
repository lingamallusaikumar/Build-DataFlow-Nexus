from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
@frontend_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@frontend_bp.route('/pipelines')
def pipelines():
    return render_template('pipeline_builder.html')

@frontend_bp.route('/connectors')
def connectors():
    return render_template('connectors.html')

@frontend_bp.route('/data-quality')
def data_quality():
    return render_template('data_quality.html')

@frontend_bp.route('/settings')
def settings():
    return render_template('settings.html')

from flask import request, jsonify
from app.ai.data_classifier import PIIClassifier

@frontend_bp.route('/api/v1/admin/test-data-quality', methods=['POST'])
def test_data_quality():
    data = request.json.get('payload', [])
    tags = PIIClassifier.classify_column(data)
    
    return jsonify({
        'status': 'success',
        'data_analyzed': data,
        'detected_pii_tags': tags if tags else ['SAFE_NO_PII']
    }), 200
