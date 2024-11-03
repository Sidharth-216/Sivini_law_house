$(document).ready(function() {
    $('#send-button').on('click', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const userMessage = $('#user-input').val();
        if (userMessage.trim() !== '') {
            $('#messages').append(`<div class="user-message">You: ${userMessage}</div>`);

            // Send message to the Flask server
            $.ajax({
                url: '/send_message',
                type: 'POST',  // This must be POST
                contentType: 'application/json',  // Ensure this is set to application/json
                data: JSON.stringify({ message: userMessage }),  // Send data as JSON
                success: function(data) {
                    $('#messages').append(`<div class="lawyer-message">Lawyer: ${data.response}</div>`);
                    $('#messages').scrollTop($('#messages')[0].scrollHeight); // Scroll to the bottom
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('Error:', textStatus, errorThrown);
                }
            });
            

            $('#user-input').val(''); // Clear the input
        }
    });
});
