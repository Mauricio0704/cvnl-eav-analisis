import sqlite3
from src.config.paths import DB_DIR


def get_connection() -> sqlite3.Connection:
    db_path = DB_DIR / "survey.db"
    conn = sqlite3.connect(db_path)
    return conn


def exists_schema(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='questions';
    """
    )

    if cursor.fetchone() is None:
        return False
    return True
