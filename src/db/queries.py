import sqlite3
import pandas as pd

from src.config.survey_data import AMM_ID, ID_TO_CITY_NAME
from src.db.utils import (
    get_injected_default_query,
    get_cities_conditional_query,
    get_age_groups_conditional_query,
    get_sex_conditional_query,
)


def get_question_options(conn: sqlite3.Connection, question_id: str) -> pd.DataFrame:
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


def get_weighted_question_by_city(conn, question_id: str):
    conditional_query = get_cities_conditional_query()

    query = get_injected_default_query(conditional_query)

    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_sex(conn, question_id: str):
    conditinal_query = get_sex_conditional_query()

    query = get_injected_default_query(conditinal_query)

    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_age_group(conn, question_id: str):
    conditional_query = get_age_groups_conditional_query()

    query = get_injected_default_query(conditional_query)

    return pd.read_sql_query(query, conn, params=(question_id,))
