// Parallax Code
var scene = document.getElementById('scene');
var parallax = new Parallax(scene);

// Disclaimer Popup Code
window.onload = function () {
    var disclaimerPopup = document.getElementById('disclaimer-popup');
    var agreeCheckbox = document.getElementById('agree-checkbox');
    var okButton = document.getElementById('ok-button');

    // Show the disclaimer popup when the page loads
    disclaimerPopup.style.display = 'block';

    // Handle OK button click
    okButton.onclick = function () {
        if (agreeCheckbox.checked) {
            disclaimerPopup.style.display = 'none'; // Hide the popup
            localStorage.setItem('disclaimerAgreed', 'true'); // Store agreement in localStorage
        } else {
            alert("Please agree to the terms and conditions.");
        }
    };

    // Check if the user has already agreed to the disclaimer
    if (localStorage.getItem('disclaimerAgreed') === 'true') {
        disclaimerPopup.style.display = 'none'; // Hide the popup if agreed
    }
};
