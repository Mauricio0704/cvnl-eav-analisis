from src.config.survey_data import AMM_ID, ID_TO_CITY_NAME, PERIFERIA_ID


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


def get_servicio_salud_donde_se_atendio_query(initial_only: bool = True) -> str:
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
        AND ra.attribute    = 'servicio_salud_donde_se_atendio'

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


def get_tipo_servicio_salud_donde_se_atendio_query(initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    query = f"""
        SELECT
            COALESCE(o.option_id, a.value)        AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT))     AS Respuesta,
            CASE
                WHEN ra.value IN (2, 3, 7, 8, 9, 10, 12, 13) THEN 'Servicios Privados'
                WHEN ra.value IN (1, 4, 5, 6, 11) THEN 'Servicios Publicos'
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o
        ON a.question_id = o.question_id
        AND a.option_id   = o.option_id

        LEFT JOIN respondent_attributes ra
        ON a.respondent_id = ra.respondent_id
        AND ra.attribute    = 'servicio_salud_donde_se_atendio'

        JOIN responses r
        ON a.respondent_id = r.respondent_id

        WHERE a.question_id = :question_id

        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            grupo
    """
    return query


def get_tipo_escuela_query(initial_only: bool = True) -> str:
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
        AND ra.attribute    = 'tipo_escuela'

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


def get_nivel_actual_estudios_by_tipo_escuela_query(school_type_id: int, initial_only: bool = True) -> str:
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
        AND ra.attribute    = 'nivel_actual_estudios'

        LEFT JOIN respondent_attributes rt
        ON a.respondent_id = rt.respondent_id
        AND rt.attribute    = 'tipo_escuela'

        LEFT JOIN options oa
        ON ra.question_id = oa.question_id
        AND ra.value       = oa.option_id
        AND rt.value = {school_type_id}

        JOIN responses r
        ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id

        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            oa.option_label
    """

    return query


def get_sexo_query(initial_only: bool = True) -> str:
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
        AND ra.attribute    = 'sexo'

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


def get_municipio_query(initial_only: bool = True) -> str:
    """
    Should take into account AMM_ID and PERIFERIA_ID constants.
    The ids are mapped to their names using ID_TO_CITY_NAME.
    The final groups should be
    All municipalities in AMM_ID as their names, a group "AMM", a group "Periferia", a group "Resto NL", and a group "Nuevo León".
    It should use the city_id from the respondent_attributes table.
    """
    weight = "r.factor_cvnl" if initial_only else "1"

    amm_list = ', '.join(map(str, AMM_ID))
    periferia_list = ', '.join(map(str, PERIFERIA_ID))
    amm_plus_perif = ', '.join(map(str, AMM_ID + PERIFERIA_ID))

    # Subquery 1: specific city rows (only for AMM municipalities)
    city_case = ''
    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        city_case += f"WHEN ra.value = {city_id} THEN '{city_name}'\n            "

    query = f"""
        -- City-level rows (only for AMM municipalities)
        SELECT
            COALESCE(o.option_id, a.value) AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT)) AS Respuesta,
            CASE
            {city_case}
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o ON a.question_id = o.question_id AND a.option_id = o.option_id
        LEFT JOIN respondent_attributes ra ON a.respondent_id = ra.respondent_id AND ra.attribute = 'municipio'
        JOIN responses r ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id
          AND ra.value IN ({amm_list})
        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            grupo

        UNION ALL

        -- Regional rows: AMM / Periferia / Resto NL
        SELECT
            COALESCE(o.option_id, a.value) AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT)) AS Respuesta,
            CASE
                WHEN ra.value IN ({amm_list}) THEN 'AMM'
                WHEN ra.value IN ({periferia_list}) THEN 'Periferia'
                WHEN ra.value NOT IN ({amm_plus_perif}) THEN 'Resto NL'
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o ON a.question_id = o.question_id AND a.option_id = o.option_id
        LEFT JOIN respondent_attributes ra ON a.respondent_id = ra.respondent_id AND ra.attribute = 'municipio'
        JOIN responses r ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id
          AND ra.value IS NOT NULL
        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            grupo

        UNION ALL

        -- Entire state row: Nuevo León (any non-null municipio)
        SELECT
            COALESCE(o.option_id, a.value) AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT)) AS Respuesta,
            'Nuevo León' AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o ON a.question_id = o.question_id AND a.option_id = o.option_id
        LEFT JOIN respondent_attributes ra ON a.respondent_id = ra.respondent_id AND ra.attribute = 'municipio'
        JOIN responses r ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id
          AND ra.value IS NOT NULL
        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT))
    """

    return query


def get_municipio_by_sex_query(sex_id: int = 0, initial_only: bool = True) -> str:
    weight = "r.factor_cvnl" if initial_only else "1"

    amm_list = ', '.join(map(str, AMM_ID))
    periferia_list = ', '.join(map(str, PERIFERIA_ID))
    amm_plus_perif = ', '.join(map(str, AMM_ID + PERIFERIA_ID))

    city_case = ''
    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        city_case += f"WHEN ra.value = {city_id} THEN '{city_name}'\n            "

    query = f"""
        -- City-level rows (only for AMM municipalities)
        SELECT
            COALESCE(o.option_id, a.value) AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT)) AS Respuesta,
            CASE
            {city_case}
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o ON a.question_id = o.question_id AND a.option_id = o.option_id
        LEFT JOIN respondent_attributes ra ON a.respondent_id = ra.respondent_id AND ra.attribute = 'municipio'
        JOIN responses r ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id
          AND ra.value IN ({amm_list})
          AND r.sexo = {sex_id}
        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            grupo
        UNION ALL
        -- Regional rows: AMM / Periferia / Resto NL
        SELECT
            COALESCE(o.option_id, a.value) AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT)) AS Respuesta,
            CASE
                WHEN ra.value IN ({amm_list}) THEN 'AMM'
                WHEN ra.value IN ({periferia_list}) THEN 'Periferia'
                WHEN ra.value NOT IN ({amm_plus_perif}) THEN 'Resto NL'
            END AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o ON a.question_id = o.question_id AND a.option_id = o.option_id
        LEFT JOIN respondent_attributes ra ON a.respondent_id = ra.respondent_id AND ra.attribute = 'municipio'
        JOIN responses r ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id
          AND ra.value IS NOT NULL
          AND r.sexo = {sex_id}
        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT)),
            grupo
        UNION ALL
        -- Entire state row: Nuevo León (any non-null municipio)
        SELECT
            COALESCE(o.option_id, a.value) AS id_respuesta,
            COALESCE(o.option_label, CAST(a.value AS TEXT)) AS Respuesta,
            'Nuevo León' AS grupo,
            SUM({weight}) AS valor
        FROM answers a
        LEFT JOIN options o ON a.question_id = o.question_id AND a.option_id = o.option_id
        LEFT JOIN respondent_attributes ra ON a.respondent_id = ra.respondent_id AND ra.attribute = 'municipio'
        JOIN responses r ON a.respondent_id = r.respondent_id
        WHERE a.question_id = :question_id
          AND ra.value IS NOT NULL
          AND r.sexo = {sex_id}
        GROUP BY
            COALESCE(o.option_id, a.value),
            COALESCE(o.option_label, CAST(a.value AS TEXT))
    """
    return query
