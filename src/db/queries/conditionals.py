from src.config.survey_data import AMM_ID, ID_TO_CITY_NAME


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


def get_income_groups_conditionals() -> list[str]:
    return [
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 1 THEN r.factor_cvnl ELSE 0 END) AS 'Sin ingreso'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 2 THEN r.factor_cvnl ELSE 0 END) AS 'Menos de 1 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 3 THEN r.factor_cvnl ELSE 0 END) AS '1-2 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 4 THEN r.factor_cvnl ELSE 0 END) AS '2-3 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 5 THEN r.factor_cvnl ELSE 0 END) AS '3-4 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 6 THEN r.factor_cvnl ELSE 0 END  AS '4-5 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 7 THEN r.factor_cvnl ELSE 0 END) AS '5-6 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 8 THEN r.factor_cvnl ELSE 0 END) AS '6-7 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 9 THEN r.factor_cvnl ELSE 0 END) AS '7-8 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 10 THEN r.factor_cvnl ELSE 0 END) AS '8-9 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 11 THEN r.factor_cvnl ELSE 0 END) AS '9-10 SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 12 THEN r.factor_cvnl ELSE 0 END) AS '10 o más SM'",
        "SUM(CASE WHEN CAST(a_income.value AS INTEGER) = 9999 THEN r.factor_cvnl ELSE 0 END) AS 'No contesta'",
    ]
