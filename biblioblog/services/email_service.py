import smtplib
import ssl
from email.message import EmailMessage

from biblioblog.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM, SMTP_USE_TLS, SMTP_USE_SSL


class EmailService:
    """
    Servicio para enviar correos electrónicos.
    
    Soporta múltiples proveedores de SMTP:
    - Gmail (smtp.gmail.com:587) - TLS
    - Outlook/Hotmail (smtp-mail.outlook.com:587) - TLS
    - Yahoo (smtp.mail.yahoo.com:465 o 587) - TLS/SSL
    - Servidores SMTP genéricos
    """

    def __init__(self):
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_password = SMTP_PASSWORD
        self.smtp_from = SMTP_FROM
        self.use_tls = SMTP_USE_TLS
        self.use_ssl = SMTP_USE_SSL

    def can_send(self) -> bool:
        """Valida si hay configuración suficiente para enviar correos."""
        return all([
            self.smtp_host,
            self.smtp_port,
            self.smtp_user,
            self.smtp_password,
            self.smtp_from
        ])

    def _get_connection(self):
        """
        Obtiene una conexión SMTP configurada según el protocolo.
        
        Soporta:
        - SSL: Conexión segura desde el inicio (puerto 465)
        - TLS: Conexión STARTTLS (puerto 587)
        """
        try:
            import ssl
            # Usar un contexto no verificado para evitar problemas de certificados locales
            try:
                context = ssl._create_unverified_context()
            except AttributeError:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

            if self.use_ssl:
                # SSL: conexión segura desde el inicio
                servidor = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=15)
            else:
                # TLS: conexión con STARTTLS
                servidor = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15)
                servidor.ehlo()
                if self.use_tls:
                    servidor.starttls(context=context)
                    servidor.ehlo()
            
            return servidor
        except Exception as e:
            print(f"Error al conectar con servidor SMTP {self.smtp_host}:{self.smtp_port}: {e}")
            return None

    def send_email(self, destinatario: str, asunto: str, cuerpo: str, es_html: bool = False) -> bool:
        """
        Envía un correo electrónico y devuelve True si fue exitoso.
        
        Args:
            destinatario: Correo del destinatario
            asunto: Asunto del correo
            cuerpo: Contenido del correo (texto o HTML)
            es_html: Si True, el cuerpo se envía como HTML
        
        Returns:
            bool: True si fue exitoso, False en caso contrario
        """
        if not self.can_send():
            print("Configuración SMTP incompleta. No se puede enviar el correo.")
            return False

        servidor = None
        try:
            # Obtener conexión SMTP
            servidor = self._get_connection()
            if not servidor:
                return False

            # Crear mensaje
            mensaje = EmailMessage()
            mensaje["Subject"] = asunto
            mensaje["From"] = self.smtp_from
            mensaje["To"] = destinatario
            
            # Establecer contenido (texto o HTML)
            if es_html:
                mensaje.set_content(cuerpo, subtype="html")
            else:
                mensaje.set_content(cuerpo)

            # Autenticar y enviar
            servidor.login(self.smtp_user, self.smtp_password)
            servidor.send_message(mensaje)

            print(f"✓ Correo enviado correctamente a {destinatario}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"✗ Error de autenticación SMTP. Verifica usuario/contraseña: {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"✗ Error SMTP al enviar correo a {destinatario}: {e}")
            return False
        except Exception as e:
            print(f"✗ Error inesperado al enviar correo a {destinatario}: {e}")
            return False
        finally:
            if servidor:
                try:
                    servidor.quit()
                except:
                    pass