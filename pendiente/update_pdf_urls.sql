-- ============================================================
-- Script para actualizar la columna pdf_url de los libros
-- con enlaces reales de dominio público (Project Gutenberg / Archive.org)
-- Ejecuta esto en tu base de datos: USE biblioblog;
-- ============================================================

USE biblioblog;

UPDATE libros SET pdf_url = 'https://www.gutenberg.org/files/2701/2701-pdf.pdf'         WHERE titulo = '1984';
UPDATE libros SET pdf_url = 'https://www.gutenberg.org/files/1342/1342-pdf.pdf'         WHERE titulo = 'Orgullo y prejuicio';
UPDATE libros SET pdf_url = 'https://www.gutenberg.org/files/2600/2600-pdf.pdf'         WHERE titulo = 'La Odisea';
UPDATE libros SET pdf_url = 'https://www.gutenberg.org/files/135/135-pdf.pdf'           WHERE titulo = 'Los miserables';
UPDATE libros SET pdf_url = 'https://www.gutenberg.org/files/345/345-pdf.pdf'           WHERE titulo = 'Drácula';
UPDATE libros SET pdf_url = 'https://www.gutenberg.org/files/84/84-pdf.pdf'             WHERE titulo = 'Frankenstein';
UPDATE libros SET pdf_url = 'https://www.gutenberg.org/files/174/174-pdf.pdf'           WHERE titulo = 'El retrato de Dorian Gray';
UPDATE libros SET pdf_url = 'https://archive.org/download/elprincipito_202003/El_Principito.pdf' WHERE titulo = 'El Principito';
UPDATE libros SET pdf_url = 'https://archive.org/download/don-quijote-de-la-mancha_202009/Don_Quijote_de_la_Mancha.pdf' WHERE titulo = 'Don Quijote de la Mancha';

-- Para libros más modernos con derechos de autor, puedes usar rutas locales:
-- UPDATE libros SET pdf_url = 'file:///C:/Users/TU_USUARIO/Documentos/libros/cien_años_soledad.pdf' WHERE titulo = 'Cien años de soledad';
-- UPDATE libros SET pdf_url = 'file:///C:/Users/TU_USUARIO/Documentos/libros/1984.pdf' WHERE titulo = '1984';

-- Verificar que se aplicaron los cambios:
SELECT titulo, LEFT(pdf_url, 50) AS url_preview FROM libros WHERE pdf_url IS NOT NULL AND pdf_url != '';
