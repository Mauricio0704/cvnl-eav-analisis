import pandas as pd

from src.config.paths import OUTPUT_DIR
from src.reporting.extend_tables import add_total_row, get_relative_table
from src.db.repository import (
    get_questions_by_section,
    get_weighted_question_by_dimension,
    get_weighted_question_by_income_group,
)
from src.utils.excel import (
    ExcelContext,
    write_text_to_excel,
    write_table_to_excel,
    get_writer_config,
)


def build_question_report(
    conn, question_id: str, question_text: str, sheet_name: str, section: str
) -> None:
    if question_id.startswith("cp"):
        initial_only = False
    else:
        initial_only = True

    general_df = add_total_row(
        get_weighted_question_by_dimension(conn, question_id, "general", initial_only)
    )
    city_df = add_total_row(
        get_weighted_question_by_dimension(conn, question_id, "city", initial_only)
    )
    age_df = add_total_row(
        get_weighted_question_by_dimension(conn, question_id, "age_group", initial_only)
    )
    sex_df = add_total_row(
        get_weighted_question_by_dimension(conn, question_id, "sex", initial_only)
    )
    men_per_city_df = add_total_row(
        get_weighted_question_by_dimension(
            conn, question_id, "men_per_city", initial_only
        )
    )
    women_per_city_df = add_total_row(
        get_weighted_question_by_dimension(
            conn, question_id, "women_per_city", initial_only
        )
    )

    titles_with_dfs = [
        ("Generales", general_df),
        ("Respuesta por unidad geográfica", city_df),
        ("Respuesta de hombres por unidad geográfica", men_per_city_df),
        ("Respuesta de mujeres por unidad geográfica", women_per_city_df),
        ("Respuesta por sexo", sex_df),
        ("Respuesta por edad", age_df),
    ]

    if section == "economia":
        income_df = add_total_row(
            get_weighted_question_by_income_group(conn, question_id)
        )
        titles_with_dfs.append(("Respuesta por grupo de ingreso", income_df))

    output_path = OUTPUT_DIR / f"{section}.xlsx"
    config = get_writer_config(output_path)

    with pd.ExcelWriter(**config) as writer:
        ctx = ExcelContext(writer, sheet_name)

        write_text_to_excel(ctx, f"{question_id} - {question_text}")

        for title, df in titles_with_dfs:
            write_text_to_excel(ctx, title)
            write_table_to_excel(ctx, df)
            relative_df = get_relative_table(df)
            write_table_to_excel(ctx, relative_df, is_relative=True)


def build_section_report(conn, section) -> None:
    questions_df = get_questions_by_section(conn, section)

    for _, question in questions_df.iterrows():
        build_question_report(
            conn, question["id"], question["q_text"], question["id"], section
        )

        if question["id"].startswith("cp"):
            build_question_report(
                conn,
                question["id"],
                question["q_text"],
                question["id"],
                section + "_sin_factor",
            )
