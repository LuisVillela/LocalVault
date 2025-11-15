# 📖 Guía de Configuración y Ejecución - LocalVault

> **Documentación paso a paso para configurar y ejecutar la aplicación LocalVault**  


---

## 📋 Índice
1. [Información General](#información-general)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación de MySQL](#instalación-de-mysql)
4. [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
5. [Instalación de Dependencias de Python](#instalación-de-dependencias-de-python)
6. [Verificación de la Configuración](#verificación-de-la-configuración)
7. [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
8. [Solución de Problemas](#solución-de-problemas)
9. [Registro de Cambios](#registro-de-cambios)

---

## 🎯 Información General

**LocalVault** es una aplicación web moderna desarrollada en Python que integra:
- **Sistema de autenticación** con base de datos MySQL
- **Gestor de contraseñas** con cifrado local por usuario
- **Interfaz web moderna** desarrollada con Flask y CSS moderno
- **Vaults personalizados** para cada usuario registrado
- **API REST** para todas las operaciones

### Arquitectura del Sistema
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Browser   │───▶│  Flask App       │───▶│  MySQL Database │
│   (localhost)   │    │  (Python/HTML)  │    │  (Ciber_Vault_db)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        ▼                        │
         │               ┌─────────────────┐              │
         └──────────────▶│   Vault Files   │◄─────────────┘
                         │   (Encrypted)   │
                         └─────────────────┘
```

---

## 🖥️ Requisitos del Sistema

### Sistema Operativo Soportado
- ✅ **macOS** (probado en macOS Sonoma)
- ✅ **Linux** (Ubuntu/Debian)
- ✅ **Windows** (con adaptaciones menores)

### Software Requerido
- **Python 3.8+** (recomendado 3.9 o superior)
- **MySQL 8.0+** (o MySQL 9.x)
- **pip** (gestor de paquetes de Python)
- **Homebrew** (solo para macOS, opcional)

---

## 🗄️ Instalación de MySQL

### En macOS (con Homebrew) - ✅ COMPLETADO
```bash
# 1. Verificar que Homebrew esté instalado
brew --version

# 2. Instalar MySQL
brew install mysql

# 3. Iniciar el servicio MySQL
brew services start mysql

# 4. Verificar instalación
mysql --version
```

**Resultado obtenido:**
```
✅ MySQL 9.5.0_2 instalado correctamente
✅ Servicio MySQL iniciado automáticamente
✅ Conexión sin contraseña para usuario root
```

### En Linux (Ubuntu/Debian)
```bash
# Actualizar repositorios
sudo apt update

# Instalar MySQL Server
sudo apt install mysql-server

# Iniciar servicio
sudo systemctl start mysql
sudo systemctl enable mysql

# Configuración segura (opcional)
sudo mysql_secure_installation
```

### En Windows
1. Descargar **MySQL Installer** desde: https://dev.mysql.com/downloads/installer/
2. Ejecutar el instalador y seguir el asistente
3. Configurar usuario root sin contraseña (para desarrollo local)

---

## 🎯 Configuración de la Base de Datos

### Paso 1: Crear la Base de Datos - ✅ COMPLETADO

**Archivo utilizado:** `database_setup.sql`

```sql
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS Ciber_Vault_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE Ciber_Vault_db;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_correo (correo),
    INDEX idx_fecha_registro (fecha_registro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Paso 2: Ejecutar el Script SQL - ✅ COMPLETADO
```bash
# Ejecutar desde la raíz del proyecto
mysql -u root < database_setup.sql
```

**Resultado verificado:**
```
✅ Base de datos 'Ciber_Vault_db' creada
✅ Tabla 'usuarios' creada con estructura correcta
✅ Índices configurados para optimización
```

### Paso 3: Verificar Configuración - ✅ COMPLETADO
```bash
# Listar bases de datos
mysql -u root -e "SHOW DATABASES;"

# Verificar estructura de tabla
mysql -u root -D Ciber_Vault_db -e "DESCRIBE usuarios;"

# Ver usuarios registrados (sin contraseñas)
mysql -u root -D Ciber_Vault_db -e "SELECT id, nombre, correo, fecha_nacimiento, fecha_registro FROM usuarios;"

# Contar total de usuarios
mysql -u root -D Ciber_Vault_db -e "SELECT COUNT(*) as total_usuarios FROM usuarios;"
```

### Comandos SQL Útiles
```bash
# Crear un usuario de prueba manualmente
mysql -u root -D Ciber_Vault_db -e "
INSERT INTO usuarios (nombre, correo, password_hash, fecha_nacimiento) 
VALUES ('Usuario Prueba', 'test@example.com', '\$2b\$12\$hash_example', '1990-01-01');
"

# Eliminar un usuario específico
mysql -u root -D Ciber_Vault_db -e "DELETE FROM usuarios WHERE correo = 'test@example.com';"

# Ver último usuario registrado
mysql -u root -D Ciber_Vault_db -e "SELECT * FROM usuarios ORDER BY fecha_registro DESC LIMIT 1;"
```

---

## 🐍 Instalación de Dependencias de Python

### Archivo requirements.txt
```
pyperclip
cryptography
mysql-connector-python
bcrypt
flask
```

### Instalación de Dependencias
```bash
# Instalar todas las dependencias
pip3 install -r requirements.txt

# O instalar individualmente
pip3 install pyperclip cryptography mysql-connector-python bcrypt flask
```

### Descripción de Dependencias
- **`pyperclip`** - Manejo del portapapeles del sistema
- **`cryptography`** - Cifrado y descifrado de vaults
- **`mysql-connector-python`** - Conexión con MySQL
- **`bcrypt`** - Hash seguro de contraseñas
- **`flask`** - Framework web para la interfaz de usuario

---

## ✅ Verificación de la Configuración

### Paso 1: Verificar Conexión MySQL - ✅ COMPLETADO
```bash
# Probar conexión desde Python
python3 -c "
from src.database_manager import DatabaseManager
db = DatabaseManager()
if db.connect():
    print('✅ Conexión exitosa a Ciber_Vault_db')
    db.disconnect()
else:
    print('❌ Error de conexión')
"
```

**Resultado:** ✅ Conexión exitosa a la base de datos Ciber_Vault_db

### Paso 2: Verificar Importaciones
```bash
# Verificar que todas las dependencias se importen correctamente
python3 -c "
import tkinter
import pyperclip
import mysql.connector
import bcrypt
from cryptography.fernet import Fernet
print('✅ Todas las dependencias importadas correctamente')
"
```

---

## 🚀 Ejecución de la Aplicación

### Aplicación Web (Recomendada)
```bash
# Ejecutar servidor web Flask
python3 app.py

# La aplicación estará disponible en:
# http://localhost:8080
```

### Aplicación de Escritorio (Alternativa)
```bash
# Ejecutar aplicación Tkinter
python3 main.py
```

### Flujo de Ejecución Web
1. **Servidor Flask** - Se inicia en puerto 8080
2. **Página de Login** - Abrir navegador en localhost:8080
3. **Registro/Login** - Pestañas para registro o inicio de sesión
4. **Autenticación** - Verificación contra base de datos MySQL
5. **Dashboard del Vault** - Interfaz web moderna para gestionar contraseñas

### Estructura de Archivos Completa
```
LocalVault/
├── app.py                     # Servidor Flask (WEB)
├── main.py                    # Aplicación Tkinter (ESCRITORIO)
├── templates/                 # Plantillas HTML
│   ├── login.html
│   └── vault.html
├── static/                    # Archivos estáticos
│   ├── css/style.css
│   └── js/
│       ├── login.js
│       └── vault.js
├── vaults/                    # Se crea automáticamente
│   └── vault_user_X.enc      # Archivos cifrados por usuario
├── src/
│   ├── database_manager.py
│   ├── login_window.py
│   ├── vault_manager.py
│   └── crypto_utils.py
└── gui/
    └── interface.py
```

---

## 🛠️ Solución de Problemas

### Error: "mysql.connector not found"
```bash
# Reinstalar dependencia
pip install --force-reinstall mysql-connector-python
```

### Error: "Connection refused MySQL"
```bash
# Verificar que MySQL esté ejecutándose
brew services restart mysql  # macOS
sudo systemctl restart mysql # Linux
```

### Error: "Access denied for user 'root'"
```bash
# Conectar a MySQL y verificar usuario
mysql -u root
# Si no funciona, configurar contraseña:
mysql -u root -p
```

### Error: "No module named 'src'"
```bash
# Asegurarse de ejecutar desde la raíz del proyecto
cd /ruta/a/LocalVault
python main.py
```
