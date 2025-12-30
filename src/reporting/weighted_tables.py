import pandas as pd

from src.config.paths import OUTPUT_DIR
from src.db.queries import (
    get_weighted_question_by_sex,
    get_weighted_question_by_city,
    get_weighted_question_by_age_group,
)


def build_question_report(
    conn, question_id: str, sheet_name: str, section: str
) -> pd.DataFrame:
    df = get_weighted_question_by_city(conn, question_id)
    age_df = get_weighted_question_by_age_group(conn, question_id)
    sex_df = get_weighted_question_by_sex(conn, question_id)
    output_path = OUTPUT_DIR / f"{section}.xlsx"

    if output_path.exists():
        mode = "a"
        if_sheet = "overlay"
    else:
        mode = "w"
        if_sheet = None

    with pd.ExcelWriter(
        output_path, engine="openpyxl", mode=mode, if_sheet_exists=if_sheet
    ) as writer:
        start_row = 0

        for title, df in [
            ("Respuesta por unidad geográfica", df),
            ("Respuesta por sexo", sex_df),
            ("Respuesta por edad", age_df),
        ]:
            pd.DataFrame([[title]]).to_excel(
                writer,
                sheet_name=sheet_name,
                startrow=start_row,
                index=False,
                header=False,
            )

            start_row += 1

            df.to_excel(
                writer,
                sheet_name=sheet_name,
                startrow=start_row,
                index=False,
            )

            start_row += len(df) + 3

    df = df.fillna(0)
    return df
