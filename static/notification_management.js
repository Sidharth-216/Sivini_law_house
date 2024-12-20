document.querySelectorAll('.notification form').forEach(form => {
    form.addEventListener('submit', event => {
        event.preventDefault(); // Prevent the form from submitting traditionally
        const url = form.action;

        fetch(url, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const notificationElement = form.closest('.notification');
                notificationElement.classList.remove('unseen');
                notificationElement.classList.add('seen');
                form.remove(); // Remove the form after marking as read
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
document.querySelectorAll('.notification form button[type="submit"]').forEach(button => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const form = event.target.closest('form');
        const response = await fetch(form.action, { method: form.method });

        if (response.ok) {
            // Mark notification as seen visually
            form.closest('.notification').classList.add('seen');
            form.remove();  // Remove the "Mark as Read" button
        } else {
            console.error('Failed to mark notification as read.');
        }
    });
});
document.querySelectorAll('.notification form button.delete-button').forEach(button => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const form = event.target.closest('form');
        const response = await fetch(form.action, { method: form.method });

        if (response.ok) {
            // Remove the notification from the UI once deleted
            form.closest('.notification').remove();
        } else {
            console.error('Failed to delete notification.');
        }
    });
});
