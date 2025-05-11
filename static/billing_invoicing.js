// Dynamic updates or animations for invoices (optional for future use)
const deleteButtons = document.querySelectorAll('.delete-invoice');

deleteButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        const confirmation = confirm("Are you sure you want to delete this invoice?");
        if (!confirmation) {
            event.preventDefault();
        }
    });
});
// Add search bar functionality to filter client list items
const searchBar = document.querySelector('#searchBar');
if (searchBar) {
    searchBar.addEventListener('input', () => {
        const searchTerm = searchBar.value.toLowerCase();
        clientItems.forEach(item => {
            const clientName = item.textContent.toLowerCase();
            if (clientName.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
}