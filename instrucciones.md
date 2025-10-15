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
