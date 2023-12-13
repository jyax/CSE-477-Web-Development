document.getElementById('sign-up').addEventListener('click', () =>{
    window.location.href = '/signup';
});

document.getElementById('sign-in-form').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch('/processlogin', {
        method: 'POST',
        body: new FormData(document.getElementById('sign-in-form'))
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/home'; // Redirect to the home page
        } else {
            alert('Invalid credentials'); // Show an error message
        }
    })
        .catch(err => console.error('Error:', err));
});