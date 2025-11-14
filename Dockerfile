FROM python:3.11-slim

# Evitar escritura de .pyc y mantener salida no bufferizada
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar y instalar dependencias primero para aprovechar la cache de Docker
COPY requirements_api.txt ./

# Instalar dependencias del sistema necesarias para compilar paquetes pip si fuese necesario
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    && pip install -r requirements_api.txt gunicorn

# Copiar el resto de la aplicación
COPY . /app

# Si el repo contiene `ventas.csv` pero no `ventas.xlsx`, convertir CSV a XLSX
# para que la aplicación encuentre el archivo (`app_api.py` soporta ambos).
RUN python - <<'PY'
import os
import pandas as pd
if os.path.exists('ventas.csv') and not os.path.exists('ventas.xlsx'):
    try:
        df = pd.read_csv('ventas.csv')
        df.to_excel('ventas.xlsx', index=False, engine='openpyxl')
        print('ventas.xlsx creado a partir de ventas.csv')
    except Exception as e:
        print('No se pudo convertir ventas.csv a ventas.xlsx:', e)
PY

# Puerto que expone la aplicación
EXPOSE 5500

# Ejecutar con Gunicorn (1 worker por defecto; aumentar si necesario)
CMD ["gunicorn", "--bind", "0.0.0.0:5500", "app_api:app", "--workers", "1", "--threads", "4"]
