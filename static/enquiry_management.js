// Optional JS for further interactivity (e.g., animations or effects)
document.querySelectorAll('.enquiry-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.transform = 'scale(1.05)';
        item.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.2)';
    });

    item.addEventListener('mouseleave', () => {
        item.style.transform = 'scale(1)';
        item.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
    });
});
