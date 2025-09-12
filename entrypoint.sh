#!/bin/sh

echo "Esperando que la base de datos esté lista..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Base de datos lista. Aplicando migraciones..."

flask db upgrade

echo "Iniciando aplicación Flask..."

exec flask run --host=0.0.0.0 --port=5000

