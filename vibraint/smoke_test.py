"""Run after downloading data to verify everything works before the hackathon."""
import sys
import os

print("=== Explainable Brains Smoke Test ===\n")

# 1. Check data files exist
DATA_DIR = "data"
required_files = [
    "cfos_statistics.csv",
    "cfos_quantification.csv",
    "atlas_hierarchy.csv",
    "diff_map.nii.gz",
    "regions.nii.gz",
    "anatomy.nii.gz",
]
print("1. Checking data files...")
missing = []
for f in required_files:
    path = f"{DATA_DIR}/{f}"
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / 1e6
        print(f"   ✓ {f} ({size_mb:.1f} MB)")
    else:
        print(f"   ✗ MISSING: {f}")
        missing.append(f)
if missing:
    print(f"\nRun `python download_data.py` to download missing files.")
    sys.exit(1)

# 2. Load stats CSV
print("\n2. Loading cfos_statistics.csv...")
import pandas as pd
stats = pd.read_csv(f"{DATA_DIR}/cfos_statistics.csv")
leaf = stats[stats["is_lowest_level"] == True]
print(f"   Total regions: {len(stats)}, leaf regions: {len(leaf)}")
required_cols = ["log2_fold_change", "p_corrected", "significant_corrected",
                 "is_lowest_level", "acronym", "region_name", "mean_A", "mean_B",
                 "n_A_eff", "n_B_eff"]
missing_cols = [c for c in required_cols if c not in stats.columns]
if missing_cols:
    print(f"   ✗ Missing columns: {missing_cols}")
    print(f"   Available: {stats.columns.tolist()}")
    sys.exit(1)
print(f"   ✓ All required columns present")
assert len(leaf) > 50, f"Expected >50 leaf regions, got {len(leaf)}"

# 3. Analysis functions
print("\n3. Testing analysis functions...")
from analysis import prepare_volcano, get_region_ranking
volcano = prepare_volcano(leaf)
assert "neg_log10_p" in volcano.columns
assert "significance" in volcano.columns
print(f"   ✓ prepare_volcano OK")

ranked = get_region_ranking(leaf, only_significant=True)
if len(ranked) > 0:
    top = ranked.iloc[0]
    print(f"   ✓ Top significant region: {top['region_name']} (p={top['p_corrected']:.4f}, log2fc={top['log2_fold_change']:.2f})")
else:
    print("   ⚠ No significant corrected regions found")

# 4. Load quantification
print("\n4. Loading cfos_quantification.csv...")
quant = pd.read_csv(f"{DATA_DIR}/cfos_quantification.csv")
id_cols = ["scan_name", "animal_nr", "group_nr"]
region_cols = [c for c in quant.columns if c not in id_cols]
print(f"   Animals: {len(quant)}, regions: {len(region_cols)}")
groups = quant["group_nr"].unique()
print(f"   Groups: {sorted(groups)}")
assert "G001" in groups and "G002" in groups, f"Expected G001/G002 groups, got {groups}"
print(f"   ✓ Groups correct (G001=Vehicle, G002=Semaglutide)")

# 5. Atlas
print("\n5. Loading atlas_hierarchy.csv...")
atlas = pd.read_csv(f"{DATA_DIR}/atlas_hierarchy.csv")
print(f"   Atlas entries: {len(atlas)}")
print(f"   Columns: {atlas.columns.tolist()}")

# 6. Anthropic API key
print("\n6. Checking ANTHROPIC_API_KEY...")
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if api_key and api_key.startswith("sk-ant-"):
    print("   ✓ ANTHROPIC_API_KEY is set")
else:
    print("   ✗ ANTHROPIC_API_KEY not set — Claude explanations will fail")
    print("     Set it: export ANTHROPIC_API_KEY=sk-ant-...")

print("\n=== All checks passed! Ready to run: streamlit run app.py ===")
