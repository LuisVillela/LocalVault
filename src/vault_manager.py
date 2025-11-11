# src/vault_manager.py
import os
from src.crypto_utils import encrypt_data, decrypt_data

VAULT_FILE = "vault.enc"

def load_vault(master_password: str):
    if not os.path.exists(VAULT_FILE):
        return {}  # nuevo vault vacío
    with open(VAULT_FILE, "rb") as f:
        blob = f.read()
    return decrypt_data(blob, master_password)

def save_vault(data: dict, master_password: str):
    blob = encrypt_data(data, master_password)
    with open(VAULT_FILE, "wb") as f:
        f.write(blob)
