import pandas as pd
import numpy as np


def get_individual_responses(survey_df: pd.DataFrame) -> pd.DataFrame:
    df = survey_df.copy()
    household_data_raw = df.filter(regex=r"^p\d+").copy()

    only_for_one = ["cp1", "cp3", "cp5"]
    household_data_raw[only_for_one] = df[only_for_one]

    household_data_raw[["respondent_id"]] = (
        df[["orden_gral_muestra_mv"]].astype(str) + "_1"
    )

    return household_data_raw
