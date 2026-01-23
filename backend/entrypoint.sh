#!/bin/sh

echo "Aguardando PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL iniciado"

echo "Executando Alembic migrations..."
python -m alembic upgrade head

echo "Executando Django migrations..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000
