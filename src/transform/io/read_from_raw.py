import pandas as pd

from src.config.paths import RAW_DATA_DIR

def read_xlsx_file(year: int, filename: str) -> pd.DataFrame:
    file_path = RAW_DATA_DIR / str(year) / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} not found for year {year}")

    df = pd.read_excel(file_path)

    return df