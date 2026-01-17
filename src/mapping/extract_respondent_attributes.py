import pandas as pd

INDIVIDUAL_ATTRIBUTES_MAP = {
    "p1": "tipo_trabajo",
    "p97": "servicio_salud_donde_se_atendio",
    "p100": "tipo_consulta",
    "p167": "ingreso",
}

HOUSEHOLD_ATTRIBUTES_MAP = {
    "city_id": "municipio",
    "cp2": "sexo",
    "cp4_1": "edad_anos",
    "cp6": "afiliacion_servicio_salud",
    "cp8": "nivel_max_estudios",
    "cp9": "nivel_actual_estudios",
    "cp11": "tipo_escuela",
}


def get_respondent_attributes(
    individual_df: pd.DataFrame, household_df: pd.DataFrame
) -> pd.DataFrame:

    # Individual
    individual_attrs = individual_df[
        individual_df["question_id"].isin(INDIVIDUAL_ATTRIBUTES_MAP)
    ].copy()

    individual_attrs["attribute"] = individual_attrs["question_id"].map(
        INDIVIDUAL_ATTRIBUTES_MAP
    )

    household_attrs = household_df[
        household_df["question_id"].isin(HOUSEHOLD_ATTRIBUTES_MAP)
    ].copy()

    household_attrs["attribute"] = household_attrs["question_id"].map(
        HOUSEHOLD_ATTRIBUTES_MAP
    )

    # Combine
    attributes_df = pd.concat([individual_attrs, household_attrs], ignore_index=True)

    attributes_df["value"] = attributes_df["value"].combine_first(
        attributes_df["option_id"]
    )

    # Keep exact structure you want
    attributes_df = attributes_df[
        ["respondent_id", "question_id", "value", "attribute"]
    ].dropna(subset=["value"])

    return attributes_df
