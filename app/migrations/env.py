import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# add your model's MetaData object here
# for 'autogenerate' support
from db.models.base_model import Base
from db.models.patients import Patient
from db.models.patients_history import PatientsHistory
from db.models.patients_data import PatientsData
from db.models.doctors import Doctors

target_metadata = Base.metadata


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

DB_STRING = 'postgresql://{username}:{password}@{container}:{port}/{db_name}'
USERNAME = os.getenv('POSTGRES_USER', 'postgres')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
CONTAINER = os.getenv('POSTGRES_CONTAINER_NAME', 'localhost')
PORT = os.getenv('POSTGRES_PORT', '8001')
DB_NAME = os.getenv('DB_NAME', 'postgres')

config.set_main_option('sqlalchemy.url',
                       DB_STRING.format(
                           username=USERNAME,
                           password=PASSWORD,
                           container=CONTAINER,
                           port=PORT,
                           db_name=DB_NAME))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

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
