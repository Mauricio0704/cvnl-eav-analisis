from src.config.survey_data import AMM_ID, ID_TO_CITY_NAME, PERIFERIA_ID


def _get_weight(initial_only: bool) -> str:
    return "r.factor_cvnl" if initial_only else "1"


def get_general_conditionals(initial_only: bool = True) -> list[str]:
    weight = _get_weight(initial_only)
    return [f"SUM({weight}) AS 'Total'"]


def get_cities_conditionals(initial_only: bool = True) -> list[str]:
    weight = _get_weight(initial_only)
    conditionals = []

    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        conditionals.append(
            f"SUM(CASE WHEN r.city = {city_id} THEN {weight} ELSE 0 END) AS '{city_name}'"
        )

    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, AMM_ID))}) THEN {weight} ELSE 0 END) AS 'AMM'"
    )

    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, PERIFERIA_ID))}) THEN {weight} ELSE 0 END) AS 'Periferia'"
    )

    conditionals.append(
        f"SUM(CASE WHEN r.city NOT IN ({', '.join(map(str, AMM_ID + PERIFERIA_ID))}) THEN {weight} ELSE 0 END) AS 'Resto NL'"
    )

    conditionals.append(f"SUM({weight}) AS 'Nuevo León'")

    return conditionals


def get_sex_conditionals(initial_only: bool = True) -> list[str]:
    weight = _get_weight(initial_only)
    return [
        f"SUM(CASE WHEN r.sexo = 0 THEN {weight} ELSE 0 END) AS 'Hombre'",
        f"SUM(CASE WHEN r.sexo = 1 THEN {weight} ELSE 0 END) AS 'Mujer'",
    ]


def get_sex_per_city_conditionals(sex_id: int, initial_only: bool = True) -> list[str]:
    weight = _get_weight(initial_only)
    conditionals = []

    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        conditionals.append(
            f"SUM(CASE WHEN r.city = {city_id} AND r.sexo = {sex_id} THEN {weight} ELSE 0 END) AS '{city_name}'"
        )

    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, AMM_ID))}) AND r.sexo = {sex_id} THEN {weight} ELSE 0 END) AS 'AMM'"
    )
    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, PERIFERIA_ID))}) AND r.sexo = {sex_id} THEN {weight} ELSE 0 END) AS 'Periferia'"
    )
    conditionals.append(
        f"SUM(CASE WHEN r.city NOT IN ({', '.join(map(str, AMM_ID + PERIFERIA_ID))}) AND r.sexo = {sex_id} THEN {weight} ELSE 0 END) AS 'Resto NL'"
    )
    conditionals.append(
        f"SUM(CASE WHEN r.sexo = {sex_id} THEN {weight} ELSE 0 END) AS 'Nuevo León'"
    )

    return conditionals


def get_men_per_city_conditionals(initial_only: bool = True) -> list[str]:
    return get_sex_per_city_conditionals(0, initial_only)


def get_women_per_city_conditionals(initial_only: bool = True) -> list[str]:
    return get_sex_per_city_conditionals(1, initial_only)


def get_age_groups_conditionals(initial_only: bool = True) -> list[str]:
    weight = _get_weight(initial_only)
    extra_conditionals = []

    if not initial_only:
        extra_conditionals = [
            f"SUM(CASE WHEN r.edad_anos BETWEEN 0 AND 5 THEN {weight} ELSE 0 END) AS '0-5'",
            f"SUM(CASE WHEN r.edad_anos BETWEEN 6 AND 12 THEN {weight} ELSE 0 END) AS '6-12'",
            f"SUM(CASE WHEN r.edad_anos BETWEEN 13 AND 17 THEN {weight} ELSE 0 END) AS '13-17'",
        ]

    return [
        *extra_conditionals,
        f"SUM(CASE WHEN r.edad_anos BETWEEN 18 AND 24 THEN {weight} ELSE 0 END) AS '18-24'",
        f"SUM(CASE WHEN r.edad_anos BETWEEN 25 AND 34 THEN {weight} ELSE 0 END) AS '25-34'",
        f"SUM(CASE WHEN r.edad_anos BETWEEN 35 AND 44 THEN {weight} ELSE 0 END) AS '35-44'",
        f"SUM(CASE WHEN r.edad_anos BETWEEN 45 AND 54 THEN {weight} ELSE 0 END) AS '45-54'",
        f"SUM(CASE WHEN r.edad_anos BETWEEN 55 AND 64 THEN {weight} ELSE 0 END) AS '55-64'",
        f"SUM(CASE WHEN r.edad_anos BETWEEN 65 AND 74 THEN {weight} ELSE 0 END) AS '65-74'",
        f"SUM(CASE WHEN r.edad_anos > 74 THEN {weight} ELSE 0 END) AS '75 o mas'",
    ]
