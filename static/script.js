document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('planner-form');
    const submitBtn = document.getElementById('submit-btn');
    const resetBtn = document.getElementById('reset-btn');
    const statusMessage = document.getElementById('status-message');
    const resultContainer = document.getElementById('result-container');
    const agentOutput = document.getElementById('agent-output');

    const subjectsContainer = document.getElementById('subjects-container');
    const addSubjectBtn = document.getElementById('add-subject-btn');

    // Add initial subject row
    addSubjectRow();

    // Adding Subject Rows
    addSubjectBtn.addEventListener('click', () => {
        addSubjectRow();
    });

    function addSubjectRow() {
        const row = document.createElement('div');
        row.className = 'subject-row';
        row.innerHTML = `
            <input type="text" class="sub-name" placeholder="Subject Name" required>
            <input type="number" class="sub-total" min="1" placeholder="Total Chps" required>
            <input type="number" class="sub-left" min="0" placeholder="Chps Left" required>
            <button type="button" class="remove-btn" title="Remove">&times;</button>
        `;

        // Remove functionality
        row.querySelector('.remove-btn').addEventListener('click', () => {
            if (subjectsContainer.children.length > 1) {
                row.remove();
            } else {
                alert("You need at least one subject.");
            }
        });

        subjectsContainer.appendChild(row);
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Gather all subjects
        const subjectRows = document.querySelectorAll('.subject-row');
        const subjects = [];
        subjectRows.forEach(row => {
            subjects.push({
                name: row.querySelector('.sub-name').value,
                total: parseInt(row.querySelector('.sub-total').value),
                left: parseInt(row.querySelector('.sub-left').value)
            });
        });

        const days = document.getElementById('days').value;
        const hours = document.getElementById('hours').value;

        // UI State: Loading
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        statusMessage.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        form.classList.add('hidden'); // Hide form for minimal layout
        agentOutput.innerHTML = '';

        try {
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ subjects, days, hours })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                let content = data.result;
                if (content.startsWith('```html')) {
                    content = content.replace(/```html/g, '').replace(/```/g, '').trim();
                }

                agentOutput.innerHTML = content;
                statusMessage.classList.add('hidden');
                resultContainer.classList.remove('hidden');

                // Adjust container size
                document.querySelector('.container').style.maxWidth = '800px';
            } else {
                throw new Error(data.error || 'Something went wrong.');
            }
        } catch (error) {
            agentOutput.innerHTML = `<div style="color: var(--danger); font-weight: 500;">Error: ${error.message}</div>`;
            statusMessage.classList.add('hidden');
            resultContainer.classList.remove('hidden');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });

    // Reset button
    resetBtn.addEventListener('click', () => {
        resultContainer.classList.add('hidden');
        form.classList.remove('hidden');
        document.querySelector('.container').style.maxWidth = '650px';

        // Clear old inputs
        subjectsContainer.innerHTML = '';
        addSubjectRow();
        document.getElementById('days').value = '';
        document.getElementById('hours').value = '';
    });
});
