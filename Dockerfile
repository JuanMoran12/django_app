# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DJANGO_DEBUG=false \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
    DJANGO_DB_PATH=/data/db.sqlite3 \
    PORT=8000

WORKDIR /app

# System deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# App code
COPY . /app

# Ensure static files are collected at build time (baked into image)
# Using a default secret for build; override via env in runtime
ENV DJANGO_SECRET_KEY=build-insecure-key
RUN python manage.py collectstatic --noinput || true

# Create a non-root user and data dir for SQLite persistence
RUN useradd -m appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /data /app

USER appuser

EXPOSE 8000

# Entrypoint runs migrations and then launches Gunicorn
ENTRYPOINT ["/bin/sh", "-c", "chmod +x /app/entrypoint.sh && /app/entrypoint.sh"]
