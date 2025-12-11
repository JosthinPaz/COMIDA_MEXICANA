from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
import os

# Agrega el directorio raíz del proyecto al path para que las importaciones funcionen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -------------------------------------------------------------
# LÓGICA DE CONEXIÓN A RAILWAY (BLOQUE CORREGIDO)
# -------------------------------------------------------------

# Intentar leer la URL de conexión desde la variable de entorno de Railway
RAILWAY_DATABASE_URL = os.getenv("MYSQL_URL")

if RAILWAY_DATABASE_URL:
    # Si la URL existe, la inyectamos en la configuración de Alembic
    # Reemplazamos 'mysql://' por 'mysql+pymysql://' para usar el driver correcto
    CORRECTED_URL = RAILWAY_DATABASE_URL.replace("mysql://", "mysql+pymysql://")
    context.config.set_main_option("sqlalchemy.url", CORRECTED_URL)
# Si no hay MYSQL_URL, Alembic usa el valor de alembic.ini (bueno para desarrollo local)

# -------------------------------------------------------------
# FIN LÓGICA DE CONEXIÓN
# -------------------------------------------------------------


from db import Base, SQLALCHEMY_DATABASE_URL
from models import Categoria, Producto , Item ,Usuario ,Rol , Inventario, Pedido, DetallePedido ,Video, Notificacion,Chat,Reseña ,Pago


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
