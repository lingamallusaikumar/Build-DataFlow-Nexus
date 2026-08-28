import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/monitoring/telemetry.py': '''import psutil
import random

class TelemetryService:
    """
    Gathers system and pipeline metrics for real-time monitoring.
    """
    @staticmethod
    def get_system_metrics():
        # CPU and Memory using psutil
        cpu_usage = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        
        # Simulated pipeline metrics (In production, query Redis State Manager)
        active_pipelines = random.randint(10, 15)
        records_per_sec = random.randint(500, 2000)
        
        return {
            'cpu_percent': cpu_usage,
            'memory_percent': memory.percent,
            'memory_used_gb': round(memory.used / (1024**3), 2),
            'active_pipelines': active_pipelines,
            'records_per_second': records_per_sec
        }
''',
    'app/monitoring/sockets.py': '''from flask_socketio import emit, join_room, leave_room
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
''',
    'app/static/js/sockets.js': '''
document.addEventListener('DOMContentLoaded', () => {
    // Connect to WebSockets
    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to DataFlow Nexus Real-Time Engine');
        const statusDot = document.getElementById('socket-status');
        if(statusDot) {
            statusDot.style.color = '#10b981'; // Green
            statusDot.title = 'Real-time Connected';
        }
    });

    socket.on('disconnect', () => {
        const statusDot = document.getElementById('socket-status');
        if(statusDot) {
            statusDot.style.color = '#ef4444'; // Red
            statusDot.title = 'Disconnected';
        }
    });

    socket.on('system_status', (data) => {
        console.log('System Status:', data);
    });

    // Handle incoming telemetry broadcasts
    socket.on('telemetry_update', (metrics) => {
        // Update DOM elements if they exist on the current page
        const cpuEl = document.getElementById('metric-cpu');
        const ramEl = document.getElementById('metric-ram');
        const activePipelinesEl = document.getElementById('metric-pipelines');
        const rpsEl = document.getElementById('metric-rps');

        if(cpuEl) cpuEl.innerText = metrics.cpu_percent.toFixed(1) + '%';
        if(ramEl) ramEl.innerText = metrics.memory_percent.toFixed(1) + '% (' + metrics.memory_used_gb + ' GB)';
        if(activePipelinesEl) activePipelinesEl.innerText = metrics.active_pipelines;
        if(rpsEl) rpsEl.innerText = metrics.records_per_second;
        
        // Dynamic color changes for high CPU
        if(cpuEl) {
            if(metrics.cpu_percent > 85) cpuEl.style.color = '#ef4444'; // Red
            else if(metrics.cpu_percent > 60) cpuEl.style.color = '#f59e0b'; // Yellow
            else cpuEl.style.color = '#10b981'; // Green
        }
    });
});
''',
    'app/templates/dashboard.html': '''{% extends "base.html" %}

{% block header %}Overview Dashboard{% endblock %}

{% block content %}
<div class="grid-3">
    <div class="card">
        <h3>Active Pipelines</h3>
        <h1 id="metric-pipelines" style="font-size: 3rem; color: var(--primary-color);">Loading...</h1>
    </div>
    <div class="card">
        <h3>Records / Second</h3>
        <h1 id="metric-rps" style="font-size: 3rem; color: #10b981;">Loading...</h1>
    </div>
    <div class="card">
        <h3>Failed Events (24h)</h3>
        <h1 style="font-size: 3rem; color: #ef4444;">14</h1>
    </div>
</div>

<div class="grid-3" style="margin-top: 20px;">
    <div class="card">
        <h3>Server CPU Usage</h3>
        <h1 id="metric-cpu" style="font-size: 2.5rem; transition: color 0.3s;">--%</h1>
    </div>
    <div class="card">
        <h3>Server RAM Usage</h3>
        <h1 id="metric-ram" style="font-size: 2.5rem;">--%</h1>
    </div>
    <div class="card">
        <h3>System Health</h3>
        <p style="margin-top: 15px; font-size: 1.1rem;">All Systems Operational. Telemetry stream is active.</p>
    </div>
</div>
{% endblock %}
'''
}

# Add psutil to requirements
requirements_path = os.path.join(base_dir, 'requirements.txt')
if os.path.exists(requirements_path):
    with open(requirements_path, 'a', encoding='utf-8') as req_file:
        req_file.write("psutil==5.9.6\n")

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 7 Deep Dive components generated successfully.')
