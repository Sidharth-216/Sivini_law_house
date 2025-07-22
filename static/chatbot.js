// Wait until DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.chat-form');
    const replySection = document.querySelector('.response-section');
    const submitButton = document.querySelector('.submit-button');

    if (form && submitButton) {
        form.addEventListener('submit', () => {
            // Add a quick animation to the button on click
            submitButton.classList.add('clicked');
            setTimeout(() => {
                submitButton.classList.remove('clicked');
            }, 200);
        });
    }

    // Scroll to AI reply smoothly when reply appears
    if (replySection) {
        replySection.scrollIntoView({ behavior: 'smooth' });
    }
});
