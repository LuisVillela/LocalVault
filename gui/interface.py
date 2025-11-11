import tkinter as tk
from tkinter import simpledialog, messagebox
from src.vault_manager import load_vault, save_vault

class LocalVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LocalVault – Password Edition")
        self.root.geometry("460x380")
        self.root.configure(bg="#1e1e1e")

        # ===== Clave maestra =====
        self.master_password = simpledialog.askstring(
            "Clave Maestra", "Introduce tu clave maestra:", show="*"
        )
        if not self.master_password:
            messagebox.showerror("Error", "Se requiere una clave maestra.")
            root.destroy()
            return

        # ===== Cargar o crear vault =====
        try:
            self.vault = load_vault(self.master_password)
        except Exception:
            messagebox.showerror("Error", "Clave incorrecta o vault dañado.")
            root.destroy()
            return

        # ===== UI Principal =====
        tk.Label(
            root, text="Gestor de Contraseñas", fg="#00bcd4",
            bg="#1e1e1e", font=("SF Pro Display", 18, "bold")
        ).pack(pady=(20, 10))

        self.listbox = tk.Listbox(root, bg="#2b2b2b", fg="white", width=50, height=10)
        self.listbox.pack(pady=10)
        self.update_listbox()

        tk.Button(root, text="Agregar Contraseña", command=self.add_password,
                  bg="#00bcd4", fg="white", relief="flat", width=20).pack(pady=5)

        tk.Button(root, text="Ver Contraseña", command=self.view_password,
                  bg="#4caf50", fg="white", relief="flat", width=20).pack(pady=5)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for key in self.vault.keys():
            self.listbox.insert(tk.END, f"🔒 {key}")

    def add_password(self):
        name = simpledialog.askstring("Servicio", "Nombre del servicio:")
        user = simpledialog.askstring("Usuario", "Usuario o correo:")
        password = simpledialog.askstring("Contraseña", "Contraseña:", show="*")
        description = simpledialog.askstring("Descripción", "Descripción breve:")

        if not name or not password:
            messagebox.showerror("Error", "Campos obligatorios.")
            return

        self.vault[name] = {
            "usuario": user,
            "password": password,
            "descripcion": description
        }
        save_vault(self.vault, self.master_password)
        self.update_listbox()
        messagebox.showinfo("Éxito", f"Contraseña para {name} guardada.")

    def view_password(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Selecciona un servicio.")
            return

        name = self.listbox.get(selection[0]).replace("🔒 ", "")
        item = self.vault.get(name)
        if not item:
            messagebox.showerror("Error", "Elemento no encontrado.")
            return

        msg = f"""
Servicio: {name}
Usuario: {item.get('usuario', '—')}
Contraseña: {item.get('password', '—')}
Descripción: {item.get('descripcion', '—')}
"""
        messagebox.showinfo("Detalle", msg)
