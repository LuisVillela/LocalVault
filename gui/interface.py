import tkinter as tk
from tkinter import messagebox, simpledialog
import pyperclip, threading, time
from src.vault_manager import load_vault, save_vault

class LocalVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LocalVault – Password Edition")
        self.root.geometry("520x400")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        # === Paso 1: pedir clave maestra ===
        self.master_key = simpledialog.askstring(
            "Clave Maestra",
            "Introduce tu clave maestra:",
            show="*"
        )
        if not self.master_key:
            messagebox.showerror("Error", "Debes ingresar una clave maestra.")
            self.root.destroy()
            return

        # === Paso 2: intentar cargar o crear el vault ===
        try:
            self.vault = load_vault(self.master_key)
        except Exception:
            messagebox.showwarning("Nuevo Vault", "No se encontró un archivo, se creará uno nuevo.")
            self.vault = {}

        # === Título ===
        tk.Label(
            root,
            text="🔒 Gestor de Contraseñas",
            fg="#00bcd4",
            bg="#1e1e1e",
            font=("SF Pro Display", 16, "bold")
        ).pack(pady=15)

        # === Listbox para mostrar los servicios ===
        self.listbox = tk.Listbox(
            root,
            bg="#2e2e2e",
            fg="white",
            selectbackground="#00bcd4",
            font=("SF Pro Display", 12),
            width=40,
            height=10,
            relief="flat"
        )
        self.listbox.pack(pady=10)

        # Cargar los elementos existentes
        self.refresh_list()

        # === Botones principales ===
        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="➕ Agregar",
            bg="#4caf50",
            fg="white",
            relief="flat",
            width=12,
            command=self.add_password
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="👁 Ver",
            bg="#2196f3",
            fg="white",
            relief="flat",
            width=12,
            command=self.view_password
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="🗑 Eliminar",
            bg="#f44336",
            fg="white",
            relief="flat",
            width=12,
            command=self.delete_password
        ).grid(row=0, column=2, padx=5)

    # === Refrescar lista ===
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in self.vault.keys():
            self.listbox.insert(tk.END, f"🔒 {name}")

    # === Agregar nueva contraseña ===
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

    # === Ver contraseña (copiar al portapapeles) ===
    def view_password(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un servicio.")
            return
        name = self.listbox.get(sel[0]).replace("🔒 ", "")

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

        pw = item.get("password")
        pyperclip.copy(pw)
        messagebox.showinfo(
            "Copiado",
            f"Contraseña de {name} copiada al portapapeles por 10 segundos."
        )

        def clear_clip():
            time.sleep(10)
            if pyperclip.paste() == pw:
                pyperclip.copy("")
        threading.Thread(target=clear_clip, daemon=True).start()

    # === Eliminar contraseña ===
    def delete_password(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un servicio para eliminar.")
            return
        name = self.listbox.get(sel[0]).replace("🔒 ", "")
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar {name}?")
        if confirm:
            self.vault.pop(name, None)
            save_vault(self.vault, self.master_key)
            self.refresh_list()
