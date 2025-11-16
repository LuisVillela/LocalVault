# src/auth_mac.py
import subprocess
from tkinter import simpledialog, messagebox

KEYCHAIN_SERVICE = "LocalVault_MasterPIN"

def set_pin(pin):
    """Guarda un nuevo PIN protegido por Touch ID en el llavero."""
    subprocess.run([
        "security", "add-generic-password",
        "-a", "local_user",
        "-s", KEYCHAIN_SERVICE,
        "-w", pin,
        "-U"
    ])

def get_pin():
    """Obtiene el PIN (esto invocará Touch ID o password del sistema)."""
    try:
        result = subprocess.check_output([
            "security", "find-generic-password",
            "-a", "local_user",
            "-s", KEYCHAIN_SERVICE,
            "-w"
        ], text=True)
        return result.strip()
    except subprocess.CalledProcessError:
        return None

def pin_exists():
    """Verifica si el PIN ya está almacenado."""
    try:
        subprocess.check_output([
            "security", "find-generic-password",
            "-a", "local_user",
            "-s", KEYCHAIN_SERVICE
        ])
        return True
    except subprocess.CalledProcessError:
        return False

def ensure_auth_gui(simpledialog, messagebox):
    """Controla la autenticación de inicio (PIN o Touch ID)."""
    if not pin_exists():
        # Configuración inicial
        pin = simpledialog.askstring("Configurar PIN", "Crea tu PIN de acceso:", show="*")
        if not pin:
            messagebox.showerror("Error", "Debes establecer un PIN.")
            return None
        confirm = simpledialog.askstring("Confirmar PIN", "Repite tu PIN:", show="*")
        if pin != confirm:
            messagebox.showerror("Error", "Los PIN no coinciden.")
            return None
        set_pin(pin)
        messagebox.showinfo("PIN creado", "Tu PIN fue guardado de forma segura en el llavero con Touch ID.")
        return pin
    else:
        # Intentar autenticación con Touch ID o PIN
        stored_pin = get_pin()
        if not stored_pin:
            messagebox.showerror("Error", "No se pudo autenticar con Touch ID.")
            return None
        return stored_pin

def biometric_check(messagebox):
    """Requiere Touch ID antes de mostrar contraseñas."""
    stored = get_pin()  # Esto lanza el diálogo Touch ID del sistema
    if not stored:
        messagebox.showerror("Error", "No se pudo autenticar con Touch ID.")
        return False
    return True
