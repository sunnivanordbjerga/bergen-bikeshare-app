"""
Initializes the database schema.
"""

import sqlite3

from database.connection import PROJECT_ROOT

SCHEMA_PATH = PROJECT_ROOT / "src" / "database" / "schema.sql"


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text())
