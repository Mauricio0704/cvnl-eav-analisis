import pandas as pd

ATTRIBUTES_MAP = {
    "p1": "tipo_trabajo",
    "p97": "servicio_salud_donde_se_atendio",
    "p167": "ingreso",
}


def get_respondent_attributes(individual_df: pd.DataFrame) -> pd.DataFrame:
    attributes_df = individual_df[
        ["respondent_id"] + list(ATTRIBUTES_MAP.keys())
    ].copy()
    
    attributes_df = attributes_df.drop_duplicates(subset=["respondent_id"])

    return attributes_df
