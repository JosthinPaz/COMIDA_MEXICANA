# --- Etapa 1: Constructor (Builder) ---
FROM python:3.11-slim-bullseye AS builder

# Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        build-essential \
        default-libmysqlclient-dev \
        libcairo2-dev \
        libfreetype6-dev \
        libssl-dev \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalamos dependencias de Python en una capa separada
# Esto solo se ejecutará si cambias el archivo requirements.txt
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Etapa 2: Producción (Final) ---
FROM python:3.11-slim-bullseye

WORKDIR /app

# Instalar SOLO las librerías de ejecución (runtime) necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmagic1 \
        default-libmysqlclient-dev \
        libcairo2 \
        libfreetype6 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copiar las librerías instaladas desde la etapa de builder
COPY --from=builder /install /usr/local

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto de FastAPI/Uvicorn
EXPOSE 8000

# Script de inicio robusto
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
