// Add an event listener to the form submission
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Get the values from the form fields
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var message = document.getElementById('message').value;



    var templateParams = {
        from_name: username,
        from_email: email,
        from_messages: message
    };


    // Send the email using EmailJS
    emailjs.send('gmail', 'Sosotech', templateParams, 'Fm3kclIdYBzU6wf8j')

    .then(function(response) {
        console.log('SUCCESS!', response.status, response.text);
        // TODO: Add code to display a success message to the user

    }, function(error) {
        console.log('FAILED...', error);
        // TODO: Add code to display an error message to the user
    });
});

console.log(username)
console.log(email)
console.log(message)