import pandas as pd

from src.db.queries.conditionals import (
    get_general_conditionals,
    get_sex_conditionals,
    get_age_groups_conditionals,
    get_men_per_city_conditionals,
    get_women_per_city_conditionals,
    get_cities_conditionals,
)
from src.db.queries.provisional import (
    get_income_query,
    get_disaggregation_query,
)

CONDITIONALS_BY_DIMENSION = {
    "general": get_general_conditionals,
    "city": get_cities_conditionals,
    "sex": get_sex_conditionals,
    "age_group": get_age_groups_conditionals,
    "men_per_city": get_men_per_city_conditionals,
    "women_per_city": get_women_per_city_conditionals,
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
        conditionals = CONDITIONALS_BY_DIMENSION[dimension](initial_only=initial_only)
    except KeyError:
        raise ValueError(f"Unknown dimension: {dimension}")

    return get_weighted_question(
        conn,
        question_id,
        conditionals,
        initial_only=initial_only,
    )


def get_weighted_question_by_income_group(
    conn,
    question_id: str,
):
    income_query = get_income_query()

    return pd.read_sql_query(
        income_query,
        conn,
        params=(question_id,),
    )


def build_disaggregation_report(
    conn,
    question_id: str,
    disaggregation: str,
    initial_only: bool = True,
) -> pd.DataFrame:
    sql = get_disaggregation_query(initial_only)

    df_long = pd.read_sql_query(
        sql,
        conn,
        params={
            "question_id": question_id,
            "dimension": disaggregation,
        },
    )

    if df_long.empty:
        return df_long

    df_pivot = df_long.pivot_table(
        index=["id_respuesta", "Respuesta"],
        columns="grupo",
        values="valor",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()

    fixed_cols = ["id_respuesta", "Respuesta"]
    group_cols = [c for c in df_pivot.columns if c not in fixed_cols]

    df_pivot = df_pivot[fixed_cols + group_cols]

    return df_pivot
