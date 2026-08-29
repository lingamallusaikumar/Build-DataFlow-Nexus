document.addEventListener('DOMContentLoaded', () => {
    const testBtn = document.getElementById('dq-test-btn');
    const inputArea = document.getElementById('dq-input');
    const resultsDiv = document.getElementById('dq-results');
    const outputArea = document.getElementById('dq-output');

    if (testBtn) {
        testBtn.addEventListener('click', async () => {
            const rawData = inputArea.value;
            if (!rawData) {
                alert("Please enter some data to test.");
                return;
            }

            // Split by comma and trim
            const dataArray = rawData.split(',').map(s => s.trim()).filter(s => s.length > 0);
            
            outputArea.innerText = "Running AI Models...";
            resultsDiv.style.display = "block";

            try {
                const response = await fetch('/api/v1/admin/test-data-quality', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ payload: dataArray })
                });

                if (response.ok) {
                    const resultData = await response.json();
                    outputArea.innerText = JSON.stringify(resultData, null, 2);
                } else {
                    const err = await response.json();
                    outputArea.innerText = "Error: " + JSON.stringify(err);
                }
            } catch (error) {
                outputArea.innerText = "Network Error: " + error;
            }
        });
    }
});
