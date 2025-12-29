import sqlite3
import pandas as pd


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
    query = """
        SELECT
            o.option_id    AS id_respuesta,
            o.option_label AS Respuesta,

            SUM(CASE WHEN r.city = 6 THEN r.factor_cvnl ELSE 0 END) AS Apodaca,
            SUM(CASE WHEN r.city = 39 THEN r.factor_cvnl ELSE 0 END) AS Monterrey

        FROM answers a
        JOIN responses r
            ON a.respondent_id = r.respondent_id
        JOIN options o
            ON a.question_id = o.question_id
        AND a.option_id = o.option_id

        WHERE a.question_id = ?
        AND r.is_initial_respondent = 1

        GROUP BY o.option_id, o.option_label
        ORDER BY o.option_id;
    """
    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_sex(conn, question_id: str):
    query = """
        SELECT
            o.option_id    AS id_respuesta,
            o.option_label AS Respuesta,

            SUM(CASE WHEN r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS Hombre,
            SUM(CASE WHEN r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS Mujer

        FROM answers a
        JOIN responses r
            ON a.respondent_id = r.respondent_id
        JOIN options o
            ON a.question_id = o.question_id
        AND a.option_id = o.option_id

        WHERE a.question_id = ?
        AND r.is_initial_respondent = 1

        GROUP BY o.option_id, o.option_label
        ORDER BY o.option_id;
    """
    return pd.read_sql_query(query, conn, params=(question_id,))


def get_weighted_question_by_age_group(conn, question_id: str):
    query = """
        SELECT
            o.option_id    AS id_respuesta,
            o.option_label AS Respuesta,

            SUM(CASE WHEN r.grupo_edad = '18-24' THEN r.factor_cvnl ELSE 0 END) AS edad_18_24,
            SUM(CASE WHEN r.grupo_edad = '25-34' THEN r.factor_cvnl ELSE 0 END) AS edad_25_34

        FROM answers a
        JOIN responses r
            ON a.respondent_id = r.respondent_id
        JOIN options o
            ON a.question_id = o.question_id
        AND a.option_id = o.option_id

        WHERE a.question_id = ?
        AND r.is_initial_respondent = 1

        GROUP BY o.option_id, o.option_label
        ORDER BY o.option_id;
    """
    return pd.read_sql_query(query, conn, params=(question_id,))