document.getElementById("paymentForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const data = {
        booking_id: document.getElementById("booking_id").value,
        payment_type: document.getElementById("payment_type").value
    };
    
    fetch('/api/payment', {  // Replace with the actual API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => alert("Payment successful!"))
    .catch(error => console.error("Error with payment:", error));
});
