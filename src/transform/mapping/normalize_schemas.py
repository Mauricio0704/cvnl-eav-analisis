import pandas as pd


def normalize_questions_schema(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()

    questions_headers_mapping = {
        "id": "q_id",
        "pregunta": "q_text",
        "seccion": "q_section",
        "tipo": "q_type",
        "notas": "q_notes",
    }

    new_df.rename(questions_headers_mapping, axis=1, inplace=True)

    question_statements_mask = new_df["q_id"].notna()

    new_df.loc[question_statements_mask, "q_id"] = (
        new_df.loc[question_statements_mask, "q_id"].astype(str).str.lower()
    )

    return new_df.rename(questions_headers_mapping, axis=1)


def normalize_disaggregations_schema(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()

    disaggregations_headers_mapping = {
        "copdigo_p": "type",
        "numero_p": "q_num",
        "inciso_p": "q_sub_num",
        "pregunta": "q_text",
    }

    new_df.rename(columns=lambda c: c.removeprefix("por_"), inplace=True)

    return new_df.rename(disaggregations_headers_mapping, axis=1)
