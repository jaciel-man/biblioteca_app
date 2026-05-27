from datetime import datetime
import sys
from biblioblog.model.database import Database
from biblioblog.utils.security import PasswordSecurity, InputValidation


class UsuarioModel:

    def registrar(self, user, password, correo, telefono, rol, codigo_verificacion=None, nombre='', apellido='', fecha_nacimiento=''):
        """Registra un nuevo usuario con código de verificación (solo clientes)."""
        # Validar entrada
        user = InputValidation.sanitize_input(user.strip() if user else "")
        password = password if password else ""
        correo = InputValidation.sanitize_input(correo.strip() if correo else "")
        telefono = InputValidation.sanitize_input(telefono.strip() if telefono else "")
        nombre = InputValidation.sanitize_input(nombre.strip() if nombre else "")
        apellido = InputValidation.sanitize_input(apellido.strip() if apellido else "")
        fecha_nacimiento = InputValidation.sanitize_input(fecha_nacimiento.strip() if fecha_nacimiento else "")
        
        if not user or not password or not correo or not telefono:
            return False
        
        # Validar formato del usuario
        is_valid, msg = InputValidation.validate_username(user)
        if not is_valid:
            return False
        
        # Validar email
        is_valid, msg = InputValidation.validate_email(correo)
        if not is_valid:
            return False
        
        # Hash de la contraseña
        try:
            password_hash = PasswordSecurity.hash_password(password)
        except Exception:
            return False
        
        fecha_registro = str(datetime.now())

        if rol == "cliente":
            if not codigo_verificacion:
                return False
            if Database.fetchone("SELECT 1 FROM clientes WHERE usuario = ?", (user,)):
                return False

            Database.execute(
                "INSERT INTO clientes (usuario, nombre, apellido, fecha_nacimiento, password, correo, telefono, fecha_registro, estado, verificado, codigo_verificacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user, nombre, apellido, fecha_nacimiento, password_hash, correo, telefono, fecha_registro, "activo", 0, codigo_verificacion),
                commit=True,
            )
            return True

        # Verificar si ya existe al menos un administrador principal
        admin_principal = Database.fetchone("SELECT 1 FROM administrador WHERE es_principal = 1")
        
        es_principal = 1 if not admin_principal else 0
        estado = "activo" if es_principal == 1 else "pendiente_aprobacion"

        Database.execute(
            "INSERT INTO administrador (usuario, nombre, apellido, fecha_nacimiento, password, correo, telefono, fecha_registro, estado, verificado, codigo_verificacion, es_principal) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user, nombre, apellido, fecha_nacimiento, password_hash, correo, telefono, fecha_registro, estado, 1, None, es_principal),
            commit=True,
        )

        return True

    def eliminar_usuario(self, user, rol):
        """Elimina un usuario de la base de datos."""
        if not user or not rol:
            return False

        if rol == "cliente":
            Database.execute("DELETE FROM clientes WHERE usuario = ?", (user,), commit=True)
        else:
            Database.execute("DELETE FROM administrador WHERE usuario = ?", (user,), commit=True)

        # Verifica que el usuario ya no existe
        existe = Database.fetchone(
            "SELECT 1 FROM clientes WHERE usuario = ?" if rol == "cliente" else "SELECT 1 FROM administrador WHERE usuario = ?",
            (user,),
        )
        return existe is None

    def login(self, user, password, rol):
        """Valida el login y devuelve estado de verificación."""
        if not user or not password:
            return False

        if rol == "cliente":
            row = Database.fetchone("SELECT password, verificado FROM clientes WHERE usuario = ?", (user,))
            if not row or not PasswordSecurity.verify_password(password, row.get("password")):
                return False
            if row.get("verificado") == 1:
                return True
            return "not_verified"

        row = Database.fetchone("SELECT password, verificado, estado FROM administrador WHERE usuario = ?", (user,))
        if not row or not PasswordSecurity.verify_password(password, row.get("password")):
            return False
        if row.get("estado") == "pendiente_aprobacion":
            return "pendiente_aprobacion"
        if row.get("verificado") == 1:
            return True
        return "not_verified"

    def obtener_codigo(self, user, rol):
        """Obtiene el código de verificación del usuario."""
        if rol == "cliente":
            row = Database.fetchone("SELECT codigo_verificacion FROM clientes WHERE usuario = ?", (user,))
            return row.get("codigo_verificacion") if row else None
        row = Database.fetchone("SELECT codigo_verificacion FROM administrador WHERE usuario = ?", (user,))
        return row.get("codigo_verificacion") if row else None

    def verificar_codigo(self, user, rol, codigo):
        """Verifica y marca a un usuario como verificado."""
        if not user or not codigo:
            return False

        row = Database.fetchone(
            "SELECT codigo_verificacion FROM clientes WHERE usuario = ?" if rol == "cliente" else "SELECT codigo_verificacion FROM administrador WHERE usuario = ?",
            (user,),
        )

        if not row or row.get("codigo_verificacion") != codigo:
            return False

        Database.execute(
            "UPDATE clientes SET verificado = 1, codigo_verificacion = NULL WHERE usuario = ?" if rol == "cliente" else "UPDATE administrador SET verificado = 1, codigo_verificacion = NULL WHERE usuario = ?",
            (user,),
            commit=True,
        )

        return True

    def actualizar_codigo(self, user, rol, nuevo_codigo):
        """Actualiza el código de verificación de un usuario."""
        if rol == "cliente":
            Database.execute(
                "UPDATE clientes SET codigo_verificacion = ? WHERE usuario = ?",
                (nuevo_codigo, user),
                commit=True,
            )
        else:
            Database.execute(
                "UPDATE administrador SET codigo_verificacion = ? WHERE usuario = ?",
                (nuevo_codigo, user),
                commit=True,
            )
        return True

    def obtener_correo(self, user, rol):
        """Obtiene el correo de un usuario."""
        if rol == "cliente":
            row = Database.fetchone("SELECT correo FROM clientes WHERE usuario = ?", (user,))
            return row.get("correo") if row else None

        row = Database.fetchone("SELECT correo FROM administrador WHERE usuario = ?", (user,))
        return row.get("correo") if row else None

    def obtener_todos_clientes(self):
        """Obtiene lista de todos los clientes."""
        rows = Database.fetchall(
            "SELECT usuario, correo, telefono, fecha_registro, estado FROM clientes ORDER BY usuario"
        )
        return rows

    def obtener_info_cliente(self, usuario):
        """Obtiene información detallada de un cliente."""
        return Database.fetchone(
            "SELECT usuario, correo, telefono, fecha_registro, estado FROM clientes WHERE usuario = ?",
            (usuario,),
        )

    def obtener_info_usuario(self, usuario, rol):
        """Obtiene información del usuario, cliente o administrador."""
        if rol == "cliente":
            return Database.fetchone(
                "SELECT usuario, correo, telefono, fecha_registro, estado FROM clientes WHERE usuario = ?",
                (usuario,),
            )
        return Database.fetchone(
            "SELECT usuario, correo, telefono, fecha_registro, estado FROM administrador WHERE usuario = ?",
            (usuario,),
        )

    def cambiar_estado_cliente(self, usuario, nuevo_estado):
        """Cambia el estado de un cliente (activo/suspendido)."""
        Database.execute(
            "UPDATE clientes SET estado = ? WHERE usuario = ?",
            (nuevo_estado, usuario),
            commit=True,
        )
        # Verifica que el cambio se realizó
        row = Database.fetchone("SELECT 1 FROM clientes WHERE usuario = ? AND estado = ?", (usuario, nuevo_estado))
        return bool(row)

    def cambiar_contraseña(self, user, rol, contraseña_actual, contraseña_nueva):
        """Cambia la contraseña de un usuario."""
        if rol == "cliente":
            row = Database.fetchone("SELECT password FROM clientes WHERE usuario = ?", (user,))
            if not row or not PasswordSecurity.verify_password(contraseña_actual, row.get("password")):
                return False

            try:
                password_hash = PasswordSecurity.hash_password(contraseña_nueva)
            except Exception:
                return False

            Database.execute(
                "UPDATE clientes SET password = ? WHERE usuario = ?",
                (password_hash, user),
                commit=True,
            )
            return True

        row = Database.fetchone("SELECT password FROM administrador WHERE usuario = ?", (user,))
        if not row or not PasswordSecurity.verify_password(contraseña_actual, row.get("password")):
            return False

        try:
            password_hash = PasswordSecurity.hash_password(contraseña_nueva)
        except Exception:
            return False

        Database.execute(
            "UPDATE administrador SET password = ? WHERE usuario = ?",
            (password_hash, user),
            commit=True,
        )
        return True

    def actualizar_perfil(self, user, rol, correo, telefono):
        """Actualiza correo y teléfono de un usuario."""
        if rol == "cliente":
            Database.execute(
                "UPDATE clientes SET correo = ?, telefono = ? WHERE usuario = ?",
                (correo, telefono, user),
                commit=True,
            )
        else:
            Database.execute(
                "UPDATE administrador SET correo = ?, telefono = ? WHERE usuario = ?",
                (correo, telefono, user),
                commit=True,
            )
        return True

    def validar_codigo_recuperacion(self, user, rol, codigo):
        """Valida el código de recuperación enviado por correo."""
        if rol == "cliente":
            row = Database.fetchone("SELECT codigo_verificacion FROM clientes WHERE usuario = ?", (user,))
        else:
            row = Database.fetchone("SELECT codigo_verificacion FROM administrador WHERE usuario = ?", (user,))
        return bool(row and row.get("codigo_verificacion") == codigo)

    def actualizar_contraseña_por_codigo(self, user, rol, nueva_contraseña):
        """Actualiza la contraseña usando código de recuperación."""
        try:
            password_hash = PasswordSecurity.hash_password(nueva_contraseña)
        except Exception:
            return False

        if rol == "cliente":
            Database.execute(
                "UPDATE clientes SET password = ?, codigo_verificacion = NULL WHERE usuario = ?",
                (password_hash, user),
                commit=True,
            )
        else:
            Database.execute(
                "UPDATE administrador SET password = ?, codigo_verificacion = NULL WHERE usuario = ?",
                (password_hash, user),
                commit=True,
            )
        return True

    def obtener_administradores_pendientes(self):
        """Obtiene la lista de administradores pendientes de aprobación."""
        rows = Database.fetchall(
            "SELECT usuario, correo, telefono, fecha_registro FROM administrador WHERE estado = 'pendiente_aprobacion' ORDER BY usuario"
        )
        return rows

    def aprobar_administrador(self, usuario):
        """Aprueba a un administrador pendiente."""
        Database.execute(
            "UPDATE administrador SET estado = 'activo' WHERE usuario = ?",
            (usuario,),
            commit=True,
        )
        return True

