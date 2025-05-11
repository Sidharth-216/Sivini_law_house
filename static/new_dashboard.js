const body = document.querySelector("body"),
      modeToggle = body.querySelector(".mode-toggle");
      sidebar = body.querySelector("nav");
      sidebarToggle = body.querySelector(".sidebar-toggle");

let getMode = localStorage.getItem("mode");
if(getMode && getMode ==="dark"){
    body.classList.toggle("dark");
}

let getStatus = localStorage.getItem("status");
if(getStatus && getStatus ==="close"){
    sidebar.classList.toggle("close");
}

modeToggle.addEventListener("click", () =>{
    body.classList.toggle("dark");
    if(body.classList.contains("dark")){
        localStorage.setItem("mode", "dark");
    }else{
        localStorage.setItem("mode", "light");
    }
});

sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    if(sidebar.classList.contains("close")){
        localStorage.setItem("status", "close");
    }else{
        localStorage.setItem("status", "open");
    }
})
// Wait for the document to be fully loaded
document.addEventListener('DOMContentLoaded', function () {

    // Fade In Animation for the Appointment List
    const appointmentsList = document.querySelector('.appointments-list');
    if (appointmentsList) {
        appointmentsList.classList.add('fade-in');
    }

    // Smooth Scroll to Appointment Form
    const backButton = document.querySelector('.back-btn');
    if (backButton) {
        backButton.addEventListener('click', function () {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Delete Appointment Confirmation
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach((button) => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const appointmentId = button.getAttribute('data-id');
            const confirmation = confirm(`Are you sure you want to delete appointment #${appointmentId}?`);

            if (confirmation) {
                // Perform the delete action (e.g., via fetch or form submission)
                window.location.href = button.href; // This will redirect to the delete route
            }
        });
    });

    // Animate form inputs on focus
    const inputs = document.querySelectorAll('.appointment-form input, .appointment-form select');
    inputs.forEach((input) => {
        input.addEventListener('focus', function () {
            input.style.backgroundColor = '#34495e';
            input.style.borderColor = '#f1c40f';
        });

        input.addEventListener('blur', function () {
            input.style.backgroundColor = '#2c3e50';
            input.style.borderColor = '#aaa';
        });
    });

    // Appointment Item Hover Animation
    const appointmentItems = document.querySelectorAll('.appointment-item');
    appointmentItems.forEach((item) => {
        item.addEventListener('mouseover', function () {
            item.style.transform = 'scale(1.03)';
            item.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.3)';
        });

        item.addEventListener('mouseout', function () {
            item.style.transform = 'scale(1)';
            item.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.2)';
        });
    });

});

// Optional: Add fade-in effect using CSS
const style = document.createElement('style');
style.innerHTML = `
    .fade-in {
        animation: fadeIn 1s ease-out;
    }

    @keyframes fadeIn {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
// Functionality for the Search Bar
const searchBar = document.getElementById('searchBar');
if (searchBar) {
    searchBar.addEventListener('input', function () {
        const filter = searchBar.value.toLowerCase();
        const appointmentItems = document.querySelectorAll('.appointment-item');

        appointmentItems.forEach((item) => {
            const appointmentText = item.textContent.toLowerCase();
            if (appointmentText.includes(filter)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
}