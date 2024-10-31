document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        phone: document.getElementById("phone").value
    };
    
    fetch('/api/register', {  // Replace with the actual API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => alert("Registration successful!"))
    .catch(error => console.error("Error registering:", error));
});
