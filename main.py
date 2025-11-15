# main.py
import tkinter as tk
from gui.interface import LocalVaultApp
from src.login_window import LoginWindow
import sys

def main():
    try:
        # Mostrar ventana de login primero
        login = LoginWindow()
        user_data, master_key = login.run()
        
        # Si no se autenticó, salir
        if not user_data or not master_key:
            print("Login cancelado o fallido")
            sys.exit(0)
        
        # Si se autenticó exitosamente, mostrar vault
        root = tk.Tk()
        app = LocalVaultApp(root, user_data, master_key)
        root.mainloop()
        
    except Exception as e:
        print(f"[Error crítico] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
