import pandas as pd
import json

from src.config.paths import PROCESSED_DATA_DIR


def export_df_to_csv(year: int, df: pd.DataFrame, filename: str) -> None:
    df = df.copy()

    df.reset_index(drop=True, inplace=True)

    df.to_csv(PROCESSED_DATA_DIR / f"{year}" / filename, index=False)


def export_df_to_xlsx(year: int, df: pd.DataFrame, filename: str) -> None:
    df = df.copy()

    df.reset_index(drop=True, inplace=True)

    df.to_excel(PROCESSED_DATA_DIR / f"{year}" / filename, index=False)


def export_dict_to_json(year: int, dissagregations: dict, filename: str) -> None:
    file_path = PROCESSED_DATA_DIR / f"{year}" / filename

    with open(file_path, "w") as json_file:
        json.dump(dissagregations, json_file, indent=4)
