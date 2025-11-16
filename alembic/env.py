from logging.config import fileConfig
import os
import asyncio
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from app.models.db_models import Character, Clan, Jutsu, CharacterJutsuLink

from alembic import context

# Cargar variables de entorno desde .env
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# Leer la URL de la base de datos desde .env
# Si no existe, usar un valor por defecto (solo para desarrollo)
database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/konohapi")

# Sobrescribir la URL en la configuración para que Alembic la use
config.set_main_option("sqlalchemy.url", database_url)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

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


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
        echo=False,
    )

    async with connectable.begin() as connection:
        await connection.run_sync(context.configure, target_metadata=target_metadata)
        await connection.run_sync(lambda conn: context.run_migrations())

    await connectable.dispose()


def main() -> None:
    """Entry point for asyncio."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


if __name__ == "__main__":
    main()
else:
    main()


