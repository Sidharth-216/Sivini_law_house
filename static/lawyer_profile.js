// Add dynamic animations or interactions
document.addEventListener("DOMContentLoaded", () => {
    const backButton = document.getElementById("backButton");

    // Hover animation for back button
    backButton.addEventListener("mouseover", () => {
        backButton.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.2)";
    });

    backButton.addEventListener("mouseout", () => {
        backButton.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
    });

    // Simulate text pop-in animation
    const profileInfo = document.querySelectorAll(".profile-info p");
    profileInfo.forEach((item, index) => {
        item.style.opacity = "0";
        setTimeout(() => {
            item.style.transition = "opacity 0.5s ease";
            item.style.opacity = "1";
        }, 300 * index);
    });
});
