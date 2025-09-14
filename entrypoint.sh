#!/bin/sh
set -e

# Wait for potential dependencies (noop for SQLite)
# You can add sleep or healthchecks if you switch to Postgres later

# Apply database migrations
python manage.py migrate --noinput

# Optionally create static if not done at build (safe to run again)
python manage.py collectstatic --noinput || true

# Start Gunicorn
: "${PORT:=8000}"
: "${GUNICORN_CMD_ARGS:=}"
exec gunicorn auditoria.wsgi:application \
  --bind 0.0.0.0:${PORT} \
  --workers 3 \
  --timeout 120 \
  ${GUNICORN_CMD_ARGS}
