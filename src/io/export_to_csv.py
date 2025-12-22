import pandas as pd

from ..config.paths import PROCESSED_DATA_DIR


def export_responses_to_csv(
    df: pd.DataFrame, demographic_codes: dict[str, str]
) -> None:
    df = df.copy()

    responses = (
        df[
            [
                "respondent_id",
                "is_initial_respondent",
                "nombre",
                *demographic_codes.keys(),
            ]
        ]
        .rename(columns={"respondent_id": "id", **demographic_codes})
        .reset_index(drop=True)
    )
    responses["edad_total_meses"] = responses["edad_anos"] * 12 + responses[
        "edad_meses"
    ].fillna(0)

    responses.to_csv(PROCESSED_DATA_DIR / "responses.csv", index=False)


def export_questions_to_csv(df: pd.DataFrame) -> None:
    df = df.copy()

    questions = df[
        [
            "id",
            "q_text",
            "section",
        ]
    ].reset_index(drop=True)

    questions.to_csv(PROCESSED_DATA_DIR / "questions.csv", index=False)
