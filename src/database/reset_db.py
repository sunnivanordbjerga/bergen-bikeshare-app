from database.connection import DB_PATH
from database.init_db import _init_db
from seed_data.seed import _seed_database


def reset_db():
    if DB_PATH.exists():
        DB_PATH.unlink()

    _init_db()

    _seed_database()

if __name__ == '__main__':
    reset_db()