from src.transform.io.read_from_raw import read_xlsx_file
from src.transform.mapping.extract_household_block import get_household_data
from src.transform.mapping.extract_individual_block import get_individual_responses
from src.transform.mapping.extract_respondent_attributes import (
    get_respondent_attributes,
)
from src.transform.cleaning.transform_structure import (
    household_members_to_long_format,
    household_questions_to_long_format,
    individual_questions_to_long_format,
    concatenate_answers,
)
from src.transform.cleaning.transform_disaggregations import disaggregations_to_dict
from src.transform.cleaning.clean_household import clean_household_responses
from src.transform.cleaning.clean_survey import (
    clean_questions,
    clean_options,
    clean_responses,
)
from src.transform.cleaning.clean_disaggregations import clean_disaggregations
from src.transform.mapping.normalize_schemas import (
    normalize_questions_schema,
    normalize_disaggregations_schema,
)
from src.transform.mapping.derived_variables import add_derived_variables
from src.transform.mapping.disaggregation_expander import expand_disaggregation_options
from src.transform.io.write_to_processed import (
    export_df_to_csv,
    export_df_to_xlsx,
    export_dict_to_json,
)
import argparse


def run(year: int = 2025):
    print("Processing data...")

    survey_df = read_xlsx_file(year, "survey_2025.xlsx")
    questions_raw = read_xlsx_file(year, "questions_2025.xlsx")
    disaggregations_raw = read_xlsx_file(year, "disaggregations_2025.xlsx")

    # Household responses
    household_df = get_household_data(survey_df)
    household_members_lf = household_members_to_long_format(household_df, 12)
    household_clean = clean_household_responses(household_members_lf)

    household_questions_lf = household_questions_to_long_format(household_clean)
    responses_clean = clean_responses(household_clean)

    # Individual responses
    individual_df = get_individual_responses(survey_df)
    individual_with_derived_df = add_derived_variables(individual_df)
    individual_lf = individual_questions_to_long_format(individual_with_derived_df)

    complete_answers = concatenate_answers(household_questions_lf, individual_lf)

    respondent_attributes_df = get_respondent_attributes(complete_answers)

    # Remove city_id from household answers before exporting
    complete_answers = complete_answers[complete_answers["question_id"] != "city_id"]

    # Questions and options
    questions_norm = normalize_questions_schema(questions_raw)
    questions_clean = clean_questions(questions_norm)
    options_clean = clean_options(questions_norm)

    # Disaggregations
    disaggregations_norm = normalize_disaggregations_schema(disaggregations_raw)
    disaggregations_clean = clean_disaggregations(disaggregations_norm)
    disaggregations_expanded = expand_disaggregation_options(disaggregations_clean)
    disaggregations_dict = disaggregations_to_dict(disaggregations_expanded)

    export_df_to_xlsx(year, household_clean, "household_clean.xlsx")
    export_df_to_csv(year, responses_clean, "responses.csv")
    export_df_to_csv(year,respondent_attributes_df, "respondent_attributes.csv")
    export_df_to_csv(year, complete_answers, "answers.csv")
    export_df_to_csv(year, questions_clean, "questions.csv")
    export_df_to_csv(year, options_clean, "options.csv")
    export_dict_to_json(year, disaggregations_dict, "disaggregations.json")

    print("Ingestion completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run ingestion for a specific survey year"
    )
    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=2025,
        help="Survey year to ingest (default: 2025)",
    )
    args = parser.parse_args()

    run(args.year)
