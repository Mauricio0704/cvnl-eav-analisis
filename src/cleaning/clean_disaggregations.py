import pandas as pd

from src.cleaning.clean_survey import generate_questions_ids


def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    print(df.head())
    new_df = df.copy()
    mask = new_df["type"].notna()
    return new_df[mask]


def clean_disaggregations(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()

    new_df = remove_empty_rows(new_df)

    numeric_cols = new_df.select_dtypes(include="number").columns
    new_df[numeric_cols] = new_df[numeric_cols].astype("Int16")

    new_df = generate_questions_ids(new_df)

    new_df.drop(["type", "q_num", "q_sub_num", "q_text", "eje"], axis=1, inplace=True)

    print(new_df.columns.tolist())

    return new_df
