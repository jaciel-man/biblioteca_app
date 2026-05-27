from biblioblog.model.database import Database


class LibroModel:
    def obtener_libros(self):
        """Obtiene la lista de todos los libros disponibles."""
        return Database.fetchall("SELECT titulo, autor, anio, genero, precio_renta, stock, pdf_url FROM libros ORDER BY titulo")

    def agregar(self, titulo, autor, anio, genero, precio_renta=0.0, stock=0, pdf_url=''):
        """Agrega un nuevo libro a la base de datos."""
        if not titulo or not autor or not anio or not genero:
            return False

        existing = Database.fetchone(
            "SELECT 1 FROM libros WHERE lower(titulo)=lower(?) AND lower(autor)=lower(?)",
            (titulo, autor),
        )
        if existing:
            return False

        Database.execute(
            "INSERT INTO libros (titulo, autor, anio, genero, precio_renta, stock, pdf_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (titulo, autor, str(anio), genero, float(precio_renta), int(stock), pdf_url),
            commit=True,
        )

        return True

    def obtener_por_id(self, titulo):
        """Obtiene un libro específico por título."""
        return Database.fetchone(
            "SELECT titulo, autor, anio, genero, precio_renta, stock, pdf_url FROM libros WHERE lower(titulo)=lower(?)",
            (titulo,),
        )

    def eliminar(self, titulo):
        """Elimina un libro de la base de datos por título."""
        if not titulo:
            return False

        existing = Database.fetchone(
            "SELECT 1 FROM libros WHERE lower(titulo)=lower(?)",
            (titulo,),
        )
        if not existing:
            return False

        Database.execute(
            "DELETE FROM libros WHERE lower(titulo)=lower(?)",
            (titulo,),
            commit=True,
        )

        return True
