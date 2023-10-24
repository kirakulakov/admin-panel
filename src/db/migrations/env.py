from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.engine import URL

from src.core.config import settings
from src.db.models.psql.base import Base

from src.db.models.psql.user import DBUser
from src.db.models.psql.item import DBItem

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata
db_settings = settings.psql


def get_url():
    return str(URL(
        drivername='postgresql',
        host=db_settings.host,
        port=db_settings.port,
        username=db_settings.user,
        password=db_settings.password,
        database=db_settings.database
    ))


config.set_main_option("sqlalchemy.url", get_url())

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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