# src/crypto_utils.py
import json, base64, os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(data: dict, password: str) -> bytes:
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    f = Fernet(key)
    payload = json.dumps(data).encode()
    token = f.encrypt(payload)
    # prepend salt so podemos derivar luego
    return salt + token

def decrypt_data(blob: bytes, password: str) -> dict:
    salt, token = blob[:16], blob[16:]
    key = _derive_key(password, salt)
    f = Fernet(key)
    decrypted = f.decrypt(token)
    return json.loads(decrypted.decode())
