// applications.js

// Function to handle back button
function goBack() {
  window.history.back();
}

// Function to handle accept/reject actions
function updateStatus(button, status) {
  // Retrieve the application ID from the data-id attribute
  const id = button.getAttribute('data-id');
  
  // Display an alert or perform any further actions
  alert(`Application ID ${id} marked as ${status}`);
  
  // Example of further processing (AJAX or fetch can be used to send this data to the server)
  // Uncomment and modify the following code if you want to actually send this to the server:
  /*
  fetch('/update_application_status', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: id, status: status })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.message);
  })
  .catch(error => console.error('Error:', error));
  */
}
