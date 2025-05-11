document.addEventListener("DOMContentLoaded", function () {
    console.log("Blog page loaded successfully!");

    // Optional: Dark Mode Toggle
    const toggleButton = document.createElement("button");
    toggleButton.textContent = "Toggle Dark Mode";
    toggleButton.style.position = "fixed";
    toggleButton.style.top = "10px";
    toggleButton.style.right = "10px";
    toggleButton.style.padding = "10px";
    toggleButton.style.background = "#007bff";
    toggleButton.style.color = "#fff";
    toggleButton.style.border = "none";
    toggleButton.style.cursor = "pointer";

    document.body.appendChild(toggleButton);

    toggleButton.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
    });

    const style = document.createElement("style");
    style.innerHTML = `
        .dark-mode {
            background-color: #222;
            color: #fff;
        }
        .dark-mode .blog-content {
            background-color: #333;
            color: #ddd;
        }
        .dark-mode header,
        .dark-mode footer {
            background-color: #0056b3;
        }
    `;
    document.head.appendChild(style);
});
