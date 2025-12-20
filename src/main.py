from pathlib import Path

from ingestion.load_data import load_survey_year, load_questions_year
from mapping.extract_household_block import get_household_data
from cleaning.transform_structure import household_data_to_long_format
from cleaning.clean_household import clean_household_responses

def main():
    base_dir = Path("data")
    year = 2025

    survey_df = load_survey_year(year, base_dir)
    household_df = get_household_data(survey_df)
    household_long = household_data_to_long_format(household_df, 12)
    household_clean = clean_household_responses(household_long)

    print(household_clean.head(n=5))

    questions_df = load_questions_year(year, base_dir)



if __name__ == "__main__":
    main()
