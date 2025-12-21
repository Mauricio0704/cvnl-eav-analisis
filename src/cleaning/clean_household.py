import pandas as pd


def clean_sex(df: pd.DataFrame, q_id: str) -> pd.DataFrame:
    df = df.copy()

    df[q_id] = df[q_id].astype(str).str.extract(r"^\s*(\d+)")[0].astype("Int16")

    return df.copy()


def clean_household_responses(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    missing_values = [
        "",
        "NA",
        "N/A",
        "No aplica",
        "No sabe",
        999,
        9999,
        99999,
        888,
        8888,
        88888,
        777,
        7777,
        77777,
    ]
    df = df.replace(missing_values, pd.NA)

    if "nombre" in df.columns:
        df["nombre"] = df["nombre"].astype(str).str.strip().str.title()

    df = clean_sex(df, "cp2")

    numeric_cols = [
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
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
