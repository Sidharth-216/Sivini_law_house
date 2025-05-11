// JavaScript to enhance user experience with form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = form.querySelector('button[type="submit"]');

    // Show success or error message after form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting for demo purposes
        const caseName = form.querySelector('[name="case_name"]').value;
        const clientName = form.querySelector('[name="client_name"]').value;
        const startDate = form.querySelector('[name="start_date"]').value;
        const status = form.querySelector('[name="status"]').value;
        const description = form.querySelector('[name="description"]').value;

        // Check if any field is empty
        if (!caseName || !clientName || !startDate || !status || !description) {
            alert("Please fill in all fields before submitting.");
        } else {
            // Assuming you have an API or backend to handle the submission
            // Here, we're just logging the data for now.
            console.log({
                case_name: caseName,
                client_name: clientName,
                start_date: startDate,
                status: status,
                description: description
            });

            // Show a success message after successful form submission
            alert('Case updated successfully!');
        }
    });

    // Optionally disable the submit button until all fields are filled
    form.addEventListener('input', function() {
        const caseName = form.querySelector('[name="case_name"]').value;
        const clientName = form.querySelector('[name="client_name"]').value;
        const startDate = form.querySelector('[name="start_date"]').value;
        const status = form.querySelector('[name="status"]').value;
        const description = form.querySelector('[name="description"]').value;

        // Enable or disable the submit button based on form validity
        if (caseName && clientName && startDate && status && description) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    });
});
