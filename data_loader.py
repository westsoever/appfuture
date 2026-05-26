import pandas as pd
import streamlit as st


@st.cache_data
def load_stats() -> pd.DataFrame:
    return pd.read_csv("data/cfos_statistics.csv")


@st.cache_data
def load_quant_long() -> pd.DataFrame:
    df = pd.read_csv("data/cfos_quantification.csv")
    meta_cols = ["scan_name", "animal_nr", "group_nr"]
    region_cols = [c for c in df.columns if c not in meta_cols]
    return df.melt(id_vars=meta_cols, value_vars=region_cols,
                   var_name="region", value_name="density")
