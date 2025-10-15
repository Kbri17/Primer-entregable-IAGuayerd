from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import logging

app = Flask(__name__)

# Logger simple
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- Carga robusta de datos ---
def cargar_datos():
    """Intenta cargar ventas desde varios formatos y maneja errores.
    Busca en el orden: ventas.xlsx, ventas.csv.
    Devuelve un DataFrame válido (puede estar vacío con columnas esperadas).
    """
    candidates = ["ventas.xlsx", "ventas.csv"]
    df = None
    for fn in candidates:
        if os.path.exists(fn):
            try:
                if fn.lower().endswith('.xlsx'):
                    logger.info(f"Cargando Excel desde {fn}")
                    df = pd.read_excel(fn, engine='openpyxl')
                else:
                    logger.info(f"Cargando CSV desde {fn}")
                    df = pd.read_csv(fn)
                break
            except Exception as e:
                logger.error(f"Error al leer {fn}: {e}")
                df = None

    if df is None:
        logger.warning("No se encontró archivo de ventas. Se creará un DataFrame vacío con columnas esperadas.")
        df = pd.DataFrame(columns=["id_venta", "fecha", "nombre_cliente", "medio_pago"])

    # Asegurar columnas mínimas y tipos
    for col in ["id_venta", "fecha", "nombre_cliente", "medio_pago"]:
        if col not in df.columns:
            df[col] = pd.NA

    # Normalizar tipos
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["nombre_cliente"] = df["nombre_cliente"].fillna("").astype(str)
    df["medio_pago"] = df["medio_pago"].fillna("").astype(str)

    return df


# Cargamos los datos al iniciar
df = cargar_datos()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/opciones")
def api_opciones():
    """Primer menú de opciones del chat"""
    opciones = [
        {"id": "resumen_mes", "texto": "📅 Ver ventas por mes"},
        {"id": "por_medio", "texto": "💳 Ver distribución por medio de pago"},
        {"id": "buscar_cliente", "texto": "👤 Buscar ventas por cliente"},
    ]
    return jsonify(opciones)

@app.route("/api/resumen_mes")
def api_resumen_mes():
    if "fecha" not in df.columns or df["fecha"].isna().all():
        return jsonify([])

    resumen = df.groupby(df["fecha"].dt.strftime("%B")).size().reset_index(name="ventas")
    resumen = resumen.sort_values("ventas", ascending=False)
    data = resumen.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/por_medio")
def api_por_medio():
    if "medio_pago" not in df.columns:
        return jsonify([])
    resumen = df["medio_pago"].value_counts().reset_index()
    resumen.columns = ["Medio de Pago", "Cantidad"]
    return jsonify(resumen.to_dict(orient="records"))

@app.route("/api/buscar_cliente", methods=["POST"])
def api_buscar_cliente():
    nombre = request.json.get("nombre", "").strip().lower()
    if not nombre:
        return jsonify({"error": "Debe ingresar un nombre"})
    if "nombre_cliente" not in df.columns:
        return jsonify({"mensaje": "No hay datos de clientes"})

    resultados = df[df["nombre_cliente"].str.lower().str.contains(nombre, na=False)]
    if resultados.empty:
        return jsonify({"mensaje": "No se encontraron ventas para ese cliente"})
    # Convertir fechas a string legible
    resultados_out = resultados.copy()
    if "fecha" in resultados_out.columns:
        resultados_out["fecha"] = resultados_out["fecha"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(resultados_out.to_dict(orient="records"))

if __name__ == "__main__":
    # Ejecutar en 0.0.0.0:5500 por defecto para facilitar pruebas locales
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5500)), debug=True)
