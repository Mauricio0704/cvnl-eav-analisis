import pandas as pd
from pathlib import Path


def get_writer_config(
    output_path: Path,
) -> dict:
    if output_path.exists():
        mode = "a"
        if_sheet = "overlay"
    else:
        mode = "w"
        if_sheet = None

    return {
        "path": output_path,
        "engine": "openpyxl",
        "mode": mode,
        "if_sheet_exists": if_sheet,
    }


def write_text_to_excel(
    writer: pd.ExcelWriter,
    sheet_name: str,
    text: str,
    start_row: int = 0,
) -> int:
    pd.DataFrame([[text]]).to_excel(
        writer,
        sheet_name=sheet_name,
        startrow=start_row,
        index=False,
        header=False,
    )
    return start_row + 2


def write_table_to_excel(
    writer: pd.ExcelWriter,
    sheet_name: str,
    df: pd.DataFrame,
    start_row: int = 0,
) -> int:
    df.to_excel(
        writer,
        sheet_name=sheet_name,
        startrow=start_row,
        index=False,
    )
    return start_row + len(df) + 3
