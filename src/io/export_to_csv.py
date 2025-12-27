import pandas as pd

from ..config.paths import PROCESSED_DATA_DIR
from ..config.survey_data import AGE_BINS, AGE_LABELS


def export_responses_to_csv(df: pd.DataFrame) -> None:
    df = df.copy()

    responses = df[
        [
            "respondent_id",
            "is_initial_respondent",
            "nombre",
            "sexo",
            "city",
            "edad_anos",
            "grupo_edad",
            "factor_cvnl",
        ]
    ].reset_index(drop=True)

    responses.to_csv(PROCESSED_DATA_DIR / "responses.csv", index=False)


def export_questions_to_csv(df: pd.DataFrame) -> None:
    df = df.copy()

    questions = df[["id", "q_text", "section"]].reset_index(drop=True)

    questions.to_csv(PROCESSED_DATA_DIR / "questions.csv", index=False)


def export_options_to_csv(df: pd.DataFrame) -> None:
    df = df.copy()

    options = df[["question_id", "option_id", "option_label"]].reset_index(drop=True)

    options.to_csv(PROCESSED_DATA_DIR / "options.csv", index=False)


def export_household_answers_to_csv(df: pd.DataFrame) -> None:
    df = df.copy()

    answers = df[["respondent_id", "question_id", "answer_id"]].reset_index(drop=True)

    answers.to_csv(PROCESSED_DATA_DIR / "answers.csv", index=False)


def export_individual_answers_to_csv(df: pd.DataFrame) -> None:
    df = df.copy()

    answers = df[["respondent_id", "question_id", "answer_id"]].reset_index(drop=True)

    answers.to_csv(
        PROCESSED_DATA_DIR / "answers.csv", index=False, mode="a", header=False
    )
