// Get references
const viewTeamBtn = document.getElementById('viewTeamBtn');
const lawyerGrid = document.getElementById('lawyerGrid');

// Toggle lawyer grid with fade-in animation
viewTeamBtn.addEventListener('click', () => {
    lawyerGrid.style.display = 'grid';
    lawyerGrid.style.opacity = 1;
    lawyerGrid.style.transform = 'translateY(0)';
});

// Contact button functionality
const contactButtons = document.querySelectorAll('.contact-btn');
contactButtons.forEach(button => {
    button.addEventListener('click', () => {
        const email = button.dataset.email;
        alert(`Contact: ${email}`);
    });
});
