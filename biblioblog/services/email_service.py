import smtplib
from email.message import EmailMessage

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM


class EmailService:
    """Servicio para enviar correos electrónicos."""

    def __init__(self):
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_password = SMTP_PASSWORD
        self.smtp_from = SMTP_FROM

    def can_send(self) -> bool:
        """Valida si hay configuración suficiente para enviar correos."""
        return all([
            self.smtp_host,
            self.smtp_port,
            self.smtp_user,
            self.smtp_password,
            self.smtp_from
        ])

    def send_email(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        """Envía un correo electrónico y devuelve True si fue exitoso."""
        if not self.can_send():
            print("Configuración SMTP incompleta. No se puede enviar el correo.")
            return False

        try:
            mensaje = EmailMessage()
            mensaje["Subject"] = asunto
            mensaje["From"] = self.smtp_from
            mensaje["To"] = destinatario
            mensaje.set_content(cuerpo)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as servidor:
                servidor.ehlo()
                servidor.starttls()
                servidor.ehlo()
                servidor.login(self.smtp_user, self.smtp_password)
                servidor.send_message(mensaje)

            print(f"Correo enviado correctamente a {destinatario}")
            return True

        except Exception as e:
            print(f"Error al enviar correo a {destinatario}: {e}")
            return False