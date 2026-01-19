import pandas as pd
import json
from tqdm import tqdm

from src.config.paths import OUTPUT_DIR, PROCESSED_DATA_DIR
from src.config.survey_data import NUMERICAL_VALUE_QUESTIONS
from src.reporting.extend_tables import (
    add_total_row,
    get_relative_table,
    add_weighted_average_row,
    add_total_column,
)
from src.db.repository import (
    get_questions_by_section,
)
from src.utils.excel import (
    ExcelContext,
    write_text_to_excel,
    write_table_to_excel,
    get_writer_config,
)
from src.db.repository import build_disaggregation_report

with open(PROCESSED_DATA_DIR / "disaggregations.json", "r") as file:
    data = json.load(file)


def build_question_report(
    conn,
    question_id: str,
    question_text: str,
    sheet_name: str,
    section: str,
    initial_only: bool = True,
) -> None:
    titles_with_dfs = []

    question_specific_disaggregations = data.get(question_id, [])

    handled_disaggregations = [
        "ingreso",
        "tipo_trabajo",
        "tipo_trabajo_por_hombres",
        "tipo_trabajo_por_mujeres",
        "trabajo_remunerado",
        "trabajo_remunerado_por_hombres",
        "trabajo_remunerado_por_mujeres",
        "afiliacion_servicio_salud",
        "nivel_max_estudios",
        "servicio_salud_donde_se_atendio",
        "tipo_servicio_salud_donde_se_atendio",
        "tipo_escuela",
        "nivel_actual_estudios",
        "nivel_actual_estudios_por_escuela_privada",
        "nivel_actual_estudios_por_escuela_publica",
        "sexo",
        "municipio",
        "municipio_por_hombres",
        "municipio_por_mujeres",
        "edad",
        "totales",
        "tipo_consulta",
        "promedio_modo_transporte_y_municipio"
    ]

    for disaggregation in question_specific_disaggregations:
        if disaggregation["type"] in handled_disaggregations:

            df = add_total_row(
                build_disaggregation_report(
                    conn,
                    question_id,
                    disaggregation["type"],
                    initial_only,
                )
            )

            if not disaggregation["type"].startswith("municipio"):
                df = add_total_column(df)

            if question_id in NUMERICAL_VALUE_QUESTIONS:
                df = add_weighted_average_row(df)

            titles_with_dfs.append((f"Respuesta por {disaggregation["type"]}", df))

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

    for _, question in tqdm(
        questions_df.iterrows(),
        total=len(questions_df),
        desc=f"Building {section} section report",
    ):
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
                initial_only=False,
            )
