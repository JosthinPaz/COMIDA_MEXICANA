# Usar una imagen base de Python oficial y ligera
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
# Incluye las librerías para MySQL y Cairo/ReportLab
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gcc \
        pkg-config \
        libcairo2-dev \
        libfreetype6-dev \
        libssl-dev \
        python3-dev \
        build-essential && \
    # Limpieza final para reducir el tamaño de la imagen
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo base
WORKDIR /app

# Copiar el archivo de dependencias y la carpeta del Backend
COPY requirements.txt /app/
COPY BACKEND /app/BACKEND

# Establecer el directorio de trabajo en la carpeta de la aplicación (BACKEND)
WORKDIR /app/BACKEND

# Upgrade pip y luego instalar las dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# El comando de inicio que se ejecutará al iniciar el contenedor
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]

# Exponer el puerto
EXPOSE 8000
