#!/usr/bin/env bash
set -euo pipefail

: "${PORT:=8000}"
: "${WORKERS:=4}"

echo "==> Running database migrations..."
python /app/src/aichhoernchen/manage.py migrate --noinput

echo "==> Collecting static files..."
python /app/src/aichhoernchen/manage.py default_deposits

echo "==> Starting Gunicorn (WSGI) on 0.0.0.0:${PORT}..."
exec gunicorn src.aichhoernchen.aichhoernchen.wsgi:application \
  --bind 0.0.0.0:"${PORT}" \
  --workers "${WORKERS}"
