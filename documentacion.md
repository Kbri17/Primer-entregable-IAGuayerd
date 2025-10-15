# Documentación del Proyecto: Análisis de Ventas

## 1. Tema, Problema y Solución

* **Tema:** Análisis interactivo de datos de ventas semestrales para una empresa con múltiples sucursales.
* **Problema:** La empresa necesita una herramienta rápida y sencilla para consultar y resumir los importes de ventas, que están clasificados por mes, categoría (Alimentos, Limpieza) y sucursal. Realizar estas consultas directamente en el archivo de Excel es un proceso manual y lento.
* **Solución:** Se ha desarrollado un programa interactivo en Python que carga los datos y permite a los usuarios consultar información específica a través de un menú en la consola. Esto agiliza el acceso a los totales por mes, categoría y los detalles por sucursal.

---

## 2. Dataset de Referencia

* **Fuente:** El dataset original es un archivo de Excel (`análisis.xlsx`) que contiene los registros de ventas del primer semestre del año.
* **Definición:** El conjunto de datos representa los importes de ventas, desglosados por seis sucursales, en dos categorías principales de productos.
* **Estructura:** Los datos están organizados de forma tabular:
    * **Filas:** Representan los meses (enero a junio).
    * **Columnas:** Representan las sucursales, agrupadas por categoría de producto (`Alimentos` y `Limpieza`).
    * **Valores:** Cifras numéricas que corresponden a los importes de venta.
* **Tipos de Datos:**
    * **Texto:** Meses, nombres de categorías y nombres de sucursales.
    * **Numérico:** Importes de las ventas (enteros).
* **Escala:** El dataset comprende 6 meses, 2 categorías y 6 sucursales.

---

## 3. Información, Pasos, Pseudocódigo y Diagrama del Programa

### Pasos del Programa

1.  **Carga de Datos:** Los datos del Excel se almacenan en una estructura de datos de Python (un diccionario anidado) para un fácil acceso.
2.  **Menú Interactivo:** El programa muestra un menú principal con las consultas disponibles.
3.  **Entrada del Usuario:** El programa espera a que el usuario seleccione una opción.
4.  **Procesamiento:** Según la opción, el programa realiza el cálculo o la búsqueda correspondiente.
5.  **Visualización:** Los resultados se presentan de forma clara y legible en la consola.
6.  **Ciclo:** El programa vuelve al menú principal hasta que el usuario elige la opción de salir.

### Pseudocódigo