import sqlite3

from src.ingestion.load_data import load_survey_year, load_questions_year
from src.mapping.extract_household_block import get_household_data
from src.mapping.extract_individual_block import get_individual_responses
from src.cleaning.transform_structure import (
    household_members_to_long_format,
    household_questions_to_long_format,
    individual_questions_to_long_format,
)
from src.cleaning.clean_household import clean_household_responses
from src.io.export_to_csv import (
    export_responses_to_csv,
    export_questions_to_csv,
    export_options_to_csv,
    export_household_answers_to_csv,
    export_individual_answers_to_csv,
)
from src.config.paths import DATA_DIR, DB_DIR
from src.config.survey_data import DEMOGRAPHIC_CODES, QUESTIONS_COLUMNS_MAPPING
from src.mapping.questions_shema import normalize_questions_schema
from src.cleaning.clean_survey import clean_questions, clean_options
from src.db.create_schema import create_schema
from src.db.load_data import load_df_to_db, clear_table, clear_all_tables
from src.db.queries import get_question_options
from src.db.utils import exists_schema


def main():
    base_dir = DATA_DIR
    year = 2025

    survey_df = load_survey_year(year, base_dir)
    individual_df = get_individual_responses(survey_df)
    individual_lf = individual_questions_to_long_format(individual_df)
    household_df = get_household_data(survey_df)
    household_members_lf = household_members_to_long_format(household_df, 12)
    household_clean = clean_household_responses(household_members_lf)
    household_questions_lf = household_questions_to_long_format(household_clean)
    export_household_answers_to_csv(household_questions_lf)
    export_individual_answers_to_csv(individual_lf)
    export_responses_to_csv(household_clean, DEMOGRAPHIC_CODES)

    questions_with_ans_df = load_questions_year(year, base_dir)
    questions_with_options_normalized = normalize_questions_schema(
        questions_with_ans_df
    )
    questions_clean = clean_questions(questions_with_options_normalized)
    export_questions_to_csv(questions_clean)

    options_clean = clean_options(questions_with_options_normalized)
    export_options_to_csv(options_clean)

    conn = sqlite3.connect("data/db/survey.db")

    if not exists_schema(conn):
        create_schema(conn)

    clear_all_tables(conn, ["answers", "questions", "options", "responses"])

    with conn:
        load_df_to_db(questions_clean, "questions", conn)
        load_df_to_db(options_clean, "options", conn)

    df = get_question_options(conn, "p12")
    print(df)

    conn.close()


if __name__ == "__main__":
    main()
