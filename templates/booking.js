document.getElementById("bookingForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const data = {
        user_id: document.getElementById("user_id").value,
        show_id: document.getElementById("show_id").value,
        seats: document.getElementById("seats").value
    };
    
    fetch('/api/book', {  // Replace with the actual API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => alert("Booking successful!"))
    .catch(error => console.error("Error booking:", error));
});
