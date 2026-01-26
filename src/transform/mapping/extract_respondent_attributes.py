import pandas as pd

ATTRIBUTES_MAP = {
    "p1": "tipo_trabajo",
    "p17": "modo_transporte",
    "p97": "servicio_salud_donde_se_atendio",
    "p100": "tipo_consulta",
    "p167": "ingreso",
    "cp2": "sexo",
    "cp4_1": "edad_anos",
    "cp6": "afiliacion_servicio_salud",
    "cp8": "nivel_max_estudios",
    "cp9": "nivel_actual_estudios",
    "cp11": "tipo_escuela",
}


def get_respondent_attributes(complete_answers: pd.DataFrame) -> pd.DataFrame:
    attrs = complete_answers[
        complete_answers["question_id"].isin(ATTRIBUTES_MAP)
    ].copy()

    attrs["attribute"] = attrs["question_id"].map(ATTRIBUTES_MAP)

    attrs["value"] = attrs["value"].combine_first(attrs["option_id"])

    result = (
        attrs[["respondent_id", "question_id", "value", "attribute"]]
        .dropna(subset=["value"])
        .reset_index(drop=True)
    )

    return result
