"""
Quick data exploration — run after download_data.py
    python explore_data.py
"""
import os
import sys
import numpy as np
import pandas as pd

DATA = "data"


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def check_file(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        print(f"  MISSING: {path}")
        return None
    size_mb = os.path.getsize(path) / 1e6
    print(f"  {name}  ({size_mb:.1f} MB)")
    return path


# ── 1. File inventory ────────────────────────────────────────────────────────
section("File inventory")
csv_files = ["cfos_statistics.csv", "cfos_quantification.csv", "atlas_hierarchy.csv"]
nifti_files = ["anatomy.nii.gz", "regions.nii.gz", "diff_map.nii.gz",
               "cfos_G001.nii.gz", "cfos_G002.nii.gz"]

missing = []
for f in csv_files + nifti_files:
    if check_file(f) is None:
        missing.append(f)

if missing:
    print(f"\n  *** {len(missing)} file(s) missing — run download_data.py first ***")
    sys.exit(1)


# ── 2. cfos_statistics.csv ───────────────────────────────────────────────────
section("cfos_statistics.csv")
stats = pd.read_csv(f"{DATA}/cfos_statistics.csv")
print(f"  Shape: {stats.shape}")
print(f"  Columns: {stats.columns.tolist()}")
print(f"\n  Dtypes:\n{stats.dtypes.to_string()}")
print(f"\n  Nulls:\n{stats.isnull().sum().to_string()}")
print(f"\n  is_lowest_level: {stats['is_lowest_level'].value_counts().to_dict()}")
print(f"  significant_corrected: {stats['significant_corrected'].value_counts().to_dict()}")
print(f"\n  log2_fold_change range: [{stats['log2_fold_change'].min():.3f}, {stats['log2_fold_change'].max():.3f}]")
print(f"  p_corrected range:      [{stats['p_corrected'].min():.2e}, {stats['p_corrected'].max():.2e}]")

lowest = stats[stats["is_lowest_level"]]
sig = lowest[lowest["significant_corrected"]]
print(f"\n  Lowest-level regions:   {len(lowest)}")
print(f"  Significant hits:       {len(sig)}")
print(f"  Up (Sema > Vehicle):    {(sig['log2_fold_change'] > 0).sum()}")
print(f"  Down (Vehicle > Sema):  {(sig['log2_fold_change'] < 0).sum()}")

print(f"\n  Top 10 hits (by |log2FC|, lowest-level, significant):")
top = sig.reindex(sig["log2_fold_change"].abs().sort_values(ascending=False).index).head(10)
print(top[["acronym", "region_name", "log2_fold_change", "p_corrected"]].to_string(index=False))


# ── 3. cfos_quantification.csv ───────────────────────────────────────────────
section("cfos_quantification.csv")
quant = pd.read_csv(f"{DATA}/cfos_quantification.csv")
print(f"  Shape: {quant.shape}")
meta_cols = ["scan_name", "animal_nr", "group_nr"]
present_meta = [c for c in meta_cols if c in quant.columns]
extra_meta = [c for c in quant.columns if c not in present_meta and not c.islower()]
print(f"  Meta cols present: {present_meta}")
if extra_meta:
    print(f"  Unexpected extra cols: {extra_meta[:5]}")
region_cols = [c for c in quant.columns if c not in meta_cols]
print(f"  Region columns: {len(region_cols)}")
if "group_nr" in quant.columns:
    print(f"  Animals per group: {quant.groupby('group_nr').size().to_dict()}")
print(f"\n  Sample (first 3 rows):\n{quant[present_meta].head(3).to_string(index=False)}")


# ── 4. atlas_hierarchy.csv ───────────────────────────────────────────────────
section("atlas_hierarchy.csv")
atlas = pd.read_csv(f"{DATA}/atlas_hierarchy.csv")
print(f"  Shape: {atlas.shape}")
print(f"  Columns: {atlas.columns.tolist()}")
print(f"\n  Sample:\n{atlas.head(5).to_string(index=False)}")
# Check expected column names used in brain_viz.py
for col in ["label", "acronym", "region_name"]:
    status = "OK" if col in atlas.columns else "MISSING — update brain_viz.py"
    print(f"  '{col}' column: {status}")


# ── 5. NIfTI shapes ──────────────────────────────────────────────────────────
section("NIfTI shapes")
try:
    import SimpleITK as sitk
    for f in nifti_files:
        img = sitk.ReadImage(f"{DATA}/{f}")
        arr = sitk.GetArrayFromImage(img)
        print(f"  {f}: shape={arr.shape}  dtype={arr.dtype}  "
              f"range=[{arr.min():.2f}, {arr.max():.2f}]")
except ImportError:
    print("  SimpleITK not installed — skipping NIfTI inspection")


# ── 6. Overlap check ─────────────────────────────────────────────────────────
section("Overlap: stats acronyms vs atlas")
stats_acr = set(stats["acronym"])
atlas_acr = set(atlas["acronym"]) if "acronym" in atlas.columns else set()
if atlas_acr:
    in_both = stats_acr & atlas_acr
    only_stats = stats_acr - atlas_acr
    only_atlas = atlas_acr - stats_acr
    print(f"  In both:       {len(in_both)}")
    print(f"  Stats only:    {len(only_stats)} e.g. {list(only_stats)[:5]}")
    print(f"  Atlas only:    {len(only_atlas)} e.g. {list(only_atlas)[:5]}")
else:
    print("  (skipped — 'acronym' not in atlas)")

print("\nDone.\n")
