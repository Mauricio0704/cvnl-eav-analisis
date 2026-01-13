import pandas as pd


def normalize_questions_schema(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()

    questions_headers_mapping = {
        "Unnamed: 0": "type",
        "ENCUESTA ASÍ VAMOS 2025": "q_num",
        "Unnamed: 2": "q_sub_num",
        "Unnamed: 3": "q_text",
    }

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
