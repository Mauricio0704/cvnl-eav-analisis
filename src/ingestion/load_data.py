from pathlib import Path
import pandas as pd


def load_survey_year(year: int, base_dir: Path) -> pd.DataFrame:
    file_path = base_dir / "raw" / str(year) / "copy_data_eav2025-raw_v2.xlsx"

    if not file_path.exists():
        raise FileNotFoundError(f"Survey file not found for year {year}")

    df = pd.read_excel(file_path)

    return df


def load_questions_year(year: int, base_dir: Path) -> pd.DataFrame:
    file_path = base_dir / "raw" / str(year) / "copy_cuestionario-eav2025_v2.xlsx"

    if not file_path.exists():
        raise FileNotFoundError(f"Questions file not found for year {year}")

    df = pd.read_excel(file_path)

    return df


def load_disaggregations(year: int, base_dir: Path) -> pd.DataFrame:
    file_path = base_dir / "raw" / str(year) / "desagregaciones_por_variable_eav2025.xlsx"

    if not file_path.exists():
        raise FileNotFoundError(f"Questions file not found for year {year}")

    df = pd.read_excel(file_path)

    return df