# src/vault_manager.py
import os
from src.crypto_utils import encrypt_data, decrypt_data

VAULT_FILE = "vault.enc"

def load_vault(master_password: str):
    """Carga el vault cifrado o crea uno nuevo si no existe."""
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()
    return decrypt_data(encrypted, master_password)

def save_vault(data: dict, master_password: str):
    """Guarda (encripta) el vault."""
    encrypted = encrypt_data(data, master_password)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)
