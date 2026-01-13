import pandas as pd


def add_total_row(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    total_row = df.iloc[:, 2:].sum()
    total_row.name = "Total"
    total_df = pd.DataFrame(total_row).T
    total_df.insert(0, df.columns[0], "Total")
    total_df.insert(1, df.columns[1], "Total")

    return pd.concat([df, total_df], ignore_index=True)


def add_weighted_average_row(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    weighted_avg = {}
    for col in df.columns[2:]:
        total = df[col].iloc[-1]
        if total == 0:
            weighted_avg[col] = 0
        else:
            df["Respuesta"] = pd.to_numeric(df["Respuesta"], errors='coerce')
            df[col] = pd.to_numeric(df[col], errors='coerce')

            weighted_avg[col] = (df[col] * df["Respuesta"]).sum() / total

    weighted_avg_row = pd.DataFrame(weighted_avg, index=["Promedio"])
    weighted_avg_row.insert(0, df.columns[0], "Promedio")
    weighted_avg_row.insert(1, df.columns[1], "Promedio")

    return pd.concat([df, weighted_avg_row], ignore_index=True)


def get_relative_table(df: pd.DataFrame) -> pd.DataFrame:
    # Remove Promedio row if exists
    df = df[df[df.columns[0]] != "Promedio"]

    if df.empty:
        return df

    relative_df = df.copy()
    for col in df.columns[2:]:
        total = df[col].iloc[-1]
        if total == 0:
            relative_df[col] = 0
        else:
            relative_df[col] = (df[col] / total) * 100
    return relative_df
