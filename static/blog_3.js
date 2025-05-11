document.addEventListener("DOMContentLoaded", function () {
    // Smooth scrolling for internal links
    document.querySelectorAll("a[href^='#']").forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    });

    // Toggle dark mode
    const toggleDarkMode = document.createElement("button");
    toggleDarkMode.innerText = "Toggle Dark Mode";
    toggleDarkMode.style.position = "fixed";
    toggleDarkMode.style.top = "10px";
    toggleDarkMode.style.right = "10px";
    toggleDarkMode.style.padding = "10px";
    toggleDarkMode.style.cursor = "pointer";
    document.body.appendChild(toggleDarkMode);

    toggleDarkMode.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
    });

    // Dark mode styles
    const darkModeStyle = document.createElement("style");
    darkModeStyle.innerHTML = `
        .dark-mode {
            background-color: #121212;
            color: white;
        }
        .dark-mode header, .dark-mode footer {
            background-color: #1f1f1f;
        }
    `;
    document.head.appendChild(darkModeStyle);
});
