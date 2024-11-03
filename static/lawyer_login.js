document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (email && password) {
        alert("Login successful!");
        // Redirect to the lawyer dashboard or perform further login validation here.
    } else {
        alert("Please enter your email and password.");
    }
});
