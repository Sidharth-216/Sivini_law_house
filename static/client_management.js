// clients.js

document.addEventListener('DOMContentLoaded', function() {
    const clientsList = document.querySelector('ul');
    
    // Fade-in effect for the clients list
    clientsList.style.opacity = 0;
    clientsList.style.transition = 'opacity 1s ease';
    
    setTimeout(() => {
        clientsList.style.opacity = 1;
    }, 500); // Delay for fade-in effect

    // Add additional animations or functionality as needed
});
