import pandas as pd

from src.config.survey_data import QUESTIONS_COLUMNS_MAPPING


def normalize_questions_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    return df.rename(columns=QUESTIONS_COLUMNS_MAPPING)
