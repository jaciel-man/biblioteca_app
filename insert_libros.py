from biblioblog.controller.app_controller import AppController

controller = AppController()
controller.rol_actual = 'administrador'

libros_para_insertar = [
    # Libros con PDF real (dummy de W3C o enlaces públicos para probar visor)
    ("Don Quijote de la Mancha", "Miguel de Cervantes", "1605", "Novela", 15.0, 5, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    ("Cien Años de Soledad", "Gabriel García Márquez", "1967", "Realismo Mágico", 20.0, 3, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    ("El Principito", "Antoine de Saint-Exupéry", "1943", "Fantasía", 10.0, 8, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    ("1984", "George Orwell", "1949", "Ciencia Ficción", 18.0, 4, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    ("Crimen y Castigo", "Fiódor Dostoyevski", "1866", "Novela", 14.0, 6, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    ("Orgullo y Prejuicio", "Jane Austen", "1813", "Romance", 12.0, 5, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    ("El Gran Gatsby", "F. Scott Fitzgerald", "1925", "Novela", 16.0, 7, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    ("Matar a un Ruiseñor", "Harper Lee", "1960", "Novela", 15.0, 4, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
    
    # Libros de otros géneros sin PDF
    ("El Hobbit", "J.R.R. Tolkien", "1937", "Fantasía", 18.0, 10, ""),
    ("Fahrenheit 451", "Ray Bradbury", "1953", "Ciencia Ficción", 15.0, 5, ""),
    ("Drácula", "Bram Stoker", "1897", "Terror", 12.0, 3, ""),
    ("Frankenstein", "Mary Shelley", "1818", "Terror", 12.0, 2, ""),
    ("Cumbres Borrascosas", "Emily Brontë", "1847", "Romance", 14.0, 4, ""),
    ("Jane Eyre", "Charlotte Brontë", "1847", "Romance", 14.0, 6, ""),
    ("Un Mundo Feliz", "Aldous Huxley", "1932", "Ciencia Ficción", 16.0, 5, ""),
    ("Los Miserables", "Victor Hugo", "1862", "Novela", 20.0, 2, ""),
    ("La Odisea", "Homero", "-800", "Historia", 10.0, 5, ""),
    ("La Ilíada", "Homero", "-750", "Historia", 10.0, 4, ""),
    ("Hamlet", "William Shakespeare", "1601", "Novela", 12.0, 8, ""),
    ("Romeo y Julieta", "William Shakespeare", "1597", "Romance", 12.0, 7, ""),
    ("El Código Da Vinci", "Dan Brown", "2003", "Misterio", 18.0, 10, ""),
    ("Ángeles y Demonios", "Dan Brown", "2000", "Misterio", 18.0, 8, ""),
    ("Harry Potter y la Piedra Filosofal", "J.K. Rowling", "1997", "Fantasía", 20.0, 15, ""),
    ("El Señor de los Anillos", "J.R.R. Tolkien", "1954", "Fantasía", 22.0, 12, ""),
    ("Crónicas Marcianas", "Ray Bradbury", "1950", "Ciencia Ficción", 14.0, 5, ""),
    ("Sapiens", "Yuval Noah Harari", "2011", "Ensayo / Historia", 19.0, 6, ""),
    ("Breve Historia del Tiempo", "Stephen Hawking", "1988", "Ensayo / Historia", 15.0, 4, ""),
    ("El Resplandor", "Stephen King", "1977", "Terror", 17.0, 7, ""),
    ("It", "Stephen King", "1986", "Terror", 18.0, 5, ""),
    ("La Sombra del Viento", "Carlos Ruiz Zafón", "2001", "Misterio", 16.0, 6, ""),
    ("Rayuela", "Julio Cortázar", "1963", "Realismo Mágico", 15.0, 4, ""),
    ("Pedro Páramo", "Juan Rulfo", "1955", "Realismo Mágico", 12.0, 5, ""),
    ("La Casa de los Espíritus", "Isabel Allende", "1982", "Realismo Mágico", 16.0, 7, ""),
    ("A Sangre Fría", "Truman Capote", "1966", "Misterio", 15.0, 5, ""),
    ("El Alquimista", "Paulo Coelho", "1988", "Fantasía", 14.0, 10, ""),
    ("El Nombre de la Rosa", "Umberto Eco", "1980", "Misterio", 17.0, 3, ""),
    ("Fundación", "Isaac Asimov", "1951", "Ciencia Ficción", 16.0, 6, ""),
    ("Dune", "Frank Herbert", "1965", "Ciencia Ficción", 18.0, 8, ""),
    ("Neuromante", "William Gibson", "1984", "Ciencia Ficción", 15.0, 4, ""),
    ("El Diario de Ana Frank", "Ana Frank", "1947", "Historia", 12.0, 7, "")
]

count = 0
for t, a, y, g, p, s, pdf in libros_para_insertar:
    if controller.agregar_libro(t, a, y, g, p, s, pdf):
        count += 1

print(f"Insertados exitosamente {count} libros.")
