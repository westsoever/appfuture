# Explainable Brains — Challenge B

## Entry point
`streamlit run app.py`

## Data files (in data/)
- cfos_statistics.csv — one row per brain region: region_id, region_name, acronym, hierarchy_level, is_lowest_level, n_A, n_B, n_A_eff, n_B_eff, mean_A, mean_B, median_A, median_B, std_A, std_B, sem_A, sem_B, mean_diff, ci_low, ci_high, fold_change, log2_fold_change, log2fc_ci_low, log2fc_ci_high, p_value, p_corrected, significant_uncorrected, significant_corrected
- cfos_quantification.csv — per-animal densities: scan_name, animal_nr, group_nr (G001/G002), [region acronyms as remaining columns]
- diff_map.nii.gz — NIfTI voxel-wise difference map G002−G001
- regions.nii.gz — NIfTI atlas region labels (integer → atlas_hierarchy.csv)
- anatomy.nii.gz — NIfTI anatomical reference
- cfos_G001.nii.gz — median c-Fos signal map, Vehicle group
- cfos_G002.nii.gz — median c-Fos signal map, Semaglutide group
- atlas_hierarchy.csv — maps integer voxel label → acronym → region_name

## Key functions
- `data_loader.py:load_stats()` → DataFrame (stats per region, is_lowest_level==True only)
- `data_loader.py:load_quantification()` → DataFrame (per-animal, long format with group col)
- `data_loader.py:load_atlas()` → DataFrame mapping label → acronym → region_name
- `analysis.py:prepare_volcano(df)` → DataFrame with neg_log10_p and color columns
- `analysis.py:get_region_ranking(df, only_significant)` → DataFrame sorted by p_corrected
- `analysis.py:get_brain_slice(region_acronym, atlas_df, axis)` → dict {diff_slice, mask_slice, anatomy_slice}
- `llm_explain.py:explain_region(region_name, acronym, log2fc, p_value, mean_a, mean_b)` → str

## Treatment groups
- G001 = Vehicle (control) = mean_A in statistics
- G002 = Semaglutide (treatment) = mean_B in statistics
- Positive log2_fold_change = higher activity in Semaglutide mice

## NIfTI loading
Use SimpleITK (sitk), NOT nibabel. sitk.GetArrayFromImage returns shape (Z, Y, X).
Coronal slice = axis 1 (Y). Example: `arr[:, mid_y, :]`

## Download data
Run `python download_data.py` to download all data files to data/.
Requires bucket credentials in bucket_access/config.py (filled in at hackathon).

## Run and test
```bash
conda activate explainable-brains
streamlit run app.py
python smoke_test.py   # verify data + analysis pipeline
```
