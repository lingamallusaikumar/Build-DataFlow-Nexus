from flask_socketio import emit, join_room, leave_room
from flask import request
from app.extensions import socketio
import logging

logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    # In production, validate JWT token from request.args before allowing connection
    logger.info(f"Client connected: {request.sid}")
    emit('system_status', {'status': 'connected', 'message': 'Welcome to DataFlow Nexus Real-Time Engine'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('subscribe_pipeline')
def handle_subscribe_pipeline(data):
    """
    Allows a client to subscribe to real-time events for a specific pipeline execution.
    """
    pipeline_id = data.get('pipeline_id')
    if pipeline_id:
        join_room(f"pipeline_{pipeline_id}")
        logger.info(f"Client {request.sid} subscribed to pipeline {pipeline_id}")
        emit('subscription_success', {'pipeline_id': pipeline_id})

@socketio.on('unsubscribe_pipeline')
def handle_unsubscribe_pipeline(data):
    pipeline_id = data.get('pipeline_id')
    if pipeline_id:
        leave_room(f"pipeline_{pipeline_id}")
        logger.info(f"Client {request.sid} unsubscribed from pipeline {pipeline_id}")
