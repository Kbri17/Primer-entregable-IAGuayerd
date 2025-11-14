from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__, static_folder='static', template_folder='templates')
# Allow cross-origin requests so the frontend can call this API when hosted elsewhere
CORS(app, resources={r"/api/*": {"origins": "*"}})
DATA_FILE = Path('ventas.xlsx')


def load_items():
    """Carga la hoja de ventas y devuelve DataFrame con columnas 'producto' y 'precio'.
    Intenta leer columnas por nombre; si no existen, usa posiciones C (index 2) y G (index 6).
    """
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=['producto', 'precio'])

    try:
        df = pd.read_excel(DATA_FILE, engine='openpyxl')
    except Exception:
        # intentar leer CSV por si acaso
        try:
            df = pd.read_csv(DATA_FILE.with_suffix('.csv'))
        except Exception:
            return pd.DataFrame(columns=['producto', 'precio'])

    # Normalizar nombres a minúsculas sin espacios para encontrar columnas
    cols = [c.strip() for c in df.columns]
    # intentar detectar columna de producto y precio
    producto_col = None
    precio_col = None
    for c in cols:
        low = c.lower()
        if any(k in low for k in ('producto', 'prod', 'nombre')) and producto_col is None:
            producto_col = c
        if any(k in low for k in ('precio', 'importe', 'valor')) and precio_col is None:
            precio_col = c

    # si no se detectan por nombre, usar índices si existen
    if producto_col is None and len(cols) > 2:
        producto_col = cols[2]
    if precio_col is None and len(cols) > 6:
        precio_col = cols[6]

    # construir DataFrame con columnas esperadas
    out = pd.DataFrame()
    if producto_col is not None:
        out['producto'] = df[producto_col].astype(str)
    else:
        out['producto'] = ''

    if precio_col is not None:
        out['precio'] = df[precio_col]
    else:
        out['precio'] = pd.NA

    # normalizar
    out['producto'] = out['producto'].str.strip()
    return out


def save_item(producto, precio):
    """Añade un item al archivo Excel (o lo crea) colocando producto en columna C y precio en G.
    Implementación simple: leemos existente si hay, añadimos la fila y guardamos solo dos columnas.
    """
    df = load_items()
    new = {'producto': str(producto).strip(), 'precio': precio}
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    # Guardar a Excel con dos columnas; si la escritura falla, lanzar excepción
    df.to_excel(DATA_FILE, index=False, engine='openpyxl')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/price')
def api_price():
    producto = request.args.get('producto', '').strip()
    # optional limit param to control number of matches returned
    try:
        limit = int(request.args.get('limit', 10))
    except Exception:
        limit = 10
    if not producto:
        return jsonify({'error': 'Parámetro "producto" es requerido'}), 400

    df = load_items()
    if df.empty:
        return jsonify({'mensaje': 'No hay datos disponibles'}), 200

    # búsqueda insensible a mayúsculas por subcadena
    mask = df['producto'].str.lower().str.contains(producto.lower(), na=False)
    resultados = df[mask]
    if resultados.empty:
        return jsonify({'mensaje': 'Producto no encontrado'}), 404

    # Construir lista de matches (producto + precio)
    results_list = []
    for _, row in resultados.head(limit).iterrows():
        precio_val = None
        try:
            precio_val = float(row['precio']) if pd.notna(row['precio']) else None
        except Exception:
            precio_val = None
        results_list.append({'producto': row['producto'], 'precio': precio_val})

    resp = {'matches': int(len(resultados)), 'limit': limit, 'results': results_list}
    return jsonify(resp)


@app.route('/api/add_item', methods=['POST'])
def api_add_item():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido o vacío'}), 400
    producto = data.get('producto')
    precio = data.get('precio')
    if not producto or precio is None:
        return jsonify({'error': 'Campos "producto" y "precio" son requeridos'}), 400

    try:
        # intentar convertir precio a número
        precio_val = float(precio)
    except Exception:
        return jsonify({'error': 'El campo "precio" debe ser numérico'}), 400

    try:
        save_item(producto, precio_val)
    except Exception as e:
        return jsonify({'error': f'Fallo al guardar: {e}'}), 500

    return jsonify({'message': 'Item agregado', 'producto': producto, 'precio': precio_val}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)
