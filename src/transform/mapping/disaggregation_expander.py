import pandas as pd


def expand_disaggregation_options(df: pd.DataFrame) -> pd.DataFrame:
    df_expanded = df.copy()

    disaggregations_to_expand = {
        "trabajo_remunerado_y_sexo": [
            "trabajo_remunerado_por_hombres",
            "trabajo_remunerado_por_mujeres",
        ],
        "tipo_trabajo_y_sexo": ["tipo_trabajo_por_hombres", "tipo_trabajo_por_mujeres"],
        "tipo_escuela_y_nivel_actual_estudios": [
            "nivel_actual_estudios_por_escuela_privada",
            "nivel_actual_estudios_por_escuela_publica",
        ],
        "sexo_y_municipio": ["municipio_por_hombres", "municipio_por_mujeres"],
    }
    
    for original_col, new_cols in disaggregations_to_expand.items():
        for new_col in new_cols:
            df_expanded[original_col] = (
                df_expanded[original_col].astype(bool).fillna(False)
            )
            df_new = df_expanded[df_expanded[original_col]].copy()
            df_new[new_col] = True
            df_new = df_new.drop(columns=[original_col])
            df_expanded = pd.concat([df_expanded, df_new], ignore_index=True)

        df_expanded = df_expanded.drop(columns=[original_col])

    return df_expanded
