// messages.js

document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.querySelector('.chat-input input');
    const sendButton = document.querySelector('.chat-input button');
    const messagesContainer = document.querySelector('.messages-container');

    // Function to append a new message to the chat
    function appendMessage(text) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `
            <div class="message-header">
                <h4>You</h4>
                <small>${new Date().toLocaleTimeString()}</small>
            </div>
            <p>${text}</p>
        `;
        messagesContainer.appendChild(messageElement);
        chatInput.value = '';
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll to the bottom
    }

    sendButton.addEventListener('click', function() {
        const messageText = chatInput.value.trim();
        if (messageText) {
            appendMessage(messageText);
        }
    });

    // Handle pressing Enter key to send message
    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
});
