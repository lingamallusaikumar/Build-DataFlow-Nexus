
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
