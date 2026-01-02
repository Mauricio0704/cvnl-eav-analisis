import pandas as pd

from src.db.create_schema import create_schema
from src.db.load_data import load_df_to_db, clear_all_tables
from src.db.utils import exists_schema, get_connection
from src.config.paths import DATA_DIR


def main():
    conn = get_connection()

    if not exists_schema(conn):
        print("Creating schema...")
        create_schema(conn)

    print("Resetting tables")
    clear_all_tables(conn, ["answers", "options", "questions", "responses"])

    print("Loading CSVs...")

    questions = pd.read_csv(DATA_DIR / "processed/questions.csv")
    options = pd.read_csv(DATA_DIR / "processed/options.csv")
    responses = pd.read_csv(DATA_DIR / "processed/responses.csv")
    answers = pd.read_csv(DATA_DIR / "processed/answers.csv")

    print("Writing to database...")
    with conn:
        load_df_to_db(questions, "questions", conn)
        load_df_to_db(options, "options", conn)
        load_df_to_db(responses, "responses", conn)
        load_df_to_db(answers, "answers", conn)

    conn.close()
    print("Load completed")


if __name__ == "__main__":
    main()
