"""
Módulo de seguridad para BiblioBlog.
Maneja hashing de contraseñas y validación.
"""

import re
import hashlib
import secrets

# Desactivar bcrypt forzosamente para compatibilidad con Android (100% Python nativo)
HAS_BCRYPT = False

class PasswordSecurity:
    """Maneja seguridad de contraseñas con bcrypt o hashlib como fallback"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash seguro de la contraseña.
        Usa bcrypt si está disponible, sino hashlib con salt.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        if not isinstance(password, str) or not password:
            raise ValueError("La contraseña debe ser una cadena no vacía")
        
        if HAS_BCRYPT:
            # Usar bcrypt si está disponible (más seguro)
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password_bytes, salt)
            return hashed.decode('utf-8')
        else:
            # Fallback: usar hashlib con salt
            salt = secrets.token_hex(16)
            password_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000  # 100k iterations
            )
            return f"$pbkdf2${salt}${password_hash.hex()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verifica una contraseña contra su hash.
        Soporta tanto bcrypt como hashlib (fallback).
        
        Args:
            password: Contraseña en texto plano
            hashed: Hash de la contraseña
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            if not isinstance(password, str) or not password or not isinstance(hashed, str):
                return False
            
            # Si es hash de bcrypt
            if hashed.startswith('$2'):
                if HAS_BCRYPT:
                    password_bytes = password.encode('utf-8')
                    hashed_bytes = hashed.encode('utf-8')
                    return bcrypt.checkpw(password_bytes, hashed_bytes)
                else:
                    # No podemos verificar bcrypt sin la librería
                    return False
            
            # Si es hash de pbkdf2
            elif hashed.startswith('$pbkdf2$'):
                parts = hashed.split('$')
                if len(parts) != 4:
                    return False
                
                salt = parts[2]
                stored_hash = parts[3]
                
                password_hash = hashlib.pbkdf2_hmac(
                    'sha256',
                    password.encode('utf-8'),
                    salt.encode('utf-8'),
                    100000
                )
                
                return password_hash.hex() == stored_hash
            
            else:
                # Hash desconocido
                return False
                
        except Exception:
            return False
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple:
        """
        Valida la fortaleza de una contraseña.
        
        Args:
            password: Contraseña a validar
            
        Returns:
            Tuple (es_valida, mensaje)
        """
        if not password:
            return False, "La contraseña no puede estar vacía"
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        if len(password) > 128:
            return False, "La contraseña es demasiado larga (máximo 128 caracteres)"
        
        return True, "Contraseña válida"


class InputValidation:
    """Valida y sanitiza entrada de usuario"""
    
    @staticmethod
    def validate_username(username: str) -> tuple:
        """
        Valida el formato del nombre de usuario.
        
        Args:
            username: Nombre de usuario a validar
            
        Returns:
            Tuple (es_valido, mensaje)
        """
        if not username or not isinstance(username, str):
            return False, "El nombre de usuario no puede estar vacío"
        
        username = username.strip()
        
        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        
        if len(username) > 120:
            return False, "El nombre de usuario es demasiado largo (máximo 120 caracteres)"
        
        if not re.match(r'^[a-zA-Z0-9_@.-]+$', username):
            return False, "El nombre de usuario solo puede contener letras, números, guiones, puntos y @"
        
        return True, "Nombre de usuario válido"
    
    @staticmethod
    def validate_email(email: str) -> tuple:
        """
        Valida el formato del correo electrónico.
        
        Args:
            email: Correo a validar
            
        Returns:
            Tuple (es_valido, mensaje)
        """
        if not email or not isinstance(email, str):
            return False, "El correo no puede estar vacío"
        
        email = email.strip()
        
        # Expresión regular simple para validar emails
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "El formato del correo electrónico no es válido"
        
        if len(email) > 120:
            return False, "El correo es demasiado largo"
        
        return True, "Correo válido"
    
    @staticmethod
    def sanitize_input(user_input: str, max_length: int = 255) -> str:
        """
        Sanitiza entrada de usuario removiendo caracteres peligrosos.
        
        Args:
            user_input: Entrada a sanitizar
            max_length: Longitud máxima permitida
            
        Returns:
            Entrada sanitizada
        """
        if not isinstance(user_input, str):
            return ""
        
        # Remover espacios en blanco al inicio y final
        user_input = user_input.strip()
        
        # Limitar longitud
        if len(user_input) > max_length:
            user_input = user_input[:max_length]
        
        # Remover caracteres de control
        user_input = ''.join(char for char in user_input if ord(char) >= 32 or char in '\n\t\r')
        
        return user_input
