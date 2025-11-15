# src/login_window.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from src.database_manager import DatabaseManager
import re

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LocalVault - Login")
        self.root.geometry("450x350")  # Hacer la ventana más grande
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        self.root.option_add("*Font", "{SF Pro Display} 11")
        
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.master_key = None
        
        # Centrar ventana
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def create_widgets(self):
        # === Contenedor principal ===
        container = tk.Frame(self.root, bg="#1e1e1e", padx=30, pady=30)
        container.pack(fill="both", expand=True)
        
        # === Título ===
        tk.Label(
            container,
            text="LocalVault",
            fg="#ffffff",
            bg="#1e1e1e",
            font=("SF Pro Display", 20, "bold"),
            anchor="center"
        ).pack(pady=(0, 30))
        
        # === Campo de correo ===
        tk.Label(
            container,
            text="Correo electrónico:",
            fg="#ffffff",
            bg="#1e1e1e",
            font=("SF Pro Display", 11)
        ).pack(anchor="w", pady=(0, 5))
        
        self.email_entry = tk.Entry(
            container,
            font=("SF Pro Display", 11),
            bg="#2a2a2a",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            borderwidth=2
        )
        self.email_entry.pack(fill="x", pady=(0, 15), ipady=8)
        
        # === Campo de contraseña ===
        tk.Label(
            container,
            text="Contraseña:",
            fg="#ffffff",
            bg="#1e1e1e",
            font=("SF Pro Display", 11)
        ).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            container,
            font=("SF Pro Display", 11),
            bg="#2a2a2a",
            fg="#ffffff",
            insertbackground="#ffffff",
            show="*",
            relief="flat",
            borderwidth=2
        )
        self.password_entry.pack(fill="x", pady=(0, 20), ipady=8)
        
        # === Botones ===
        # Botón de login
        login_btn = tk.Button(
            container,
            text="Iniciar Sesión",
            bg="#0f52ba",
            fg="#ffffff",
            font=("SF Pro Display", 12, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.login
        )
        login_btn.pack(fill="x", pady=(0, 15), ipady=10)
        
        # Separador visual
        separator = tk.Label(
            container,
            text="¿No tienes cuenta?",
            fg="#888888",
            bg="#1e1e1e",
            font=("SF Pro Display", 10)
        )
        separator.pack(pady=(0, 10))
        
        # Botón de registro (más visible)
        register_btn = tk.Button(
            container,
            text="Crear Nueva Cuenta",
            bg="#28a745",  # Verde para destacar
            fg="#ffffff",
            font=("SF Pro Display", 11, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.show_register_dialog
        )
        register_btn.pack(fill="x", ipady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus en el campo de correo
        self.email_entry.focus()
    
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        
        # Autenticar usuario
        user = self.db_manager.authenticate_user(email, password)
        
        if user:
            self.current_user = user
            # Generar clave maestra única para el usuario
            self.master_key = self.db_manager.generate_master_key_for_user(user['id'], password)
            
            messagebox.showinfo("Éxito", f"Bienvenido, {user['nombre']}!")
            self.root.destroy()  # Cerrar ventana de login
            return True
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")
            # Limpiar campos
            self.password_entry.delete(0, tk.END)
            self.email_entry.focus()
            return False
    
    def show_register_dialog(self):
        """Muestra el diálogo de registro"""
        register_window = RegisterDialog(self.root, self.db_manager)
        self.root.wait_window(register_window.dialog)
    
    def run(self):
        self.root.mainloop()
        return self.current_user, self.master_key


class RegisterDialog:
    def __init__(self, parent, db_manager):
        self.db_manager = db_manager
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Registro de Usuario")
        self.dialog.geometry("450x400")
        self.dialog.configure(bg="#1e1e1e")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar diálogo
        self.center_dialog(parent)
        
        self.create_widgets()
    
    def center_dialog(self, parent):
        """Centra el diálogo sobre la ventana padre"""
        self.dialog.update_idletasks()
        
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        pos_x = parent_x + (parent_width // 2) - (dialog_width // 2)
        pos_y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{pos_x}+{pos_y}")
    
    def create_widgets(self):
        container = tk.Frame(self.dialog, bg="#1e1e1e", padx=30, pady=20)
        container.pack(fill="both", expand=True)
        
        # Título
        tk.Label(
            container,
            text="Crear Nueva Cuenta",
            fg="#ffffff",
            bg="#1e1e1e",
            font=("SF Pro Display", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Campo nombre
        tk.Label(container, text="Nombre completo:", fg="#ffffff", bg="#1e1e1e").pack(anchor="w", pady=(0, 5))
        self.name_entry = tk.Entry(container, font=("SF Pro Display", 11), bg="#2a2a2a", fg="#ffffff", 
                                 insertbackground="#ffffff", relief="flat")
        self.name_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Campo correo
        tk.Label(container, text="Correo electrónico:", fg="#ffffff", bg="#1e1e1e").pack(anchor="w", pady=(0, 5))
        self.email_entry = tk.Entry(container, font=("SF Pro Display", 11), bg="#2a2a2a", fg="#ffffff", 
                                  insertbackground="#ffffff", relief="flat")
        self.email_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Campo contraseña
        tk.Label(container, text="Contraseña:", fg="#ffffff", bg="#1e1e1e").pack(anchor="w", pady=(0, 5))
        self.password_entry = tk.Entry(container, font=("SF Pro Display", 11), bg="#2a2a2a", fg="#ffffff", 
                                     insertbackground="#ffffff", show="*", relief="flat")
        self.password_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Campo fecha nacimiento
        tk.Label(container, text="Fecha de nacimiento (YYYY-MM-DD):", fg="#ffffff", bg="#1e1e1e").pack(anchor="w", pady=(0, 5))
        self.birthdate_entry = tk.Entry(container, font=("SF Pro Display", 11), bg="#2a2a2a", fg="#ffffff", 
                                      insertbackground="#ffffff", relief="flat")
        self.birthdate_entry.pack(fill="x", pady=(0, 20), ipady=5)
        
        # Botones
        btn_frame = tk.Frame(container, bg="#1e1e1e")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        tk.Button(
            btn_frame,
            text="Registrarse",
            bg="#0f52ba",
            fg="#ffffff",
            font=("SF Pro Display", 11, "bold"),
            relief="flat",
            command=self.register,
            cursor="hand2"
        ).pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=8)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            bg="#2a2a2a",
            fg="#ffffff",
            font=("SF Pro Display", 11),
            relief="flat",
            command=self.dialog.destroy,
            cursor="hand2"
        ).pack(side="right", fill="x", expand=True, padx=(5, 0), ipady=8)
        
        self.name_entry.focus()
    
    def validate_input(self, name, email, password, birthdate):
        """Valida los datos de entrada"""
        errors = []
        
        # Validar nombre
        if len(name.strip()) < 2:
            errors.append("El nombre debe tener al menos 2 caracteres")
        elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', name):
            errors.append("El nombre solo puede contener letras y espacios")
        
        # Validar email
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append("El formato del correo electrónico no es válido")
        
        # Validar contraseña
        if len(password) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres")
        elif len(re.findall(r'[A-Z]', password)) < 2:
            errors.append("La contraseña debe tener al menos 2 mayúsculas")
        elif not re.search(r'\d', password):
            errors.append("La contraseña debe tener al menos 1 dígito")
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("La contraseña debe tener al menos 1 carácter especial")
        
        # Validar fecha
        try:
            from datetime import datetime
            birth_date = datetime.strptime(birthdate, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 17:
                errors.append("Debes ser mayor de 17 años")
        except ValueError:
            errors.append("Formato de fecha inválido (use YYYY-MM-DD)")
        
        return errors
    
    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        birthdate = self.birthdate_entry.get().strip()
        
        # Validar entrada
        errors = self.validate_input(name, email, password, birthdate)
        
        if errors:
            messagebox.showerror("Errores de validación", "\n".join(errors))
            return
        
        # Intentar registrar usuario
        if self.db_manager.register_user(name, email, password, birthdate):
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario. Es posible que el correo ya esté en uso.")