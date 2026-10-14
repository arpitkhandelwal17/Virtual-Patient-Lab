"""Where things live, and settings read from the private .env file."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "storage" / "db"  # database files (ignored by Git)
APP_DATABASE = "virtual_patient_lab"


def read_env_file(path: Path | None = None) -> dict[str, str]:
    """Read simple KEY=value lines from .env. A missing file gives an empty result."""
    path = path or PROJECT_ROOT / ".env"
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def get_setting(name: str) -> str | None:
    """A setting from the real environment first, then from .env. Empty counts as not set."""
    return os.environ.get(name) or read_env_file().get(name) or None
