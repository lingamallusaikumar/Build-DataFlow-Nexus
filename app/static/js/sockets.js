
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
