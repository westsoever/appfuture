import pandas as pd
import numpy as np


def rank_regions(stats: pd.DataFrame) -> pd.DataFrame:
    """Leaf regions sorted by absolute log2 fold change."""
    return (
        stats[stats["is_lowest_level"] == True]
        .assign(abs_log2fc=lambda d: d["log2_fold_change"].abs())
        .sort_values("abs_log2fc", ascending=False)
        .drop(columns="abs_log2fc")
        .reset_index(drop=True)
    )


def volcano_data(stats: pd.DataFrame) -> pd.DataFrame:
    """Add neg_log10_p column and significance label for volcano plot."""
    df = stats[stats["is_lowest_level"] == True].copy()
    df["neg_log10_p"] = -np.log10(df["p_corrected"].clip(lower=1e-10))
    df["significance"] = "ns"
    df.loc[df["significant_uncorrected"] == True, "significance"] = "uncorrected"
    return df
