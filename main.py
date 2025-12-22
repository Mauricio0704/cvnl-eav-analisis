from src.ingestion.load_data import load_survey_year, load_questions_year
from src.mapping.extract_household_block import get_household_data
from src.cleaning.transform_structure import household_data_to_long_format
from src.cleaning.clean_household import clean_household_responses
from src.io.export_to_csv import (
    export_responses_to_csv,
    export_questions_to_csv,
    export_answers_to_csv,
)
from src.config.paths import DATA_DIR
from src.config.survey_data import DEMOGRAPHIC_CODES, QUESTIONS_COLUMNS_MAPPING
from src.mapping.questions_shema import normalize_questions_schema
from src.cleaning.clean_survey import clean_questions, clean_options


def main():
    base_dir = DATA_DIR
    year = 2025

    survey_df = load_survey_year(year, base_dir)
    household_df = get_household_data(survey_df)
    household_long = household_data_to_long_format(household_df, 12)
    household_clean = clean_household_responses(household_long)

    export_responses_to_csv(household_clean, DEMOGRAPHIC_CODES)

    questions_with_ans_df = load_questions_year(year, base_dir)
    questions_with_options_normalized = normalize_questions_schema(
        questions_with_ans_df
    )
    questions_clean = clean_questions(questions_with_options_normalized)

    export_questions_to_csv(questions_clean)

    options_clean = clean_options(questions_with_options_normalized)

    export_answers_to_csv(options_clean)


if __name__ == "__main__":
    main()
