import pandas as pd

from src.config.survey_data import (
    HOUSEHOLD_DATA_AND_QUESTIONS,
    NUMERICAL_VALUE_QUESTIONS,
)
from src.transform.dataframe import generate_id

def remove_emtpy_rows(household_data: pd.DataFrame) -> pd.DataFrame:
    person_mask = household_data.loc[
        (household_data["nombre"].notna()) & (household_data["nombre"] != "Fin")
    ].index
    return household_data.loc[person_mask].copy()


def household_members_to_long_format(
    household_data: pd.DataFrame, max_members_per_household: int
) -> pd.DataFrame:
    df = household_data.copy()

    household_cols = ["household_id", "city_id", "factor_cvnl"]

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

    household_with_id = household_with_id[HOUSEHOLD_DATA_AND_QUESTIONS].copy()

    return household_with_id


def household_questions_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    new_df = pd.melt(
        df,
        id_vars=["respondent_id"],
        value_vars=[
            "city_id",
            "cp2",
            "cp4_1",
            "cp4_2",
            "cp6",
            "cp7",
            "cp8",
            "cp9",
            "cp10_a",
            "cp10_b",
            "cp11",
            "cp12",
            "cp13",
            "cp14",
            "cp15_1",
            "cp15_2",
            "cp16",
            "cp17",
            "cp18",
            "cp19",
        ],
        var_name="question_id",
        value_name="answer_id",
    )
    new_df = new_df[new_df["answer_id"].notna()]
    new_df["answer_id"] = new_df["answer_id"].astype("Int64")

    is_numeric = new_df["question_id"].isin(NUMERICAL_VALUE_QUESTIONS)
    new_df["value"] = new_df["answer_id"].where(is_numeric)
    new_df["option_id"] = new_df["answer_id"].where(~is_numeric)

    return new_df.drop("answer_id", axis=1)


def individual_questions_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    new_df = pd.melt(
        df,
        id_vars=["respondent_id"],
        value_vars=df.columns.tolist().remove("respondent_id"),
        var_name="question_id",
        value_name="answer_id",
    )
    new_df = new_df[new_df["answer_id"].notna()]
    new_df["answer_id"] = new_df["answer_id"].astype("Int64")

    is_numeric = new_df["question_id"].isin(NUMERICAL_VALUE_QUESTIONS)
    new_df["value"] = new_df["answer_id"].where(is_numeric)
    new_df["option_id"] = new_df["answer_id"].where(~is_numeric)

    return new_df.drop("answer_id", axis=1)


def concatenate_answers(
    household_questions: pd.DataFrame, individual_questions: pd.DataFrame
) -> pd.DataFrame:
    return pd.concat([household_questions, individual_questions], ignore_index=True)