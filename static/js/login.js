// JavaScript para página de login

// Cambiar entre pestañas de login y registro
function showTab(tabName) {
    // Ocultar todas las pestañas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Quitar clase active de todos los botones
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostrar pestaña seleccionada
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Activar botón correspondiente
    event.target.classList.add('active');
    
    // Limpiar mensajes
    clearMessages();
}

// Manejo del formulario de login
document.getElementById('login-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const spinner = submitBtn.querySelector('.spinner');
    const btnText = submitBtn.querySelector('.btn-text');
    
    // Mostrar loading
    spinner.style.display = 'block';
    btnText.textContent = 'Iniciando...';
    submitBtn.disabled = true;
    
    try {
        const formData = {
            email: document.getElementById('login-email').value,
            password: document.getElementById('login-password').value
        };
        
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage(result.message, 'success');
            setTimeout(() => {
                window.location.href = result.redirect;
            }, 1000);
        } else {
            showMessage(result.message, 'error');
        }
        
    } catch (error) {
        showMessage('Error de conexión. Inténtalo de nuevo.', 'error');
    } finally {
        // Ocultar loading
        spinner.style.display = 'none';
        btnText.textContent = 'Iniciar Sesión';
        submitBtn.disabled = false;
    }
});

// Manejo del formulario de registro
document.getElementById('register-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const spinner = submitBtn.querySelector('.spinner');
    const btnText = submitBtn.querySelector('.btn-text');
    
    // Mostrar loading
    spinner.style.display = 'block';
    btnText.textContent = 'Creando...';
    submitBtn.disabled = true;
    
    try {
        const formData = {
            name: document.getElementById('register-name').value,
            email: document.getElementById('register-email').value,
            password: document.getElementById('register-password').value,
            birthdate: document.getElementById('register-birthdate').value
        };
        
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage(result.message, 'success');
            // Limpiar formulario
            this.reset();
            // Cambiar a pestaña de login después de 2 segundos
            setTimeout(() => {
                showTab('login');
            }, 2000);
        } else {
            showMessage(result.message, 'error');
        }
        
    } catch (error) {
        showMessage('Error de conexión. Inténtalo de nuevo.', 'error');
    } finally {
        // Ocultar loading
        spinner.style.display = 'none';
        btnText.textContent = 'Crear Cuenta';
        submitBtn.disabled = false;
    }
});

// Función para mostrar mensajes
function showMessage(text, type) {
    const messageArea = document.getElementById('message-area');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    
    // Limpiar mensajes anteriores
    messageArea.innerHTML = '';
    messageArea.appendChild(messageDiv);
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

// Función para limpiar mensajes
function clearMessages() {
    document.getElementById('message-area').innerHTML = '';
}

// Validación en tiempo real de contraseña
document.getElementById('register-password').addEventListener('input', function() {
    const password = this.value;
    const hint = this.parentNode.querySelector('.password-hint');
    
    let requirements = [];
    
    if (password.length < 8) requirements.push('8 caracteres');
    if (!/[A-Z].*[A-Z]/.test(password)) requirements.push('2 mayúsculas');
    if (!/\d/.test(password)) requirements.push('1 dígito');
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) requirements.push('1 carácter especial');
    
    if (requirements.length === 0) {
        hint.style.color = '#28a745';
        hint.textContent = '✓ Contraseña válida';
    } else {
        hint.style.color = '#dc3545';
        hint.textContent = 'Faltan: ' + requirements.join(', ');
    }
});