import pandas as pd
import os
import logging
# Asegúrate de tener todos los imports de Flask
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Logger simple
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cargar_ventas():
    """Carga los datos desde 'ventas.xlsx'."""
    fn = "ventas.xlsx"
    columnas_esperadas = [
        "id_venta", "fecha", "id_cliente", "nombre_cliente", 
        "email", "medio_pago"
    ]
    df = None

    if os.path.exists(fn):
        try:
            logger.info(f"Cargando Excel desde {fn}")
            df = pd.read_excel(fn, engine='openpyxl')
        except Exception as e:
            logger.error(f"Error al leer {fn}: {e}")

    if df is None:
        logger.warning(f"No se encontró {fn}. Se crea DataFrame vacío.")
        df = pd.DataFrame(columns=columnas_esperadas)

    # Asegurar columnas mínimas
    for col in columnas_esperadas:
        if col not in df.columns:
            df[col] = pd.NA

    # Normalizar tipos
    df["id_venta"] = pd.to_numeric(df["id_venta"], errors="coerce").astype("Int64")
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce") # ¡Importante para resumen_mes!
    df["id_cliente"] = pd.to_numeric(df["id_cliente"], errors="coerce").astype("Int64")
    df["nombre_cliente"] = df["nombre_cliente"].fillna("").astype(str)
    df["email"] = df["email"].fillna("").astype(str)
    df["medio_pago"] = df["medio_pago"].fillna("").astype(str)

    logger.info(f"Archivo de VENTAS cargado con {len(df)} registros.")
    logger.info(f"Columnas de VENTAS: {list(df.columns)}")
    return df


def cargar_detalles():
    """Carga los datos desde 'detalle_ventas.xlsx'."""
    fn = "detalle_ventas.xlsx"
    columnas_esperadas = [
        "id_venta", "id_producto", "nombre_producto",
        "cantidad", "precio_unitario", "importe"
    ]
    df = None

    if os.path.exists(fn):
        try:
            logger.info(f"Cargando Excel desde {fn}")
            df = pd.read_excel(fn, engine='openpyxl')
        except Exception as e:
            logger.error(f"Error al leer {fn}: {e}")

    if df is None:
        logger.warning(f"No se encontró {fn}. Se crea DataFrame vacío.")
        df = pd.DataFrame(columns=columnas_esperadas)

    # Asegurar columnas mínimas
    for col in columnas_esperadas:
        if col not in df.columns:
            df[col] = pd.NA

    # Normalizar tipos (esta es tu lógica original, que estaba bien para detalles)
    df["id_venta"] = pd.to_numeric(df["id_venta"], errors="coerce").astype("Int64")
    df["id_producto"] = pd.to_numeric(df["id_producto"], errors="coerce").astype("Int64")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)
    df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0)
    df["importe"] = pd.to_numeric(df["importe"], errors="coerce").fillna(0)
    df["nombre_producto"] = df["nombre_producto"].fillna("").astype(str)

    logger.info(f"Archivo de DETALLE VENTAS cargado con {len(df)} registros.")
    logger.info(f"Columnas de DETALLE VENTAS: {list(df.columns)}")
    return df


# --- Cargamos AMBOS datos al iniciar ---
df_ventas = cargar_ventas()
df_detalles = cargar_detalles()


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
        {"id": "productos_top", "texto": "🏆 Top 10 productos por importe"},
        {"id": "productos_mas_cantidades", "texto": "📦 Top 10 productos por cantidad"},
        {"id": "ticket_promedio", "texto": "💰 Ver ticket promedio por venta"},
        {"id": "buscar_producto", "texto": "🔎 Buscar producto"},
    ]
    return jsonify(opciones)

# --- Endpoints que usan df_ventas ---

@app.route("/api/resumen_mes")
def api_resumen_mes():
    # Usa df_ventas
    if "fecha" not in df_ventas.columns or df_ventas["fecha"].isna().all():
        return jsonify([])

    resumen = df_ventas.groupby(df_ventas["fecha"].dt.strftime("%B")).size().reset_index(name="ventas")
    resumen = resumen.sort_values("ventas", ascending=False)
    data = resumen.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/por_medio")
def api_por_medio():
    # Usa df_ventas
    if "medio_pago" not in df_ventas.columns:
        return jsonify([])
    resumen = df_ventas["medio_pago"].value_counts().reset_index()
    resumen.columns = ["Medio de Pago", "Cantidad"]
    return jsonify(resumen.to_dict(orient="records"))

@app.route("/api/buscar_cliente", methods=["POST"])
def api_buscar_cliente():
    # Usa df_ventas
    nombre = request.json.get("nombre", "").strip().lower()
    if not nombre:
        return jsonify({"error": "Debe ingresar un nombre"})
    if "nombre_cliente" not in df_ventas.columns:
        return jsonify({"mensaje": "No hay datos de clientes"})

    resultados = df_ventas[df_ventas["nombre_cliente"].str.lower().str.contains(nombre, na=False)]
    if resultados.empty:
        return jsonify({"mensaje": "No se encontraron ventas para ese cliente"})
    
    resultados_out = resultados.copy()
    if "fecha" in resultados_out.columns:
        # Formatear fecha para que sea legible en JSON
        resultados_out["fecha"] = resultados_out["fecha"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Excluir columnas que no son JSON serializables si es necesario (ej. NaT)
    resultados_out = resultados_out.fillna("N/A") 
    
    return jsonify(resultados_out.to_dict(orient="records"))

# --- Endpoints que usan df_detalles ---

@app.route("/api/productos_top")
def api_productos_top():
    # Usa df_detalles
    if "nombre_producto" not in df_detalles.columns:
        return jsonify([])

    resumen = (
        df_detalles.groupby("nombre_producto")["importe"]
        .sum()
        .reset_index()
        .sort_values("importe", ascending=False)
        .head(10)
    )
    resumen.columns = ["Producto", "Total vendido (S/.)"]
    return jsonify(resumen.to_dict(orient="records"))

@app.route("/api/productos_mas_cantidades")
def api_productos_mas_cantidades():
    # Usa df_detalles
    if "nombre_producto" not in df_detalles.columns:
        return jsonify([])
    resumen = (
        df_detalles.groupby("nombre_producto")["cantidad"]
        .sum()
        .reset_index()
        .sort_values("cantidad", ascending=False)
        .head(10)
    )
    resumen.columns = ["Producto", "Cantidad total"]
    return jsonify(resumen.to_dict(orient="records"))

@app.route("/api/ticket_promedio")
def api_ticket_promedio():
    # Usa df_detalles
    if "id_venta" not in df_detalles.columns or "importe" not in df_detalles.columns:
        return jsonify({})
    resumen = df_detalles.groupby("id_venta")["importe"].sum()
    ticket_promedio = resumen.mean()
    total_ventas = len(resumen)
    return jsonify({
        "ticket_promedio": round(ticket_promedio, 2),
        "total_ventas": total_ventas
    })

@app.route("/api/buscar_producto", methods=["POST"])
def api_buscar_producto():
    # Usa df_detalles
    nombre = request.json.get("nombre", "").strip().lower()
    if not nombre:
        return jsonify({"error": "Debe ingresar un nombre de producto"})
    if "nombre_producto" not in df_detalles.columns:
        return jsonify({"mensaje": "No hay datos de productos"})

    resultados = df_detalles[df_detalles["nombre_producto"].str.lower().str.contains(nombre, na=False)]
    if resultados.empty:
        return jsonify({"mensaje": "No se encontraron coincidencias"})
    
    resultados_out = resultados.to_dict(orient="records")
    return jsonify(resultados_out)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5500)), debug=True)