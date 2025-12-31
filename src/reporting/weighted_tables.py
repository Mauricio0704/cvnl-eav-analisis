import pandas as pd

from src.config.paths import OUTPUT_DIR
from src.db.queries import (
    get_weighted_question_by_sex,
    get_weighted_question_by_city,
    get_weighted_question_by_age_group,
    get_questions_by_section,
)
from src.utils.excel import write_text_to_excel, write_table_to_excel, get_writer_config


def build_question_report(
    conn, question_id: str, question_text: str, sheet_name: str, section: str
) -> None:
    city_df = get_weighted_question_by_city(conn, question_id)
    age_df = get_weighted_question_by_age_group(conn, question_id)
    sex_df = get_weighted_question_by_sex(conn, question_id)

    titles_with_dfs = [
        ("Respuesta por unidad geográfica", city_df),
        ("Respuesta por sexo", sex_df),
        ("Respuesta por edad", age_df),
    ]

    output_path = OUTPUT_DIR / f"{section}.xlsx"
    config = get_writer_config(output_path)

    with pd.ExcelWriter(**config) as writer:
        start_row = write_text_to_excel(
            writer, sheet_name, f"{question_id} - {question_text}"
        )

        for title, df in titles_with_dfs:
            start_row = write_text_to_excel(writer, sheet_name, title, start_row)
            start_row = write_table_to_excel(writer, sheet_name, df, start_row)


def build_section_report(conn, section) -> None:
    questions_df = get_questions_by_section(conn, section)

    for _, question in questions_df.iterrows():
        build_question_report(
            conn, question["id"], question["q_text"], question["id"], section
        )
