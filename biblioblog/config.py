import os

# Configuración de correo electrónico (usado por el servicio de notificaciones)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "biblioblog.soporte@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "xxhq qydu shjq dxhq")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

# Tiempo en segundos entre verificaciones de préstamos próximos a vencer
NOTIFICATION_CHECK_INTERVAL = int(os.getenv("NOTIFICATION_CHECK_INTERVAL", "3600"))
