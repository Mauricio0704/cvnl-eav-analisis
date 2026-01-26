import pandas as pd
import numpy as np


# Ocupación

def tiempo_trabajo_minutes(df):
    # (p3_1 * 60) + p3_2
    new_df = df.copy()

    valid_p3_1 = new_df["p3_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p3_2 = new_df["p3_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["tiempo_trabajo"] = (valid_p3_1 * 60) + valid_p3_2
    
    return new_df


def prestaciones(df):
    # Those who answered all P5_X = 1
    new_df = df.copy()

    prestaciones_cols = [f"p5_{i}" for i in range(1, 9)]

    new_df["prestaciones"] = new_df[prestaciones_cols].apply(lambda row: 1 if all(row == 1) else (0 if any(row == 0) else pd.NA), axis=1)

    return new_df


def trabajo_formal(df):
    # Those who answered 1 in P5_1, P5_2, y P5_5

    new_df = df.copy()

    formal_cols = ["p5_1", "p5_2", "p5_5"]

    new_df["trabajo_formal"] = new_df[formal_cols].apply(lambda row: 1 if all(row == 1) else (0 if any(row == 0) else pd.NA), axis=1)

    return new_df


def quehaceres_hogar(df):
    # (p7_1 * 60) + p7_2
    new_df = df.copy()

    valid_p7_1 = new_df["p7_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p7_2 = new_df["p7_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["quehaceres_hogar"] = (valid_p7_1 * 60) + valid_p7_2

    return new_df


def cuidado_personas(df):
    # (p8_1 * 60) + p8_2

    new_df = df.copy()

    valid_p8_1 = new_df["p8_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p8_2 = new_df["p8_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["cuidados_personas"] = (valid_p8_1 * 60) + valid_p8_2

    return new_df


def total_trabajo_minutes(df):
    # tiempo_trabajo + quehaceres_hogar + cuidados_personas
    new_df = df.copy()

    df_filtered = new_df[new_df["p1"].isin([1, 4, 6])]

    new_df.loc[df_filtered.index, "total_min_trabajo_rem_y_norem"] = df_filtered[["tiempo_trabajo", "quehaceres_hogar", "cuidados_personas"]].sum(axis=1, min_count=1)

    return new_df


def ocio(df):
    # (p9_1 * 60) + p9_2
    new_df = df.copy()

    valid_p9_1 = new_df["p9_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p9_2 = new_df["p9_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["ocio"] = (valid_p9_1 * 60) + valid_p9_2

    return new_df


# Salud

def tiempo_espera_consulta(df):
    # (p103_1 * 60) + p103_2
    new_df = df.copy()

    valid_p103_1 = new_df["p103_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p103_2 = new_df["p103_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)

    new_df["tiempo_espera_consulta"] = (valid_p103_1 * 60) + valid_p103_2

    return new_df


def problema_mental(df):
    # Those  who answered 1, 2 or 3 in p107_1, p107_2 or p107_3
    new_df = df.copy()

    mental_cols = ["p107_1", "p107_2", "p107_3"]

    new_df["al_menos_un_problema_mental"] = (
        new_df[mental_cols]
        .isin([1, 2, 3])
        .any(axis=1)
        .astype(int)
    )

    return new_df


# Generales respondiente

def rangos_edad(df):
    new_df = df.copy()

    bins = [17, 24, 34, 44, 54, 64, 74, 123]
    labels = [
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65-74",
        "75 o más",
    ]

    new_df["rangos_edad"] = pd.cut(
        new_df["cp4_1"].replace(9999, pd.NA),
        bins=bins,
        labels=labels,
        right=True
    )

    return new_df


#Generales hogar

# Movilidad

def tiempo_espera(df):
    # (p21_1 * 60) + p21_2
    new_df = df.copy()

    valid_p21_1 = new_df["p21_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p21_2 = new_df["p21_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    new_df["tiempo_espera"] = (valid_p21_1 * 60) + valid_p21_2

    return new_df


def costo_total_viaje(df):
    # p24 + p25
    new_df = df.copy()

    valid_p24 = new_df["p24"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p25 = new_df["p25"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    new_df["costo_total_viaje_redondo"] = valid_p24 + valid_p25

    return new_df


def tiempo_ida(df):
    # (27_1 * 60) + p27_2
    new_df = df.copy()

    valid_p27_1 = new_df["p27_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p27_2 = new_df["p27_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    new_df["tiempo_ida"] = (valid_p27_1 * 60) + valid_p27_2

    return new_df


def tiempo_regreso(df):
    # (p28_1 * 60) + p28_2
    new_df = df.copy()

    valid_p28_1 = new_df["p28_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p28_2 = new_df["p28_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    new_df["tiempo_regreso"] = (valid_p28_1 * 60) + valid_p28_2

    return new_df


def tiempo_total_traslado(df):
    # tiempo_ida + tiempo_regreso
    new_df = df.copy()

    new_df["tiempo_total_traslado"] = new_df[["tiempo_ida", "tiempo_regreso"]].sum(axis=1, min_count=1)

    return new_df


def usa_transporte_publico(df):
    new_df = df.copy()

    new_df["usa_transporte_publico"] = (
        new_df["p17"].isin([2, 8, 10]) |
        new_df["p29"].isin([1])
    ).astype(int)

    return new_df


def usa_metro(df):
    new_df = df.copy()

    new_df["usa_metro"] = (
        new_df["p17"].isin([8]) |
        new_df["p30"].isin([1])
    ).astype(int)

    return new_df


def victima_tp(df):
    new_df = df.copy()

    victima_cols = ["p39_1", "p39_2", "p39_3", "p39_4"]

    fue_victima = new_df[victima_cols].isin([1]).any(axis=1)

    usa_tp = new_df["usa_transporte_publico"] == 1

    new_df["victima_tp"] = np.where(
        usa_tp,
        fue_victima.astype(int),
        np.nan
    )

    return new_df


def tiempo_camina(df):
    # (p20_1 * 60) + p20_2
    new_df = df.copy()

    valid_p20_1 = new_df["p20_1"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    valid_p20_2 = new_df["p20_2"].apply(lambda x: x if x not in [9999, 8888, 7777] else pd.NA)
    new_df["tiempo_camina"] = (valid_p20_1 * 60) + valid_p20_2

    return new_df


# Discriminación

def num_discriminaciones(df):
    # Count of questions p89_1 to p89_16 with answer 1
    new_df = df.copy()

    discrim_cols = [f"p89_{i}" for i in range(1, 17)]

    new_df["num_discriminaciones"] = (
        new_df[discrim_cols]
        .isin([1])
        .sum(axis=1)
    )

    return new_df


def al_menos_una_discriminacion(df):
    # Those who answered 1 in any of p89_1 to p89_16
    new_df = df.copy()

    discrim_cols = [f"p89_{i}" for i in range(1, 17)]

    new_df["al_menos_una_discriminacion"] = (
        new_df[discrim_cols]
        .isin([1])
        .any(axis=1)
        .astype(int)
    )

    return new_df


# Gobierno

def num_acciones_pc(df):
    # Count of questions p161_1 to p161_9 with answer 1
    new_df = df.copy()

    accion_cols = [f"p161_{i}" for i in range(1, 10)]
    new_df["num_acciones_pc"] = (
        new_df[accion_cols]
        .isin([1])
        .sum(axis=1)
    )

    return new_df


def al_menos_una_accion_pc(df):
    # Those who answered 1 in any of p161_1 to p161_9
    new_df = df.copy()

    accion_cols = [f"p161_{i}" for i in range(1, 10)]

    new_df["al_menos_una_accion_pc"] = (
        new_df[accion_cols]
        .isin([1])
        .any(axis=1)
        .astype(int)
    )

    return new_df

# Vivienda

def p56_ultimos_5_anios(df):
    """
    Filter p56 to only include respondents who have moved in the last 5 years (p55 <= 2).
    """
    new_df = df.copy()

    moved_recently = new_df["p55"].isin([1, 2])

    new_df["p56_ultimos_5_anios"] = np.where(
        moved_recently,
        new_df["p56"],
        np.nan
    )

    return new_df


def p57_ultimos_5_anios(df):
    """
    Filter p57 to only include respondents who have moved in the last 5 years (p55 <= 2).
    """
    new_df = df.copy()

    moved_recently = new_df["p55"].isin([1, 2])

    new_df["p57_ultimos_5_anios"] = np.where(
        moved_recently,
        new_df["p57"],
        np.nan
    )

    return new_df


def p58_ultimos_5_anios(df):
    """
    Filter p58 to only include respondents who have moved in the last 5 years (p55 <= 2).
    """
    new_df = df.copy()

    moved_recently = new_df["p55"].isin([1, 2])

    new_df["p58_ultimos_5_anios"] = np.where(
        moved_recently,
        new_df["p58"],
        np.nan
    )

    return new_df


def p56_ultimos_10_anios(df):
    """
    Filter p56 to only include respondents who have moved in the last 10 years (p55 <= 3).
    """
    new_df = df.copy()

    moved_recently = new_df["p55"].isin([1, 2, 3])

    new_df["p56_ultimos_10_anios"] = np.where(
        moved_recently,
        new_df["p56"],
        np.nan
    )

    return new_df


def p57_ultimos_10_anios(df):
    """
    Filter p57 to only include respondents who have moved in the last 10 years (p55 <= 3).
    """
    new_df = df.copy()

    moved_recently = new_df["p55"].isin([1, 2, 3])

    new_df["p57_ultimos_10_anios"] = np.where(
        moved_recently,
        new_df["p57"],
        np.nan
    )

    return new_df


def p58_ultimos_10_anios(df):
    """
    Filter p58 to only include respondents who have moved in the last 10 years (p55 <= 3).
    """
    new_df = df.copy()

    moved_recently = new_df["p55"].isin([1, 2, 3])

    new_df["p58_ultimos_10_anios"] = np.where(
        moved_recently,
        new_df["p58"],
        np.nan
    )

    return new_df


def add_derived_variables(df):
    df = tiempo_trabajo_minutes(df)
    df = prestaciones(df)
    df = trabajo_formal(df)
    df = quehaceres_hogar(df)
    df = cuidado_personas(df)
    df = total_trabajo_minutes(df)
    df = ocio(df)
    df = tiempo_espera_consulta(df)
    df = problema_mental(df)
    ##df = rangos_edad(df)
    df = tiempo_espera(df)
    df = costo_total_viaje(df)
    df = tiempo_ida(df)
    df = tiempo_regreso(df)
    df = tiempo_total_traslado(df)
    df = usa_transporte_publico(df)
    df = usa_metro(df)
    df = victima_tp(df)
    df = tiempo_camina(df)
    df = num_discriminaciones(df)
    df = al_menos_una_discriminacion(df)
    df = num_acciones_pc(df)
    df = al_menos_una_accion_pc(df)
    df = p56_ultimos_5_anios(df)
    df = p57_ultimos_5_anios(df)
    df = p58_ultimos_5_anios(df)
    df = p56_ultimos_10_anios(df)
    df = p57_ultimos_10_anios(df)
    df = p58_ultimos_10_anios(df)

    return df