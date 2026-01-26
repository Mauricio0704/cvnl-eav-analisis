from pathlib import Path
import pandas as pd


def read_excel_file(year: int, filename: str, base_dir: Path) -> pd.DataFrame:
    file_path = base_dir / "source" / str(year) / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} not found for year {year}")

    df = pd.read_excel(file_path)

    return df
