import pandas as pd

from ..utils.dataframe import generate_id
from ..config.survey_data import QUESTION_SECTIONS


def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    empty = df.isna().all(axis=1)

    first_empty_in_block = empty & ~empty.shift(1, fill_value=False)

    # # Conservar las filas no vacías y la primera fila vacía de cada bloque
    keep = ~empty | first_empty_in_block

    questions = df.loc[keep].reset_index(drop=True)[3:]

    return questions


def add_question_section(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["section"] = pd.NA

    for section, bounds in QUESTION_SECTIONS.items():
        start_idx = df.loc[df["id"].str.match(rf"^{bounds['start']}($|_)", na=False)].index[0]
        end_idx = df.loc[df["id"].str.match(rf"^{bounds['end']}($|_)", na=False)].index[-1]

        df.loc[start_idx:end_idx, 'section'] = section

    return df


def clean_questions(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_empty_rows(df)

    question_statements = df[(df["type"] == "CP") | (df["type"] == "P")].copy()

    question_statements_with_id = generate_id(
        question_statements, id_name="id", id_cols=["type", "q_num"], sep=''
    )

    mask = question_statements_with_id["q_sub_num"].notna()

    question_statements_with_id.loc[mask, "id"] = (
        question_statements_with_id.loc[mask, "id"].astype(str)
        + "_"
        + question_statements_with_id.loc[mask, "q_sub_num"].astype(str)
    )

    questions_raw = question_statements_with_id[["id", "q_text"]].copy()

    questions_raw = add_question_section(questions_raw)

    return questions_raw
