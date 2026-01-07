from src.config.survey_data import AMM_ID, ID_TO_CITY_NAME, PERIFERIA_ID


def get_general_conditionals() -> list[str]:
    return [
        "SUM(r.factor_cvnl) AS 'Total'",
    ]


def get_cities_conditionals() -> list[str]:
    conditionals = []

    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        conditionals.append(
            f"SUM(CASE WHEN r.city = {city_id} THEN r.factor_cvnl ELSE 0 END) AS '{city_name}'"
        )
    
    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, AMM_ID))}) THEN r.factor_cvnl ELSE 0 END) AS 'AMM'"
    )
    
    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, PERIFERIA_ID))}) THEN r.factor_cvnl ELSE 0 END) AS 'Periferia'"
    )

    conditionals.append(
        f"SUM(CASE WHEN r.city NOT IN ({', '.join(map(str, AMM_ID + PERIFERIA_ID))}) THEN r.factor_cvnl ELSE 0 END) AS 'Resto NL'"
    )

    conditionals.append(
        "SUM(r.factor_cvnl) AS 'Nuevo León'"
    )

    return conditionals


def get_sex_conditionals() -> list[str]:
    return [
        "SUM(CASE WHEN r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS 'Hombre'",
        "SUM(CASE WHEN r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS 'Mujer'",
    ]

def get_men_per_city_conditionals() -> list[str]:
    conditionals = []

    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        conditionals.append(
            f"SUM(CASE WHEN r.city = {city_id} AND r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS '{city_name}'"
        )
    
    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, AMM_ID))}) AND r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS 'AMM'"
    )
    
    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, PERIFERIA_ID))}) AND r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS 'Periferia'"
    )

    conditionals.append(
        f"SUM(CASE WHEN r.city NOT IN ({', '.join(map(str, AMM_ID + PERIFERIA_ID))}) AND r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS 'Resto NL'"
    )

    conditionals.append(
        "SUM(CASE WHEN r.sexo = 0 THEN r.factor_cvnl ELSE 0 END) AS 'Nuevo León'"
    )

    return conditionals

def get_women_per_city_conditionals() -> list[str]:
    conditionals = []

    for city_id in AMM_ID:
        city_name = ID_TO_CITY_NAME[city_id]
        conditionals.append(
            f"SUM(CASE WHEN r.city = {city_id} AND r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS '{city_name}'"
        )
    
    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, AMM_ID))}) AND r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS 'AMM'"
    )
    
    conditionals.append(
        f"SUM(CASE WHEN r.city IN ({', '.join(map(str, PERIFERIA_ID))}) AND r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS 'Periferia'"
    )

    conditionals.append(
        f"SUM(CASE WHEN r.city NOT IN ({', '.join(map(str, AMM_ID + PERIFERIA_ID))}) AND r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS 'Resto NL'"
    )

    conditionals.append(
        "SUM(CASE WHEN r.sexo = 1 THEN r.factor_cvnl ELSE 0 END) AS 'Nuevo León'"
    )

    return conditionals


def get_age_groups_conditionals() -> list[str]:
    return [
        "SUM(CASE WHEN r.edad_anos BETWEEN 18 AND 24 THEN r.factor_cvnl ELSE 0 END) AS '18-24'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 25 AND 34 THEN r.factor_cvnl ELSE 0 END) AS '25-34'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 35 AND 44 THEN r.factor_cvnl ELSE 0 END) AS '35-44'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 45 AND 54 THEN r.factor_cvnl ELSE 0 END) AS '45-54'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 55 AND 64 THEN r.factor_cvnl ELSE 0 END) AS '55-64'",
        "SUM(CASE WHEN r.edad_anos BETWEEN 65 AND 74 THEN r.factor_cvnl ELSE 0 END) AS '65-74'",
        "SUM(CASE WHEN r.edad_anos > 74 THEN r.factor_cvnl ELSE 0 END) AS '75 o mas'",
    ]
