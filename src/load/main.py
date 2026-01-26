import pandas as pd

from src.load.database import create_schema, exists_schema, get_connection
from src.load.write_to_db import load_df_to_db, clear_all_tables
from src.config.paths import PROCESSED_DATA_DIR


def run(year):
    conn = get_connection()

    if not exists_schema(conn):
        print("Creating schema...")
        create_schema(conn)

    print("Resetting tables")
    clear_all_tables(
        conn, ["answers", "options", "questions", "responses", "respondent_attributes"]
    )

    print("Loading CSVs...")

    questions = pd.read_csv(PROCESSED_DATA_DIR / f"{year}" / "questions.csv")
    options = pd.read_csv(PROCESSED_DATA_DIR / f"{year}" / "options.csv")
    responses = pd.read_csv(PROCESSED_DATA_DIR / f"{year}" / "responses.csv")
    answers = pd.read_csv(PROCESSED_DATA_DIR / f"{year}" / "answers.csv")
    respondent_attributes = pd.read_csv(
        PROCESSED_DATA_DIR / f"{year}" / "respondent_attributes.csv"
    )

    print("Writing to database...")
    with conn:
        load_df_to_db(questions, "questions", conn)
        load_df_to_db(options, "options", conn)
        load_df_to_db(responses, "responses", conn)
        load_df_to_db(answers, "answers", conn)
        load_df_to_db(respondent_attributes, "respondent_attributes", conn)

    conn.close()
    print("Load completed")


if __name__ == "__main__":
    run(2025)
