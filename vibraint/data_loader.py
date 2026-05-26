import pandas as pd
import streamlit as st

DATA_DIR = "data"

@st.cache_data
def load_stats():
    df = pd.read_csv(f"{DATA_DIR}/cfos_statistics.csv")
    return df[df["is_lowest_level"] == True].copy().reset_index(drop=True)

@st.cache_data
def load_quantification():
    df = pd.read_csv(f"{DATA_DIR}/cfos_quantification.csv")
    id_cols = ["scan_name", "animal_nr", "group_nr"]
    region_cols = [c for c in df.columns if c not in id_cols]
    long = df.melt(id_vars=id_cols, value_vars=region_cols,
                   var_name="region", value_name="density")
    long["group"] = long["group_nr"].map({"G001": "Vehicle", "G002": "Semaglutide"})
    return long

@st.cache_data
def load_atlas():
    return pd.read_csv(f"{DATA_DIR}/atlas_hierarchy.csv")
