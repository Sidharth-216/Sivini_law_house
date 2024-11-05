document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.querySelector('form[action="/upload_document"]');
    
    // Handle form submission with validation
    uploadForm.addEventListener('submit', function(event) {
        const fileInput = uploadForm.querySelector('input[type="file"]');
        const clientNameInput = uploadForm.querySelector('input[name="client_name"]');

        if (!fileInput.files.length) {
            alert("Please select a file to upload.");
            event.preventDefault();
        } else if (!clientNameInput.value.trim()) {
            alert("Please enter the client name.");
            event.preventDefault();
        } else {
            // Optionally, you can add some animations or loading indicators here
            alert("Uploading your document...");
        }
    });
    
    // Optionally, add any other interactive features here
});
