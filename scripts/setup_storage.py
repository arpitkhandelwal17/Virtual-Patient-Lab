"""Create the storage/ folders (spec section 5.1). Safe to run more than once.

Run from the project folder:  python scripts/setup_storage.py
Nothing in storage/ is ever saved to Git.
"""
from pathlib import Path

FOLDERS = [
    "uploads",      # user uploads, one subfolder per organisation
    "sources",      # copies of fetched DailyMed / PubMed documents
    "populations",  # virtual population (Parquet)
    "results",      # simulation results, one subfolder per run (Parquet)
    "reports",      # generated PDF and Excel reports
    "logs",         # error and activity logs
    "db",           # local database files (development)
]


def main() -> None:
    root = Path(__file__).resolve().parent.parent / "storage"
    for name in FOLDERS:
        folder = root / name
        existed = folder.exists()
        folder.mkdir(parents=True, exist_ok=True)
        print(f"{'already there' if existed else 'created':14} {folder.relative_to(root.parent)}")


if __name__ == "__main__":
    main()
