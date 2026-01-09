import pandas as pd

def tiempo_trabajo_minutes(df):
    # (p3_1 * 60) + p3_2
    new_df = df.copy()

    valid_p3_1 = new_df["p3_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p3_2 = new_df["p3_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["TIEMPO_TRABAJO"] = (valid_p3_1 * 60) + valid_p3_2
    
    return new_df


def prestaciones(df):
    # Those who answered all P5_X = 1
    new_df = df.copy()

    prestaciones_cols = [f"p5_{i}" for i in range(1, 9)]

    new_df["PRESTACIONES"] = new_df[prestaciones_cols].apply(lambda row: 1 if all(row == 1) else (0 if any(row == 0) else pd.NA), axis=1)

    return new_df


def trabajo_formal(df):
    # Those who answered 1 in P5_1, P5_2, y P5_5

    new_df = df.copy()

    formal_cols = ["p5_1", "p5_2", "p5_5"]

    new_df["TRABAJO_FORMAL"] = new_df[formal_cols].apply(lambda row: 1 if all(row == 1) else (0 if any(row == 0) else pd.NA), axis=1)

    return new_df


def quehaceres_hogar(df):
    # (p7_1 * 60) + p7_2
    new_df = df.copy()

    valid_p7_1 = new_df["p7_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p7_2 = new_df["p7_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["QUEHACERES_HOGAR"] = (valid_p7_1 * 60) + valid_p7_2

    return new_df


def cuidado_personas(df):
    # (p8_1 * 60) + p8_2

    new_df = df.copy()

    valid_p8_1 = new_df["p8_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p8_2 = new_df["p8_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["CUIDADOS_PERSONAS"] = (valid_p8_1 * 60) + valid_p8_2

    return new_df


def total_trabajo_minutes(df):
    # tiempo_trabajo + quehaceres_hogar + cuidados_personas
    new_df = df.copy()

    df_filtered = new_df[new_df["p1"].isin([1, 4, 6])]

    new_df.loc[df_filtered.index, "TOTAL_MIN_TRABAJO_REM_Y_NOREM"] = df_filtered[["TIEMPO_TRABAJO", "QUEHACERES_HOGAR", "CUIDADOS_PERSONAS"]].sum(axis=1, min_count=1)

    return new_df


def ocio(df):
    # (p9_1 * 60) + p9_2
    new_df = df.copy()

    valid_p9_1 = new_df["p9_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p9_2 = new_df["p9_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["OCIO"] = (valid_p9_1 * 60) + valid_p9_2

    return new_df


def add_derived_variables(df):
    df = tiempo_trabajo_minutes(df)
    df = prestaciones(df)
    df = trabajo_formal(df)
    df = quehaceres_hogar(df)
    df = cuidado_personas(df)
    df = total_trabajo_minutes(df)
    df = ocio(df)
    return df