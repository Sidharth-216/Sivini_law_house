function validatePassword() {
    const newPassword = document.getElementById("new_password").value;
    const confirmPassword = document.getElementById("confirm_password").value;
    const errorMessage = document.getElementById("error-message");

    if (newPassword !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match!";
        return false;
    }
    return true;
}
