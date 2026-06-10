"""
Initializes the database schema
"""

from src.database.connection import get_connection
from pathlib import Path

SCHEMA_PATH = Path("src/database/schema.sql")

def init_db() -> None:
    with get_connection() as conn:
     conn.executescript(SCHEMA_PATH.read_text())

if __name__ == "__main__":
    init_db()