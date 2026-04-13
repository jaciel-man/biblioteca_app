import json
import os
import sqlite3
from datetime import datetime

DB_FILE = "biblioblog.db"
JSON_FILE = "biblioblog_db.json"


class Database:
    @staticmethod
    def _get_connection():
        """
        Obtiene una conexion a la base de datos SQLite.
        Se usa check_same_thread=False para permitir accesos desde multiples hilos.
        """

        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def initialize():
        conn = Database._get_connection()
        cur = conn.cursor()

        # Tablas principales
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS propietario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                password TEXT,
                correo TEXT,
                telefono TEXT,
                fecha_registro TEXT,
                estado TEXT,
                verificado INTEGER DEFAULT 0,
                codigo_verificacion TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                password TEXT,
                correo TEXT,
                telefono TEXT,
                fecha_registro TEXT,
                estado TEXT,
                verificado INTEGER DEFAULT 0,
                codigo_verificacion TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                autor TEXT,
                anio TEXT,
                UNIQUE(titulo COLLATE NOCASE, autor COLLATE NOCASE)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                libro TEXT,
                fecha_prestamo TEXT,
                fecha_vencimiento TEXT,
                devuelto INTEGER DEFAULT 0,
                fecha_devolucion TEXT,
                renovaciones INTEGER DEFAULT 0,
                FOREIGN KEY(usuario) REFERENCES clientes(usuario)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS notificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prestamo_id INTEGER,
                tipo TEXT,
                enviado_en TEXT,
                UNIQUE(prestamo_id, tipo)
            )
            """
        )

        conn.commit()
        conn.close()

        # Agregar columnas de verificación si no existen
        Database._add_column_if_not_exists("propietario", "verificado", "INTEGER DEFAULT 0")
        Database._add_column_if_not_exists("propietario", "codigo_verificacion", "TEXT")
        Database._add_column_if_not_exists("clientes", "verificado", "INTEGER DEFAULT 0")
        Database._add_column_if_not_exists("clientes", "codigo_verificacion", "TEXT")

        # Migrar datos existentes desde JSON a SQLite si es necesario
        Database._migrate_from_json()

    @staticmethod
    def _migrate_from_json():
        """Migra datos desde el archivo JSON existente (si existe) hacia SQLite."""
        if not os.path.exists(JSON_FILE):
            return

        # Si ya hay datos en la DB, asumimos que la migración ya se hizo.
        conn = Database._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM clientes")
        if cur.fetchone()[0] > 0:
            conn.close()
            return

        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            conn.close()
            return

        propietario = data.get("propietario")
        if propietario:
            cur.execute(
                "INSERT OR IGNORE INTO propietario (usuario, password, correo, telefono, fecha_registro, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    propietario.get("usuario"),
                    propietario.get("password"),
                    propietario.get("correo"),
                    propietario.get("telefono"),
                    propietario.get("fecha_registro"),
                    propietario.get("estado", "activo"),
                ),
            )

        for usuario, info in data.get("clientes", {}).items():
            cur.execute(
                "INSERT OR IGNORE INTO clientes (usuario, password, correo, telefono, fecha_registro, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    usuario,
                    info.get("password"),
                    info.get("correo"),
                    info.get("telefono"),
                    info.get("fecha_registro"),
                    info.get("estado", "activo"),
                ),
            )

        for libro in data.get("libros", []):
            cur.execute(
                "INSERT OR IGNORE INTO libros (titulo, autor, anio) VALUES (?, ?, ?)",
                (libro.get("titulo"), libro.get("autor"), libro.get("anio")),
            )

        for prestamo in data.get("prestamos", []):
            cur.execute(
                "INSERT OR IGNORE INTO prestamos (usuario, libro, fecha_prestamo, fecha_vencimiento, devuelto, fecha_devolucion, renovaciones) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    prestamo.get("usuario"),
                    prestamo.get("libro"),
                    prestamo.get("fecha_prestamo"),
                    prestamo.get("fecha_vencimiento"),
                    int(prestamo.get("devuelto", False)),
                    prestamo.get("fecha_devolucion"),
                    int(prestamo.get("renovaciones", 0)),
                ),
            )

        conn.commit()
        conn.close()

    @staticmethod
    def _add_column_if_not_exists(table, column, definition):
        conn = Database._get_connection()
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cur.fetchall()]
        if column not in columns:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
            conn.commit()
        conn.close()

    @staticmethod
    def fetchall(query, params=()):
        """Ejecuta una consulta SELECT y devuelve una lista de diccionarios."""
        Database.initialize()
        conn = Database._get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def fetchone(query, params=()):
        """Ejecuta una consulta SELECT y devuelve una fila (diccionario) o None."""
        Database.initialize()
        conn = Database._get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def execute(query, params=(), commit=False):
        """Ejecuta una consulta (INSERT/UPDATE/DELETE) y opcionalmente confirma."""
        Database.initialize()
        conn = Database._get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        if commit:
            conn.commit()
        lastrowid = cur.lastrowid
        conn.close()
        return lastrowid

    @staticmethod
    def marcar_notificacion_enviada(prestamo_id, tipo):
        """Registra que se ha enviado una notificación para un préstamo específico."""
        Database.execute(
            "INSERT OR IGNORE INTO notificaciones (prestamo_id, tipo, enviado_en) VALUES (?, ?, ?)",
            (prestamo_id, tipo, datetime.now().isoformat()),
            commit=True,
        )

    @staticmethod
    def notificacion_enviada(prestamo_id, tipo):
        """Comprueba si ya se envió una notificación para un préstamo y tipo dado."""
        row = Database.fetchone(
            "SELECT 1 FROM notificaciones WHERE prestamo_id = ? AND tipo = ?", (prestamo_id, tipo)
        )
        return row is not None
