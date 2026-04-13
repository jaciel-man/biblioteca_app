import concurrent.futures
import threading

from config import NOTIFICATION_CHECK_INTERVAL
from model.database import Database
from model.prestamos import PrestamoModel
from .email_service import EmailService


class NotificationService:
    """Servicio en segundo plano para enviar notificaciones por correo."""

    def __init__(self, prestamo_model: PrestamoModel = None, email_service: EmailService = None, interval: int = None):
        self.prestamo_model = prestamo_model or PrestamoModel()
        self.email_service = email_service or EmailService()
        self.interval = interval or NOTIFICATION_CHECK_INTERVAL

        self._stop_event = threading.Event()
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Detiene el hilo de notificaciones."""
        self._stop_event.set()
        self._thread.join(timeout=2)
        self._executor.shutdown(wait=False)

    def _run(self):
        """Bucle principal del servicio."""
        while not self._stop_event.is_set():
            try:
                self._process_notifications()
            except Exception as e:
                print(f"Error en NotificationService: {e}")

            self._stop_event.wait(self.interval)

    def _process_notifications(self):
        """Procesa las notificaciones pendientes de préstamos próximos a vencer."""
        if not self.email_service.can_send():
            print("No se puede procesar notificaciones: servicio de correo no configurado.")
            return

        prestamos = self.prestamo_model.verificar_prestamos_proximos_a_vencer()

        for prestamo in prestamos:
            prestamo_id = prestamo.get("id")
            if not prestamo_id:
                continue

            if Database.notificacion_enviada(prestamo_id, "vencimiento_proximo"):
                continue

            correo = prestamo.get("correo")
            if not correo:
                continue

            # Enviar notificación en un hilo separado para no bloquear el proceso principal
            self._executor.submit(self._send_notification, prestamo)

    def _send_notification(self, prestamo: dict):
        """Envía la notificación de vencimiento para un préstamo."""
        prestamo_id = prestamo.get("id")
        if not prestamo_id:
            return

        if Database.notificacion_enviada(prestamo_id, "vencimiento_proximo"):
            return

        correo = prestamo.get("correo")
        if not correo:
            return

        dias = prestamo.get("dias_restantes", 0)
        usuario = prestamo.get("usuario", "usuario")
        libro = prestamo.get("libro", "libro")
        fecha_vencimiento = prestamo.get("fecha_vencimiento", "fecha no disponible")

        asunto = "Recordatorio: préstamo próximo a vencer"
        cuerpo = (
            f"Hola {usuario},\n\n"
            f"Tu préstamo del libro '{libro}' vence en {dias} día(s), con fecha de vencimiento {fecha_vencimiento}.\n\n"
            "Por favor devuélvelo o renueva el préstamo para evitar sanciones.\n\n"
            "Saludos,\n"
            "BiblioBlog"
        )

        enviado = self.email_service.send_email(correo, asunto, cuerpo)

        if enviado:
            Database.marcar_notificacion_enviada(prestamo_id, "vencimiento_proximo")
            print(f"Notificación marcada como enviada para préstamo {prestamo_id}")