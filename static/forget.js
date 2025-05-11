document.addEventListener("DOMContentLoaded", function () {
    const forgotForm = document.getElementById("forgotPasswordForm");

    forgotForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form from auto-submitting

        // Get input values
        const username = document.getElementById("username").value.trim();
        const phone = document.getElementById("phone").value.trim();

        // Validate inputs
        if (username === "" || phone === "") {
            alert("Please fill in all fields.");
            return;
        }

        // WhatsApp number validation (basic format check)
        const phonePattern = /^\+?[0-9]{10,15}$/; // Accepts numbers with optional "+"
        if (!phone.match(phonePattern)) {
            alert("Please enter a valid WhatsApp number (e.g., +91XXXXXXXXXX).");
            return;
        }

        // Simulate sending reset request
        alert(`Reset link will be sent to ${phone} via WhatsApp.`);

        // Here, you would normally send data to the backend (Flask) using fetch()
        // Example:
        /*
        fetch("/forgot-password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, phone })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Error:", error));
        */
        
        forgotForm.reset(); // Clear form fields
    });
});
