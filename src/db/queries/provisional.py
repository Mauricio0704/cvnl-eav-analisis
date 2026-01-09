def get_income_query() -> str:
    query = """
        WITH income AS (
            SELECT
                respondent_id,
                option_id AS income
            FROM answers
            WHERE question_id = 'p167'
        )
        SELECT
            o.option_id AS id_respuesta,
            o.option_label AS Respuesta,

            SUM(CASE WHEN i.income = 1  THEN r.factor_cvnl ELSE 0 END) AS 'Sin ingreso',
            SUM(CASE WHEN i.income = 2  THEN r.factor_cvnl ELSE 0 END) AS 'Menos de 1 SM',
            SUM(CASE WHEN i.income = 3  THEN r.factor_cvnl ELSE 0 END) AS '1-2 SM',
            SUM(CASE WHEN i.income = 4  THEN r.factor_cvnl ELSE 0 END) AS '2-3 SM',
            SUM(CASE WHEN i.income = 5  THEN r.factor_cvnl ELSE 0 END) AS '3-4 SM',
            SUM(CASE WHEN i.income = 6  THEN r.factor_cvnl ELSE 0 END) AS '4-5 SM',
            SUM(CASE WHEN i.income = 7  THEN r.factor_cvnl ELSE 0 END) AS '5-6 SM',
            SUM(CASE WHEN i.income = 8  THEN r.factor_cvnl ELSE 0 END) AS '6-7 SM',
            SUM(CASE WHEN i.income = 9  THEN r.factor_cvnl ELSE 0 END) AS '7-8 SM',
            SUM(CASE WHEN i.income = 10 THEN r.factor_cvnl ELSE 0 END) AS '8-9 SM',
            SUM(CASE WHEN i.income = 11 THEN r.factor_cvnl ELSE 0 END) AS '9-10 SM',
            SUM(CASE WHEN i.income = 12 THEN r.factor_cvnl ELSE 0 END) AS '10 o más SM',
            SUM(CASE WHEN i.income = 9999 THEN r.factor_cvnl ELSE 0 END) AS 'No contesta'

        FROM answers a
        JOIN responses r
        ON a.respondent_id = r.respondent_id

        LEFT JOIN income i
        ON i.respondent_id = a.respondent_id

        JOIN options o
        ON a.question_id = o.question_id
        AND a.option_id = o.option_id

        WHERE r.is_initial_respondent = 1
        AND a.question_id = ?

        GROUP BY o.option_id, o.option_label
        ORDER BY o.option_id;
    """
    return query


def get_disaggregation_query() -> str:
    query = f"""
        SELECT
            o.option_id        AS id_respuesta,
            o.option_label     AS Respuesta,
            oa.option_label    AS grupo,
            SUM(r.factor_cvnl) AS valor
        FROM answers a
        JOIN options o
        ON a.question_id = o.question_id
        AND a.option_id   = o.option_id

        LEFT JOIN respondent_attributes ra
        ON a.respondent_id = ra.respondent_id
        AND ra.attribute    = :dimension

        LEFT JOIN options oa
        ON ra.question_id = oa.question_id
        AND ra.value       = oa.option_id

        JOIN responses r
        ON a.respondent_id = r.respondent_id

        WHERE a.question_id = :question_id

        GROUP BY
            o.option_id,
            o.option_label,
            oa.option_label
    """
    return query