import tkinter as tk
from tkinter import messagebox, simpledialog
import pyperclip
from src.vault_manager import load_vault, save_vault


class LocalVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LocalVault – Password Edition")
        self.root.geometry("560x420")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        self.root.option_add("*Font", "Helvetica 11")

        # === Clave maestra ===
        self.master_key = simpledialog.askstring(
            "Clave Maestra",
            "Introduce tu clave maestra:",
            show="*"
        )
        if not self.master_key:
            messagebox.showerror("Error", "Debes ingresar una clave maestra.")
            self.root.destroy()
            return

        try:
            self.vault = load_vault(self.master_key)
        except Exception:
            messagebox.showwarning("Nuevo Vault", "No se encontró un archivo, se creará uno nuevo.")
            self.vault = {}

        # === Contenedor principal ===
        container = tk.Frame(root, bg="#1e1e1e", padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # === Título ===
        tk.Label(
            container,
            text="Gestor de Contraseñas",
            fg="#00bcd4",
            bg="#1e1e1e",
            font=("SF Pro Display", 18, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        # === Frame de lista ===
        list_frame = tk.Frame(container, bg="#1e1e1e")
        list_frame.pack(fill="both", expand=True)

        self.list_container = tk.Frame(list_frame, bg="#2a2a2a")
        self.list_container.pack(fill="both", expand=True)

        # === Botón agregar (fijo abajo) ===
        tk.Button(
            container,
            text="Agregar Contraseña",
            bg="#00bcd4",
            fg="white",
            relief="flat",
            font=("SF Pro Display", 12, "bold"),
            height=2,
            command=self.add_password
        ).pack(fill="x", pady=(15, 0))

        self.refresh_list()

    def refresh_list(self):
        # Limpiar lista
        for widget in self.list_container.winfo_children():
            widget.destroy()

        if not self.vault:
            tk.Label(
                self.list_container,
                text="No hay contraseñas guardadas.",
                fg="#aaaaaa",
                bg="#2a2a2a",
                font=("SF Pro Display", 11, "italic")
            ).pack(pady=20)
            return

        for name in self.vault.keys():
            row = tk.Frame(self.list_container, bg="#2a2a2a", pady=5)
            row.pack(fill="x", padx=4, pady=2)

            tk.Label(
                row,
                text=name,
                fg="white",
                bg="#2a2a2a",
                anchor="w"
            ).pack(side="left", padx=(8, 0), fill="x", expand=True)

            # Botones "View" y "Delete"
            tk.Button(
                row,
                text="View",
                bg="#2a2a2a",
                fg="#00bcd4",
                relief="flat",
                cursor="hand2",
                command=lambda n=name: self.view_password(n)
            ).pack(side="right", padx=(0, 10))
            tk.Button(
                row,
                text="Delete",
                bg="#2a2a2a",
                fg="#f44336",
                relief="flat",
                cursor="hand2",
                command=lambda n=name: self.delete_password(n)
            ).pack(side="right", padx=(0, 5))

    def add_password(self):
        name = simpledialog.askstring("Servicio", "Nombre del servicio:")
        if not name:
            return
        user = simpledialog.askstring("Usuario", "Nombre de usuario:")
        password = simpledialog.askstring("Contraseña", "Contraseña:")
        desc = simpledialog.askstring("Descripción", "Descripción (opcional):")

        if not password:
            messagebox.showerror("Error", "Debe ingresar una contraseña.")
            return

        self.vault[name] = {
            "user": user or "",
            "password": password,
            "description": desc or ""
        }
        save_vault(self.vault, self.master_key)
        self.refresh_list()

    def view_password(self, name):
        re_pass = simpledialog.askstring("Confirmar clave maestra", "Introduce tu clave maestra:", show="*")
        if not re_pass:
            return

        try:
            vault = load_vault(re_pass)
        except Exception:
            messagebox.showerror("Error", "Clave maestra incorrecta.")
            return

        item = vault.get(name)
        if not item:
            messagebox.showerror("Error", "Elemento no encontrado.")
            return

        # === Modal de detalles ===
        modal = tk.Toplevel(self.root)
        modal.title(f"{name}")
        modal.geometry("460x280")
        modal.configure(bg="#1e1e1e", padx=20, pady=20)
        modal.resizable(False, False)

        tk.Label(modal, text=name, fg="#00bcd4", bg="#1e1e1e",
                 font=("SF Pro Display", 16, "bold"), anchor="w").pack(fill="x", pady=(0, 15))

        info = f"Usuario: {item.get('user', '—')}\n\n" \
               f"Contraseña: {item.get('password', '—')}\n\n" \
               f"Descripción: {item.get('description', '—')}"
        tk.Label(modal, text=info, fg="white", bg="#1e1e1e",
                 justify="left", anchor="w", font=("SF Pro Display", 12)).pack(fill="x", pady=(0, 20))

        def copy_now():
            pyperclip.copy(item.get('password', ''))
            messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles (sin límite de tiempo).")

        tk.Button(modal, text="Copiar al Portapapeles", bg="#00bcd4", fg="white",
                  font=("SF Pro Display", 12, "bold"), relief="flat", height=2,
                  command=copy_now).pack(fill="x", pady=(10, 0))

        modal.transient(self.root)
        modal.grab_set()
        self.root.wait_window(modal)

    def delete_password(self, name):
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar {name}?")
        if confirm:
            self.vault.pop(name, None)
            save_vault(self.vault, self.master_key)
            self.refresh_list()
