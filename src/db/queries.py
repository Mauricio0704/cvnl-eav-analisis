import sqlite3
import pandas as pd


def get_question_options(conn:sqlite3.Connection, question_id: str) -> pd.DataFrame:
    sql = """
        SELECT
        q.id,
        q.q_text,
        o.option_id,
        o.option_label
        FROM questions q
        JOIN options o
        ON q.id = o.question_id
        WHERE q.id = ?
        ORDER BY o.option_id;
    """
    return pd.read_sql_query(sql, conn, params=[question_id])
