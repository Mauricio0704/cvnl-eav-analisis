import pandas as pd

from src.db.queries.conditionals import (
    get_general_conditionals,
    get_sex_conditionals,
    get_age_groups_conditionals,
    get_cities_conditionals,
)

CONDITIONALS_BY_DIMENSION = {
    "general": get_general_conditionals,
    "city": get_cities_conditionals,
    "sex": get_sex_conditionals,
    "age_group": get_age_groups_conditionals,
}

from src.db.queries.questions import (
    get_question_sections_query,
    get_questions_by_section_query,
    get_weighted_question,
)


def get_question_sections(conn) -> list[str]:
    query = get_question_sections_query()
    df = pd.read_sql_query(query, conn)

    return df["section"].tolist()


def get_questions_by_section(conn, section: str) -> pd.DataFrame:
    query = get_questions_by_section_query(section)
    df = pd.read_sql_query(query, conn)

    return df


def get_weighted_question_by_dimension(
    conn,
    question_id: str,
    dimension: str,
    initial_only: bool = True,
):
    try:
        conditionals = CONDITIONALS_BY_DIMENSION[dimension]()
    except KeyError:
        raise ValueError(f"Unknown dimension: {dimension}")

    return get_weighted_question(
        conn,
        question_id,
        conditionals,
        initial_only=initial_only,
    )
