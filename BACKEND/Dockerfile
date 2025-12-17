# --- Etapa 1: Constructor (Builder) ---
FROM python:3.11-slim-bullseye AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instalamos dependencias para añadir repositorios y el conector actualizado
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg2 \
        gcc \
        pkg-config \
        build-essential \
        libssl-dev \
        python3-dev \
        libcairo2-dev \
        libfreetype6-dev

# 2. AÑADIR REPOSITORIO OFICIAL DE MARIADB para obtener libmariadb-dev >= 3.3.1
RUN curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash -s -- --mariadb-server-version="mariadb-10.11" && \
    apt-get update && \
    apt-get install -y libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Etapa 2: Producción (Final) ---
FROM python:3.11-slim-bullseye

WORKDIR /app

# Repetimos la configuración del repositorio para tener la librería de ejecución correcta
RUN apt-get update && apt-get install -y curl ca-certificates && \
    curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash -s -- --mariadb-server-version="mariadb-10.11" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libmariadb3 \
        libmagic1 \
        libcairo2 \
        libfreetype6 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
