import subprocess
import os

def biometric_check():
    """Verifica Touch ID en macOS."""
    try:
        result = subprocess.run(
            ["osascript", "-e",
             'display dialog "Autenticación Touch ID requerida" buttons {"Cancelar", "Continuar"} default button "Continuar"'],
            capture_output=True
        )
        return result.returncode == 0
    except Exception:
        return False

def ensure_auth_gui(simpledialog, messagebox):
    """Pide un PIN al usuario para autenticación local."""
    pin = simpledialog.askstring("Autenticación", "Introduce tu PIN de acceso:", show="*")
    if not pin:
        messagebox.showerror("Error", "Debes ingresar un PIN para continuar.")
        return None
    return pin
