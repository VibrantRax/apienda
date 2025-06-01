document.getElementById('loginForm').onsubmit = async function (e) {
    e.preventDefault(); // Evita el envío tradicional

    const AdminUserName = document.getElementById('AdminUserName').value;
    const AdminContraseña = document.getElementById('AdminContraseña').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ AdminUserName, AdminContraseña }),
        });

        const result = await response.json(); // Obtener el JSON de la respuesta

        // Manejo del mensaje de respuesta
        const messageDiv = document.getElementById('responseMessage');
        if (response.ok) {  // 200 OK
            if (result.redirect) {
                window.location.href = result.redirect; // Redirigir a la URL proporcionada
            } else {
                messageDiv.innerText = "Inicio de sesión exitoso, pero sin redirección explícita.";
                messageDiv.classList.add('success');
                messageDiv.classList.remove('error');
            }
        } else {
            messageDiv.innerText = result.message;
            messageDiv.classList.add('error');
            messageDiv.classList.remove('success');
        }
    } catch (error) {
        console.error('Error al enviar la solicitud:', error);
        const messageDiv = document.getElementById('responseMessage');
        messageDiv.innerText = "Ocurrió un error al procesar la solicitud.";
        messageDiv.classList.add('error');
        messageDiv.classList.remove('success');
    }
};