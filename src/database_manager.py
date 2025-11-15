# src/database_manager.py
import mysql.connector
from mysql.connector import Error
import bcrypt
import hashlib
from typing import Optional, Dict, Any
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.host = 'localhost'
        self.database = 'Ciber_Vault_db'
        self.user = 'root'
        self.password = ''
    
    def connect(self):
        """Conecta a la base de datos MySQL"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    charset='utf8mb4',
                    use_unicode=True
                )
                print("Conexión a MySQL establecida")
            return True
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return False
    
    def disconnect(self):
        """Desconecta de la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a MySQL cerrada")
    
    def authenticate_user(self, correo: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario con correo y contraseña
        Retorna los datos del usuario si es exitoso, None si falla
        """
        if not self.connect():
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, nombre, correo, password_hash FROM usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            user = cursor.fetchone()
            
            if user and self._verify_password(password, user['password_hash']):
                # Remover el hash de la contraseña antes de retornar
                del user['password_hash']
                return user
            return None
            
        except Error as e:
            print(f"Error en autenticación: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def register_user(self, nombre: str, correo: str, password: str, fecha_nacimiento: str) -> bool:
        """
        Registra un nuevo usuario en la base de datos
        """
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # Verificar si el correo ya existe
            check_query = "SELECT id FROM usuarios WHERE correo = %s"
            cursor.execute(check_query, (correo,))
            if cursor.fetchone():
                print("El correo ya está registrado")
                return False
            
            # Hash de la contraseña
            password_hash = self._hash_password(password)
            
            # Insertar nuevo usuario
            insert_query = """
            INSERT INTO usuarios (nombre, correo, password_hash, fecha_nacimiento) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (nombre, correo, password_hash, fecha_nacimiento))
            self.connection.commit()
            
            print("Usuario registrado exitosamente")
            return True
            
        except Error as e:
            print(f"Error al registrar usuario: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su ID"""
        if not self.connect():
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, nombre, correo, fecha_nacimiento, fecha_registro FROM usuarios WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user
            
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def _hash_password(self, password: str) -> str:
        """Genera hash de la contraseña usando bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verifica una contraseña contra su hash"""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    def generate_master_key_for_user(self, user_id: int, user_password: str) -> str:
        """
        Genera una clave maestra única para el usuario basada en:
        - ID del usuario
        - Hash de su contraseña
        - Un salt único
        """
        # Crear un identificador único basado en el usuario
        unique_string = f"{user_id}_{user_password}_{self.database}"
        
        # Generar hash SHA256 para usar como clave maestra
        master_key = hashlib.sha256(unique_string.encode()).hexdigest()[:32]
        return master_key
    
    def __del__(self):
        """Destructor para cerrar conexión"""
        self.disconnect()