import pandas as pd

from src.db.queries.conditionals import (
    get_sex_conditionals,
    get_age_groups_conditionals,
    get_cities_conditionals,
)
from src.db.queries.questions import get_question_sections_query, get_questions_by_section_query
from src.db.queries.aggregation import build_question_aggregation_query


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

    query = build_question_aggregation_query(question_id, conditionals, initial_only=True)

    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_sex(conn, question_id: str):
    conditionals = get_sex_conditionals()

    query = build_question_aggregation_query(question_id, conditionals, initial_only=True)

    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_age_group(conn, question_id: str):
    conditionals = get_age_groups_conditionals()

    query = build_question_aggregation_query(question_id, conditionals, initial_only=True)

    return pd.read_sql_query(query, conn, params=(question_id,))
