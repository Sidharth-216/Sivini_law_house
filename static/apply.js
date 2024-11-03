document.getElementById('jobApplicationForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent default form submission

    // Show SweetAlert and submit form after user clicks 'OK'
    Swal.fire({
        title: 'Application Submitted!',
        text: 'Thank you for your application. We will contact you soon.',
        icon: 'success',
        confirmButtonText: 'OK'
    }).then((result) => {
        if (result.isConfirmed) {
            // Submit the form after SweetAlert confirmation
            e.target.submit();  // Manually submit the form
        }
    });
});
