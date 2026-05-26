# Explainable Brains Hackathon — Execution Plan
**Event:** May 26, 2026 · 16:00–20:00 · Copenhagen  
**Build window:** 2.5 hours (≈16:30–19:00)  
**This plan:** Pre-hackathon setup (do TODAY, May 25)

---

## Current Focus *(updated May 26, 00:24)*

App is fully coded and syntax-clean. All imports available in current Python env. **One blocker before running:** need `bucket_access` module from hackathon starter repo to download data. Once at hackathon: activate conda env → `python download_data.py` → `python smoke_test.py` → `streamlit run app.py`.

---

## Blockers & Manual Input Needed

- [ ] 🔑 **ANTHROPIC_API_KEY** — `export ANTHROPIC_API_KEY=sk-ant-...` (claimed at hackathon start)
- [ ] 📦 **bucket_access module** — install hackathon starter kit (`pip install .` in cloned repo) or copy `bucket_access/` folder into `appfuture/`
- [ ] 💾 **Data download** — run `python download_data.py` once bucket_access works
- [ ] 🐍 **conda env** — `conda activate explainable-brains` (or verify current Python env has all deps)

---

## Up Next (at hackathon 16:00–16:30)

1. `conda activate explainable-brains && python download_data.py` — get all data files
2. `python smoke_test.py` — verify columns and imports, catch any name mismatches
3. `streamlit run app.py` — confirm live end-to-end before build window opens
4. Pre-select 3 demo regions: expect NTS, ARC or DMH, one surprising hit

## Backlog (if time allows after 17:45)

- [ ] Add a "top findings" summary card on volcano tab (1 sentence: "X regions upregulated, Y downregulated")
- [ ] Pre-cache Claude explanations for top-5 regions so button is instant on demo
- [ ] Add axis toggle (coronal/sagittal/axial) to brain slice view
- [ ] Colour the brain slice mask by direction (red = up, blue = down) instead of yellow

---

## Done ✓

- [x] Phase 0: Discovery complete — repo found, strategy decided (Challenge B)
- [x] Phase 3: All 5 source files written (`app.py`, `data_loader.py`, `analysis.py`, `brain_viz.py`, `llm.py`, `smoke_test.py`)
- [x] `download_data.py` written
- [x] Bug fix: `analysis.py:23` `p_value` → `p_corrected` (column doesn't exist in schema)
- [x] Volcano: top-5 significant hits labelled with acronym annotations
- [x] Ranking tab: sig-only default=True, red/blue fold-change colouring, human-readable column headers
- [x] LLM prompt: structured 3-sentence format with disease relevance hook, bumped max_tokens 200→300
- [x] Syntax-verified all files clean

---

## Session Log

| Date/Time | Summary |
|-----------|---------|
| May 25, 22:00 | Built full app skeleton (all 5 files), smoke test, download script. Phase 0 discovery complete, strategy locked as Challenge B. |
| May 26, 00:24 | Fixed p_value bug, added volcano labels, improved ranking UX + LLM prompt. App syntax-clean, imports verified. Blocked on bucket_access until hackathon start. |

---

---

## Phase 0: Discovery — COMPLETE

**Findings:**
- Repo `explainable-brains/explainable-brains-hackathon` is public and accessible
- `ANTHROPIC_API_KEY` is **NOT set** — critical blocker, fix first
- conda env `explainable-brains` does **not exist** yet
- `anthropic` Python package v0.83.0 is installed in current env
- Strategy: Challenge B (volcano + region table + NIfTI slice + Claude explain)

---

## Phase 1: Environment Setup

**Goal:** Clone repo, create env, set API key, verify bucket access.

### Steps

```bash
# 1. Fork on GitHub (do this manually in browser), then clone
cd ~/aiw
git clone https://github.com/<YOUR_FORK>/explainable-brains-hackathon
cd explainable-brains-hackathon

# 2. Create conda env
conda env create -f environment.yml
conda activate explainable-brains

# 3. Set ANTHROPIC_API_KEY (add to ~/.zshrc for persistence)
export ANTHROPIC_API_KEY="sk-ant-..."

# 4. Smoke test: bucket access
python -c "
from bucket_access.bucket_utils import list_files
files = list_files('challengeB/')
print(f'Bucket accessible: {len(files)} files found')
for f in files[:10]:
    print(' ', f)
"
```

### Verification
- [ ] `conda activate explainable-brains` succeeds
- [ ] Bucket lists files without auth error
- [ ] `python -c "import anthropic; print(anthropic.__version__)"` prints version

---

## Phase 2: Data Pre-download

**Goal:** Download all data files while on home WiFi — event WiFi may be slow.

### Download script (`download_data.py`)

```python
from bucket_access.bucket_utils import download_file
import os

files = [
    ('challengeB/tabular_data_quantification/cfos_object_density_statistics_G002_vs_G001.csv', 'cfos_statistics.csv'),
    ('challengeB/tabular_data_quantification/cfos_object_density_quantification.csv', 'cfos_quantification.csv'),
    ('challengeB/spatial_brain_maps/cfos_group_median_difference_G002_vs_G001.nii.gz', 'diff_map.nii.gz'),
    ('challengeB/spatial_brain_maps/brain_atlas_regions.nii.gz', 'regions.nii.gz'),
    ('challengeB/spatial_brain_maps/brain_atlas_anatomy.nii.gz', 'anatomy.nii.gz'),
    ('challengeB/spatial_brain_maps/atlas_hierarchy.csv', 'atlas_hierarchy.csv'),
]

os.makedirs('data', exist_ok=True)
for src, dst in files:
    dst_path = f'data/{dst}'
    if os.path.exists(dst_path):
        print(f'SKIP (exists): {dst_path}')
        continue
    print(f'Downloading {src} ...')
    download_file(src, dst_path)
    size_mb = os.path.getsize(dst_path) / 1e6
    print(f'  → {dst_path} ({size_mb:.1f} MB)')
```

### Inspect columns (run after download)

```python
import pandas as pd
stats = pd.read_csv('data/cfos_statistics.csv')
quant = pd.read_csv('data/cfos_quantification.csv')
print('STATS columns:', stats.columns.tolist())
print('STATS shape:', stats.shape)
print(stats.head(3))
print('\nQUANT columns:', quant.columns.tolist()[:20])
```

### Verification
- [ ] `data/cfos_statistics.csv` exists, >100 rows
- [ ] `data/cfos_quantification.csv` exists
- [ ] `data/diff_map.nii.gz` exists, >50 MB
- [ ] `data/regions.nii.gz` exists
- [ ] Columns include: `log2_fold_change`, `p_corrected`, `significant_corrected`, `is_lowest_level`

---

## Phase 3: Build Skeleton Files

**Goal:** Write all 5 source files BEFORE the hackathon so Claude Code can extend them during the build window.

### 3a. `CLAUDE.md`

```markdown
# Explainable Brains — Challenge B

## Entry point
`streamlit run app.py`

## Data files (in data/)
- cfos_statistics.csv — one row per brain region: acronym, region_name, log2_fold_change, p_corrected, significant_corrected, mean_A, mean_B, n_A_eff, n_B_eff, is_lowest_level
- cfos_quantification.csv — per-animal densities: scan_name, animal_nr, group_nr, [region acronyms as columns]
- diff_map.nii.gz — NIfTI voxel-wise difference map G002−G001
- regions.nii.gz — NIfTI atlas region labels (integer → atlas_hierarchy.csv)
- anatomy.nii.gz — NIfTI anatomical reference
- atlas_hierarchy.csv — maps integer voxel label → acronym → region_name

## Key functions
- `data_loader.py:load_stats()` → DataFrame (stats per region, lowest-level only)
- `data_loader.py:load_quantification()` → DataFrame (per-animal, long format)
- `analysis.py:prepare_volcano(df)` → DataFrame with x, y, color columns for volcano plot
- `analysis.py:get_region_ranking(df)` → DataFrame sorted by significance
- `analysis.py:get_brain_slice(region_acronym, axis)` → dict with img array + metadata
- `llm_explain.py:explain_region(row)` → str explanation from Claude

## Treatment groups
- G001 = Vehicle (control)
- G002 = Semaglutide (treatment)
- Positive log2_fold_change = higher in Semaglutide

## Run and test
streamlit run app.py
```

### 3b. `data_loader.py`

```python
import pandas as pd
import streamlit as st

DATA_DIR = "data"

@st.cache_data
def load_stats():
    df = pd.read_csv(f"{DATA_DIR}/cfos_statistics.csv")
    return df[df["is_lowest_level"] == True].copy()

@st.cache_data  
def load_quantification():
    df = pd.read_csv(f"{DATA_DIR}/cfos_quantification.csv")
    # Melt to long format: columns = scan_name, animal_nr, group_nr, region, density
    id_cols = ["scan_name", "animal_nr", "group_nr"]
    region_cols = [c for c in df.columns if c not in id_cols]
    return df.melt(id_vars=id_cols, value_vars=region_cols, var_name="region", value_name="density")

@st.cache_data
def load_atlas():
    return pd.read_csv(f"{DATA_DIR}/atlas_hierarchy.csv")
```

### 3c. `analysis.py`

```python
import numpy as np
import nibabel as nib
import pandas as pd

def prepare_volcano(df):
    out = df.copy()
    out["neg_log10_p"] = -np.log10(out["p_corrected"].clip(lower=1e-10))
    out["color"] = "not significant"
    out.loc[out["p_corrected"] < 0.05, "color"] = "significant (corrected)"
    return out

def get_region_ranking(df, only_significant=False):
    if only_significant:
        df = df[df["significant_corrected"] == True]
    return df.sort_values("p_corrected").reset_index(drop=True)

def get_brain_slice(region_acronym, atlas_df, regions_nii_path, diff_nii_path, axis="coronal"):
    regions_img = nib.load(regions_nii_path)
    diff_img = nib.load(diff_nii_path)
    regions_data = regions_img.get_fdata()
    diff_data = diff_img.get_fdata()

    # Get voxel label for this region
    match = atlas_df[atlas_df["acronym"] == region_acronym]
    if match.empty:
        return None
    label = int(match.iloc[0]["label"])

    # Find center of mass of this region
    mask = (regions_data == label)
    if not mask.any():
        return None
    coords = np.argwhere(mask)
    center = coords.mean(axis=0).astype(int)

    axis_map = {"sagittal": 0, "coronal": 1, "axial": 2}
    ax = axis_map.get(axis, 1)
    idx = center[ax]

    slices = [slice(None)] * 3
    slices[ax] = idx
    
    return {
        "diff_slice": diff_data[tuple(slices)],
        "mask_slice": mask[tuple(slices)],
        "center": center,
        "axis": axis,
    }
```

### 3d. `llm_explain.py`

```python
import anthropic
import streamlit as st

@st.cache_data(show_spinner=False)
def explain_region(region_name, acronym, log2fc, p_value, mean_a, mean_b):
    client = anthropic.Anthropic()
    prompt = f"""Brain region: {region_name} ({acronym})
In a c-Fos mouse study, Semaglutide-treated mice vs Vehicle:
- Log2 fold change: {log2fc:.2f} (positive = higher in Semaglutide)
- Corrected p-value: {p_value:.4f}
- Mean density Vehicle: {mean_a:.1f} cells/mm³, Semaglutide: {mean_b:.1f} cells/mm³

In 3 sentences: what is this region's known role in the brain, and what might this activation difference mean for understanding how semaglutide works? Be accessible to a non-expert."""
    
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

### 3e. `app.py` (skeleton)

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

from data_loader import load_stats, load_quantification, load_atlas
from analysis import prepare_volcano, get_region_ranking, get_brain_slice
from llm_explain import explain_region

st.set_page_config(page_title="Explainable Brains", layout="wide")
st.title("Explainable Brains: Where Does Semaglutide Rewire the Mouse Brain?")

stats = load_stats()
quant = load_quantification()
atlas = load_atlas()

page = st.sidebar.radio("View", ["Volcano Plot", "Region Ranking", "Region Deep Dive"])

if page == "Volcano Plot":
    st.header("All Brain Regions: Semaglutide vs Vehicle")
    volcano_df = prepare_volcano(stats)
    fig = px.scatter(
        volcano_df,
        x="log2_fold_change",
        y="neg_log10_p",
        color="color",
        hover_data=["region_name", "acronym", "p_corrected", "mean_A", "mean_B"],
        color_discrete_map={
            "significant (corrected)": "#e74c3c",
            "not significant": "#95a5a6",
        },
        labels={"log2_fold_change": "Log2 Fold Change (Sema/Vehicle)", "neg_log10_p": "-log10(p corrected)"},
    )
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Region Ranking":
    st.header("Brain Regions Ranked by Statistical Significance")
    only_sig = st.toggle("Only significant (corrected)", value=True)
    ranked = get_region_ranking(stats, only_significant=only_sig)
    selected = st.dataframe(
        ranked[["region_name", "acronym", "log2_fold_change", "p_corrected", "mean_A", "mean_B"]],
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
    )

elif page == "Region Deep Dive":
    st.header("Region Deep Dive")
    region_options = stats.sort_values("p_corrected")["acronym"].tolist()
    selected_acronym = st.selectbox("Select region", region_options)
    row = stats[stats["acronym"] == selected_acronym].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        # Per-animal violin plot
        region_quant = quant[quant["region"] == selected_acronym].copy()
        region_quant["group"] = region_quant["group_nr"].map({1: "Vehicle", 2: "Semaglutide"})
        fig2 = px.violin(region_quant, x="group", y="density", box=True, points="all",
                         color="group", title=f"c-Fos density: {row['region_name']}")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Brain slice
        slice_data = get_brain_slice(
            selected_acronym, atlas,
            "data/regions.nii.gz", "data/diff_map.nii.gz"
        )
        if slice_data:
            fig3, ax = plt.subplots()
            ax.imshow(slice_data["diff_slice"].T, origin="lower", cmap="RdBu_r")
            mask_overlay = np.ma.masked_where(~slice_data["mask_slice"].T, slice_data["mask_slice"].T)
            ax.imshow(mask_overlay, origin="lower", cmap="Greens", alpha=0.5)
            ax.set_title(f"{selected_acronym} location")
            ax.axis("off")
            st.pyplot(fig3)
    
    st.subheader("What does this mean?")
    if st.button("Explain this region with Claude"):
        with st.spinner("Asking Claude..."):
            explanation = explain_region(
                row["region_name"], row["acronym"],
                row["log2_fold_change"], row["p_corrected"],
                row["mean_A"], row["mean_B"]
            )
        st.info(explanation)
```

### Verification
- [ ] `streamlit run app.py` launches without import errors
- [ ] Volcano plot renders with correct axes
- [ ] `explain_region("NTS", "NTS", 0.8, 0.001, 100.0, 180.0)` returns text
- [ ] No hardcoded column names that don't exist in CSVs

---

## Phase 4: Final Smoke Test + Demo Prep

### Smoke test script (`smoke_test.py`)

```python
import pandas as pd
from data_loader import load_stats, load_quantification
from analysis import prepare_volcano, get_region_ranking

stats = load_stats()
assert len(stats) > 50, "stats too small"
assert "log2_fold_change" in stats.columns
assert "p_corrected" in stats.columns
assert "significant_corrected" in stats.columns
assert "is_lowest_level" in stats.columns

quant = load_quantification()
assert "density" in quant.columns

volcano = prepare_volcano(stats)
assert "neg_log10_p" in volcano.columns
assert "color" in volcano.columns

ranked = get_region_ranking(stats, only_significant=True)
print(f"Top hit: {ranked.iloc[0]['region_name']} (p={ranked.iloc[0]['p_corrected']:.4f})")
print("All assertions passed.")
```

### Demo flow to rehearse (2 min exactly)

```
0:00 — "Ozempic changes how the brain works. We built a tool to see exactly where."
0:15 — Volcano plot: "400+ brain regions. Right = more active in Ozempic mice. Up = significant."
0:30 — Click NTS or top hit: "The brainstem hunger centre — upregulated. Expected."
0:45 — Click 'Explain this region': Claude gives plain-English interpretation live.
1:00 — Show a surprising/unexpected region with high significance.
1:15 — Brain slice view: "Here's where that region is physically."
1:30 — "This works for any Vibraint study — just swap the CSV."
1:45 — "From raw imaging to biological insight, for anyone."
2:00 — Done.
```

### Day-of checklist (16:00 on May 26)

- [ ] Claim API credits at hackathon link (page open before 16:00)
- [ ] `conda activate explainable-brains`
- [ ] `python smoke_test.py` — confirm data loads
- [ ] `streamlit run app.py` — confirm app is live before build window opens
- [ ] Have demo script on phone or printed

---

## Critical Gaps to Fix NOW

| Gap | Fix |
|-----|-----|
| `ANTHROPIC_API_KEY` not set | `echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc && source ~/.zshrc` |
| conda env missing | `conda env create -f environment.yml` after cloning repo |
| Repo not cloned | Fork + clone tonight |
| NIfTI files not downloaded | Run `python download_data.py` (large files, do on home WiFi) |

---

## Column name assumptions (verify after Phase 2)

The code above assumes these column names. Confirm after downloading CSVs:

| Assumed name | Alternative if wrong |
|---|---|
| `log2_fold_change` | `log2fc`, `fold_change` |
| `p_corrected` | `p_adj`, `q_value`, `corrected_pvalue` |
| `significant_corrected` | `significant`, `is_significant` |
| `is_lowest_level` | `lowest_level`, `leaf` |
| `mean_A` | `mean_vehicle`, `mean_G001` |
| `mean_B` | `mean_sema`, `mean_G002` |
| `acronym` | `region_acronym`, `label` |
| `region_name` | `name`, `region` |

After `python download_data.py`, run the inspect snippet in Phase 2 and update column names in all files before the hackathon.
