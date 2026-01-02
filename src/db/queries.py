import pandas as pd

from src.db.utils import (
    get_sex_conditionals,
    get_age_groups_conditionals,
    get_cities_conditionals,
    get_question_sections_query,
    get_questions_by_section_query,
    get_question_aggregation,
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
    conditionals = get_cities_conditionals()

    query = get_question_aggregation(question_id, conditionals, initial_only=True)

    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_sex(conn, question_id: str):
    conditionals = get_sex_conditionals()

    query = get_question_aggregation(question_id, conditionals, initial_only=True)

    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_age_group(conn, question_id: str):
    conditionals = get_age_groups_conditionals()

    query = get_question_aggregation(question_id, conditionals, initial_only=True)

    return pd.read_sql_query(query, conn, params=(question_id,))
