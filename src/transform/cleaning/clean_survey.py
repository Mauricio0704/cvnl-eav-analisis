import pandas as pd

from src.transform.dataframe import generate_id


def generate_questions_ids(df: pd.DataFrame) -> pd.DataFrame:
    question_statements = df[df["type"].notna()].copy()

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

    questions = df.loc[keep].reset_index(drop=True)

    return questions


def clean_questions(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_empty_rows(df)

    q_text_raw = df["q_text"]
    q_text_clean = q_text_raw.astype(str).str.strip()

    question_mask = (
        q_text_raw.notna()
        & (q_text_clean != "")
        & ~q_text_clean.str.match(r"^\d+", na=False)
    )

    question_statements_with_id = df.loc[
        question_mask, ["q_id", "q_text", "q_section", "q_type", "q_notes"]
    ].copy()

    # Normalize whitespace for exported fields
    question_statements_with_id["q_id"] = (
        question_statements_with_id["q_id"].astype(str).str.strip()
    )
    question_statements_with_id["q_text"] = (
        question_statements_with_id["q_text"].astype(str).str.strip()
    )

    # Drop rows where after normalization q_text is the literal 'nan' or empty
    qtxt = question_statements_with_id["q_text"].replace("nan", "").str.strip()
    question_statements_with_id = question_statements_with_id.loc[
        qtxt != ""
    ].reset_index(drop=True)

    return question_statements_with_id


def clean_options(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_empty_rows(df)

    question_options = df[["q_id", "q_text"]].copy()

    # Propagate question id to answers
    is_separator = question_options["q_id"].isna() & question_options["q_text"].isna()
    block = is_separator.cumsum()
    question_options["question_id"] = question_options["q_id"].groupby(block).ffill()

    # Normalize types
    question_options["q_id"] = question_options["q_id"].astype(str).str.strip()
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

    options = options.drop_duplicates(
        subset=["question_id", "option_id"], keep="first"
    ).reset_index(drop=True)

    options["option_id"] = options["option_id"].astype("Int64")

    return options


def clean_responses(df: pd.DataFrame) -> pd.DataFrame:
    responses = df[
        [
            "respondent_id",
            "is_initial_respondent",
            "nombre",
            "factor_cvnl",
            "city_id",
        ]
    ]

    return responses
