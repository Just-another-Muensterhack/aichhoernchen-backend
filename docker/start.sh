#!/usr/bin/env bash
set -euo pipefail

: "${PORT:=8000}"
: "${WORKERS:=4}"

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Importing default data..."
python manage.py default_deposits
python manage.py default_objects

echo "==> Collecting static files..."
python manage.py createsuperuser --noinput

echo "==> Starting Gunicorn (WSGI) on 0.0.0.0:${PORT}..."
exec gunicorn aichhoernchen.wsgi:application \
  --bind 0.0.0.0:"${PORT}" \
  --workers "${WORKERS}"
