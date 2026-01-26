from extract.read_fom_source import read_excel_file
from src.config.paths import DATA_DIR
import argparse


def run(year: int = 2025):
    base_dir = DATA_DIR

    survey_df = read_excel_file(year, "data_eav2025.xlsx", base_dir)
    questions_raw = read_excel_file(year, "cuestionario_eav2025.xlsx", base_dir)
    disaggregations_raw = read_excel_file(year, "desagregaciones_eav2025.xlsx", base_dir)

    # ------------------------------------------------------------------------------------
    # This file is just a placeholder to add more extraction logic if needed in the future
    # ------------------------------------------------------------------------------------

    survey_df.to_excel(base_dir / "raw" / f"{year}" / f"survey_{year}.xlsx", index=False)
    questions_raw.to_excel(base_dir / "raw" / f"{year}" / f"questions_{year}.xlsx", index=False)
    disaggregations_raw.to_excel(base_dir / "raw" / f"{year}" /  f"disaggregations_{year}.xlsx", index=False)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ingestion for a specific survey year")
    parser.add_argument("--year", "-y", type=int, default=2025, help="Survey year to ingest (default: 2025)")
    args = parser.parse_args()

    run(args.year)
