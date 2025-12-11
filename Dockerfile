# Usar una imagen base de Python oficial y ligera
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para compilar el conector MariaDB
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gcc \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todo el contenido del repositorio al directorio de trabajo del contenedor
COPY . /app

# Establecer el directorio de trabajo en la carpeta de la aplicación (BACKEND)
WORKDIR /app/BACKEND

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# El comando de inicio que se ejecutará al iniciar el contenedor
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]

# Exponer el puerto
EXPOSE 8000
