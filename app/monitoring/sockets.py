from flask_socketio import emit, join_room, leave_room
from flask import request
from app.extensions import socketio
from app.monitoring.telemetry import TelemetryService
import logging
import time

logger = logging.getLogger(__name__)

# Global background thread to avoid launching multiple
bg_thread = None

def telemetry_background_task():
    """
    Background task that emits telemetry data to all connected clients every 2 seconds.
    """
    while True:
        socketio.sleep(2)
        metrics = TelemetryService.get_system_metrics()
        socketio.emit('telemetry_update', metrics)

@socketio.on('connect')
def handle_connect():
    global bg_thread
    logger.info(f"Client connected: {request.sid}")
    
    # Start the telemetry broadcaster if it's not running
    if bg_thread is None:
        bg_thread = socketio.start_background_task(telemetry_background_task)
        
    emit('system_status', {'status': 'connected', 'message': 'Welcome to DataFlow Nexus Real-Time Engine'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('subscribe_pipeline')
def handle_subscribe_pipeline(data):
    pipeline_id = data.get('pipeline_id')
    if pipeline_id:
        join_room(f"pipeline_{pipeline_id}")
        emit('subscription_success', {'pipeline_id': pipeline_id})

@socketio.on('unsubscribe_pipeline')
def handle_unsubscribe_pipeline(data):
    pipeline_id = data.get('pipeline_id')
    if pipeline_id:
        leave_room(f"pipeline_{pipeline_id}")
