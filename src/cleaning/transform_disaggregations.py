import pandas as pd


def disaggregations_to_dict(df: pd.DataFrame) -> dict:
    new_df = df.copy()

    disagg_cols = new_df.columns.drop("id")

    result = (
        new_df.set_index("id")[disagg_cols]
        .apply(
            lambda row: [{"type": col} for col, val in row.items() if val == 1], axis=1
        )
        .to_dict()
    )

    return result
