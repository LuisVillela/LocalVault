# src/vault_manager.py
import os
from src.crypto_utils import encrypt_data, decrypt_data

def get_vault_file(user_id: int) -> str:
    """Genera un nombre de archivo único para cada usuario"""
    vault_dir = "vaults"
    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir)
    return os.path.join(vault_dir, f"vault_user_{user_id}.enc")

def load_vault(master_password: str, user_id: int):
    vault_file = get_vault_file(user_id)
    if not os.path.exists(vault_file):
        return {}  # nuevo vault vacío
    with open(vault_file, "rb") as f:
        blob = f.read()
    return decrypt_data(blob, master_password)

def save_vault(data: dict, master_password: str, user_id: int):
    vault_file = get_vault_file(user_id)
    blob = encrypt_data(data, master_password)
    with open(vault_file, "wb") as f:
        f.write(blob)
