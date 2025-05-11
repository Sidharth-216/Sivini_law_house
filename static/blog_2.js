// Smooth Scroll for Internal Links
document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll("h2");

    links.forEach(link => {
        link.addEventListener("click", () => {
            link.scrollIntoView({ behavior: "smooth" });
        });
    });
});

// Back to Top Button
const backToTop = document.createElement("button");
backToTop.innerText = "↑ Top";
backToTop.id = "backToTop";
document.body.appendChild(backToTop);

backToTop.style.position = "fixed";
backToTop.style.bottom = "20px";
backToTop.style.right = "20px";
backToTop.style.padding = "10px 15px";
backToTop.style.background = "#002b5c";
backToTop.style.color = "#fff";
backToTop.style.border = "none";
backToTop.style.borderRadius = "5px";
backToTop.style.cursor = "pointer";
backToTop.style.display = "none";

window.addEventListener("scroll", function () {
    if (window.scrollY > 300) {
        backToTop.style.display = "block";
    } else {
        backToTop.style.display = "none";
    }
});

backToTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
