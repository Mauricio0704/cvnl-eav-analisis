HOUSEHOLD_DATA_AND_QUESTIONS = [
    "respondent_id",
    "is_initial_respondent",
    "nombre",
    "city_id",
    "cp2",
    "cp4_1",
    "cp4_2",
    "cp6",
    "cp7",
    "cp8",
    "cp9",
    "cp10a",
    "cp10b",
    "cp11",
    "cp13",
    "cp14",
    "cp15_1",
    "cp15_2",
    "cp16",
    "cp17",
    "cp18",
    "cp19",
    "factor_cvnl",
]

DEMOGRAPHIC_CODES = {
    "cp2": "sexo",
    "city_id": "city",
    "cp4_1": "edad_anos",
    "cp4_2": "edad_meses",
    "factor_cvnl": "factor_cvnl",
}


QUESTIONS_COLUMNS_MAPPING = {
    "Unnamed: 0": "type",
    "ENCUESTA ASÍ VAMOS 2025": "q_num",
    "Unnamed: 2": "q_sub_num",
    "Unnamed: 3": "q_text",
}

MISSING_VALUES = [
    "",
    "NA",
    "N/A",
    "No aplica",
    "No sabe",
    "No contesta",
    777,
    7777,
    77777,
    888,
    8888,
    88888,
    999,
    9999,
    99999,
]

HOUSEHOLD_NUMERIC_QUESTIONS = [
    "cp2",
    "cp4_1",
    "cp4_2",
    "cp6",
    "cp7",
    "cp8",
    "cp9",
    "cp10a",
    "cp10b",
    "cp11",
    "cp13",
    "cp14",
    "cp15_1",
    "cp15_2",
    "cp16",
    "cp17",
    "cp18",
    "cp19",
    "factor_cvnl",
]

QUESTION_SECTIONS = {
    "generales": {"start": "cp1", "end": "cp7"},
    "educacion": {"start": "cp8", "end": "cp19"},
    "ocupacion": {"start": "p1", "end": "p9"},
    "movilidad": {"start": "p10", "end": "p51"},
    "vivienda": {"start": "p52", "end": "p68"},
    "medio_ambiente": {"start": "p69", "end": "p85"},
    "economia": {"start": "p86", "end": "p88"},
    "discriminacion": {"start": "p89", "end": "p91"},
    "salud": {"start": "p92", "end": "p110"},
    "seguridad": {"start": "p111", "end": "p127"},
    "gobierno": {"start": "p128", "end": "p167"},
}

AGE_BINS = [0, 17, 24, 34, 44, 54, 64, 74, 999]
AGE_LABELS = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75 o más"]
