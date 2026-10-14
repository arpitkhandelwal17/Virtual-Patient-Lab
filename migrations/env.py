"""Alembic setup: how database changes are applied."""
import sqlalchemy as sa
from alembic import context

from server.database import get_database_url

config = context.config
target_metadata = None  # tables are added from M2-T1 onwards


def _url() -> str:
    return config.get_main_option("sqlalchemy.url") or get_database_url()


def run_migrations_offline() -> None:
    context.configure(url=_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = sa.create_engine(_url())
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
