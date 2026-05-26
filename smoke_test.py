"""Smoke test — run after download_data.py to verify everything is ready."""
import os
import sys

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
errors = 0


def check(label, condition, fix=""):
    global errors
    if condition:
        print(f"  {PASS} {label}")
    else:
        print(f"  {FAIL} {label}")
        if fix:
            print(f"      → {fix}")
        errors += 1


print("\n── Data files ──")
expected_files = [
    "data/cfos_statistics.csv",
    "data/cfos_quantification.csv",
    "data/atlas_hierarchy.csv",
    "data/anatomy.nii.gz",
    "data/regions.nii.gz",
    "data/diff_map.nii.gz",
    "data/cfos_G001.nii.gz",
    "data/cfos_G002.nii.gz",
]
for f in expected_files:
    check(f, os.path.exists(f), fix=f"Run: python download_data.py")

print("\n── CSV schema ──")
try:
    import pandas as pd

    stats = pd.read_csv("data/cfos_statistics.csv")
    required_cols = [
        "acronym", "region_name", "log2_fold_change", "p_corrected",
        "significant_corrected", "mean_A", "mean_B", "is_lowest_level",
        "n_A_eff", "n_B_eff",
    ]
    for col in required_cols:
        check(f"  stats has column '{col}'", col in stats.columns,
              fix=f"Column missing — check actual columns: {list(stats.columns)[:8]}")

    leaf = stats[stats["is_lowest_level"] == True]
    check(f"  is_lowest_level filter works ({len(leaf)} leaf regions)", len(leaf) > 0)

    top3 = (leaf.assign(afc=lambda d: d["log2_fold_change"].abs())
               .nlargest(3, "afc")[["acronym", "region_name", "log2_fold_change", "p_corrected"]])
    print("\n── Top 3 regions by |log2FC| ──")
    print(top3.to_string(index=False))

    quant = pd.read_csv("data/cfos_quantification.csv")
    check("  cfos_quantification has group_nr column", "group_nr" in quant.columns)
    check(f"  quant has {len(quant)} animals",  len(quant) > 0)

    atlas = pd.read_csv("data/atlas_hierarchy.csv")
    check("  atlas_hierarchy loaded", len(atlas) > 0)
    has_label = any(c in atlas.columns for c in ["label", "region_id", "id"])
    check("  atlas has a label/id column", has_label,
          fix=f"Check columns: {list(atlas.columns)} — update brain_viz.py:get_slice() line ~30")

except FileNotFoundError as e:
    print(f"  {FAIL} pandas read failed: {e}")
    errors += 1

print("\n── Imports ──")
try:
    import streamlit  # noqa
    check("streamlit importable", True)
except ImportError:
    check("streamlit importable", False, fix="pip install streamlit")

try:
    import SimpleITK  # noqa
    check("SimpleITK importable", True)
except ImportError:
    check("SimpleITK importable", False, fix="pip install SimpleITK")

try:
    import plotly  # noqa
    check("plotly importable", True)
except ImportError:
    check("plotly importable", False, fix="pip install plotly")

print("\n── Anthropic API key ──")
key = os.environ.get("ANTHROPIC_API_KEY", "")
check("ANTHROPIC_API_KEY set", bool(key),
      fix="export ANTHROPIC_API_KEY=sk-ant-... (or wait for credits at 16:00)")
if key:
    check("key starts with sk-ant-", key.startswith("sk-ant-"),
          fix="Key format looks wrong — check Console")

print()
if errors == 0:
    print("All checks passed. Ready to run: streamlit run app.py\n")
else:
    print(f"{errors} check(s) failed. Fix above before the hackathon starts.\n")
    sys.exit(1)
