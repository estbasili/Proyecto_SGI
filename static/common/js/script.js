// static/js/script.js

// Ejemplo de validación de formulario de login
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const email = document.querySelector('#email').value;
            const password = document.querySelector('#password').value;
            
            if (!email || !password) {
                event.preventDefault();
                alert('Por favor complete todos los campos.');
            }
        });
    }
});


