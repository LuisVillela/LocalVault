# src/database_manager.py
import sqlite3
import bcrypt
import hashlib
from typing import Optional, Dict, Any
import os
from datetime import datetime

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vault.db'))

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._initialize_tables()

    def _initialize_tables(self):
        """Crea las tablas si no existen"""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                fecha_nacimiento TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def authenticate_user(self, correo: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica un usuario por correo y contraseña"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        user = cursor.fetchone()

        if user and self._verify_password(password, user['password_hash']):
            return dict(user)
        return None

    def register_user(self, nombre: str, correo: str, password: str, fecha_nacimiento: str) -> bool:
        """Registra un nuevo usuario"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE correo = ?", (correo,))
        if cursor.fetchone():
            return False  # correo ya registrado

        password_hash = self._hash_password(password)
        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, password_hash, fecha_nacimiento)
            VALUES (?, ?, ?, ?)
        """, (nombre, correo, password_hash, fecha_nacimiento))
        self.connection.commit()
        return True

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene datos de un usuario"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None

    def _hash_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def _verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def generate_master_key_for_user(self, user_id: int, user_password: str) -> str:
        """Genera una clave maestra única para cifrado"""
        unique_string = f"{user_id}_{user_password}_localvault"
        master_key = hashlib.sha256(unique_string.encode()).hexdigest()[:32]
        return master_key
