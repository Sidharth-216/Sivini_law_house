document.addEventListener("DOMContentLoaded", () => {
    const reviewForm = document.getElementById("review-form");
    const reviewsList = document.getElementById("reviews-list");

    // Array to store reviews (in-memory, no database)
    const reviews = [];

    // Handle form submission
    reviewForm.addEventListener("submit", (event) => {
        event.preventDefault();

        // Get form data
        const name = document.getElementById("name").value.trim();
        const reviewText = document.getElementById("review").value.trim();

        // Validate input
        if (name === "" || reviewText === "") {
            alert("Please fill in all fields.");
            return;
        }

        // Add review to the list
        reviews.push({ name, reviewText });
        renderReviews();

        // Clear form
        reviewForm.reset();
    });

    // Function to render reviews
    function renderReviews() {
        reviewsList.innerHTML = ""; // Clear the list

        reviews.forEach((review) => {
            const reviewItem = document.createElement("div");
            reviewItem.className = "review-item";

            reviewItem.innerHTML = `
                <h3>${review.name}</h3>
                <p>${review.reviewText}</p>
            `;

            reviewsList.appendChild(reviewItem);
        });
    }
});
