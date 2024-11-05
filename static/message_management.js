// message_management.js

document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.querySelector('.messages-container');
    const sendButton = document.querySelector('#sendButton');
    const chatInput = document.querySelector('.chat-input input');

    const senderId = "lawyer_id"; // Replace with actual lawyer ID
    const receiverId = "client_id"; // Replace with actual client ID

    // Function to fetch messages
    async function fetchMessages() {
        const response = await fetch(`/messages?sender_id=${senderId}&receiver_id=${receiverId}`);
        const messages = await response.json();

        messagesContainer.innerHTML = ''; // Clear the container before adding messages
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = 'message';
            messageElement.innerHTML = `
                <div class="message-header">
                    <h4>${message.sender === 'lawyer' ? 'You' : 'Client'}</h4>
                    <small>${message.time}</small>
                </div>
                <p>${message.text}</p>
            `;
            messagesContainer.appendChild(messageElement);
        });

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
                chatInput.value = ''; // Clear input after sending
                fetchMessages(); // Refresh messages after sending
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

    // Initial fetch of messages
    fetchMessages();
});
