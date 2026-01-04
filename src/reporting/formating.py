import pandas as pd


def add_percentage(df: pd.DataFrame) -> pd.DataFrame:
    formatted_df = df.copy()
    for col in df.columns[2:]:
        formatted_df[col] = df[col].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else x)
    return formatted_df
