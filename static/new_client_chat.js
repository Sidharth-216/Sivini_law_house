document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.querySelector(".chat-box");
    const form = document.querySelector("form");
    const input = form.querySelector("input[name='message']");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = input.value.trim();

        if (message) {
            // Display client message
            const messageDiv = document.createElement("div");
            messageDiv.classList.add("message", "client");
            messageDiv.textContent = message;
            chatBox.appendChild(messageDiv);

            // Scroll to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;

            // Clear input
            input.value = "";

            // Simulate lawyer response
            setTimeout(() => {
                const lawyerMessage = document.createElement("div");
                lawyerMessage.classList.add("message", "lawyer");
                lawyerMessage.textContent = "Thank you for your message. I'll respond shortly.";
                chatBox.appendChild(lawyerMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000);
        }
    });
});
