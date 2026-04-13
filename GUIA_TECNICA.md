# 🔑 Guía Técnica - Verificación por Correo y Sistema de Lógica de Negocios

*Nota*: las funcionalidades de verificación por correo y notificaciones se han eliminado del sistema. El registro e inicio de sesión ahora son directos sin envío de mensajes.

---

## 🎯 Lógica de Negocio para Clientes

### Renta de Libros

```python
# Validaciones Previas:
1. ¿Existe el libro? → Si no, rechazar
2. ¿El cliente ya tiene este libro rentado? → Si sí, rechazar
3. ¿El cliente está activo? → Si no, rechazar

# Proceso:
- Fecha Préstamo: HOY
- Fecha Vencimiento: HOY + 7 días
- Estado: "Activo"
- Renovaciones: 0 (máximo 2)

# Notificaciones:
- A los 5 días: Recordatorio de vencimiento
- A los 2 días: Recordatorio final
```

### Renovación de Préstamo

```python
# Validaciones:
1. ¿El préstamo está activo? (no devuelto)
2. ¿Renovaciones < 2? (máximo 2 renovaciones)
3. ¿El usuario es el propietario del préstamo?

# Proceso:
- Nueva fecha de vencimiento: Vencimiento Anterior + 7 días
- Renovaciones += 1 (1 o 2)
- Se guarda la información actualizada

# Resultado:
- ✅ Éxito: "Préstamo renovado exitosamente"
- ❌ Error: "No hay más renovaciones disponibles"
```

### Devolución de Libro

```python
# Validaciones:
1. ¿El préstamo existe?
2. ¿No está ya devuelto?

# Proceso:
- Marcar como devuelto: True
- Fecha de devolución: HOY
- Status: "Completado"

# Datos Guardados:
- Historial completo para reporte
```

---

## 🎯 Lógica de Negocio para Propietarios

### Gestión de Clientes

```python
# Información Disponible:
- Usuario (nombre único)
- Correo (para notificaciones)
- Teléfono (contacto)
- Estado (activo/suspendido)
- Verificado (True/False)
- Fecha de Registro

# Acciones:
1. Ver todos los clientes
2. Cambiar estado a "suspendido" → Bloquea préstamos
3. Ver información detallada
4. Ver historial de préstamos del cliente
```

### Análisis de Préstamos Vencidos

```python
# Sistema detecta automáticamente:
- Préstamos que ya pasaron la fecha de vencimiento
- Calcula días de retraso
- Permite tomar acciones

# Acciones del Propietario:
1. Ver lista de préstamos vencidos
2. Enviar recordatorio al cliente
3. Cambiar estado del cliente si es necesario
4. Registrar devolución forzada
```

### Estadísticas del Sistema

```
Total de Libros: Mostrado en Control de Inventario
Total de Clientes: Para análisis de uso
Préstamos Activos: Libros que están rentados
Préstamos Finalizados: Libros devueltos
Préstamos Vencidos: Que superan la fecha límite
```

---

#*El servicio de correo fue eliminado. Ya no existen métodos relacionados.*

---

## 📊 Estructura de Datos de Préstamo

```json
{
  "usuario": "juan_perez",
  "libro": "El Quijote",
  "fecha_prestamo": "2026-03-04",
  "fecha_vencimiento": "2026-03-11",
  "devuelto": false,
  "fecha_devolucion": null,
  "renovaciones": 0,
  "dias_restantes": 7,
  "dias_vencido": 0
}
```

---

## 🎨 Interfaz con Sistema de Tabs

### Tabs para Cliente
- **Libros**: Catálogo completo con filtro
- **Mis Préstamos**: Historial y acciones
- **Búsqueda**: Búsqueda avanzada
- **Mi Perfil**: Información personal

### Tabs para Propietario
- **Agregar Libro**: Formulario de ingreso
- **Mis Libros**: Catálogo completo
- **Préstamos**: Vista de TODOS los préstamos
- **Clientes**: Gestión de usuarios
- **Estadísticas**: Análisis del sistema
- **Mi Perfil**: Configuración

---

## 🚀 Optimizaciones Implementadas

### Performance
- ✅ Tab system (evita cargar todo de una vez)
- ✅ Queries directas a JSON (sin búsquedas innecesarias)
- ✅ Validaciones antes de operaciones costosas

### Usabilidad
- ✅ Botones de navegación clara
- ✅ Colores para indicar pestaña activa
- ✅ Mensajes de error específicos
- ✅ Confirmaciones de éxito

### Seguridad
- ✅ Verificación de correo doble (registro y login)
- ✅ Códigos con expiración temporal
- ✅ Validación de datos de entrada
- ✅ Acceso basado en rol

---



---

## 📋 Casos de Uso Documentados

### Caso 1: Nuevo Usuario se Registra
```
1. Juan va a "Crear nueva cuenta"
2. Ingresa: juan_perez, contraseña, juan@example.com, +1234567890
3. ✅ Cuenta creada y puede hacer login
```

### Caso 2: Cliente Renta Libro
```
1. Juan hace login
2. Va a "Libros"
3. Click en "Rentar" para "El Quijote"
4. ✅ Rentado por 7 días (hasta 2026-03-11)
5. En "Mis Préstamos" ve el libro con datos
```

### Caso 3: Propietario Ve Préstamos Vencidos
```
1. Admin hace login
2. Va a "Préstamos"
3. Filtra por "Vencidos"
4. Ve lista de clientes con retraso
5. Puede tomar acciones administrativas
```

---

## ✅ Testing Checklist

- [ ] Registro con verificación de correo
- [ ] Login con 2FA
- [ ] Rentar libro
- [ ] Renovar préstamo
- [ ] Devolver libro
- [ ] Buscar libros
- [ ] Ver estadísticas
- [ ] Ver lista de clientes
- [ ] Cambiar estado de cliente
- [ ] Ver historial de préstamos

---

**Documento de Referencia Técnica**  
**Versión**: 2.0  
**Última Actualización**: 4 de Marzo 2026
