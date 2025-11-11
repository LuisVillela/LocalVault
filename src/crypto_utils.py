# src/crypto_utils.py
from cryptography.fernet import Fernet
import base64, hashlib, json

def generate_key(master_password: str):
    """Deriva una clave simétrica segura desde la contraseña maestra."""
    return base64.urlsafe_b64encode(hashlib.sha256(master_password.encode()).digest())

def encrypt_data(data: dict, master_password: str) -> bytes:
    key = generate_key(master_password)
    fernet = Fernet(key)
    json_data = json.dumps(data).encode()
    return fernet.encrypt(json_data)

def decrypt_data(encrypted_data: bytes, master_password: str) -> dict:
    key = generate_key(master_password)
    fernet = Fernet(key)
    decrypted_json = fernet.decrypt(encrypted_data).decode()
    return json.loads(decrypted_json)
