import pandas as pd
import numpy as np


def get_household_data(survey_df: pd.DataFrame) -> pd.DataFrame:
    df = survey_df.copy()
    household_data_raw = df.filter(regex=r"^cp\d+").copy()

    only_for_one = ["cp1", "cp3_1", "cp4_1_ed", "cp5_1"]
    household_data_raw.drop(only_for_one, axis=1, inplace=True)

    household_data_raw["cp4_2_1"] = np.nan

    column_mapping = {"cp4_1": "cp4_1_1"}
    household_data_raw.rename(mapper=column_mapping, axis=1, inplace=True)

    household_data_raw[["household_id", "city_id"]] = df[
        ["orden_gral_muestra_mv", "mun_mv"]
    ].copy()

    return household_data_raw
