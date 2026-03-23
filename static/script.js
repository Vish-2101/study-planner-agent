document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('planner-form');
    const submitBtn = document.getElementById('submit-btn');
    const statusMessage = document.getElementById('status-message');
    const resultContainer = document.getElementById('result-container');
    const agentOutput = document.getElementById('agent-output');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get values
        const subjects = document.getElementById('subjects').value;
        const days = document.getElementById('days').value;
        const hours = document.getElementById('hours').value;

        // UI State: Loading
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        statusMessage.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        agentOutput.innerHTML = ''; // reset

        try {
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ subjects, days, hours })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Remove Markdown code block wrappers if present, safely handling HTML from the LLM
                let content = data.result;
                if (content.startsWith('```html')) {
                    content = content.replace(/```html/g, '').replace(/```/g, '').trim();
                }

                agentOutput.innerHTML = content;

                statusMessage.classList.add('hidden');
                resultContainer.classList.remove('hidden');

                // Adjust container size smoothly
                document.querySelector('.container').style.maxWidth = '800px';
            } else {
                throw new Error(data.error || 'Something went wrong.');
            }
        } catch (error) {
            agentOutput.innerHTML = `<div style="color: #ff7eb3; font-weight: bold;">Error: ${error.message}</div>`;
            statusMessage.classList.add('hidden');
            resultContainer.classList.remove('hidden');
        } finally {
            // Re-enable button
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });
});
