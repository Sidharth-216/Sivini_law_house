// Validation for Forgot Password Form
function validateForm() {
    var username = document.getElementById("username").value;
    var phone = document.getElementById("phone").value;

    if (username.trim() === "" || phone.trim() === "") {
        alert("Please fill in all fields.");
        return false;
    }

    if (!phone.match(/^\+?[0-9]{10,15}$/)) {
        alert("Please enter a valid WhatsApp number.");
        return false;
    }

    return true;
}

// Validation for Reset Password Form
function validateResetForm() {
    var password = document.getElementById("new_password").value;
    var confirmPassword = document.getElementById("confirm_password").value;

    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return false;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }

    return true;
}
