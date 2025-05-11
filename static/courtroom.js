document.getElementById('submit-argument').addEventListener('click', async () => {
    const argument = document.getElementById('lawyer-argument').value;
    const caseId = "{{ case['id'] }}";

    const response = await fetch('/submit_argument', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ argument, case_id: caseId })
    });

    const data = await response.json();

    // Update the page with AI response, rating, and verdict
    document.getElementById('judge-response-text').textContent = data.ai_response;
    document.getElementById('case-rating').textContent = `Rating: ${data.rating}/10`;
    document.getElementById('case-verdict').textContent = `Verdict: ${data.verdict}`;
});
document.getElementById('back-button').addEventListener('click', () => {
    window.location.href = 'index.html';
});