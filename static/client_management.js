// Add scaling animation for client list items on hover
const clientItems = document.querySelectorAll('.client-item');
clientItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.transform = 'scale(1.05)';
        item.style.transition = 'transform 0.3s ease-in-out';
    });
    item.addEventListener('mouseleave', () => {
        item.style.transform = 'scale(1)';
        item.style.transition = 'transform 0.3s ease-in-out';
    });
});

// Add glowing border and shadow animation for form inputs on focus
const formInputs = document.querySelectorAll('.client-form input');
formInputs.forEach(input => {
    input.addEventListener('focus', () => {
        input.style.borderColor = '#ffcb45';
        input.style.boxShadow = '0 0 10px rgba(255, 203, 69, 0.7)';
        input.style.transition = 'box-shadow 0.3s ease-in-out';
    });
    input.addEventListener('blur', () => {
        input.style.borderColor = '#ccc';
        input.style.boxShadow = 'none';
    });
});

// Add smooth scrolling effect for navigation (if needed)
const backButton = document.querySelector('#backButton');
if (backButton) {
    backButton.addEventListener('click', event => {
        event.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}
