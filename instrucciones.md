# 🧭 Instrucciones para Copilot 

A continuación se presentan los prompts y directrices actualizadas para generar un sistema interactivo de análisis de ventas basado en datos reales de un archivo Excel.

---

### 🧩 Prompt 1: Lectura y Estructura de Datos desde Excel

"Tengo un archivo de Excel llamado `ventas.xlsx` que contiene los datos de ventas de un negocio.  
Necesito que leas el archivo usando `pandas` (`pd.read_excel`) y detectes automáticamente el nombre de la hoja (`sheet_name=None` si es necesario).  
Convierte los datos en una estructura de Python usando un diccionario anidado con el formato:

```python
datos['mes']['categoria']['sucursal']
```

De esta manera, podré acceder fácilmente a las ventas de una sucursal dentro de una categoría en un mes específico.  
Asegúrate de manejar correctamente los nombres de las columnas y filas según los encabezados del Excel."

---

### 💬 Prompt 2: Interfaz de Chat Restrictivo (Menú Interactivo)

"Escribe una función `main_chat()` en Python que simule un chat interactivo en consola.  
Debe mostrar opciones como botones numerados (por ejemplo: `[1] Ver resumen general`, `[2] Ver total por categoría`, `[3] Ver detalle por sucursal`, `[4] Salir`).  
El usuario solo puede escoger entre las opciones mostradas (no puede escribir texto libre).  
Además, incluye una opción para **retroceder** en los submenús y volver al menú anterior.  
Usa bucles `while` y funciones separadas para cada funcionalidad."

---

### 📊 Prompt 3: Visualización de Datos en Tablas

"Crea una función `mostrar_tabla(datos)` que use `tabulate` o `pandas` para mostrar la información en formato de tabla con encabezados claros.  
Cada vez que se muestren datos (por ejemplo, el detalle de una sucursal o el resumen mensual), deben verse bien alineados, con columnas y filas claramente etiquetadas."

Ejemplo de salida:

```
+--------+-------------+-------------+
|  Mes   |  Alimentos  |  Limpieza   |
+--------+-------------+-------------+
|  Ene   |   12000.00  |   8700.00   |
|  Feb   |   13000.00  |   9200.00   |
+--------+-------------+-------------+
```

---

### 🧠 Prompt 4: Funcionalidades Específicas

1. **Resumen general por mes:**  
   Mostrar el total de ventas combinadas (todas las sucursales) para cada mes.

2. **Totales por categoría:**  
   Calcular y mostrar el total de ventas de 'Alimentos' y 'Limpieza' en todos los meses.

3. **Detalle por sucursal:**  
   Pedir al usuario que seleccione una sucursal de una lista generada automáticamente.  
   Mostrar las ventas por mes, separadas por categoría.

4. **Volver / Salir:**  
   Permitir al usuario volver al menú anterior o salir completamente del programa.

---

### 🧩 Prompt 5: Pseudocódigo General

"Genera el pseudocódigo de un programa interactivo de consola para analizar datos de ventas.  
El sistema debe:
- Leer los datos desde un archivo Excel (`ventas.xlsx`).
- Convertirlos en una estructura de datos anidada (`datos[mes][categoria][sucursal]`).
- Mostrar menús con opciones seleccionables (sin texto libre).
- Permitir navegar entre menús (entrar/salir/volver).
- Mostrar la información en tablas bien formateadas.
- Terminar con un mensaje de despedida."

---

### 🧩 Prompt 6: Especificación de la API (Flask)
"Define los endpoints REST que debe exponer la aplicación Flask, incluyendo método HTTP, ruta, payload esperado y formato de respuesta (JSON). Indica códigos de estado para casos exitosos y errores (200, 400, 404, 500). Deben incluirse al menos:
- GET /api/opciones
- GET /api/resumen_mes
- GET /api/por_medio
- POST /api/buscar_cliente (payload: { "nombre": "..." })
- POST /api/buscar_producto (payload: { "nombre": "..." })
- GET /api/productos_top
- GET /api/productos_mas_cantidades
- GET /api/ticket_promedio
Describe ejemplos de respuestas y mensajes cuando no hay datos."

### 🧩 Prompt 7: Carga robusta de datos y lógica de fallback
"Escribe funciones para cargar `ventas.xlsx`/`ventas.csv` y `detalle_ventas.xlsx`/`detalle_ventas.csv` con pandas. Reglas:
- Intentar primero .xlsx, luego .csv.
- Detectar y usar la hoja correcta si hay múltiples hojas.
- Normalizar nombres de columnas (minúsculas, sin espacios).
- Asegurar columnas mínimas y crearlas si faltan.
- Registrar (logger) errores y devolver DataFrames vacíos con columnas mínimas en caso de fallo.
Incluye manejo de excepciones y mensajes claros en logs."

### 🧩 Prompt 8: Búsquedas y paginación
"Define la lógica para `buscar_cliente` y `buscar_producto`:
- Búsqueda insensible a mayúsculas y por subcadena.
- Parámetros opcionales: `limit` y `offset` para paginación.
- Formato de entrada JSON y validación (400 si faltan campos).
- Formato de salida: lista de objetos con campos clave; si la fecha existe, devolverla como string ISO o formato legible.
- Si no hay coincidencias, devolver `{ "mensaje": "No se encontraron coincidencias" }` con 200."

### 🧩 Prompt 9: Agregaciones de productos
"Define la lógica para endpoints `productos_top` y `productos_mas_cantidades`:
- Agrupar por `nombre_producto`, sumar `importe` o `cantidad`.
- Aceptar parámetro opcional `top_n` (por query string) con valor por defecto 10.
- Formato de salida: lista ordenada con columnas `Producto`, `Total` (o `Cantidad total`)."

### 🧩 Prompt 10: Cálculo de ticket promedio
"Describe cómo calcular `ticket_promedio`:
- Usar `df_detalles` para sumar `importe` por `id_venta`.
- Calcular promedio sobre ventas distintas y devolver `{ 'ticket_promedio': X, 'total_ventas': N }`.
- Manejar división por cero y devolver `0` si no hay ventas."

### 🧩 Prompt 11: Frontend: comportamiento del chat JS
"Especifica los requisitos para `static/script.js`:
- Cargar `/api/opciones` al inicio.
- Mantener estado `currentAction` para decidir a qué endpoint enviar POST.
- Habilitar entrada solo cuando se selecciona una opción de búsqueda.
- Renderizar respuestas en tablas HTML (encabezados dinámicos).
- Manejar y mostrar mensajes de error y 'no hay resultados'.
- Soportar parámetros de paginación (mostrar botones 'siguiente'/'anterior' si el endpoint soporta `limit`/`offset`)."

### 🧩 Prompt 12: Tests unitarios y de integración
"Genera tests (pytest) para:
- Funciones de carga: `cargar_ventas()`, `cargar_detalles()` con archivos de muestra y casos faltantes.
- Endpoints principales: `/api/resumen_mes`, `/api/buscar_cliente`, `/api/buscar_producto`, `/api/productos_top`, `/api/ticket_promedio`.
- Casos: respuestas exitosas, inputs inválidos (400), sin datos (listas vacías o mensajes).
Incluye fixtures con DataFrames pequeños y ejemplos de uso de Flask test_client."

### 🧩 Prompt 13: Requisitos, ejecución y despliegue local
"Genera `requirements.txt` y las instrucciones para ejecutar localmente en Windows y en producción (ej. usar gunicorn en Linux). Incluir:
- Comandos de instalación pip.
- Variables de entorno (`PORT`).
- Ejemplo de servicio systemd o comando `gunicorn app:app -b 0.0.0.0:5500` para despliegue.
- Notas sobre seguridad mínima: no habilitar debug en producción y validar inputs."

### 🧩 Prompt 14: Buenas prácticas y mejoras futuras
"Lista sugerencias implementables:
- Añadir autenticación básica para endpoints de administración.
- Añadir paginación y filtrado avanzado (rango de fechas, sucursal, categoría).
- Endpoint para exportar resultados a CSV/XLSX.
- Pipeline de tests en CI (GitHub Actions) que ejecute linters y pytest.
- Documentar API con OpenAPI/Swagger."
