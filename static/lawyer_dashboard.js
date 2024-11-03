// Active link highlight in the sidebar
const links = document.querySelectorAll('.nav-links li a');
links.forEach(link => {
    link.addEventListener('click', () => {
        links.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Dynamic content simulation (for future backend integration)
document.getElementById("activeCases").querySelector("p").textContent = "12";
document.getElementById("appointments").querySelector("p").textContent = "5";
document.getElementById("messages").querySelector("p").textContent = "3";

// Profile form submission
document.getElementById('profileForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert("Profile updated successfully!");
    // Here, you would typically save updated profile data to the server.
});
