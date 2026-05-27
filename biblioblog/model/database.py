import json
import os
import sqlite3
import re
from datetime import datetime
from biblioblog.config import USE_MYSQL, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

DB_FILE = "biblioblog.db"
JSON_FILE = "biblioblog_db.json"

if USE_MYSQL:
    import pymysql
    import pymysql.cursors

class Database:
    @staticmethod
    def _get_connection():
        """Obtiene una conexion a la base de datos (SQLite o MySQL)."""
        if USE_MYSQL:
            conn = pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DB,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            return conn, "mysql"
        else:
            conn = sqlite3.connect(DB_FILE, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn, "sqlite"

    @staticmethod
    def _adapt_query(query, db_type):
        """Adapta la sintaxis de las consultas SQL al tipo de base de datos."""
        if db_type == "mysql":
            query = query.replace("AUTOINCREMENT", "AUTO_INCREMENT")
            query = query.replace("INSERT OR IGNORE", "INSERT IGNORE")
            query = query.replace("COLLATE NOCASE", "")
            # Reemplazar parámetros '?' de SQLite a '%s' de MySQL
            # Ojo: No reemplaza signos de interrogación en cadenas literal, pero
            # en nuestro código los '?' son exclusivamente para placeholders
            query = query.replace("?", "%s")
        return query

    @staticmethod
    def initialize():
        if USE_MYSQL:
            # Crear base de datos si no existe
            conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD)
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
            conn.close()

        conn, db_type = Database._get_connection()
        cur = conn.cursor()

        # Tablas principales
        cur.execute(Database._adapt_query(
            """
            CREATE TABLE IF NOT EXISTS administrador (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario VARCHAR(255) UNIQUE,
                nombre VARCHAR(255),
                apellido VARCHAR(255),
                fecha_nacimiento VARCHAR(50),
                password VARCHAR(255),
                correo VARCHAR(255),
                telefono VARCHAR(100),
                fecha_registro VARCHAR(100),
                estado VARCHAR(100),
                verificado INTEGER DEFAULT 0,
                codigo_verificacion VARCHAR(100),
                es_principal INTEGER DEFAULT 0
            )
            """, db_type))

        cur.execute(Database._adapt_query(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario VARCHAR(255) UNIQUE,
                nombre VARCHAR(255),
                apellido VARCHAR(255),
                fecha_nacimiento VARCHAR(50),
                password VARCHAR(255),
                correo VARCHAR(255),
                telefono VARCHAR(100),
                fecha_registro VARCHAR(100),
                estado VARCHAR(100),
                verificado INTEGER DEFAULT 0,
                codigo_verificacion VARCHAR(100)
            )
            """, db_type))

        cur.execute(Database._adapt_query(
            """
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo VARCHAR(255),
                autor VARCHAR(255),
                anio VARCHAR(50),
                precio_renta FLOAT DEFAULT 0.0,
                stock INTEGER DEFAULT 0,
                pdf_url VARCHAR(255),
                UNIQUE(titulo COLLATE NOCASE, autor COLLATE NOCASE)
            )
            """, db_type))

        # Agregar columnas si no existen (para retrocompatibilidad)
        try:
            cur.execute("ALTER TABLE libros ADD COLUMN genero VARCHAR(255) DEFAULT 'Sin Género'")
            cur.execute("ALTER TABLE libros ADD COLUMN precio_renta FLOAT DEFAULT 0.0")
            cur.execute("ALTER TABLE libros ADD COLUMN stock INTEGER DEFAULT 0")
            cur.execute("ALTER TABLE libros ADD COLUMN pdf_url VARCHAR(255)")
        except Exception:
            pass  # La columna ya existe

        cur.execute(Database._adapt_query(
            """
            CREATE TABLE IF NOT EXISTS rentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario VARCHAR(255),
                libro VARCHAR(255),
                fecha_renta VARCHAR(100),
                fecha_vencimiento VARCHAR(100),
                devuelto INTEGER DEFAULT 0,
                fecha_devolucion VARCHAR(100),
                renovaciones INTEGER DEFAULT 0,
                FOREIGN KEY(usuario) REFERENCES clientes(usuario)
            )
            """, db_type))

        cur.execute(Database._adapt_query(
            """
            CREATE TABLE IF NOT EXISTS notificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prestamo_id INTEGER,
                tipo VARCHAR(100),
                enviado_en VARCHAR(100),
                UNIQUE(prestamo_id, tipo)
            )
            """, db_type))

        if db_type == "sqlite":
            conn.commit()
            
        cur.close()
        conn.close()

        # Agregar columnas de verificación si no existen
        Database._add_column_if_not_exists("administrador", "verificado", "INTEGER DEFAULT 0")
        Database._add_column_if_not_exists("administrador", "codigo_verificacion", "VARCHAR(100)")
        Database._add_column_if_not_exists("administrador", "es_principal", "INTEGER DEFAULT 0")
        Database._add_column_if_not_exists("clientes", "verificado", "INTEGER DEFAULT 0")
        Database._add_column_if_not_exists("clientes", "codigo_verificacion", "VARCHAR(100)")
        Database._add_column_if_not_exists("administrador", "nombre", "VARCHAR(255)")
        Database._add_column_if_not_exists("administrador", "apellido", "VARCHAR(255)")
        Database._add_column_if_not_exists("administrador", "fecha_nacimiento", "VARCHAR(50)")
        Database._add_column_if_not_exists("clientes", "nombre", "VARCHAR(255)")
        Database._add_column_if_not_exists("clientes", "apellido", "VARCHAR(255)")
        Database._add_column_if_not_exists("clientes", "fecha_nacimiento", "VARCHAR(50)")

        # Migrar datos existentes desde JSON a SQLite si es necesario (sólo para SQLite)
        if not USE_MYSQL:
            Database._migrate_from_json()

    @staticmethod
    def _migrate_from_json():
        """Migra datos desde el archivo JSON existente (si existe) hacia SQLite."""
        if not os.path.exists(JSON_FILE):
            return

        conn, _ = Database._get_connection()
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

        administrador = data.get("administrador") or data.get("propietario")
        if administrador:
            cur.execute(
                "INSERT OR IGNORE INTO administrador (usuario, password, correo, telefono, fecha_registro, estado, es_principal) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (administrador.get("usuario"), administrador.get("password"), administrador.get("correo"),
                 administrador.get("telefono"), administrador.get("fecha_registro"), administrador.get("estado", "activo"), 1)
            )

        for usuario, info in data.get("clientes", {}).items():
            cur.execute(
                "INSERT OR IGNORE INTO clientes (usuario, password, correo, telefono, fecha_registro, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (usuario, info.get("password"), info.get("correo"), info.get("telefono"),
                 info.get("fecha_registro"), info.get("estado", "activo"))
            )

        for libro in data.get("libros", []):
            cur.execute(
                "INSERT OR IGNORE INTO libros (titulo, autor, anio) VALUES (?, ?, ?)",
                (libro.get("titulo"), libro.get("autor"), libro.get("anio"))
            )

        for renta in data.get("rentas", data.get("prestamos", [])):
            cur.execute(
                "INSERT OR IGNORE INTO rentas (usuario, libro, fecha_renta, fecha_vencimiento, devuelto, fecha_devolucion, renovaciones) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (renta.get("usuario"), renta.get("libro"), renta.get("fecha_renta", renta.get("fecha_prestamo")),
                 renta.get("fecha_vencimiento"), int(renta.get("devuelto", False)),
                 renta.get("fecha_devolucion"), int(renta.get("renovaciones", 0)))
            )

        conn.commit()
        conn.close()

    @staticmethod
    def _add_column_if_not_exists(table, column, definition):
        """Agrega una columna a la tabla si no existe."""
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table): raise ValueError("Nombre de tabla inválido")
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', column): raise ValueError("Nombre de columna inválido")
        
        conn, db_type = Database._get_connection()
        cur = conn.cursor()
        
        if db_type == "sqlite":
            cur.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cur.fetchall()]
        else:
            cur.execute(f"SHOW COLUMNS FROM {table}")
            columns = [row['Field'] for row in cur.fetchall()]
            
        if column not in columns:
            try:
                cur.execute(Database._adapt_query(f"ALTER TABLE {table} ADD COLUMN {column} {definition}", db_type))
                if db_type == "sqlite":
                    conn.commit()
            except Exception as e:
                print(f"Error adding column {column} to {table}: {e}")
        
        cur.close()
        conn.close()

    @staticmethod
    def fetchall(query, params=()):
        Database.initialize()
        conn, db_type = Database._get_connection()
        cur = conn.cursor()
        cur.execute(Database._adapt_query(query, db_type), params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if db_type == "sqlite":
            return [dict(r) for r in rows]
        return rows  # pymysql con DictCursor ya devuelve dicts

    @staticmethod
    def fetchone(query, params=()):
        Database.initialize()
        conn, db_type = Database._get_connection()
        cur = conn.cursor()
        cur.execute(Database._adapt_query(query, db_type), params)
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        if db_type == "sqlite":
            return dict(row)
        return row

    @staticmethod
    def execute(query, params=(), commit=False):
        Database.initialize()
        conn, db_type = Database._get_connection()
        cur = conn.cursor()
        cur.execute(Database._adapt_query(query, db_type), params)
        if commit or db_type == "sqlite":
            conn.commit()
        lastrowid = cur.lastrowid
        cur.close()
        conn.close()
        return lastrowid

    @staticmethod
    def marcar_notificacion_enviada(prestamo_id, tipo):
        Database.execute(
            "INSERT OR IGNORE INTO notificaciones (prestamo_id, tipo, enviado_en) VALUES (?, ?, ?)",
            (prestamo_id, tipo, datetime.now().isoformat()),
            commit=True,
        )

    @staticmethod
    def notificacion_enviada(prestamo_id, tipo):
        row = Database.fetchone(
            "SELECT 1 FROM notificaciones WHERE prestamo_id = ? AND tipo = ?", (prestamo_id, tipo)
        )
        return row is not None
