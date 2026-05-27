import os



SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "biblioblog.soporte@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "xxhq qydu shjq dxhq")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

# Protocolo de seguridad
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() == "true"  # Para STARTTLS (puerto 587)
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "False").lower() == "true"  # Para conexión SSL (puerto 465)

# ============================================================
# OTRAS CONFIGURACIONES
# ============================================================

# Base de datos
USE_MYSQL = os.getenv("USE_MYSQL", "True").lower() == "true"
MYSQL_HOST = os.getenv("MYSQL_HOST", "192.168.100.22")  # <-- Cambiado para la App Móvil
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "mysql")
MYSQL_DB = os.getenv("MYSQL_DB", "biblioblog")

# Tiempo en segundos entre verificaciones de préstamos próximos a vencer
NOTIFICATION_CHECK_INTERVAL = int(os.getenv("NOTIFICATION_CHECK_INTERVAL", "3600"))
