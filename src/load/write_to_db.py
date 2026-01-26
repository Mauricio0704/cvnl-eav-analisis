import pandas as pd
import sqlite3


def load_df_to_db(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection) -> None:
    df.to_sql(table_name, conn, if_exists="append", index=False)


def clear_table(conn: sqlite3.Connection, table_name: str) -> None:
    conn.execute(f"DELETE FROM {table_name}")
    conn.commit()


def clear_all_tables(conn: sqlite3.Connection, table_names: list[str]) -> None:
    conn.execute("PRAGMA foreign_keys = OFF")

    for table in table_names:
        conn.execute(f"DELETE FROM {table}")

    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON")
