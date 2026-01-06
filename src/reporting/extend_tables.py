import pandas as pd

def add_total_row(df: pd.DataFrame) -> pd.DataFrame:
    total_row = df.iloc[:, 2:].sum()
    total_row.name = 'Total'
    total_df = pd.DataFrame(total_row).T
    total_df.insert(0, df.columns[0], 'Total')
    total_df.insert(1, df.columns[1], 'Total')

    return pd.concat([df, total_df], ignore_index=True)


def get_relative_table(df: pd.DataFrame) -> pd.DataFrame:
    relative_df = df.copy()
    for col in df.columns[2:]:
        total = df[col].iloc[-1]
        if total == 0:
            relative_df[col] = 0
        else:
            relative_df[col] = (df[col] / total) * 100
    return relative_df