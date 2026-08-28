
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
