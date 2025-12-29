from pathlib import Path
import pandas as pd

from src.config.paths import OUTPUT_DIR
from src.db.utils import get_connection
from src.reporting.weighted_tables import build_question_report


def main():
    conn = get_connection()

    questions = {
        "p1": "Principal ocupacion",
        "p2": "Modalidad",
    }

    output_file = OUTPUT_DIR / "ocupacion.xlsx"

    with pd.ExcelWriter(output_file) as writer:
        for question_id, sheet_name in questions.items():
            df = build_question_report(conn, question_id)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    conn.close()
    print(f"Report generated at {output_file}")


if __name__ == "__main__":
    main()
