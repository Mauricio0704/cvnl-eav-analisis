import pandas as pd


def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    empty = df.isna().all(axis=1)

    first_empty_in_block = empty & ~empty.shift(1, fill_value=False)

    # # Conservar las filas no vacías y la primera fila vacía de cada bloque
    keep = ~empty | first_empty_in_block

    questions = df.loc[keep].reset_index(drop=True)

    return questions
