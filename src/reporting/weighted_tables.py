import pandas as pd
from src.db.queries import get_weighted_question_by_sex


def build_question_report(conn, question_id: str) -> pd.DataFrame:
    df = get_weighted_question_by_sex(conn, question_id)

    df = df.fillna(0)
    return df
