// JavaScript para página del vault

let passwords = [];
let currentPassword = null;
let isViewMode = false;

// Cargar contraseñas al iniciar
document.addEventListener('DOMContentLoaded', function() {
    loadPasswords();
    
    // Event listeners
    document.getElementById('add-password-btn').addEventListener('click', openAddModal);
    document.getElementById('password-form').addEventListener('submit', handlePasswordSubmit);
});

// Cargar lista de contraseñas
async function loadPasswords() {
    try {
        const response = await fetch('/api/vault/passwords');
        const result = await response.json();
        
        if (result.success) {
            passwords = result.passwords;
            renderPasswords();
        } else {
            showMessage('Error al cargar contraseñas: ' + result.message, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión al cargar contraseñas.', 'error');
    }
}

// Renderizar lista de contraseñas
function renderPasswords() {
    const passwordsList = document.getElementById('passwords-list');
    const noPasswords = document.getElementById('no-passwords');
    
    if (passwords.length === 0) {
        passwordsList.style.display = 'none';
        noPasswords.style.display = 'block';
        return;
    }
    
    passwordsList.style.display = 'grid';
    noPasswords.style.display = 'none';
    
    passwordsList.innerHTML = passwords.map(password => `
        <div class="password-card" onclick="viewPassword('${password.name}')">
            <h3>${escapeHtml(password.name)}</h3>
            <div class="user">${escapeHtml(password.user || 'Sin usuario')}</div>
            <div class="description">${escapeHtml(password.description || 'Sin descripción')}</div>
        </div>
    `).join('');
}

// Abrir modal para agregar contraseña
function openAddModal() {
    isViewMode = false;
    currentPassword = null;
    
    document.getElementById('modal-title').textContent = 'Agregar Contraseña';
    document.getElementById('password-form').style.display = 'block';
    document.getElementById('view-buttons').style.display = 'none';
    
    // Mostrar botones del formulario
    const formButtons = document.querySelector('#password-form .modal-buttons');
    if (formButtons) formButtons.style.display = 'flex';
    
    // Habilitar todos los campos
    document.querySelectorAll('#password-form input, #password-form textarea').forEach(field => {
        field.disabled = false;
    });
    
    // Limpiar formulario
    document.getElementById('password-form').reset();
    
    // Restablecer campo de contraseña a modo oculto
    const passwordField = document.getElementById('password-password');
    const toggleBtn = document.querySelector('.toggle-password');
    passwordField.type = 'password';
    toggleBtn.textContent = '👁️';
    
    // Mostrar modal
    document.getElementById('password-modal').style.display = 'block';
}

// Ver detalles de una contraseña con verificación previa
async function viewPassword(name) {
    try {
        // === Paso 1: solicitar verificación ===
        const userPassword = prompt("Introduce tu contraseña para continuar:");
        if (!userPassword) return;

        // Llamar al endpoint de verificación
        const verifyRes = await fetch('/api/verify-account-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: userPassword })
        });
        const verifyResult = await verifyRes.json();

        if (!verifyResult.success) {
            showMessage(verifyResult.message || 'Contraseña incorrecta.', 'error');
            return;
        }

        // === Paso 2: cargar la contraseña real si la verificación fue exitosa ===
        const response = await fetch(`/api/vault/passwords/${encodeURIComponent(name)}`);
        const result = await response.json();
        
        if (result.success) {
            isViewMode = true;
            currentPassword = result.data;
            
            document.getElementById('modal-title').textContent = 'Ver Contraseña';
            document.getElementById('password-form').style.display = 'block';
            document.getElementById('view-buttons').style.display = 'flex';
            
            const formButtons = document.querySelector('#password-form .modal-buttons');
            if (formButtons) formButtons.style.display = 'none';
            
            document.getElementById('password-name').value = currentPassword.name;
            document.getElementById('password-user').value = currentPassword.user;
            document.getElementById('password-password').value = currentPassword.password;
            document.getElementById('password-description').value = currentPassword.description;
            
            document.querySelectorAll('#password-form input, #password-form textarea').forEach(field => {
                field.disabled = true;
            });
            
            document.querySelector('.toggle-password').disabled = false;
            document.querySelector('.toggle-password').style.opacity = '1';
            document.querySelector('.toggle-password').style.pointerEvents = 'auto';
            
            document.getElementById('password-modal').style.display = 'block';
        } else {
            showMessage('Error al cargar contraseña: ' + result.message, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión al cargar contraseña.', 'error');
    }
}


// Manejar envío del formulario
async function handlePasswordSubmit(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('password-name').value,
        user: document.getElementById('password-user').value,
        password: document.getElementById('password-password').value,
        description: document.getElementById('password-description').value
    };
    
    try {
        const response = await fetch('/api/vault/passwords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage(result.message, 'success');
            closeModal();
            loadPasswords(); // Recargar lista
        } else {
            showMessage('Error: ' + result.message, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión al guardar contraseña.', 'error');
    }
}

// Copiar contraseña al portapapeles
async function copyPassword() {
    if (currentPassword) {
        try {
            await navigator.clipboard.writeText(currentPassword.password);
            showMessage('Contraseña copiada al portapapeles', 'success');
        } catch (error) {
            // Fallback para navegadores que no soportan clipboard API
            const textArea = document.createElement('textarea');
            textArea.value = currentPassword.password;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showMessage('Contraseña copiada al portapapeles', 'success');
        }
    }
}

// Eliminar contraseña
async function deletePassword() {
    if (currentPassword && confirm(`¿Estás seguro de eliminar la contraseña de "${currentPassword.name}"?`)) {
        try {
            const response = await fetch(`/api/vault/passwords/${encodeURIComponent(currentPassword.name)}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                showMessage(result.message, 'success');
                closeModal();
                loadPasswords(); // Recargar lista
            } else {
                showMessage('Error: ' + result.message, 'error');
            }
        } catch (error) {
            showMessage('Error de conexión al eliminar contraseña.', 'error');
        }
    }
}

// Alternar visibilidad de contraseña
function togglePasswordVisibility() {
    const passwordField = document.getElementById('password-password');
    const toggleBtn = document.querySelector('.toggle-password');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleBtn.textContent = '🙈';
    } else {
        passwordField.type = 'password';
        toggleBtn.textContent = '👁️';
    }
}

// Cerrar modal
function closeModal() {
    document.getElementById('password-modal').style.display = 'none';
    
    // Rehabilitar campos
    document.querySelectorAll('#password-form input, #password-form textarea').forEach(field => {
        field.disabled = false;
    });
    
    // Restaurar visibilidad del formulario y botones
    document.getElementById('password-form').style.display = 'block';
    document.getElementById('view-buttons').style.display = 'none';
    
    // Mostrar botones del formulario nuevamente
    const formButtons = document.querySelector('#password-form .modal-buttons');
    if (formButtons) formButtons.style.display = 'flex';
    
    // Restablecer campo de contraseña a modo oculto
    const passwordField = document.getElementById('password-password');
    const toggleBtn = document.querySelector('.toggle-password');
    passwordField.type = 'password';
    toggleBtn.textContent = '👁️';
    
    // Limpiar formulario
    document.getElementById('password-form').reset();
    
    currentPassword = null;
    isViewMode = false;
}

// Cerrar modal al hacer clic fuera
window.addEventListener('click', function(event) {
    const modal = document.getElementById('password-modal');
    if (event.target === modal) {
        closeModal();
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
    
    // Auto-ocultar después de 3 segundos
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 3000);
}

async function requestPasswordVerification() {
    const userPassword = prompt("Introduce tu contraseña para continuar:");
    if (!userPassword) return false;

    const res = await fetch('/api/verify-account-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: userPassword })
    });

    const result = await res.json();
    if (!result.success) {
        alert(result.message || "Contraseña incorrecta.");
        return false;
    }
    return true;
}


// Función para escapar HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}