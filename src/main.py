from pathlib import Path

from ingestion.load_data import load_survey_year, load_questions_year


def main():
    base_dir = Path("data")
    year = 2025

    survey_df = load_survey_year(year, base_dir)
    questions_df = load_questions_year(year, base_dir)


if __name__ == "__main__":
    main()
