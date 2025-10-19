# Documentación del Proyecto: Análisis de Ventas (Web + Terminal)

## Resumen ejecutivo
Proyecto que contiene dos interfaces para consultar ventas semestrales:
- app.py — Servicio web (Flask) que carga datos desde `ventas.xlsx` / `ventas.csv` y expone una API para: resumen por mes, distribución por medio de pago y búsqueda por cliente.
- programa.py — Herramienta independiente de consola que usa un diccionario interno con datos por mes, categoría (Alimentos, Limpieza) y sucursal; permite ver resúmenes y detalles por sucursal mediante un menú interactivo.

## Estado actual
- app.py: orientado a ejecución local como API/pequeña web. Requiere pandas, openpyxl y flask.
- programa.py: implementación autónoma en terminal que ya contiene los datos (6 meses, 2 categorías, 6 sucursales) y no necesita dependencias externas.

## Estructura de datos esperada
- app.py:
  - Archivos aceptados: `ventas.xlsx` (preferible) o `ventas.csv`.
  - Columnas mínimas: `id_venta`, `fecha`, `nombre_cliente`, `medio_pago`.
- programa.py:
  - Usa variable `datos` (estructura dict): meses -> categorías -> sucursales -> importes.
  - Para actualizar los valores en programa.py, editar el diccionario `datos` dentro del archivo.

## Cómo ejecutar (Windows)

- Ejecutar la API web (app.py)
  1. Instalar dependencias:
     ```
     python -m pip install flask pandas openpyxl
     ```
  2. Ejecutar:
     ```
     set PORT=5500
     python c:\Users\Kenia\Desktop\IA\app.py
     ```
  3. Abrir: http://127.0.0.1:5500

- Ejecutar la versión terminal (programa.py)
  1. No requiere dependencias externas (Python 3.x).
  2. Ejecutar:
     ```
     python c:\Users\Kenia\Desktop\IA\programa.py
     ```

## Endpoints (app.py)
- GET `/` → plantilla `index.html` si existe.
- GET `/api/opciones` → opciones disponibles (resumen mes, por medio, buscar cliente).
- GET `/api/resumen_mes` → resumen agrupado por mes (nombre del mes, cantidad).
- GET `/api/por_medio` → distribución por `medio_pago`.
- POST `/api/buscar_cliente` → buscar por `nombre` en JSON: `{ "nombre": "texto" }`.

## Menú (programa.py)
- 1: Resumen general por mes (total por categoría y total general).
- 2: Total de ventas por categoría en el semestre.
- 3: Detalle de ventas por sucursal (ventas mensuales por categoría).
- 4: Salir.

## Notas prácticas y recomendaciones
- app.py está pensado para leer datasets externos; programa.py es ideal para demostraciones o cuando no hay archivos externos.
- Para mantener un único origen de verdad, considerar:
  - Convertir `ventas.xlsx` en la estructura `datos` y cargarla en programa.py al inicio, o
  - Añadir en app.py endpoints que devuelvan datos por sucursal/categoría como los que muestra programa.py.
- Mejoras sugeridas:
  - Añadir tests unitarios (rutas de Flask y funciones de programa.py).
  - Añadir paginación/limitado en búsqueda de clientes.
  - Crear una UI que consuma la API y/o una opción para que programa.py lea CSV/XLSX.

## Registro de cambios
- 2025-10-19: Documento actualizado para incluir ambas implementaciones (web y terminal).