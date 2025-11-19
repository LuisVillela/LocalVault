# src/vault_manager.py
import os
import json
from typing import Dict, Optional


def get_vault_file(user_id: int) -> str:
    """Genera un nombre de archivo único para cada usuario (almacena JSON con blobs en base64)."""
    vault_dir = "vaults"
    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir, exist_ok=True)
    return os.path.join(vault_dir, f"vault_user_{user_id}.json")


def load_encrypted_vault(user_id: int) -> Dict[str, str]:
    """Carga el vault ENCRIPTADO del usuario como mapping name -> base64_blob"""
    vault_file = get_vault_file(user_id)
    if not os.path.exists(vault_file):
        return {}
    with open(vault_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # Expect a dict mapping name -> base64 blob
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}


def save_encrypted_vault(vault_dict: Dict[str, str], user_id: int):
    """Guarda el vault ENCRIPTADO (map name -> base64_blob) tal cual."""
    vault_file = get_vault_file(user_id)
    with open(vault_file, "w", encoding="utf-8") as f:
        json.dump(vault_dict, f, ensure_ascii=False)


def store_encrypted_entry(name: str, base64_blob: str, user_id: int):
    vault = load_encrypted_vault(user_id)
    vault[name] = base64_blob
    save_encrypted_vault(vault, user_id)


def get_encrypted_entry(name: str, user_id: int) -> Optional[str]:
    vault = load_encrypted_vault(user_id)
    return vault.get(name)


def delete_encrypted_entry(name: str, user_id: int):
    vault = load_encrypted_vault(user_id)
    if name in vault:
        del vault[name]
        save_encrypted_vault(vault, user_id)
