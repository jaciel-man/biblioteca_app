from datetime import datetime, timedelta

from biblioblog.model.database import Database


class PrestamoModel:

    def rentar(self, usuario, titulo):
        """Registra una nueva renta de libro."""
        if not usuario or not titulo:
            return False

        # Verificar stock
        libro_info = Database.fetchone(
            "SELECT stock FROM libros WHERE lower(titulo)=lower(?)", (titulo,)
        )
        if not libro_info:
            return False
        
        # En caso de MySQL dict, o SQLite Row:
        stock = libro_info.get('stock') if isinstance(libro_info, dict) else dict(libro_info).get('stock')
        if stock <= 0:
            return "sin_stock"

        # Verificar límite de rentas (máximo 3)
        activos = Database.fetchall(
            "SELECT id FROM rentas WHERE usuario = ? AND devuelto = 0",
            (usuario,),
        )
        if len(activos) >= 3:
            return "limite_alcanzado"

        # Verificar que el usuario no tiene el mismo libro rentado
        existente = Database.fetchone(
            "SELECT 1 FROM rentas WHERE usuario = ? AND lower(libro)=lower(?) AND devuelto = 0",
            (usuario, titulo),
        )
        if existente:
            return "ya_rentado"

        fecha = datetime.now().date()
        vencimiento = fecha + timedelta(days=7)

        Database.execute(
            """
            INSERT INTO rentas (usuario, libro, fecha_renta, fecha_vencimiento, devuelto, fecha_devolucion, renovaciones)
            VALUES (?, ?, ?, ?, 0, NULL, 0)
            """,
            (usuario, titulo, str(fecha), str(vencimiento)),
            commit=True,
        )
        
        # Reducir stock
        Database.execute(
            "UPDATE libros SET stock = stock - 1 WHERE lower(titulo)=lower(?)",
            (titulo,),
            commit=True
        )
        return True

    def obtener_por_usuario(self, usuario):
        """Obtiene todas las rentas de un usuario."""
        if not usuario:
            return []

        return Database.fetchall(
            "SELECT * FROM rentas WHERE usuario = ? ORDER BY fecha_renta DESC",
            (usuario,),
        )

    def devolver_libro(self, usuario, titulo):
        """Marca un libro como devuelto."""
        if not usuario or not titulo:
            return False

        # Marcar renta como devuelto
        Database.execute(
            """
            UPDATE rentas
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
            "SELECT 1 FROM rentas WHERE usuario = ? AND lower(libro)=lower(?) AND devuelto = 1",
            (usuario, titulo),
        )
        if updated:
            # Aumentar stock
            Database.execute(
                "UPDATE libros SET stock = stock + 1 WHERE lower(titulo)=lower(?)",
                (titulo,),
                commit=True
            )
            return True
        return False

    def renovar(self, usuario, titulo):
        """Renueva una renta por 7 días más."""
        if not usuario or not titulo:
            return False

        prestamo = Database.fetchone(
            "SELECT * FROM rentas WHERE usuario = ? AND lower(libro)=lower(?) AND devuelto = 0",
            (usuario, titulo),
        )
        if not prestamo:
            return False

        # Manejar caso dict / Row
        p_dict = dict(prestamo) if not isinstance(prestamo, dict) else prestamo

        renovaciones = p_dict.get("renovaciones", 0) or 0
        if renovaciones >= 2:
            return False

        fecha_vencimiento = datetime.strptime(p_dict["fecha_vencimiento"], "%Y-%m-%d").date()
        nueva_fecha_vencimiento = fecha_vencimiento + timedelta(days=7)

        Database.execute(
            """
            UPDATE rentas
            SET fecha_vencimiento = ?, renovaciones = renovaciones + 1
            WHERE id = ?
            """,
            (str(nueva_fecha_vencimiento), p_dict["id"]),
            commit=True,
        )
        return True

    def obtener_todos(self):
        """Obtiene todas las rentas registradas."""
        return Database.fetchall("SELECT * FROM rentas ORDER BY fecha_renta DESC")

    def verificar_prestamos_proximos_a_vencer(self, dias=2):
        """Verifica rentas próximos a vencer en los próximos `dias` días."""
        prestamos = Database.fetchall(
            """
            SELECT p.*, c.correo AS correo
            FROM rentas p
            LEFT JOIN clientes c ON p.usuario = c.usuario
            WHERE p.devuelto = 0
            """
        )

        hoy = datetime.now().date()
        resultados = []
        for prestamo in prestamos:
            p_dict = dict(prestamo) if not isinstance(prestamo, dict) else prestamo
            try:
                fecha_vencimiento = datetime.strptime(p_dict["fecha_vencimiento"], "%Y-%m-%d").date()
            except (TypeError, ValueError):
                continue

            dias_restantes = (fecha_vencimiento - hoy).days
            if 0 <= dias_restantes <= dias:
                prestamo_info = p_dict.copy()
                prestamo_info["dias_restantes"] = dias_restantes
                resultados.append(prestamo_info)

        return resultados

    def obtener_prestamos_vencidos(self):
        """Obtiene rentas que ya pasaron la fecha de vencimiento sin devolver."""
        prestamos = Database.fetchall(
            """
            SELECT p.*, c.correo AS correo
            FROM rentas p
            LEFT JOIN clientes c ON p.usuario = c.usuario
            WHERE p.devuelto = 0
            """
        )

        hoy = datetime.now().date()
        vencidos = []
        for prestamo in prestamos:
            p_dict = dict(prestamo) if not isinstance(prestamo, dict) else prestamo
            try:
                fecha_vencimiento = datetime.strptime(p_dict["fecha_vencimiento"], "%Y-%m-%d").date()
            except (TypeError, ValueError):
                continue

            if fecha_vencimiento < hoy:
                prestamo_info = p_dict.copy()
                prestamo_info["dias_vencido"] = (hoy - fecha_vencimiento).days
                vencidos.append(prestamo_info)

        return vencidos

    def obtener_historial_cliente(self, usuario):
        """Obtiene el historial completo de rentas de un cliente."""
        if not usuario:
            return []

        return Database.fetchall(
            "SELECT * FROM rentas WHERE usuario = ? ORDER BY fecha_renta DESC",
            (usuario,),
        )

    @staticmethod
    def obtener_correo_usuario(usuario):
        """Obtiene el correo de un usuario (método privado)."""
        if not usuario:
            return None

        row = Database.fetchone("SELECT correo FROM clientes WHERE usuario = ?", (usuario,))
        if row and dict(row).get("correo"):
            return dict(row).get("correo")

        row = Database.fetchone("SELECT correo FROM administrador WHERE usuario = ?", (usuario,))
        if row:
            return dict(row).get("correo")

        return None
