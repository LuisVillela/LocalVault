# src/vault_manager.py
import os
from pathlib import Path
from typing import Optional
from src.crypto_utils import encrypt_data, decrypt_data

# ✅ Carpeta absoluta del directorio de vaults (funciona en Render o local)
VAULTS_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vaults')))
VAULTS_DIR.mkdir(parents=True, exist_ok=True)

# Archivo vault local (modo escritorio sin user_id)
LOCAL_VAULT_FILE = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vault_local.enc')))

def get_vault_file(user_id: int) -> str:
    """Genera un nombre de archivo único para cada usuario"""
    return str(VAULTS_DIR / f"vault_user_{user_id}.enc")

def load_vault(master_password: str, user_id: Optional[int] = None):
    """Carga el vault cifrado del usuario o el vault local si user_id es None"""
    if user_id is None:
        vault_file = str(LOCAL_VAULT_FILE)
    else:
        vault_file = get_vault_file(user_id)

    if not os.path.exists(vault_file):
        return {}  # Vault vacío si no existe
    with open(vault_file, "rb") as f:
        blob = f.read()
    return decrypt_data(blob, master_password)

def save_vault(data: dict, master_password: str, user_id: Optional[int] = None):
    """Guarda el vault cifrado del usuario o en el vault local si user_id is None"""
    if user_id is None:
        vault_file = str(LOCAL_VAULT_FILE)
    else:
        vault_file = get_vault_file(user_id)

    try:
        blob = encrypt_data(data, master_password)
        with open(vault_file, "wb") as f:
            f.write(blob)
    except Exception as e:
        import traceback
        print(f"[❌ Error al guardar vault {vault_file}] {e}")
        traceback.print_exc()
        raise

