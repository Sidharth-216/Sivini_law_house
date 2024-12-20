// DOM Elements
const paymentButton = document.getElementById("paymentButton");
const bookButton = document.getElementById("bookButton");
const backButton = document.getElementById("backButton");
const inputs = document.querySelectorAll(".animated-input");

// Button Animation on Hover
function addButtonHoverEffect(button) {
    button.addEventListener("mouseenter", () => {
        button.style.transform = "scale(1.1)";
        button.style.boxShadow = "0 6px 10px rgba(0, 0, 0, 0.4)";
    });

    button.addEventListener("mouseleave", () => {
        button.style.transform = "scale(1)";
        button.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.3)";
    });
}

// profile.js

// Function to go back to the previous page when back button is clicked
document.getElementById("backButton").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent any default button behavior
    window.history.back(); // Go back to the previous page in the browser history
});



// Apply hover effect to buttons
addButtonHoverEffect(paymentButton);
addButtonHoverEffect(bookButton);
addButtonHoverEffect(backButton);

// Smooth Scroll Back to Top (for Back Button)
backButton.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
});

// Input Focus Animation
inputs.forEach((input) => {
    input.addEventListener("focus", () => {
        input.style.boxShadow = "0 0 8px rgba(0, 123, 255, 0.5)";
    });

    input.addEventListener("blur", () => {
        input.style.boxShadow = "none";
    });
});

// Smooth Scrolling for Internal Links
document.querySelectorAll("a").forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
        const href = this.getAttribute("href");
        if (href.startsWith("#")) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: "smooth",
                block: "start",
            });
        }
    });
});
