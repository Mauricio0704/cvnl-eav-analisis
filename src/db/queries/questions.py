import pandas as pd
from src.db.queries.aggregation import build_question_aggregation_query


def get_question_sections_query() -> str:
    query = """
        SELECT DISTINCT
            section
        FROM questions
        WHERE section IS NOT NULL
        ORDER BY section;
    """
    return query


def get_questions_by_section_query(section: str) -> str:
    query = f"""
        SELECT
            id,
            q_text
        FROM questions
        WHERE section = '{section}'
        ORDER BY id;
    """
    return query


def get_weighted_question(
    conn,
    question_id: str,
    conditionals: list[str],
    initial_only: bool = True,
) -> pd.DataFrame:
    query = build_question_aggregation_query(
        question_id,
        conditionals,
        initial_only=initial_only,
    )

    return pd.read_sql_query(query, conn, params=(question_id,))
