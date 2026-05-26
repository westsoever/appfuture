# Explainable Brains — Challenge B

## Run
```
streamlit run app.py
```

## Data (in data/ — gitignored)
- `cfos_statistics.csv` — one row per brain region: acronym, region_name, log2_fold_change, p_corrected, significant_corrected, mean_A, mean_B, n_A_eff, n_B_eff, is_lowest_level
- `cfos_quantification.csv` — per-animal c-Fos densities (wide → long after load)
- `atlas_hierarchy.csv` — integer label ↔ acronym ↔ region_name (for NIfTI masks)
- `anatomy.nii.gz`, `regions.nii.gz`, `diff_map.nii.gz`, `cfos_G001.nii.gz`, `cfos_G002.nii.gz`

Download all data: `python download_data.py`

## Module map
| File | Exports |
|------|---------|
| `data_loader.py` | `load_stats()` → DataFrame; `load_quant_long()` → DataFrame (long) |
| `analysis.py` | `rank_regions(stats_df)` → DataFrame sorted by abs(log2_fold_change), filtered to is_lowest_level |
| `brain_viz.py` | `get_slice(acronym, axis=1)` → dict(anatomy, diff, mask) as 2D numpy arrays |
| `llm.py` | `explain_region(row)` → str (3 sentences plain English via Claude API) |
| `app.py` | Streamlit entry point — 3 tabs: Volcano, Ranking, Region Deep Dive |

## Key data rules
- Always filter `is_lowest_level == True` before ranking — avoids parent/child double-counting
- `significant_corrected == True` = high-confidence hits (use as default filter)
- `log2_fold_change > 0` = higher in Semaglutide (G002); `< 0` = higher in Vehicle (G001)
- NIfTI arrays from SimpleITK are shape (Z, Y, X) — axis 1 is coronal (anterior-posterior)

## How to extend
- New analysis: add pure function to `analysis.py`
- New NIfTI logic: add to `brain_viz.py` (no Streamlit imports here)
- New UI: edit `app.py` only — all data is cached, no risk of breaking loaders
- New Claude feature: add to `llm.py`

## Environment
```
conda activate explainable-brains
```
