import sqlite3
from src.config.paths import DB_DIR
from src.config.survey_data import AMM_ID, ID_TO_CITY_NAME, NUMERICAL_VALUE_QUESTIONS
from src.db.query_builder import QueryBuilder


def get_connection() -> sqlite3.Connection:
    db_path = DB_DIR / "survey.db"
    conn = sqlite3.connect(db_path)
    return conn


def exists_schema(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='questions';
    """
    )

    if cursor.fetchone() is None:
        return False
    return True


def get_question_aggregation(
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


def get_cities_conditionals() -> list[str]:
    conditionals = []

    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        conditionals.append(
            f"SUM(CASE WHEN r.city = {city_id} THEN r.factor_cvnl ELSE 0 END) AS '{city_name}'"
        )

    conditionals.append(
        f"SUM(CASE WHEN r.city NOT IN ({', '.join(map(str, AMM_ID))}) THEN r.factor_cvnl ELSE 0 END) AS 'Resto NL'"
    )

    return conditionals


def get_sex_conditionals() -> list[str]:
    return [
        "SUM(CASE WHEN r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS 'Hombre'",
        "SUM(CASE WHEN r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS 'Mujer'",
    ]


def get_age_groups_conditionals() -> list[str]:
    return [
        "SUM(CASE WHEN r.edad_anos BETWEEN 18 AND 25 THEN r.factor_cvnl ELSE 0 END) AS '18-24'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 26 AND 35 THEN r.factor_cvnl ELSE 0 END) AS '25-34'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 36 AND 45 THEN r.factor_cvnl ELSE 0 END) AS '35-44'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 46 AND 55 THEN r.factor_cvnl ELSE 0 END) AS '45-54'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 56 AND 65 THEN r.factor_cvnl ELSE 0 END) AS '55-64'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 66 AND 75 THEN r.factor_cvnl ELSE 0 END) AS '65-74'",
        "SUM(CASE WHEN r.edad_anos > 74 THEN r.factor_cvnl ELSE 0 END) AS '75 o mas'",
    ]
