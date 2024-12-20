// Sidebar active link highlight
const links = document.querySelectorAll('.nav-links li a');
links.forEach(link => {
    link.addEventListener('click', () => {
        links.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Dynamic content simulation for cards
document.getElementById("activeCases").querySelector("p").textContent = "12";
document.getElementById("appointments").querySelector("p").textContent = "5";
document.getElementById("messages").querySelector("p").textContent = "3";

// Card hover animations
const cards = document.querySelectorAll(".card");
cards.forEach(card => {
    card.addEventListener("mouseover", () => {
        card.classList.add("hovered");
    });
    card.addEventListener("mouseleave", () => {
        card.classList.remove("hovered");
    });
});
