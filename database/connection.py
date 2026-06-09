"""
Database connection utilities for the Bergen Bysykkel application.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "bysykkel.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn