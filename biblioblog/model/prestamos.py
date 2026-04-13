from datetime import datetime, timedelta

from model.database import Database


class PrestamoModel:

    def rentar(self, usuario, titulo):
        """Registra un nuevo préstamo de libro."""
        if not usuario or not titulo:
            return False

        # Verificar que el libro existe
        libro_existe = Database.fetchone(
            "SELECT 1 FROM libros WHERE lower(titulo)=lower(?)", (titulo,)
        )
        if not libro_existe:
            return False

        # Verificar que el usuario no tiene el mismo libro rentado
        existente = Database.fetchone(
            "SELECT 1 FROM prestamos WHERE usuario = ? AND lower(libro)=lower(?) AND devuelto = 0",
            (usuario, titulo),
        )
        if existente:
            return False

        fecha = datetime.now().date()
        vencimiento = fecha + timedelta(days=7)

        Database.execute(
            """
            INSERT INTO prestamos (usuario, libro, fecha_prestamo, fecha_vencimiento, devuelto, fecha_devolucion, renovaciones)
            VALUES (?, ?, ?, ?, 0, NULL, 0)
            """,
            (usuario, titulo, str(fecha), str(vencimiento)),
            commit=True,
        )
        return True

    def obtener_por_usuario(self, usuario):
        """Obtiene todos los préstamos de un usuario."""
        if not usuario:
            return []

        return Database.fetchall(
            "SELECT * FROM prestamos WHERE usuario = ? ORDER BY fecha_prestamo DESC",
            (usuario,),
        )

    def devolver_libro(self, usuario, titulo):
        """Marca un libro como devuelto."""
        if not usuario or not titulo:
            return False

        # Marcar préstamo como devuelto
        Database.execute(
            """
            UPDATE prestamos
            SET devuelto = 1,
                fecha_devolucion = ?
            WHERE usuario = ?
              AND lower(libro) = lower(?)
              AND devuelto = 0
            """,
            (str(datetime.now().date()), usuario, titulo),
            commit=True,
        )

        updated = Database.fetchone(
            "SELECT 1 FROM prestamos WHERE usuario = ? AND lower(libro)=lower(?) AND devuelto = 1",
            (usuario, titulo),
        )
        return bool(updated)

    def renovar(self, usuario, titulo):
        """Renueva un préstamo por 7 días más."""
        if not usuario or not titulo:
            return False

        prestamo = Database.fetchone(
            "SELECT * FROM prestamos WHERE usuario = ? AND lower(libro)=lower(?) AND devuelto = 0",
            (usuario, titulo),
        )
        if not prestamo:
            return False

        renovaciones = prestamo.get("renovaciones", 0) or 0
        if renovaciones >= 2:
            return False

        fecha_vencimiento = datetime.strptime(prestamo["fecha_vencimiento"], "%Y-%m-%d").date()
        nueva_fecha_vencimiento = fecha_vencimiento + timedelta(days=7)

        Database.execute(
            """
            UPDATE prestamos
            SET fecha_vencimiento = ?, renovaciones = renovaciones + 1
            WHERE id = ?
            """,
            (str(nueva_fecha_vencimiento), prestamo["id"]),
            commit=True,
        )
        return True

    def obtener_todos(self):
        """Obtiene todos los préstamos registrados."""
        return Database.fetchall("SELECT * FROM prestamos ORDER BY fecha_prestamo DESC")

    def verificar_prestamos_proximos_a_vencer(self, dias=2):
        """Verifica préstamos próximos a vencer en los próximos `dias` días."""
        prestamos = Database.fetchall(
            """
            SELECT p.*, c.correo AS correo
            FROM prestamos p
            LEFT JOIN clientes c ON p.usuario = c.usuario
            WHERE p.devuelto = 0
            """
        )

        hoy = datetime.now().date()
        resultados = []
        for prestamo in prestamos:
            try:
                fecha_vencimiento = datetime.strptime(prestamo["fecha_vencimiento"], "%Y-%m-%d").date()
            except (TypeError, ValueError):
                continue

            dias_restantes = (fecha_vencimiento - hoy).days
            if 0 <= dias_restantes <= dias:
                prestamo_info = dict(prestamo)
                prestamo_info["dias_restantes"] = dias_restantes
                resultados.append(prestamo_info)

        return resultados

    def obtener_prestamos_vencidos(self):
        """Obtiene préstamos que ya pasaron la fecha de vencimiento sin devolver."""
        prestamos = Database.fetchall(
            """
            SELECT p.*, c.correo AS correo
            FROM prestamos p
            LEFT JOIN clientes c ON p.usuario = c.usuario
            WHERE p.devuelto = 0
            """
        )

        hoy = datetime.now().date()
        vencidos = []
        for prestamo in prestamos:
            try:
                fecha_vencimiento = datetime.strptime(prestamo["fecha_vencimiento"], "%Y-%m-%d").date()
            except (TypeError, ValueError):
                continue

            if fecha_vencimiento < hoy:
                prestamo_info = dict(prestamo)
                prestamo_info["dias_vencido"] = (hoy - fecha_vencimiento).days
                vencidos.append(prestamo_info)

        return vencidos

    def obtener_historial_cliente(self, usuario):
        """Obtiene el historial completo de préstamos de un cliente."""
        if not usuario:
            return []

        return Database.fetchall(
            "SELECT * FROM prestamos WHERE usuario = ? ORDER BY fecha_prestamo DESC",
            (usuario,),
        )

    @staticmethod
    def obtener_correo_usuario(usuario):
        """Obtiene el correo de un usuario (método privado)."""
        if not usuario:
            return None

        row = Database.fetchone("SELECT correo FROM clientes WHERE usuario = ?", (usuario,))
        if row and row.get("correo"):
            return row.get("correo")

        row = Database.fetchone("SELECT correo FROM propietario WHERE usuario = ?", (usuario,))
        if row:
            return row.get("correo")

        return None
