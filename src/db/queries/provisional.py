def get_disaggregation_query(initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            o.option_id        AS id_respuesta,
            o.option_label     AS Respuesta,
            oa.option_label    AS grupo,
            SUM({weight}) AS valor
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
