// Parallax Code
// User Login Display Code
window.onload = function () {
    var username = localStorage.getItem('username');
    var loginDisplay = document.getElementById('login-display');
    var logoutButton = document.getElementById('logout-button');

    if (username) {
        loginDisplay.innerHTML = `Welcome, ${username} <button id="logout-button">Logout</button>`;
        logoutButton = document.getElementById('logout-button');
        logoutButton.onclick = function () {
            localStorage.removeItem('username');
            location.reload();
        };
    }

    // Existing disclaimer popup code
    var disclaimerPopup = document.getElementById('disclaimer-popup');
    var agreeCheckbox = document.getElementById('agree-checkbox');
    var okButton = document.getElementById('ok-button');

    disclaimerPopup.style.display = 'block';

    okButton.onclick = function () {
        if (agreeCheckbox.checked) {
            disclaimerPopup.style.display = 'none';
            localStorage.setItem('disclaimerAgreed', 'true');
        } else {
            alert("Please agree to the terms and conditions.");
        }
    };

    if (localStorage.getItem('disclaimerAgreed') === 'true') {
        disclaimerPopup.style.display = 'none';
    }
};
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

// Smooth scrolling for anchor links in footer
document.querySelectorAll('.footer a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

