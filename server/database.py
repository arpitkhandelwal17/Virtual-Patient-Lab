"""The local database: start it, stop it, and connect to it.

Development uses a bundled PostgreSQL that needs no Windows installer. Its files
live in storage/db/. The live server will use a normal PostgreSQL instead and
give its address through DATABASE_URL in .env.
"""
import platform
import shutil
import subprocess
from pathlib import Path

import pixeltable_pgserver as pgserver
import sqlalchemy as sa
from pixeltable_pgserver.utils import POSTGRES_VERSIONS, TARGET_POSTGRES_VERSION, PostmasterInfo

from server import config

HELPER_DLL = "libwinpthread-1.dll"


class DatabaseNotRunning(RuntimeError):
    pass


def _postgres_bin() -> Path:
    return Path(POSTGRES_VERSIONS[TARGET_POSTGRES_VERSION])


def ensure_runtime_dll() -> str:
    """The bundled PostgreSQL package forgot one helper file on Windows.

    Copy it from Git for Windows if it is missing. Returns a short message.
    """
    if platform.system() != "Windows":
        return "not needed on this system"
    target_dir = _postgres_bin()
    if (target_dir / HELPER_DLL).exists():
        return "helper file already in place"
    git = shutil.which("git")
    candidates: list[Path] = []
    if git:
        git_root = Path(git).resolve().parent.parent
        candidates = [git_root / sub / "bin" / HELPER_DLL for sub in ("ucrt64", "mingw64")]
        candidates.append(git_root / "usr" / "bin" / HELPER_DLL)
    for source in candidates:
        if source.exists():
            shutil.copy2(source, target_dir / HELPER_DLL)
            return f"copied {HELPER_DLL} from Git for Windows"
    raise RuntimeError(
        f"The database needs a helper file ({HELPER_DLL}) that was not found. "
        "It normally comes with Git for Windows. Install Git for Windows, or ask for help."
    )


def _ensure_app_database(server_uri: str) -> None:
    """Create the app's database inside the server if it is not there yet."""
    engine = sa.create_engine(server_uri, isolation_level="AUTOCOMMIT")
    try:
        with engine.connect() as conn:
            exists = conn.execute(
                sa.text("select 1 from pg_database where datname = :n"), {"n": config.APP_DATABASE}
            ).scalar()
            if not exists:
                conn.execute(sa.text(f'create database "{config.APP_DATABASE}"'))
    finally:
        engine.dispose()


def start_db() -> str:
    """Start the local database (leave it running) and make sure the app database exists."""
    ensure_runtime_dll()
    config.DB_DIR.parent.mkdir(parents=True, exist_ok=True)
    server = pgserver.get_server(config.DB_DIR, cleanup_mode=None)
    _ensure_app_database(server.get_uri(driver="psycopg"))
    return server.get_uri(database=config.APP_DATABASE, driver="psycopg")


def stop_db() -> bool:
    """Stop the local database. Returns False if it was not running."""
    info = PostmasterInfo.read_from_pgdata(config.DB_DIR) if config.DB_DIR.exists() else None
    if info is None or not info.is_running():
        return False
    exe = _postgres_bin() / ("pg_ctl.exe" if platform.system() == "Windows" else "pg_ctl")
    subprocess.run([str(exe), "-w", "-D", str(config.DB_DIR), "stop"], check=True, capture_output=True)
    return True


def get_database_url() -> str:
    """The address the server uses to reach the database.

    DATABASE_URL (environment or .env) wins, for the live server. Otherwise ask the
    local database that start-db started.
    """
    explicit = config.get_setting("DATABASE_URL")
    if explicit:
        return explicit.replace("postgresql://", "postgresql+psycopg://", 1)
    info = PostmasterInfo.read_from_pgdata(config.DB_DIR) if config.DB_DIR.exists() else None
    if info is None or not info.is_running():
        raise DatabaseNotRunning("The database is not running. Start it with:  uv run start-db")
    return info.get_uri(database=config.APP_DATABASE, driver="psycopg")


def make_engine(url: str | None = None) -> sa.Engine:
    return sa.create_engine(url or get_database_url())


def start_db_command() -> None:
    print("Starting the local database...")
    start_db()
    print("Database is running. Stop it with:  uv run stop-db")


def stop_db_command() -> None:
    print("Database stopped." if stop_db() else "Database was not running.")
