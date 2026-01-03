import pandas as pd

def add_total_row(df: pd.DataFrame) -> pd.DataFrame:
    total_row = df.iloc[:, 2:].sum()
    total_row.name = 'Total'
    total_df = pd.DataFrame(total_row).T
    total_df.insert(0, df.columns[0], 'Total')
    total_df.insert(1, df.columns[1], 'Total')

    return pd.concat([df, total_df], ignore_index=True)


