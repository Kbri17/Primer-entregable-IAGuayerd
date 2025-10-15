# Instrucciones para Copilot

A continuación, se presentan ejemplos de los prompts utilizados para guiar la generación de código con una IA asistente para el proyecto de análisis de ventas.

### Prompt 1: Estructura de Datos

"Tengo datos de ventas en un formato de tabla de Excel. Las filas son los meses ('ene' a 'jun'), y las columnas son sucursales agrupadas en dos categorías principales: 'Alimentos' y 'Limpieza'. Genera una estructura de datos en Python usando un diccionario anidado para almacenar esta información de forma eficiente. La estructura debe permitirme acceder a un dato así: `datos['mes']['categoria']['sucursal']`."

### Prompt 2: Función para el Menú Principal

"Escribe una función en Python llamada `main` que muestre un menú de consola con 4 opciones: 'Ver resumen general por mes', 'Ver total de ventas por categoría', 'Ver detalle de ventas por sucursal' y 'Salir'. La función debe usar un bucle `while` para que el menú se repita hasta que el usuario elija la opción 'Salir'. También debe incluir un mensaje de bienvenida y de despedida."

### Prompt 3: Lógica para una Funcionalidad Específica

"Crea una función en Python llamada `mostrar_detalle_por_sucursal`. Esta función debe:
1. Pedir al usuario que ingrese el nombre de una sucursal.
2. Buscar en la estructura de datos anidada (previamente creada) las ventas de 'Alimentos' y 'Limpieza' para esa sucursal en cada mes.
3. Imprimir los resultados en una tabla bien formateada con columnas para 'Mes', 'Alimentos' y 'Limpieza'.
4. Manejar el caso en que el nombre de la sucursal ingresada no exista."

### Prompt 4: Pseudocódigo

"Genera el pseudocódigo para un programa interactivo de consola que analiza datos de ventas. Los datos están almacenados en una estructura interna. El programa debe ofrecer un menú para ver resúmenes por mes, totales por categoría, detalles por sucursal y una opción para salir."