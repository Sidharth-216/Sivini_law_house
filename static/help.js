// Smooth Scrolling for In-Page Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

// Fade-In Animation on Scroll
const fadeInElements = document.querySelectorAll('.step');

function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
    );
}

function handleScroll() {
    fadeInElements.forEach(el => {
        if (isElementInViewport(el)) {
            el.classList.add('fade-in');
        }
    });
}

// Back Button Functionality
const backButton = document.getElementById('backButton');
backButton.addEventListener('click', () => {
    window.history.back();
});

window.addEventListener('scroll', handleScroll);
window.addEventListener('load', handleScroll); // Trigger animation on page load
