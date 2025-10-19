# 1) Builder: instala dependencias
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app


COPY requirements.txt ./
RUN pip install --upgrade pip && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# 2) Runtime
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# libs del sistema para psycopg/psycopg2, Pillow, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copia codigo y deps
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . /app

# Asegura que DB_HOST apunte al servicio "db"
ENV DB_HOST=db
# Abre puerto de Django
EXPOSE 8000

# Comando de arranque (migraciones + runserver/gunicorn)
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput || true && \
    gunicorn psis_api.wsgi:application --bind 0.0.0.0:8000 --workers 3
