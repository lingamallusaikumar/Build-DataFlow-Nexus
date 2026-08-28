import os

base_dir = r'c:\Users\saiku\OneDrive\Desktop\ELEVATEIQ\datapipeline\dataflow_nexus'

files = {
    'app/static/css/style.css': '''
:root {
    --primary-color: #2563eb;
    --secondary-color: #475569;
    --bg-color: #f8fafc;
    --text-color: #0f172a;
    --border-color: #e2e8f0;
}

body {
    font-family: 'Inter', -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    padding: 0;
}

.dashboard-container {
    display: flex;
    height: 100vh;
}

.sidebar {
    width: 250px;
    background-color: #1e293b;
    color: white;
    padding: 20px 0;
    display: flex;
    flex-direction: column;
}

.sidebar-logo {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    padding-bottom: 20px;
    border-bottom: 1px solid #334155;
    margin-bottom: 20px;
}

.nav-item {
    padding: 15px 25px;
    color: #cbd5e1;
    text-decoration: none;
    transition: 0.3s;
}

.nav-item:hover, .nav-item.active {
    background-color: #334155;
    color: white;
}

.main-content {
    flex: 1;
    overflow-y: auto;
    padding: 30px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border-color);
}

.card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

/* Pipeline Builder Styles */
#pipeline-canvas {
    width: 100%;
    height: 600px;
    background-color: #f1f5f9;
    border: 2px dashed #cbd5e1;
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}

.node {
    width: 150px;
    padding: 15px;
    background: white;
    border: 2px solid var(--primary-color);
    border-radius: 6px;
    position: absolute;
    cursor: grab;
    text-align: center;
    font-weight: 500;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
''',
    'app/static/js/sockets.js': '''
document.addEventListener('DOMContentLoaded', () => {
    // Connect to WebSockets
    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to DataFlow Nexus Real-Time Engine');
        const statusDot = document.getElementById('socket-status');
        if(statusDot) {
            statusDot.style.color = 'green';
            statusDot.title = 'Real-time Connected';
        }
    });

    socket.on('system_status', (data) => {
        console.log('System Status:', data);
    });
});
''',
    'app/static/js/pipeline_builder.js': '''
// Basic Pipeline Builder Logic (Simulating a visual DAG builder)
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('pipeline-canvas');
    if(!canvas) return;

    let nodeCount = 0;

    window.addNode = function(type) {
        nodeCount++;
        const node = document.createElement('div');
        node.className = 'node';
        node.innerText = `${type} Node ${nodeCount}`;
        node.style.left = `${50 + (nodeCount * 20)}px`;
        node.style.top = `${50 + (nodeCount * 20)}px`;
        
        // Simple drag functionality
        node.onmousedown = function(event) {
            let shiftX = event.clientX - node.getBoundingClientRect().left;
            let shiftY = event.clientY - node.getBoundingClientRect().top;

            function moveAt(pageX, pageY) {
                node.style.left = pageX - shiftX - canvas.getBoundingClientRect().left + 'px';
                node.style.top = pageY - shiftY - canvas.getBoundingClientRect().top + 'px';
            }

            function onMouseMove(event) {
                moveAt(event.pageX, event.pageY);
            }

            document.addEventListener('mousemove', onMouseMove);

            node.onmouseup = function() {
                document.removeEventListener('mousemove', onMouseMove);
                node.onmouseup = null;
            };
        };

        node.ondragstart = function() {
            return false;
        };

        canvas.appendChild(node);
    };
});
''',
    'app/templates/base.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataFlow Nexus</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body>
    <div class="dashboard-container">
        <nav class="sidebar">
            <div class="sidebar-logo">DataFlow Nexus</div>
            <a href="/dashboard" class="nav-item">Dashboard</a>
            <a href="/pipelines" class="nav-item">Pipelines</a>
            <a href="/connectors" class="nav-item">Connectors</a>
            <a href="/data-quality" class="nav-item">Data Quality</a>
            <a href="/settings" class="nav-item">Settings</a>
        </nav>
        
        <main class="main-content">
            <header class="topbar">
                <h2>{% block header %}{% endblock %}</h2>
                <div>
                    <span id="socket-status" style="color: red; font-size: 24px;">&#9679;</span>
                    <button class="btn">Logout</button>
                </div>
            </header>
            
            <div class="content">
                {% block content %}{% endblock %}
            </div>
        </main>
    </div>

    <script src="{{ url_for('static', filename='js/sockets.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
''',
    'app/templates/dashboard.html': '''{% extends "base.html" %}

{% block header %}Overview Dashboard{% endblock %}

{% block content %}
<div class="grid-3">
    <div class="card">
        <h3>Active Pipelines</h3>
        <h1 style="font-size: 3rem; color: var(--primary-color);">12</h1>
    </div>
    <div class="card">
        <h3>Records Processed (24h)</h3>
        <h1 style="font-size: 3rem; color: #10b981;">2.4M</h1>
    </div>
    <div class="card">
        <h3>Failed Events</h3>
        <h1 style="font-size: 3rem; color: #ef4444;">14</h1>
    </div>
</div>

<div class="card">
    <h3>System Health & Analytics</h3>
    <p>Real-time metrics streaming via WebSockets...</p>
    <div style="height: 200px; background: #f8fafc; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: center;">
        [ Chart Placeholder ]
    </div>
</div>
{% endblock %}
''',
    'app/templates/pipeline_builder.html': '''{% extends "base.html" %}

{% block header %}Visual Pipeline Builder{% endblock %}

{% block content %}
<div class="card" style="margin-bottom: 15px;">
    <button onclick="addNode('Source')" style="padding: 8px 15px; cursor: pointer;">+ Add Source</button>
    <button onclick="addNode('Transform')" style="padding: 8px 15px; cursor: pointer;">+ Add Transform</button>
    <button onclick="addNode('Destination')" style="padding: 8px 15px; cursor: pointer;">+ Add Destination</button>
    <button onclick="addNode('AI Model')" style="padding: 8px 15px; cursor: pointer;">+ Add AI/ML</button>
    
    <button style="padding: 8px 15px; cursor: pointer; float: right; background: var(--primary-color); color: white; border: none; border-radius: 4px;">Save Pipeline</button>
</div>

<div id="pipeline-canvas">
    <!-- Nodes will be injected here via JS -->
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/pipeline_builder.js') }}"></script>
{% endblock %}
''',
    'app/frontend_routes.py': '''from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
@frontend_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@frontend_bp.route('/pipelines')
def pipelines():
    return render_template('pipeline_builder.html')
'''
}

# Add frontend Blueprint to app/__init__.py
init_file = os.path.join(base_dir, 'app/__init__.py')
with open(init_file, 'r', encoding='utf-8') as f:
    init_content = f.read()

if 'from app.frontend_routes import frontend_bp' not in init_content:
    init_content = init_content.replace(
        "    from app.admin.routes import admin_bp",
        "    from app.frontend_routes import frontend_bp\n    app.register_blueprint(frontend_bp)\n\n    from app.admin.routes import admin_bp"
    )
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Frontend UI templates and static assets generated.')
