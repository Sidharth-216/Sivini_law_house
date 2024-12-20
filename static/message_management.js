// Fetch messages from the server
async function fetchMessages() {
    const response = await fetch('/get_messages');
    const messages = await response.json();
    const chatMessages = document.getElementById('chatMessages');

    chatMessages.innerHTML = '';
    messages.forEach(msg => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', msg.sender === 'client' ? 'client' : 'lawyer');
        messageDiv.innerHTML = `
            <div class="sender">${msg.sender}</div>
            <div class="content">${msg.content}</div>
        `;
        chatMessages.appendChild(messageDiv);
    });
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
}

// Send a new message
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (message) {
        await fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender: 'lawyer', content: message })
        });
        messageInput.value = '';
        fetchMessages(); // Refresh messages
    }
}

document.getElementById('sendMessageButton').addEventListener('click', sendMessage);

// Load messages on page load
fetchMessages();
setInterval(fetchMessages, 3000); // Refresh every 3 seconds
