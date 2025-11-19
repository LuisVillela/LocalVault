// JavaScript para página del vault

let passwords = [];
let currentPassword = null;
let isViewMode = false;
let derivedKey = null; // CryptoKey used for encrypt/decrypt

// Cargar contraseñas al iniciar
document.addEventListener('DOMContentLoaded', function() {
    requestPasswordAndInit();
    
    // Event listeners
    document.getElementById('add-password-btn').addEventListener('click', openAddModal);
    document.getElementById('password-form').addEventListener('submit', handlePasswordSubmit);
});

// --- Web Crypto helpers ---
function b64ToArrayBuffer(b64) {
    const binary_string = window.atob(b64);
    const len = binary_string.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}

function arrayBufferToB64(buffer) {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

async function deriveKey(password) {
    if (!window.CURRENT_USER_ID) throw new Error('No user id available');
    const enc = new TextEncoder();
    const salt = enc.encode(`localvault_user_${window.CURRENT_USER_ID}_salt`);
    const baseKey = await crypto.subtle.importKey('raw', enc.encode(password), {name: 'PBKDF2'}, false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey(
        {name: 'PBKDF2', salt, iterations: 200000, hash: 'SHA-256'},
        baseKey,
        {name: 'AES-GCM', length: 256},
        false,
        ['encrypt', 'decrypt']
    );
    return key;
}

async function encryptEntryObject(obj, key) {
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const data = new TextEncoder().encode(JSON.stringify(obj));
    const cipher = await crypto.subtle.encrypt({name: 'AES-GCM', iv}, key, data);
    // prepend iv
    const combined = new Uint8Array(iv.byteLength + cipher.byteLength);
    combined.set(iv, 0);
    combined.set(new Uint8Array(cipher), iv.byteLength);
    return arrayBufferToB64(combined.buffer);
}

async function decryptEntryBlob(b64blob, key) {
    const combined = new Uint8Array(b64ToArrayBuffer(b64blob));
    const iv = combined.slice(0, 12);
    const cipher = combined.slice(12).buffer;
    const decrypted = await crypto.subtle.decrypt({name: 'AES-GCM', iv}, key, cipher);
    return JSON.parse(new TextDecoder().decode(decrypted));
}

async function requestPasswordAndInit() {
    // Prompt the user for their account password to derive the master key locally.
    const pw = prompt('Introduce tu contraseña de cuenta para desbloquear el vault (no se enviará al servidor):');
    if (!pw) {
        // redirect to logout or deny
        window.location.href = '/logout';
        return;
    }
    try {
        derivedKey = await deriveKey(pw);
        await loadPasswords();
    } catch (err) {
        showMessage('Error al derivar la clave local: ' + err.message, 'error');
    }
}

// Cargar lista de contraseñas
async function loadPasswords() {
    try {
        const response = await fetch('/api/vault/passwords');
        const result = await response.json();
        
        if (result.success) {
            passwords = [];
            // result.entries: [{name, blob}]
            for (const e of result.entries) {
                try {
                    const decrypted = await decryptEntryBlob(e.blob, derivedKey);
                    passwords.push({
                        name: e.name,
                        user: decrypted.user || '',
                        password: decrypted.password || '',
                        description: decrypted.description || ''
                    });
                } catch (err) {
                    // If decryption fails, mark as locked so user knows
                    passwords.push({name: e.name, user: '', password: '', description: '', _locked: true});
                }
            }
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

// Ver detalles de una contraseña
async function viewPassword(name) {
    try {
        const response = await fetch(`/api/vault/passwords/${encodeURIComponent(name)}`);
        const result = await response.json();

        if (result.success) {
            isViewMode = true;
            // result.data.blob contains base64 encrypted blob
            try {
                const decrypted = await decryptEntryBlob(result.data.blob, derivedKey);
                currentPassword = {
                    name: name,
                    user: decrypted.user || '',
                    password: decrypted.password || '',
                    description: decrypted.description || ''
                };
            } catch (err) {
                showMessage('No se pudo desencriptar la entrada con la clave local proporcionada.', 'error');
                return;
            }

            document.getElementById('modal-title').textContent = 'Ver Contraseña';
            document.getElementById('password-form').style.display = 'block'; // Mantener visible para el botón
            document.getElementById('view-buttons').style.display = 'flex';

            // Ocultar botones del formulario en modo vista
            const formButtons = document.querySelector('#password-form .modal-buttons');
            if (formButtons) formButtons.style.display = 'none';

            // Llenar campos (solo lectura)
            document.getElementById('password-name').value = currentPassword.name;
            document.getElementById('password-user').value = currentPassword.user;
            document.getElementById('password-password').value = currentPassword.password;
            document.getElementById('password-description').value = currentPassword.description;

            // Deshabilitar campos pero permitir ver contraseña
            document.querySelectorAll('#password-form input, #password-form textarea').forEach(field => {
                field.disabled = true;
            });

            // Mantener funcionalidad del botón de ver contraseña
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
        // Encrypt locally then send blob to server
        const entryObj = {user: formData.user, password: formData.password, description: formData.description};
        const blob = await encryptEntryObject(entryObj, derivedKey);

        const response = await fetch('/api/vault/passwords', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: formData.name, blob})
        });
        const result = await response.json();
        if (result.success) {
            showMessage(result.message, 'success');
            closeModal();
            await loadPasswords(); // Recargar lista
        } else {
            showMessage('Error: ' + result.message, 'error');
        }
    } catch (error) {
        showMessage('Error de conexión al guardar contraseña o encriptando localmente.', 'error');
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