import pandas as pd

from src.config.survey_data import HOUSEHOLD_NUMERIC_QUESTIONS


def clean_sex(df: pd.DataFrame, q_id: str) -> pd.DataFrame:
    df = df.copy()

    df[q_id] = df[q_id].astype(str).str.extract(r"^\s*(\d+)")[0].astype("Int16")

    return df.copy()


def clean_household_responses(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "nombre" in df.columns:
        df["nombre"] = df["nombre"].astype(str).str.strip().str.title()

    df = clean_sex(df, "cp2")
    df["cp4_1"] = df["cp4_1"].astype("Int16")
    df["cp4_2"] = df["cp4_2"].astype("Int16")

    mask = df["cp4_2"].notna() & (df["cp4_2"] >= 0)
    df.loc[mask, "cp4_1"] = 0

    for col in HOUSEHOLD_NUMERIC_QUESTIONS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
