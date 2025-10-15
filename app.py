from flask import Flask, jsonify, send_from_directory
import os
import programa as prog

app = Flask(__name__, static_folder='web', static_url_path='')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/resumen')
def api_resumen():
    resumen = []
    for mes, categorias in prog.datos.items():
        total_al = sum(categorias['Alimentos'].values())
        total_li = sum(categorias['Limpieza'].values())
        resumen.append({'mes': mes, 'alimentos': total_al, 'limpieza': total_li, 'total': total_al + total_li})
    return jsonify(resumen)


@app.route('/api/categorias')
def api_categorias():
    total_al = 0
    total_li = 0
    for mes in prog.datos:
        total_al += sum(prog.datos[mes]['Alimentos'].values())
        total_li += sum(prog.datos[mes]['Limpieza'].values())
    return jsonify({'Alimentos': total_al, 'Limpieza': total_li})


@app.route('/api/sucursal/<nombre>')
def api_sucursal(nombre):
    nombre_cap = nombre.replace('%20', ' ').title()
    meses = []
    for mes, categorias in prog.datos.items():
        meses.append({'mes': mes, 'alimentos': categorias['Alimentos'].get(nombre_cap, 0), 'limpieza': categorias['Limpieza'].get(nombre_cap, 0)})
    return jsonify({'sucursal': nombre_cap, 'ventas': meses})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5500))
    app.run(host='0.0.0.0', port=port, debug=True)
