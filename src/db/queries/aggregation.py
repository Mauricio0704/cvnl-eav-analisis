from src.config.survey_data import NUMERICAL_VALUE_QUESTIONS
from src.db.query_builder import QueryBuilder


def build_question_aggregation_query(
    question_id: str,
    conditional_columns: list[str],
    initial_only: bool = True,
) -> str:

    qb = QueryBuilder()

    if initial_only:
        qb.where("r.is_initial_respondent = 1")

    if question_id in NUMERICAL_VALUE_QUESTIONS:
        qb.select(
            "a.value AS id_respuesta",
            "a.value AS Respuesta",
        ).group_by(
            "a.value"
        ).order_by("a.value")

    else:
        qb.select(
            "o.option_id AS id_respuesta",
            "o.option_label AS Respuesta",
        ).join(
            """JOIN options o
               ON a.question_id = o.question_id
              AND a.option_id = o.option_id"""
        ).group_by("o.option_id", "o.option_label",).order_by("o.option_id")

    qb.select(*conditional_columns).from_("answers a").where("a.question_id = ?").join(
        "JOIN responses r ON a.respondent_id = r.respondent_id"
    )

    return qb.build()
