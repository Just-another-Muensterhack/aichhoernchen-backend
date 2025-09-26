#!/usr/bin/env bash
set -euo pipefail

: "${DB_HOST:=postgres}"
: "${DB_PORT:=5432}"
: "${DB_USER:=postgres}"
: "${DB_NAME:=aichhoernchen}"
: "${DB_PASSWORD:=postgres}"

: "${PORT:=8000}"



echo "==> Running database migrations..."
python /app/src/aichhoernchen/manage.py migrate --noinput

echo "==> Collecting static files..."
python /app/src/aichhoernchen/manage.py collectstatic --noinput

echo "==> Starting Uvicorn on 0.0.0.0:${PORT}..."
exec uvicorn src.aichhoernchen.aichhoernchen.asgi:application \
  --host 0.0.0.0 \
  --port "${PORT}"
