// Get references to the main card and lawyer grid
const mainCard = document.getElementById('mainCard');
const lawyerGrid = document.getElementById('lawyerGrid');

// Function to toggle visibility of lawyer cards with fade-in effect
mainCard.addEventListener('click', () => {
    if (lawyerGrid.style.display === 'flex') {
        lawyerGrid.style.display = 'none';
    } else {
        lawyerGrid.style.display = 'flex';
        lawyerGrid.style.opacity = 0; // Start with opacity 0
        let opacity = 0;
        const fadeIn = setInterval(() => {
            if (opacity >= 1) {
                clearInterval(fadeIn);
            }
            lawyerGrid.style.opacity = opacity;
            opacity += 0.1; // Increase opacity for the fade-in effect
        }, 50); // Control fade-in speed (50ms interval)
    }
});

// Hover effect on lawyer cards (scale up on hover)
const lawyerCards = document.querySelectorAll('.lawyer-card');

lawyerCards.forEach(card => {
    // Scale the card on hover
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'scale(1.05)'; // Slightly enlarge the card
        card.style.transition = 'transform 0.3s'; // Smooth transition
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'scale(1)'; // Return to original size
    });

    // Add click event to contact buttons
    const contactBtn = card.querySelector('.contact-btn');
    contactBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering the main card click
        const email = contactBtn.getAttribute('data-email');
        alert(`Contacting: ${email}`); // Replace with any desired action (like opening an email client)
    });
});

// Additional hover effect with rotation and translation
lawyerCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-10px) rotateY(10deg) rotateX(10deg)'; // Translate and rotate card
        card.style.transition = 'transform 0.3s'; // Smooth transition
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) rotateY(0) rotateX(0)'; // Reset to original position
    });
});
