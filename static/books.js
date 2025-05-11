// Example: Add a bounce effect to the book cards on hover
document.addEventListener('DOMContentLoaded', () => {
    const bookCards = document.querySelectorAll('.book-card');

    bookCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.style.animation = 'bounce 0.5s';
        });
        card.addEventListener('animationend', () => {
            card.style.animation = '';
        });
    });
});

// Bounce animation keyframes
const styleSheet = document.createElement('style');
styleSheet.textContent = `
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}`;
document.head.appendChild(styleSheet);
