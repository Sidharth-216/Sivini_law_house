document.getElementById('registerForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const license = document.getElementById('license').value;
    const specialization = document.getElementById('specialization').value;
    const experience = document.getElementById('experience').value;

    if (name && email && password && license && specialization && experience) {
        alert("Registration successful!");
        // Further processing, such as sending data to a server, can be done here.
    } else {
        alert("Please fill in all fields.");
    }
});
