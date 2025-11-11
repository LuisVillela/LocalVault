from cryptography.fernet import Fernet
import base64, hashlib

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
