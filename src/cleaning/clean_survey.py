import pandas as pd

from ..utils.dataframe import generate_id
from ..config.survey_data import QUESTION_SECTIONS


def generate_questions_ids(df: pd.DataFrame) -> pd.DataFrame:
    question_statements = df[(df["type"] == "CP") | (df["type"] == "P")].copy()

    question_statements_with_id = generate_id(
        question_statements, id_name="id", id_cols=["type", "q_num"], sep=""
    )

    mask = question_statements_with_id["q_sub_num"].notna()

    question_statements_with_id.loc[mask, "id"] = (
        question_statements_with_id.loc[mask, "id"].astype(str)
        + "_"
        + question_statements_with_id.loc[mask, "q_sub_num"].astype(str)
    )

    df["id"] = question_statements_with_id["id"]
    return df


def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    empty = df.isna().all(axis=1)

    first_empty_in_block = empty & ~empty.shift(1, fill_value=False)

    keep = ~empty | first_empty_in_block

    questions = df.loc[keep].reset_index(drop=True)[3:]

    return questions


def add_question_section(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["section"] = pd.NA

    for section, bounds in QUESTION_SECTIONS.items():
        start_question = df.loc[
            df["id"].str.match(rf"^{bounds['start']}($|_)", na=False)
        ]
        end_question = df.loc[df["id"].str.match(rf"^{bounds['end']}($|_)", na=False)]

        start_idx = start_question.index[0]
        end_idx = end_question.index[-1]

        df.loc[start_idx:end_idx, "section"] = section

    return df


def clean_questions(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_empty_rows(df)
    df = generate_questions_ids(df)

    question_statements_with_id = df[(df["type"] == "CP") | (df["type"] == "P")].copy()

    questions_raw = question_statements_with_id[["id", "q_text"]].copy()

    questions_raw = add_question_section(questions_raw)

    return questions_raw


def clean_options(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_empty_rows(df)
    df = generate_questions_ids(df)

    question_options = df[["id", "q_text"]].copy()

    # Propagate question id to answers
    is_separator = question_options["id"].isna() & question_options["q_text"].isna()
    block = is_separator.cumsum()
    question_options["question_id"] = question_options["id"].groupby(block).ffill()

    # Normalize types
    question_options["id"] = question_options["id"].astype(str).str.strip()
    question_options["q_text"] = question_options["q_text"].astype(str).str.strip()

    # Get answer rows
    question_options = question_options.loc[~question_options.isna().all(axis=1)]
    answer_mask = question_options["q_text"].str.match(r"^\d+", na=False)

    # Separate and assign option ids and labels
    split_id_and_label = question_options.loc[answer_mask, "q_text"].str.split(
        r"\.", n=1, expand=True
    )
    question_options.loc[answer_mask, "option_id"] = split_id_and_label[0].str.strip()
    question_options.loc[answer_mask, "option_label"] = (
        split_id_and_label[1].str.strip().fillna(split_id_and_label[0].str.strip())
    )

    answers = question_options.loc[
        answer_mask, ["question_id", "option_id", "option_label"]
    ]

    options = answers.copy()

    options = (
        options
        .drop_duplicates(subset=["question_id", "option_id"], keep="first")
        .reset_index(drop=True)
    )

    return options
