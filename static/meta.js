// This JavaScript file can be used for additional interactive features on the page
// Example: form validation, dynamic changes, etc. In this case, it's not necessary
// but can be extended later if you wish to add more features.

// Example of a simple input validation for the client username field:
document.querySelector("form").addEventListener("submit", function(event) {
    const clientUsername = document.getElementById("client_username").value.trim();

    if (clientUsername === "") {
        alert("Please enter a valid client username.");
        event.preventDefault();
    }
});
