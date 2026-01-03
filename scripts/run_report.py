from src.utils.database import get_connection
from src.reporting.builder import build_section_report
from src.db.repository import get_question_sections


def main():
    conn = get_connection()

    sections = get_question_sections(conn)

    for section in sections:
        build_section_report(conn, section)
        print(f"Report generated for {section} section.")

    conn.close()


if __name__ == "__main__":
    main()
