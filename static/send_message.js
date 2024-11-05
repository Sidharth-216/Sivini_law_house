// send_message.js

document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.querySelector('.messages-container');
    const sendButton = document.querySelector('#sendMessageButton');
    const chatInput = document.querySelector('#messageInput');

    const senderId = "client_id"; // Replace with actual client ID
    const receiverId = "lawyer_id"; // Replace with actual lawyer ID

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

    // Function to send a new message
    async function sendMessage() {
        const messageText = chatInput.value.trim();
        if (messageText) {
            const messageData = {
                sender_id: senderId,
                receiver_id: receiverId,
                message: messageText
            };

            const response = await fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(messageData)
            });

            if (response.ok) {
                appendMessage(messageText); // Append message to chat
            } else {
                console.error('Failed to send message');
            }
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
