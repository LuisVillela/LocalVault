import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64, hashlib, os

# ====== Funciones de cifrado/descifrado ======
def generate_key(password: str):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    new_path = file_path + ".enc"
    with open(new_path, 'wb') as f:
        f.write(encrypted)
    return new_path

def decrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)
    with open(file_path, 'rb') as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    new_path = file_path.replace(".enc", "_dec.txt")
    with open(new_path, 'wb') as f:
        f.write(decrypted)
    return new_path


# ====== Interfaz principal ======
class LocalVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LocalVault")
        self.root.geometry("420x320")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.file_path = None

        # ====== Layout ======
        tk.Label(root, text="🔒 LocalVault", fg="#00bcd4", bg="#1e1e1e",
                 font=("SF Pro Display", 18, "bold")).pack(pady=(25, 10))

        self.path_label = tk.Label(root, text="Ningún archivo seleccionado", fg="white",
                                   bg="#1e1e1e", font=("SF Pro Display", 10))
        self.path_label.pack(pady=5)

        tk.Button(root, text="Seleccionar archivo", command=self.select_file,
                  bg="#00bcd4", fg="white", relief="flat", width=20, height=1).pack(pady=8)

        tk.Label(root, text="Contraseña:", fg="white", bg="#1e1e1e",
                 font=("SF Pro Display", 10)).pack(pady=(10, 0))
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Encriptar", command=self.encrypt_action,
                  bg="#4caf50", fg="white", relief="flat", width=15, height=1).pack(pady=10)

        tk.Button(root, text="Desencriptar", command=self.decrypt_action,
                  bg="#f44336", fg="white", relief="flat", width=15, height=1).pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.path_label.config(text=os.path.basename(file_path))

    def encrypt_action(self):
        if not self.file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero.")
            return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Introduce una contraseña.")
            return
        try:
            out = encrypt_file(self.file_path, password)
            messagebox.showinfo("Éxito", f"Archivo encriptado:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_action(self):
        if not self.file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero.")
            return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Introduce una contraseña.")
            return
        try:
            out = decrypt_file(self.file_path, password)
            messagebox.showinfo("Éxito", f"Archivo desencriptado:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = LocalVaultApp(root)
    root.mainloop()
