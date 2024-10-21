window.onload = function() {
    const bookingData = localStorage.getItem('newBooking');
    if (bookingData) {
        const booking = JSON.parse(bookingData);
        const bookingsList = document.getElementById('bookingsList');

        const card = document.createElement('div');
        card.className = 'booking-card';
        card.innerHTML = `
            <div class="booking-item">
                <label>Lawyer Name:</label>
                <input type="text" value="${booking.lawyerName}" readonly>
            </div>
            <div class="booking-item">
                <label>Specialization:</label>
                <input type="text" value="${booking.specialization}" readonly>
            </div>
            <div class="booking-item">
                <label>Contact:</label>
                <input type="tel" value="${booking.contact}" readonly>
            </div>
            <div class="booking-item">
                <label>Date:</label>
                <input type="date" value="${booking.date}" readonly>
            </div>
            <div class="booking-item">
                <label>Time:</label>
                <input type="time" value="${booking.time}" readonly>
            </div>
        `;
        bookingsList.appendChild(card);

        // Clear the stored booking data
        localStorage.removeItem('newBooking');
    }
};