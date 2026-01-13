def get_disaggregation_query(initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            oa.option_label    AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
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
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            oa.option_label
    """
    return query


def get_trabajo_remunerado_query(initial_only: bool = True) -> str:
    """Get paid work data (tipo_trabajo values 1, 4, 6) for male respondents."""

    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            oa.option_label    AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
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
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            oa.option_label
    """

    return query


def get_trabajo_remunerado_by_sex_query(
    sex_id: int = 0, initial_only: bool = True
) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            oa.option_label    AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
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
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            oa.option_label
    """
    return query


def get_tipo_trabajo_query(initial_only: bool = True) -> str:
    """Categorize respondents by trabajo remunerado (1,4,6) vs trabajo no remunerado (5)."""

    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            CASE
                WHEN ra.value IN (1, 4, 6) THEN 'trabajo remunerado'
                WHEN ra.value = 5 THEN 'trabajo no remunerado'
                ELSE 'otro'
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
        ON a.question_id = o.question_id
        AND a.option_id   = o.option_id

        LEFT JOIN respondent_attributes ra
        ON a.respondent_id = ra.respondent_id
        AND ra.attribute    = 'tipo_trabajo'

        JOIN responses r
        ON a.respondent_id = r.respondent_id

        WHERE a.question_id = :question_id

        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            grupo
    """
    return query


def get_tipo_trabajo_by_sex_query(sex_id: int = 0, initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            CASE
                WHEN ra.value IN (1, 4, 6) THEN 'trabajo remunerado'
                WHEN ra.value = 5 THEN 'trabajo no remunerado'
                ELSE 'otro'
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
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
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            grupo
    """

    return query


def get_afiliacion_servicio_salud_query(initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            oa.option_label    AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
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
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            oa.option_label
    """
    return query


def get_nivel_max_estudios_query(initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            oa.option_label    AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
        ON a.question_id = o.question_id
        AND a.option_id   = o.option_id 

        LEFT JOIN respondent_attributes ra
        ON a.respondent_id = ra.respondent_id
        AND ra.attribute    = 'nivel_max_estudios'

        LEFT JOIN options oa
        ON ra.question_id = oa.question_id
        AND ra.value       = oa.option_id

        JOIN responses r
        ON a.respondent_id = r.respondent_id

        WHERE a.question_id = :question_id

        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            oa.option_label
    """
    return query
