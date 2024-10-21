document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('lawyer-booking-form');
    const lawyerCards = document.querySelectorAll('.lawyer-card');
    const submitButton = form.querySelector('button[type="submit"]');

    // Highlight selected lawyer type
    lawyerCards.forEach(card => {
        card.addEventListener('click', function() {
            const lawyerType = this.getAttribute('data-type');
            document.getElementById('lawyer-type').value = lawyerType;
            lawyerCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');

            // Add a ripple effect
            const ripple = document.createElement('div');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            ripple.style.left = '50%';
            ripple.style.top = '50%';
            setTimeout(() => ripple.remove(), 1000);
        });
    });

    // Animate form labels on input focus
    const formInputs = form.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.previousElementSibling.classList.add('active');
        });
        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.previousElementSibling.classList.remove('active');
            }
        });
    });

    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const lawyerType = document.getElementById('lawyer-type').value;
        const caseDescription = document.getElementById('case-description').value;

        console.log('Booking submitted:', { name, email, lawyerType, caseDescription });

        // Animate the submit button
        submitButton.classList.add('submitting');
        submitButton.textContent = 'Submitting...';

        // Simulate a server request
        setTimeout(() => {
            submitButton.classList.remove('submitting');
            submitButton.textContent = 'Book Consultation';
            alert('Thank you for your booking request. We will contact you shortly.');
            form.reset();
            lawyerCards.forEach(c => c.classList.remove('selected'));
            formInputs.forEach(input => input.previousElementSibling.classList.remove('active'));
        }, 2000);
    });
});