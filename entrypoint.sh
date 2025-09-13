#!/bin/sh

echo "Aplicando migraciones..."
flask db upgrade || echo "Migraciones ya aplicadas o fallo en la conexión a Neon"

echo "Iniciando aplicación Flask..."
exec gunicorn -b 0.0.0.0:$PORT run:app
