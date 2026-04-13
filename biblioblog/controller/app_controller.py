from model.usuario import UsuarioModel
from model.libros import LibroModel
from model.prestamos import PrestamoModel
from services.email_service import EmailService

class AppController:

    def __init__(self):
        self.usuario_model = UsuarioModel()
        self.libro_model = LibroModel()
        self.prestamo_model = PrestamoModel()
        self.email_service = EmailService()

        self.usuario_actual = None
        self.rol_actual = None

    def registrar_usuario(self, user, password, correo, telefono, rol):
        """Registra un nuevo usuario (clientes con código, propietario sin código)."""
        if not all([user, password, correo, telefono]):
            return False

        if rol == "cliente":
            codigo = self._generar_codigo_verificacion()
            registrado = self.usuario_model.registrar(user, password, correo, telefono, rol, codigo)
            if not registrado:
                return False
            return codigo
        ##excepcion de codigo en este si pasa algo que no llena la pestaña que si esta basio o si preciona el cancelar este no lo registre la cuenta a la base de datos


        # Propietario no necesita código
        registrado = self.usuario_model.registrar(user, password, correo, telefono, rol)
        if not registrado:
            return False

        return True

    def login(self, user, password, rol):
        """Autentica un usuario y comprueba verificación."""
        if not user or not password:
            return False

        return self.usuario_model.login(user, password, rol)

    def _generar_codigo_verificacion(self):
        import random

        return "{:06d}".format(random.randint(0, 999999))

    def verificar_codigo(self, user, rol, codigo):
        return self.usuario_model.verificar_codigo(user, rol, codigo)

    def eliminar_usuario(self, user, rol):
        return self.usuario_model.eliminar_usuario(user, rol)

    def reenviar_codigo(self, user, rol):
        nuevo_codigo = self._generar_codigo_verificacion()
        self.usuario_model.actualizar_codigo(user, rol, nuevo_codigo)
        correo = self.usuario_model.obtener_correo(user, rol)
        if not correo:
            return False
        return self.enviar_confirmacion_registro(user, correo, nuevo_codigo)

    def enviar_confirmacion_registro(self, usuario, correo, codigo=None):
        """Envía un correo de confirmación tras el registro."""
        if not usuario or not correo:
            return False

        if not self.email_service.can_send():
            return False

        if codigo:
            asunto = "Confirmación de registro - BiblioBlog"
            cuerpo = (
                f"Hola {usuario},\n\n"
                "¡Gracias por registrarte en BiblioBlog!\n\n"
                f"Tu código de verificación es: {codigo}\n\n"
                "Ingresa este código en la pantalla de login para activar tu cuenta.\n\n"
                "Saludos,\n"
                "El equipo de BiblioBlog"
            )
        else:
            asunto = "Bienvenido a BiblioBlog"
            cuerpo = (
                f"Hola {usuario},\n\n"
                "Tu cuenta de propietario ha sido creada y activada correctamente.\n\n"
                "Ya puedes iniciar sesión directamente.\n\n"
                "Saludos,\n"
                "El equipo de BiblioBlog"
            )

        return self.email_service.send_email(correo, asunto, cuerpo)

    def obtener_libros(self):
        """Obtiene todos los libros disponibles"""
        return self.libro_model.obtener_libros()

    def agregar_libro(self, titulo, autor, anio):
        """Agrega un nuevo libro a la biblioteca"""
        if titulo and autor and anio:
            self.libro_model.agregar(titulo, autor, anio)
            return True
        return False

    def eliminar_libro(self, titulo):
        """Elimina un libro de la biblioteca (solo propietario)."""
        if self.rol_actual != "propietario" or not titulo:
            return False
        return self.libro_model.eliminar(titulo)

    def rentar_libro(self, titulo):
        """Renta un libro para el usuario actual"""
        if self.usuario_actual and titulo:
            self.prestamo_model.rentar(self.usuario_actual, titulo)
            return True
        return False

    def obtener_mis_prestamos(self):
        """Obtiene los préstamos del usuario actual"""
        if self.usuario_actual:
            return self.prestamo_model.obtener_por_usuario(self.usuario_actual)
        return []

    def obtener_todos_prestamos(self):
        """Obtiene todos los préstamos (solo para propietario)"""
        if self.rol_actual == "propietario":
            return self.prestamo_model.obtener_todos()
        return []

    def devolver_libro(self, usuario, titulo):
        """Devuelve un libro"""
        if self.rol_actual == "cliente" and self.usuario_actual == usuario:
            return self.prestamo_model.devolver_libro(usuario, titulo)
        elif self.rol_actual == "propietario":
            return self.prestamo_model.devolver_libro(usuario, titulo)
        return False

    def renovar_prestamo(self, usuario, titulo):
        """Renueva un préstamo por 7 días más"""
        if self.rol_actual == "cliente" and self.usuario_actual == usuario:
            return self.prestamo_model.renovar(usuario, titulo)
        elif self.rol_actual == "propietario":
            return self.prestamo_model.renovar(usuario, titulo)
        return False

    def obtener_clientes(self):
        """Obtiene lista de todos los clientes (solo para propietario)"""
        if self.rol_actual == "propietario":
            return self.usuario_model.obtener_todos_clientes()
        return []

    def obtener_info_cliente(self, usuario):
        """Obtiene información de un cliente específico"""
        if self.rol_actual == "propietario":
            return self.usuario_model.obtener_info_cliente(usuario)
        return None

    def obtener_info_usuario(self, user, rol):
        return self.usuario_model.obtener_info_usuario(user, rol)

    def actualizar_perfil(self, user, rol, correo, telefono):
        return self.usuario_model.actualizar_perfil(user, rol, correo, telefono)

    def cambiar_contraseña(self, user, rol, contraseña_actual, contraseña_nueva):
        return self.usuario_model.cambiar_contraseña(user, rol, contraseña_actual, contraseña_nueva)

    def solicitar_codigo_recuperacion(self, user, rol):
        codigo = self._generar_codigo_verificacion()
        if not self.usuario_model.actualizar_codigo(user, rol, codigo):
            return False
        correo = self.usuario_model.obtener_correo(user, rol)
        if not correo:
            return False
        asunto = "Recuperación de contraseña - BiblioBlog"
        cuerpo = (
            f"Hola {user},\n\n"
            "Has solicitado restablecer tu contraseña.\n\n"
            f"Tu código de recuperación es: {codigo}\n\n"
            "Ingresa este código en la app para cambiar tu contraseña.\n\n"
            "Si no solicitaste este código, ignora este correo.\n\n"
            "Saludos,\nEl equipo de BiblioBlog"
        )
        return self.email_service.send_email(correo, asunto, cuerpo)

    def verificar_codigo_recuperacion(self, user, rol, codigo):
        return self.usuario_model.validar_codigo_recuperacion(user, rol, codigo)

    def restablecer_contraseña_por_codigo(self, user, rol, codigo, nueva_contraseña):
        if not self.usuario_model.validar_codigo_recuperacion(user, rol, codigo):
            return False
        return self.usuario_model.actualizar_contraseña_por_codigo(user, rol, nueva_contraseña)

