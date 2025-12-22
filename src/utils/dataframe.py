import pandas as pd


def generate_id(
    df: pd.DataFrame,
    id_name: str,
    id_cols: list[str],
    sep: str = "_",
) -> pd.DataFrame:
    df = df.copy()

    missing = set(id_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns for ID generation: {missing}")

    df[id_name] = df[id_cols].astype(str).agg(sep.join, axis=1).str.lower()
    return df.drop(columns=id_cols)
