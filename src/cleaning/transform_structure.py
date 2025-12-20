import pandas as pd


def generate_id(df: pd.DataFrame, id_name: str, id_cols: list[str]) -> pd.DataFrame:
    df = df.copy()

    df[id_name] = df[id_cols].astype(str).agg("_".join, axis=1)

    return df.drop(columns=id_cols)


def remove_emtpy_rows(household_data: pd.DataFrame) -> pd.DataFrame:
    person_mask = household_data.loc[
        (household_data["nombre"].notna()) & (household_data["nombre"] != "Fin")
    ].index
    return household_data.loc[person_mask].copy()


def household_data_to_long_format(
    household_data: pd.DataFrame, max_members_per_household: int
) -> pd.DataFrame:
    df = household_data.copy()

    household_cols = ["household_id", "city_id"]

    long_parts = []

    for n in range(1, max_members_per_household + 1):
        cols_p = [c for c in df.columns if c.endswith(f"_{n}")]
        cols = household_cols + cols_p
        cols.append(f"cp{n}_nombre")

        tmp = df[cols].copy()
        tmp["member_id"] = n
        tmp["is_respondent"] = True if n == 1 else False

        # Renombrar variables cp[q]_[n] -> cp[q] y cp[n]_nombre -> nombre
        tmp = tmp.rename(columns={c: c.rsplit("_", 1)[0] for c in cols_p})
        tmp = tmp.rename(columns={f"cp{n}_nombre": "nombre"})

        long_parts.append(tmp)

    household_long = (
        pd.concat(long_parts, ignore_index=True)
        .sort_values(["household_id", "member_id"])
        .reset_index(drop=True)
    )

    household_person = remove_emtpy_rows(household_long)
    household_with_id = generate_id(
        household_person, id_name="respondent_id", id_cols=["household_id", "member_id"]
    )

    headers_order = [
        "respondent_id",
        "is_respondent",
        "nombre",
        "city_id",
        "cp2",
        "cp4_1",
        "cp4_2",
        "cp6",
        "cp7",
        "cp8",
        "cp9",
        "cp10a",
        "cp10b",
        "cp11",
        "cp13",
        "cp14",
        "cp15_1",
        "cp15_2",
        "cp16",
        "cp17",
        "cp18",
        "cp19",
    ]

    household_with_id = household_with_id[headers_order].copy()

    return household_with_id
