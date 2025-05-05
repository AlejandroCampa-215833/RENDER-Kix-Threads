document.querySelector('form').addEventListener('submit', function(e) {
    const username = document.getElementById('username').value;
    const usernamePattern = /^[A-Za-z]{6,}$/;

    if (!usernamePattern.test(username)) {
        e.preventDefault(); // Detiene el envío del formulario
        alert('El nombre de usuario debe tener al menos 6 letras, sin números ni símbolos.');
    }
});