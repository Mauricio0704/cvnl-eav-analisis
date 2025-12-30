import pandas as pd

from src.db.utils import (
    get_injected_default_query,
    get_cities_conditional_query,
    get_age_groups_conditional_query,
    get_sex_conditional_query,
    get_question_sections_query,
    get_questions_by_section_query
)

def get_question_sections(conn) -> list[str]:
    query = get_question_sections_query()
    df = pd.read_sql_query(query, conn)

    return df["section"].tolist()


def get_questions_by_section(conn, section: str) -> pd.DataFrame:
    query = get_questions_by_section_query(section)
    df = pd.read_sql_query(query, conn)

    return df


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
