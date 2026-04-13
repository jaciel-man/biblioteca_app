# 📚 BiblioBlog - Sistema de Biblioteca Mejorado

## ✨ Nuevas Características Implementadas

*Nota*: la aplicación ahora utiliza una base de datos SQLite (`biblioblog.db`) en lugar de almacenamiento JSON. Además se incluye un servicio opcional de notificaciones por correo para préstamos próximos a vencer (configurable mediante variables de entorno).

### 📊 **Sistema de Gestión Mejorado**

#### **Para Clientes:**
1. **📖 Pestaña de Libros**
   - Ver todos los libros disponibles en una tabla interactiva
   - Rentar libros con un click
   - Información completa: título, autor, año

2. **📋 Pestaña de Mis Préstamos**
   - Ver todos los préstamos activos y finalizados
   - Fecha de préstamo y vencimiento
   - Cantidad de renovaciones utilizadas
   - Estado actual del préstamo

3. **🔍 Pestaña de Búsqueda**
   - Buscar libros por título o autor
   - Resultados en tiempo real
   - Rentar directamente desde los resultados

4. **👤 Pestaña de Perfil**
   - Ver información personal
   - Cambiar contraseña (próximo)
   - Ver datos de registro

#### **Para Propietarios/Empleados:**
1. **➕ Agregar Libro**
   - Formulario mejorado para agregar nuevos libros
   - Validación de datos
   - Confirmación de éxito

2. **📚 Mis Libros**
   - Lista completa de todos los libros agregados
   - Tabla con título, autor y año
   - Gestión centralizada

3. **📋 Préstamos**
   - Ver TODOS los préstamos del sistema
   - Cliente, libro, fechas y estado
   - Seguimiento completo de cada transacción

4. **👥 Gestión de Clientes**
   - Lista de todos los clientes registrados
   - Información: correo, teléfono, estado
   - Datos de registro
   - Control de estado (activo/suspendido)

5. **📊 Estadísticas**
   - Total de libros en el sistema
   - Total de clientes registrados
   - Préstamos activos
   - Préstamos finalizados
   - Préstamos vencidos

6. **👤 Perfil del Propietario**
   - Información del administrador
   - Cambiar contraseña
   - Configuración de cuenta

---

### 🚀 **Funcionalidades Técnicas Adicionales**

#### **Modelo de Usuario Mejorado**
```python
- Registro con correo, teléfono, estado de verificación
- Login con validación
- Obtener correo de usuario
- Marcar como verificado
- Gestión de clientes (solo propietario)
- Cambio de contraseña
- Información detallada del cliente
```

#### **Modelo de Préstamos Mejorado**
```python
- Rentar con validaciones
- Devolver libro
- Renovar préstamo (máximo 2 renovaciones)
- Verificar préstamos próximos a vencer
- Obtener préstamos vencidos
- Historial completo de clientes
```

*El servicio de correo electrónico fue eliminado del proyecto.*

---

## 📱 **Interfaz Mejorada con Tabs**

### Sistema de Navegación por Pestañas
- Cada rol tiene sus propias pestañas
- Cambio de color para indicar pestaña activa
- Acceso rápido a todas las funciones
- Interfaz intuitiva y moderna

---

## 🔒 **Seguridad de Datos**

- ✅ Verificación de correo para nuevas cuentas
- ✅ Autenticación de dos factores (2FA) en login
- ✅ Validación de campos obligatorios
- ✅ Códigos de verificación con expiración
- ✅ Protección contra acceso no autorizado
- ✅ Almacenamiento seguro en SQLite (`biblioblog.db`) (sin encriptación de contraseña como se solicitó)

---


---

## 🗂️ **Estructura del Proyecto**

```
biblioblog/
├── main.py                      # Punto de entrada
├── controller/
│   └── app_controller.py        # Lógica principal de la aplicación
├── model/
│   ├── database.py              # Acceso a datos SQLite (migración automática desde JSON si existe)
│   ├── usuario.py               # Gestión de usuarios
│   ├── libros.py                # Gestión de libros
│   └── prestamos.py             # Gestión de préstamos
├── services/
   # (anteriormente se livraba un servicio de correo, ahora eliminado)
└── view/
    ├── app.py                   # Ventana principal
    ├── login_view.py            # Pantalla de login
    ├── registro_view.py         # Pantalla de registro
    ├── verificacion_view.py     # Pantalla de verificación de correo
    └── dashboard_view.py        # Panel principal (cliente/propietario)
```

---

## 💾 **Base de Datos (SQLite)**

- El sistema ahora utiliza una base de datos SQLite (`biblioblog.db`) ubicada en el mismo directorio del proyecto.
- Si existe un archivo `biblioblog_db.json`, se migran los datos automáticamente en el primer inicio.

### Configuración de correo (notificaciones)

El envío de correos se activa cuando se configuran las siguientes variables de entorno:

- `SMTP_HOST` (ej. `smtp.gmail.com`)
- `SMTP_PORT` (ej. `587`)
- `SMTP_USER` (usuario de correo)
- `SMTP_PASSWORD` (contraseña o token de aplicación)
- `SMTP_FROM` (dirección remitente; opcional, por defecto se usa `SMTP_USER`)

---

## 📝 **Cómo Usar**

### Registro
1. Click en "Crear nueva cuenta"
2. Llenar todos los campos
3. Seleccionar tipo de usuario (Cliente/Propietario)
4. Click en "Registrar"

### Login
1. Ingresar usuario y contraseña
2. Seleccionar tipo de usuario
3. Click en "Entrar"

### Rentar Libro (Cliente)
1. Ir a pestaña "Libros"
2. Click en el botón "Rentar" del libro deseado
3. El libro se alquila por 7 días

### Renovar Préstamo (Cliente)
1. Ir a pestaña "Mis Préstamos"
2. El sistema muestra las renovaciones disponibles
3. Máximo 2 renovaciones por préstamo

### Agregar Libro (Propietario)
1. Ir a pestaña "Agregar Libro"
2. Ingresar título, autor y año
3. Click en "Agregar Libro"

---

## 🎯 **Próximas Mejoras Sugeridas**

- [ ] Implementar cambio de contraseña
- [ ] Agregar multas por retraso
- [ ] Sistema de comentarios/reseñas
- [ ] Reserva de libros
- [ ] Reportes estadísticos avanzados
- [ ] Integración con gmail real
- [ ] Encriptación de contraseñas
- [ ] Base de datos SQL

---

## 📞 **Soporte**

Para reportar problemas o solicitar nuevas funciones, contacta al equipo de desarrollo.

---

**Versión**: 2.0  
**Fecha**: 4 de Marzo de 2026  
**Estado**: ✅ En Producción
