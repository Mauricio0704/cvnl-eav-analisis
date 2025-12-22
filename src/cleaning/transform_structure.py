import pandas as pd

from ..config.survey_data import HOUSEHOLD_QUESTIONS
from ..utils.dataframe import generate_id


def remove_emtpy_rows(household_data: pd.DataFrame) -> pd.DataFrame:
    person_mask = household_data.loc[
        (household_data["nombre"].notna()) & (household_data["nombre"] != "Fin")
    ].index
    return household_data.loc[person_mask].copy()


def household_data_to_long_format(
    household_data: pd.DataFrame, max_members_per_household: int
) -> pd.DataFrame:
    df = household_data.copy()

    household_cols = ["household_id", "city_id"]

    long_parts = []

    for n in range(1, max_members_per_household + 1):
        cols_p = [c for c in df.columns if c.endswith(f"_{n}")]
        cols = household_cols + cols_p
        cols.append(f"cp{n}_nombre")

        tmp = df[cols].copy()
        tmp["member_id"] = n
        tmp["is_initial_respondent"] = True if n == 1 else False

        # Renombrar variables cp[q]_[n] -> cp[q] y cp[n]_nombre -> nombre
        tmp = tmp.rename(columns={c: c.rsplit("_", 1)[0] for c in cols_p})
        tmp = tmp.rename(columns={f"cp{n}_nombre": "nombre"})

        long_parts.append(tmp)

    household_long = (
        pd.concat(long_parts, ignore_index=True)
        .sort_values(["household_id", "member_id"])
        .reset_index(drop=True)
    )

    household_person = remove_emtpy_rows(household_long)
    household_with_id = generate_id(
        household_person, id_name="respondent_id", id_cols=["household_id", "member_id"]
    )

    household_with_id = household_with_id[HOUSEHOLD_QUESTIONS].copy()

    return household_with_id
