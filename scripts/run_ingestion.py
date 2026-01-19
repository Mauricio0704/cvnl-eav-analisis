from src.ingestion.load_data import (
    load_survey_year,
    load_questions_year,
    load_disaggregations,
)
from src.mapping.extract_household_block import get_household_data
from src.mapping.extract_individual_block import get_individual_responses
from src.mapping.extract_respondent_attributes import get_respondent_attributes
from src.cleaning.transform_structure import (
    household_members_to_long_format,
    household_questions_to_long_format,
    individual_questions_to_long_format,
)
from src.cleaning.transform_disaggregations import disaggregations_to_dict
from src.cleaning.clean_household import clean_household_responses
from src.cleaning.clean_survey import clean_questions, clean_options, clean_responses
from src.cleaning.clean_disaggregations import clean_disaggregations
from src.mapping.normalize_schemas import (
    normalize_questions_schema,
    normalize_disaggregations_schema,
)
from src.mapping.derived_variables import add_derived_variables
from src.mapping.disaggregation_expander import expand_disaggregation_options
from src.io.export_to_csv import (
    export_responses_to_csv,
    export_questions_to_csv,
    export_options_to_csv,
    export_household_answers_to_csv,
    export_individual_answers_to_csv,
    export_respondent_attributes_to_csv,
    export_household_wide_to_xlsx,
)
from src.io.export_disaggregations import dissagregations_to_json
from src.config.paths import DATA_DIR
from src.config.survey_data import DEMOGRAPHIC_CODES


def main():
    year = 2025
    base_dir = DATA_DIR

    print("Loading raw survey data...")
    survey_df = load_survey_year(year, base_dir)

    print("Processing data...")

    # Household responses
    household_df = get_household_data(survey_df)
    household_members_lf = household_members_to_long_format(household_df, 12)
    household_clean = clean_household_responses(household_members_lf)
    export_household_wide_to_xlsx(household_clean)
    household_questions_lf = household_questions_to_long_format(household_clean)
    responses_clean = clean_responses(household_clean, DEMOGRAPHIC_CODES)
    export_responses_to_csv(responses_clean)

    # Individual responses
    individual_df = get_individual_responses(survey_df)
    individual_with_derived_df = add_derived_variables(individual_df)
    individual_lf = individual_questions_to_long_format(individual_with_derived_df)

    respondent_attributes_df = get_respondent_attributes(
        individual_lf, household_questions_lf
    )
    export_respondent_attributes_to_csv(respondent_attributes_df)

    # Remove city_id from household answers before exporting
    household_questions_lf = household_questions_lf[
        household_questions_lf["question_id"] != "city_id"
    ]

    export_household_answers_to_csv(household_questions_lf)
    export_individual_answers_to_csv(individual_lf)

    # Questions and options
    questions_raw = load_questions_year(year, base_dir)
    questions_norm = normalize_questions_schema(questions_raw)

    questions_clean = clean_questions(questions_norm)
    options_clean = clean_options(questions_norm)

    export_questions_to_csv(questions_clean)
    export_options_to_csv(options_clean)

    # Disaggregations
    disaggregations_raw = load_disaggregations(year, base_dir)
    disaggregations_norm = normalize_disaggregations_schema(disaggregations_raw)
    disaggregations_clean = clean_disaggregations(disaggregations_norm)
    disaggregations_expanded = expand_disaggregation_options(disaggregations_clean)
    disaggregations_dict = disaggregations_to_dict(disaggregations_expanded)

    dissagregations_to_json(disaggregations_dict)

    print("Ingestion completed.")


if __name__ == "__main__":
    main()
