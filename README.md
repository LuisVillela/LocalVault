# LocalVault 🔐
**Gestor de contraseñas moderno con interfaz web y encriptación AES-256**

## 📋 Descripción
LocalVault es un gestor de contraseñas completo que combina:
- 🌐 **Interfaz web moderna** con Flask y diseño responsive
- 🔒 **Encriptación AES-256** para máxima seguridad
- 🗄️ **Base de datos MySQL** para autenticación robusta
- 🛡️ **Almacenamiento local** sin dependencias cloud
- 📱 **Compatible** con desktop y móvil

## ⚡ Ejecución Rápida

### Aplicación Web (Recomendada)
```
📍 **Acceso:** http://localhost:8080

### Interfaz de Escritorio (Alternativa)
```bash
source venv/bin/activate
python3 gui/interface.py
```

### Configuración Original
```bash
source venv/bin/activate
python3 main.py
```

## 🚀 Características Principales

### 🌟 Interfaz Web
- **Login/Registro** con validación en tiempo real
- **Diseño responsive** adaptable a cualquier dispositivo
- **Gestión visual** de contraseñas con tarjetas organizadas
- **Modales interactivos** para agregar/editar contraseñas
- **Copia automática** al portapapeles con un clic

### 🔐 Seguridad
- **Encriptación AES-256** para archivos de contraseñas
- **Hashing bcrypt** para credenciales de usuarios
- **Claves maestras** únicas por usuario
- **Sesiones seguras** con Flask-Session
- **Almacenamiento local** sin exposición cloud

### 🛠️ Tecnologías
- **Backend:** Python 3.x, Flask, MySQL
- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **Seguridad:** cryptography, bcrypt, mysql-connector-python
- **UI/UX:** Gradientes, animaciones, iconos Font Awesome

## 📁 Estructura del Proyecto
```
LocalVault/
├── app.py                    # 🌐 Aplicación web Flask
├── main.py                   # 🔧 Script principal original
├── database_setup.sql        # 🗄️ Configuración MySQL
├── requirements.txt          # 📦 Dependencias Python
├── SETUP_GUIDE.md           # 📋 Guía completa de instalación
├── 
├── templates/               # 🎨 Plantillas HTML
│   ├── login.html          # 🔑 Página de autenticación
│   └── vault.html          # 🔐 Gestión de contraseñas
├── 
├── static/                  # 🎯 Recursos estáticos
│   └── css/
│       └── style.css       # 🎨 Estilos modernos
├── 
├── gui/                     # 🖥️ Interfaz de escritorio
│   └── interface.py        # 🐍 GUI Tkinter
├── 
├── src/                     # ⚙️ Lógica principal
│   ├── vault_manager.py    # 🔒 Gestión de contraseñas
│   ├── crypto_utils.py     # 🔐 Utilidades de encriptación
│   └── database_manager.py # 🗄️ Conexión MySQL
├── 
├── api/                     # 🌐 API original PHP
│   └── registro.php        # 📝 Sistema de registro
└── 
└── landing/                 # 🎯 Página de aterrizaje
    └── index.html          # 🏠 Página principal
```

## ⚙️ Instalación Completa

Para una guía paso a paso detallada, consulta **[SETUP_GUIDE.md](./SETUP_GUIDE.md)**

### Resumen Rápido:
1. **Clonar repositorio**
2. **Instalar MySQL** y crear base de datos
3. **Configurar entorno Python** con dependencias
4. **Ejecutar aplicación web** en puerto 8080
5. **¡Disfrutar!** 🎉


---
**💡 ¿Problemas de instalación?** Revisa [SETUP_GUIDE.md](./SETUP_GUIDE.md) para soluciones detalladas.bash
source venv/bin/activate
python3 app.py
