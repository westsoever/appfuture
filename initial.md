# Morning checklist — before the hackathon (today, May 26)

## Status: what exists
All app files are written and ready. The app will run once data is downloaded.

```
appfuture/
├── CLAUDE.md          ← done, Claude Code compass
├── .gitignore         ← done, excludes data/
├── app.py             ← done, 3-tab Streamlit app
├── data_loader.py     ← done, cached CSV loaders
├── analysis.py        ← done, rank_regions() + volcano_data()
├── brain_viz.py       ← done, NIfTI slice extractor
├── llm.py             ← done, Claude API explain_region()
├── download_data.py   ← done, run this first
└── data/              ← empty, gitignored
```

---

## Step 1 — Fork + clone the starter repo (do first)

The files above need to live inside the forked repo so you get `bucket_access/`:

```bash
gh repo fork explainable-brains/explainable-brains-hackathon --clone
cd explainable-brains-hackathon
```

Then copy these files in:
```bash
cp /Users/lyo/aiw/appfuture/{CLAUDE.md,app.py,data_loader.py,analysis.py,brain_viz.py,llm.py,download_data.py,.gitignore} .
mkdir -p data
```

---

## Step 2 — Environment

```bash
conda env create -f environment.yml
conda activate explainable-brains
pip install anthropic   # if not already in environment.yml
```

---

## Step 3 — Verify bucket access

```bash
python -c "from bucket_access.bucket_utils import list_files; list_files('challengeB/')"
```

If this fails, check `bucket_access/config.py` for credential setup.

---

## Step 4 — Download all data (do NOW, not on event WiFi)

```bash
python download_data.py
```

Downloads ~300MB of NIfTI files + 2 CSVs into `data/`. Takes a few minutes.
Verify: `ls -lh data/` should show 8 files.

---

## Step 5 — Set Anthropic API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or add to `.env` (already gitignored). Test it:
```bash
python -c "from llm import explain_region; import pandas as pd; print(explain_region({'region_name':'Hypothalamus','acronym':'HY','log2_fold_change':0.8,'p_corrected':0.001,'mean_A':120,'mean_B':80}))"
```

Note: API credits link goes live at **16:00** at the event. Have Claude Console open.

---

## Step 6 — Smoke-test the app

```bash
streamlit run app.py
```

Expected: 3 tabs load, volcano plot renders, region table shows ~400 rows.
If NIfTI slice tab fails with FileNotFoundError → re-run `download_data.py`.

---

## Known issues / things to watch

**`atlas_hierarchy.csv` column name for label**
`brain_viz.py` assumes the integer-label column is called `label`. Check:
```python
import pandas as pd; pd.read_csv("data/atlas_hierarchy.csv").columns.tolist()
```
If it's named differently (e.g. `region_id`), update `brain_viz.py:get_slice()` line ~30.

**NIfTI axis orientation**
`brain_viz.py` uses `axis=1` for coronal slices (Z,Y,X array from SimpleITK).
If slices look wrong (sagittal instead of coronal), try `axis=0` or `axis=2`.

**`mean_A` vs `mean_B` labelling**
In `cfos_statistics.csv`: A = G002 (Semaglutide), B = G001 (Vehicle). Confirm with:
```python
pd.read_csv("data/cfos_statistics.csv").columns.tolist()
```
If column names differ, update `llm.py` and `app.py` accordingly.

---

## During the hackathon (16:30–19:00)

| Time | Goal |
|------|------|
| 16:30 | Claim API credits, confirm app still runs |
| 16:45 | Volcano tab polished — labels on top 5 hits |
| 17:15 | Region deep dive working end-to-end with Claude button |
| 17:45 | Brain slice overlay working |
| 18:15 | Buffer / polish / fix broken demo paths |
| 18:30 | Rehearse 2-minute demo script (see hackathon_strategy.md) |
| 19:00 | Demos start |

---

## Demo script (2 min) — see hackathon_strategy.md for full version

1. Hook: "Ozempic changes how the brain works. We built a tool to see exactly where."
2. Volcano: point to NTS, ARC, CEA as top hits
3. Click region → violin plot → brain slice
4. Click "Explain this region" → Claude output live
5. Scalability close: "works for any Vibraint study"
