# Documentación del Proyecto: Análisis de Ventas (Web + Terminal) — Actualizado

## Resumen ejecutivo
Aplicación que ofrece dos formas de consultar ventas semestrales:

- app.py — Servicio web (Flask) que carga `ventas.xlsx` / `detalle_ventas.xlsx` y expone una API REST para:
  - resumen por mes,
  - distribución por medio de pago,
  - búsqueda por cliente,
  - búsqueda por producto,
  - top de productos (por importe y por cantidad),
  - ticket promedio por venta.
  - Interfaz web: chat/UI en static/index.html + static/script.js (botón/menú interactivo).

- programa.py — Herramienta independiente de consola que contiene un diccionario `datos` con meses → categorías → sucursales → importes; permite resúmenes y detalle por sucursal sin depender de archivos externos.

## Estado actual
- app.py: funcionando como API local; depende de pandas, openpyxl y flask. Carga dos fuentes: `ventas.xlsx` y `detalle_ventas.xlsx` (si no existen crea DataFrames vacíos con columnas mínimas).
- static/script.js: cliente web tipo "chat" que ya soporta correctamente las acciones de buscar cliente y buscar producto (envía a los endpoints correctos).
- programa.py: ejecutable por terminal y autónomo; actualizar datos editando el diccionario `datos` dentro del archivo.

## Estructura de datos esperada
- ventas (ventas.xlsx / ventas.csv)
  - Columnas mínimas: `id_venta`, `fecha`, `id_cliente`, `nombre_cliente`, `email`, `medio_pago`.
  - `fecha` se parsea con pandas; si falla queda NaT.
- detalle_ventas (detalle_ventas.xlsx)
  - Columnas mínimas: `id_venta`, `id_producto`, `nombre_producto`, `cantidad`, `precio_unitario`, `importe`.

## Endpoints (resumen)
- GET / → plantilla `index.html` (UI chat)  
- GET /api/opciones → lista de acciones disponibles (incluye buscar producto y productos top)  
- GET /api/resumen_mes → resumen agrupado por mes (nombre del mes, cantidad de ventas)  
- GET /api/por_medio → distribución por `medio_pago`  
- POST /api/buscar_cliente → payload { "nombre": "texto" } → filas coincidentes en ventas  
- POST /api/buscar_producto → payload { "nombre": "texto" } → filas coincidentes en detalle_ventas  
- GET /api/productos_top → top 10 productos por `importe`  
- GET /api/productos_mas_cantidades → top 10 productos por `cantidad`  
- GET /api/ticket_promedio → ticket promedio por venta y total de ventas

Notas:
- Respuestas vacías devuelven listas o mensajes tipo `{ "mensaje": "..." }`.
- Las búsquedas son insensibles a mayúsculas y admiten subcadenas.

## Interfaz web (chat)
- El cliente JS (static/script.js) muestra opciones; al seleccionar "Buscar producto" activa el campo de entrada y, al enviar, hace POST a `/api/buscar_producto`.
- Se renderizan tablas HTML con las filas devueltas; para errores se muestran mensajes legibles.
- Si antes no funcionaba buscar producto, se corrigió el script para llamar al endpoint correcto según la acción seleccionada.

## Cómo ejecutar (Windows)
1. Instalar dependencias:
   ```
   python -m pip install flask pandas openpyxl
   ```
2. Ejecutar la API (desde la carpeta del proyecto):
   ```
   set PORT=5500
   python app.py
   ```
   Abrir: http://127.0.0.1:5500

3. Ejecutar programa de terminal:
   ```
   python rograma.py
   ```

## Ejemplos (curl)
- Buscar producto:
  ```
  curl -s -X POST -H "Content-Type: application/json" -d "{\"nombre\":\"aceite\"}" http://127.0.0.1:5500/api/buscar_producto
  ```
- Buscar cliente:
  ```
  curl -s -X POST -H "Content-Type: application/json" -d "{\"nombre\":\"juan\"}" http://127.0.0.1:5500/api/buscar_cliente
  ```
- Top productos por importe:
  ```
  curl http://127.0.0.1:5500/api/productos_top
  ```
- Ticket promedio:
  ```
  curl http://127.0.0.1:5500/api/ticket_promedio
  ```

## Recomendaciones y mejoras
- Unificar origen de datos (que app.py exporte la estructura usada por programa.py o programa.py lea el Excel).
- Añadir paginación y límite en búsquedas (si hay muchos resultados).
- Añadir tests unitarios para endpoints y para funciones de programa.py.
- Crear una página de administración para subir/actualizar los archivos Excel.

## Registro de cambios
- 2025-10-19: Documento actualizado para incluir endpoints de productos y corrección en static/script.js (buscar producto).