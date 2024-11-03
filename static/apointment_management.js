// appointments.js

document.addEventListener('DOMContentLoaded', function() {
    const appointmentsList = document.querySelector('ul');

    // Fade-in effect for the appointments list
    appointmentsList.style.opacity = 0;
    appointmentsList.style.transition = 'opacity 1s ease';

    setTimeout(() => {
        appointmentsList.style.opacity = 1;
    }, 500); // Delay for fade-in effect

    // Add additional animations or functionality as needed
});
