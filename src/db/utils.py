import sqlite3
import pandas as pd


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