// Add an event listener to the form submission
document.querySelector('form').addEventListener('submit', function(event) {
    // Get the values from the form fields
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var messages = document.getElementById('messages').value;

    // Send the email using EmailJS
    emailjs.send('gmail', 'Sosotech', {
        from_name: name,
        from_email: email,
        from_messages: messages
    }, '6hBKUU6AaZsir5LFX')

    .then(function(response) {
        console.log('SUCCESS!', response.status, response.text);
        // TODO: Add code to display a success message to the user

    }, function(error) {
        console.log('FAILED...', error);
        // TODO: Add code to display an error message to the user
    });
});