# app.py - Aplicación web Flask para LocalVault
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from src.database_manager import DatabaseManager
from src.vault_manager import load_vault, save_vault
import os
import secrets

import sys
import logging

# 🔍 Mostrar errores completos en Render
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Clave secreta para sesiones

# Instancia global del manager de base de datos
db_manager = DatabaseManager()

@app.route('/')
def index():
    """Página principal - redirige según el estado de login"""
    if 'user_id' in session:
        return redirect(url_for('vault'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    """Página de login"""
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint para autenticación"""
    data = request.get_json()
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Correo y contraseña son requeridos'}), 400
    
    # Autenticar usuario
    user = db_manager.authenticate_user(email, password)
    
    if user:
        # Guardar datos de sesión
        session['user_id'] = user['id']
        session['user_name'] = user['nombre']
        session['user_email'] = user['correo']
        
        # Generar clave maestra
        master_key = db_manager.generate_master_key_for_user(user['id'], password)
        session['master_key'] = master_key
        
        return jsonify({
            'success': True,
            'message': f'Bienvenido, {user["nombre"]}!',
            'redirect': url_for('vault')
        })
    else:
        return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos'}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint para registro de usuarios"""
    data = request.get_json()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    birthdate = data.get('birthdate', '').strip()
    
    # Validaciones básicas
    if not all([name, email, password, birthdate]):
        return jsonify({'success': False, 'message': 'Todos los campos son requeridos'}), 400
    
    if len(password) < 8:
        return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 8 caracteres'}), 400
    
    # Intentar registrar usuario
    success = db_manager.register_user(name, email, password, birthdate)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.'
        })
    else:
        return jsonify({'success': False, 'message': 'Error al registrar usuario. Es posible que el correo ya esté en uso.'}), 400

@app.route('/vault')
def vault():
    """Página principal del vault - requiere autenticación"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('vault.html', 
                         user_name=session.get('user_name'),
                         user_email=session.get('user_email'))

@app.route('/api/vault/passwords')
def api_get_passwords():
    """API para obtener todas las contraseñas del usuario"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401
    
    try:
        user_id = session['user_id']
        master_key = session['master_key']
        
        vault_data = load_vault(master_key, user_id)
        
        # Convertir a formato para el frontend
        passwords = []
        for name, data in vault_data.items():
            passwords.append({
                'name': name,
                'user': data.get('user', ''),
                'description': data.get('description', '')
                # No enviamos la contraseña por seguridad
            })
        
        return jsonify({'success': True, 'passwords': passwords})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/vault/passwords', methods=['POST'])
def api_add_password():
    """API para agregar una nueva contraseña"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401
    
    data = request.get_json()
    
    name = data.get('name', '').strip()
    user = data.get('user', '').strip()
    password = data.get('password', '')
    description = data.get('description', '').strip()
    
    if not name or not password:
        return jsonify({'success': False, 'message': 'Nombre y contraseña son requeridos'}), 400
    
    try:
        user_id = session['user_id']
        master_key = session['master_key']
        
        # Cargar vault existente
        vault_data = load_vault(master_key, user_id)
        
        # Agregar nueva entrada
        vault_data[name] = {
            'user': user,
            'password': password,
            'description': description
        }
        
        # Guardar vault
        save_vault(vault_data, master_key, user_id)
        
        return jsonify({'success': True, 'message': 'Contraseña agregada exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/vault/passwords/<name>')
def api_get_password(name):
    """API para obtener una contraseña específica"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401
    
    try:
        user_id = session['user_id']
        master_key = session['master_key']
        
        vault_data = load_vault(master_key, user_id)
        
        if name not in vault_data:
            return jsonify({'success': False, 'message': 'Contraseña no encontrada'}), 404
        
        password_data = vault_data[name]
        return jsonify({
            'success': True,
            'data': {
                'name': name,
                'user': password_data.get('user', ''),
                'password': password_data.get('password', ''),
                'description': password_data.get('description', '')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/vault/passwords/<name>', methods=['DELETE'])
def api_delete_password(name):
    """API para eliminar una contraseña"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401
    
    try:
        user_id = session['user_id']
        master_key = session['master_key']
        
        vault_data = load_vault(master_key, user_id)
        
        if name not in vault_data:
            return jsonify({'success': False, 'message': 'Contraseña no encontrada'}), 404
        
        # Eliminar entrada
        del vault_data[name]
        
        # Guardar vault
        save_vault(vault_data, master_key, user_id)
        
        return jsonify({'success': True, 'message': 'Contraseña eliminada exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/verify-account-password', methods=['POST'])
def verify_account_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401

    data = request.get_json()
    password = data.get('password', '')
    user = db_manager.authenticate_user(session['user_email'], password)

    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401



@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('login'))

# Crear carpeta de vaults si no existe (para Render o local)
if not os.path.exists('vaults'):
    os.makedirs('vaults')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Iniciando LocalVault Web en puerto {port}...")
    app.run(host='0.0.0.0', port=port)

