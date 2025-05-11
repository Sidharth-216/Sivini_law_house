document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("user_input");
    const button = document.querySelector(".submit-button");

    // Add focus effect on the textarea
    textarea.addEventListener("focus", () => {
        textarea.style.boxShadow = "0px 0px 10px #6a11cb";
    });

    textarea.addEventListener("blur", () => {
        textarea.style.boxShadow = "none";
    });

    // Add button click animation
    button.addEventListener("mousedown", () => {
        button.style.transform = "scale(0.9)";
    });

    button.addEventListener("mouseup", () => {
        button.style.transform = "scale(1)";
    });
});
