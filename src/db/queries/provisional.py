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


def get_trabajo_remunerado_query(initial_only: bool = True) -> str:
    """
    This query retrieves data about respondents who have paid work, i.e. those who answered
    1, 4 or 6 to attribute tipo_trabajo. It takes as input a boolean indicating whether to use weights and
    the question ID for disaggregation. It sould get the question id corresponding to the attribute 'tipo_trabajo' from
    the table respondent_attributes. It should use as column headers the option labels corresponding to the values
    1, 4 and 6 from the options table. Only for respondents who are men.
    """
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
        AND ra.attribute    = 'tipo_trabajo'

        LEFT JOIN options oa
        ON ra.question_id = oa.question_id
        AND ra.value       = oa.option_id
        AND ra.value IN (1, 4, 6)

        JOIN responses r
        ON a.respondent_id = r.respondent_id

        WHERE a.question_id = :question_id

        GROUP BY
            o.option_id,
            o.option_label,
            oa.option_label
    """

    return query


def get_trabajo_remunerado_by_sex_query(
    sex_id: int = 0, initial_only: bool = True
) -> str:
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
        AND ra.attribute    = 'tipo_trabajo'

        LEFT JOIN options oa
        ON ra.question_id = oa.question_id
        AND ra.value       = oa.option_id
        AND ra.value IN (1, 4, 6)

        JOIN responses r
        ON a.respondent_id = r.respondent_id

        WHERE a.question_id = :question_id
        AND r.sexo = {sex_id}

        GROUP BY
            o.option_id,
            o.option_label,
            oa.option_label
    """
    return query


def get_tipo_trabajo_query(initial_only: bool = True) -> str:
    """
    Is similar to get_trabajo_remunerado_query. It should consider as trabajo remunerado those respondents
    who answered 1, 4 or 6 to attribute tipo_trabajo and as trabajo no remunerado those who answered 5.
    It should use as column headers trabajo remunerado and trabajo no remunerado.
    """

    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            o.option_id        AS id_respuesta,
            o.option_label     AS Respuesta,
            CASE
                WHEN ra.value IN (1, 4, 6) THEN 'trabajo remunerado'
                WHEN ra.value = 5 THEN 'trabajo no remunerado'
                ELSE 'otro'
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        JOIN options o
        ON a.question_id = o.question_id
        AND a.option_id   = o.option_id

        LEFT JOIN respondent_attributes ra
        ON a.respondent_id = ra.respondent_id
        AND ra.attribute    = 'tipo_trabajo'

        JOIN responses r
        ON a.respondent_id = r.respondent_id

        WHERE a.question_id = :question_id

        GROUP BY
            o.option_id,
            o.option_label,
            grupo
    """
    return query


def get_tipo_trabajo_by_sex_query(sex_id: int = 0, initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            o.option_id        AS id_respuesta,
            o.option_label     AS Respuesta,
            CASE
                WHEN ra.value IN (1, 4, 6) THEN 'trabajo remunerado'
                WHEN ra.value = 5 THEN 'trabajo no remunerado'
                ELSE 'otro'
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        JOIN options o
        ON a.question_id = o.question_id
        AND a.option_id   = o.option_id
        LEFT JOIN respondent_attributes ra
        ON a.respondent_id = ra.respondent_id
        AND ra.attribute    = 'tipo_trabajo'
        JOIN responses r
        ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id
        AND r.sexo = {sex_id}
        GROUP BY
            o.option_id,
            o.option_label,
            grupo
    """

    return query


def get_afiliacion_servicio_salud_query(initial_only: bool = True) -> str:
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
        AND ra.attribute    = 'afiliacion_servicio_salud'

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