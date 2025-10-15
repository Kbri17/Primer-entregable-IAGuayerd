# --- Datos del Proyecto ---
# Los datos se han extraído del archivo Excel y se almacenan aquí.
datos = {
    'ene': {
        'Alimentos': {'Alta Gracia': 9680, 'Carlos Paz': 18760, 'Cordoba': 60822, 'Mendiolaza': 21600, 'Rio Cuarto': 52405, 'Villa Maria': 87447},
        'Limpieza': {'Alta Gracia': 47243, 'Carlos Paz': 42741, 'Cordoba': 45200, 'Mendiolaza': 11988, 'Rio Cuarto': 53316, 'Villa Maria': 78558}
    },
    'feb': {
        'Alimentos': {'Alta Gracia': 37337, 'Carlos Paz': 22277, 'Cordoba': 29687, 'Mendiolaza': 11900, 'Rio Cuarto': 69206, 'Villa Maria': 27858},
        'Limpieza': {'Alta Gracia': 57491, 'Carlos Paz': 44308, 'Cordoba': 34190, 'Mendiolaza': 4066, 'Rio Cuarto': 22624, 'Villa Maria': 46097}
    },
    'mar': {
        'Alimentos': {'Alta Gracia': 41052, 'Carlos Paz': 16493, 'Cordoba': 42248, 'Mendiolaza': 0, 'Rio Cuarto': 25028, 'Villa Maria': 1664},
        'Limpieza': {'Alta Gracia': 76783, 'Carlos Paz': 51694, 'Cordoba': 44610, 'Mendiolaza': 0, 'Rio Cuarto': 80255, 'Villa Maria': 8436}
    },
    'abr': {
        'Alimentos': {'Alta Gracia': 69502, 'Carlos Paz': 61960, 'Cordoba': 3328, 'Mendiolaza': 0, 'Rio Cuarto': 10043, 'Villa Maria': 0},
        'Limpieza': {'Alta Gracia': 58731, 'Carlos Paz': 20841, 'Cordoba': 15035, 'Mendiolaza': 0, 'Rio Cuarto': 11084, 'Villa Maria': 0}
    },
    'may': {
        'Alimentos': {'Alta Gracia': 27098, 'Carlos Paz': 36290, 'Cordoba': 48271, 'Mendiolaza': 60510, 'Rio Cuarto': 109302, 'Villa Maria': 15076},
        'Limpieza': {'Alta Gracia': 296547, 'Carlos Paz': 2871, 'Cordoba': 2280, 'Mendiolaza': 10710, 'Rio Cuarto': 37182, 'Villa Maria': 167402}
    },
    'jun': {
        'Alimentos': {'Alta Gracia': 18060, 'Carlos Paz': 10124, 'Cordoba': 40957, 'Mendiolaza': 47056, 'Rio Cuarto': 82015, 'Villa Maria': 0},
        'Limpieza': {'Alta Gracia': 8658, 'Carlos Paz': 25022, 'Cordoba': 105424, 'Mendiolaza': 34644, 'Rio Cuarto': 115523, 'Villa Maria': 24434}
    }
}

# --- Funciones del Programa ---

def mostrar_resumen_general():
    """Muestra una tabla con el total de ventas por mes, desglosado por categoría."""
    print("\n--- Resumen General por Mes ---")
    print(f"{'Mes':<10} | {'Alimentos':>12} | {'Limpieza':>12} | {'Total General':>15}")
    print("-" * 55)
    
    for mes, categorias in datos.items():
        total_alimentos = sum(categorias['Alimentos'].values())
        total_limpieza = sum(categorias['Limpieza'].values())
        total_mes = total_alimentos + total_limpieza
        print(f"{mes.capitalize():<10} | {total_alimentos:>12,} | {total_limpieza:>12,} | {total_mes:>15,}")

def mostrar_total_por_categoria():
    """Calcula y muestra el total de ventas del semestre para cada categoría."""
    print("\n--- Total de Ventas por Categoría (Semestre) ---")
    total_alimentos = 0
    total_limpieza = 0
    
    for mes in datos:
        total_alimentos += sum(datos[mes]['Alimentos'].values())
        total_limpieza += sum(datos[mes]['Limpieza'].values())
        
    print(f"Total Alimentos: {total_alimentos:,}")
    print(f"Total Limpieza:  {total_limpieza:,}")

def mostrar_detalle_por_sucursal():
    """Pide al usuario una sucursal y muestra sus ventas mensuales por categoría."""
    sucursales = list(datos['ene']['Alimentos'].keys())
    print("\nSucursales disponibles:", ", ".join(sucursales))
    nombre_sucursal = input("Ingresa el nombre de la sucursal que quieres consultar: ").title()

    if nombre_sucursal not in sucursales:
        print(f"\nError: La sucursal '{nombre_sucursal}' no fue encontrada.")
        return

    print(f"\n--- Detalle de Ventas para: {nombre_sucursal} ---")
    print(f"{'Mes':<10} | {'Alimentos':>12} | {'Limpieza':>12}")
    print("-" * 40)

    for mes, categorias in datos.items():
        venta_alimentos = categorias['Alimentos'].get(nombre_sucursal, 0)
        venta_limpieza = categorias['Limpieza'].get(nombre_sucursal, 0)
        print(f"{mes.capitalize():<10} | {venta_alimentos:>12,} | {venta_limpieza:>12,}")


# --- Programa Principal ---

def main():
    """Función principal que ejecuta el menú interactivo."""
    print("¡Bienvenido al Sistema de Análisis de Ventas!")
    
    while True:
        print("\n--- Menú Principal ---")
        print("1. Ver resumen general por mes")
        print("2. Ver total de ventas por categoría")
        print("3. Ver detalle de ventas por sucursal")
        print("4. Salir")
        
        opcion = input("Por favor, elige una opción (1-4): ")
        
        if opcion == '1':
            mostrar_resumen_general()
        elif opcion == '2':
            mostrar_total_por_categoria()
        elif opcion == '3':
            mostrar_detalle_por_sucursal()
        elif opcion == '4':
            print("\nGracias por usar el sistema. ¡Adiós! 👋")
            break
        else:
            print("\nOpción no válida. Por favor, ingresa un número del 1 al 4.")

# Ejecutar el programa
if __name__ == "__main__":
    main()