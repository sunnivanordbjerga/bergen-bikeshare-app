"""
Initializes the database schema.
"""

from src.database.connection import get_connection, PROJECT_ROOT

SCHEMA_PATH = PROJECT_ROOT / "src" / "database" / "schema.sql"


def _init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text())


if __name__ == "__main__":
    _init_db()
