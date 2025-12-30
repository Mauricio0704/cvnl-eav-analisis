from src.config.paths import OUTPUT_DIR
from src.db.utils import get_connection
from src.reporting.weighted_tables import build_question_report
from src.db.queries import get_question_sections, get_questions_by_section


def main():
    conn = get_connection()

    sections = get_question_sections(conn)

    for section in sections[:1]:
        questions_df = get_questions_by_section(conn, section)

        for _, row in questions_df.iterrows():
            question_id = row["id"]

            build_question_report(conn, question_id, question_id, section)
        print(f"Report generated for {section} section.")
    
    conn.close()


if __name__ == "__main__":
    main()
