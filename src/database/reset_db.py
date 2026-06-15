"""
Recreates and seeds the local development database

WARNING: Deletes the existing database file if it exists.
"""

from database.connection import DB_PATH
from database.init_db import init_db
from seed_data.seed import seed_database


def reset_db() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    init_db()
    seed_database()


if __name__ == "__main__":
    reset_db()
