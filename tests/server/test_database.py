"""M1-T5: the server can reach the database, and the first migration works.

These tests start their own throwaway database, so they never touch the real one.
"""
import pixeltable_pgserver as pgserver
import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config

from server import config, database


@pytest.fixture(scope="module")
def throwaway_db(tmp_path_factory):
    database.ensure_runtime_dll()
    folder = tmp_path_factory.mktemp("pg") / "data"
    server = pgserver.get_server(folder, cleanup_mode="delete")
    yield server.get_uri(driver="psycopg")
    server.cleanup()


def test_server_connects_writes_and_reads_back(throwaway_db):
    engine = database.make_engine(throwaway_db)
    with engine.begin() as conn:
        conn.execute(sa.text("create temporary table check_row (id int primary key, note text)"))
        conn.execute(sa.text("insert into check_row values (1, 'dolo650 placeholder')"))
        rows = conn.execute(sa.text("select id, note from check_row")).all()
    engine.dispose()
    assert rows == [(1, "dolo650 placeholder")]


def test_first_migration_applies(throwaway_db):
    alembic_config = Config(str(config.PROJECT_ROOT / "alembic.ini"))
    alembic_config.set_main_option("sqlalchemy.url", throwaway_db.replace("%", "%%"))
    command.upgrade(alembic_config, "head")
    engine = database.make_engine(throwaway_db)
    with engine.connect() as conn:
        version = conn.execute(sa.text("select version_num from alembic_version")).scalar()
    engine.dispose()
    assert version == "0001"


def test_env_setting_overrides_local_database(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://example-host/example_db")
    assert database.get_database_url() == "postgresql+psycopg://example-host/example_db"


def test_clear_message_when_database_not_running(monkeypatch, tmp_path):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(config, "read_env_file", lambda path=None: {})
    monkeypatch.setattr(config, "DB_DIR", tmp_path / "nothing_here")
    with pytest.raises(database.DatabaseNotRunning, match="uv run start-db"):
        database.get_database_url()


def test_helper_file_is_in_place_after_check():
    message = database.ensure_runtime_dll()
    assert message
