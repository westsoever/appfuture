# Explainable Brains — Semaglutide vs Vehicle

An interactive Streamlit dashboard for exploring c-Fos brain activity data comparing **Semaglutide (Ozempic)** against **Vehicle controls** in mice. Built for the [Vibraint](https://vibraint.com) Explainable Brains Challenge B hackathon.

The app maps which brain regions become more or less active under GLP-1 agonist treatment — and uses **Claude (Anthropic)** to generate plain-English explanations of each finding.

---

## Features

### Volcano Plot
Interactive scatter plot of all ~459 brain regions. Each point is a region; position encodes effect size (log₂ fold change) and statistical confidence (−log₁₀ p). Top-5 hits are labelled automatically. A one-click **"Auto-summarize"** button asks Claude to narrate the key findings in 4 sentences.

### Region Ranking
Sortable table of leaf-level brain regions ranked by absolute log₂ fold change. Toggle between all regions and nominally significant hits. Red = higher in Semaglutide, blue = higher in Vehicle.

### Region Deep Dive
Pick any region to see:
- **Per-animal violin plot** — c-Fos cell density for each mouse, by group
- **Brain slice viewer** — coronal MRI slice with the selected region highlighted and the group-difference map overlaid
- **Claude explanation** — 3-sentence plain-English summary: what the region normally does, what the activity change suggests about Semaglutide's mechanism, and why it matters for obesity/addiction/brain health research

---

## Highlighted Findings

| Region | Acronym | Direction | Significance |
|--------|---------|-----------|--------------|
| Nucleus of the Solitary Tract | NTS | ↑ Semaglutide | Uncorrected |
| Arcuate Hypothalamic Nucleus | ARH | ↑ Semaglutide | Uncorrected |
| Lateral Hypothalamic Area | LHA | ↓ Semaglutide | Uncorrected |
| Mediodorsal Nucleus of Thalamus | MD | ↑ Semaglutide | Uncorrected |

The NTS and ARH results confirm known GLP-1 satiety circuits. The MD finding (a prefrontal–limbic relay) is unexpected and suggests Semaglutide may reshape cognitive control and decision-making, not just hunger signalling.

---

## Setup

### Prerequisites
- Python 3.11
- Conda (recommended) or pip
- An [Anthropic API key](https://console.anthropic.com)

### Install

```bash
conda create -n explainable-brains python=3.11
conda activate explainable-brains
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
# edit .env and add your ANTHROPIC_API_KEY
```

`.env` format:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Download data

Data files are not included in this repository. Download them with:

```bash
python download_data.py
```

> **Note:** This requires Hetzner Object Storage credentials (`HETZNER_ACCESS_KEY` / `HETZNER_SECRET_KEY` in `.env`). These are provided as part of the Vibraint hackathon. External users will need to supply their own c-Fos NIfTI data in the expected format (see `CLAUDE.md` for the schema).

### Run

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501).

### Smoke test

After downloading data, verify everything is wired up:

```bash
python smoke_test.py
```

---

## Project Structure

```
app.py              # Streamlit entry point — 3 tabs
data_loader.py      # load_stats(), load_quant_long() with caching
analysis.py         # rank_regions(), volcano_data()
brain_viz.py        # get_slice() — coronal NIfTI slices per region
llm.py              # explain_region(), explain_top_findings() via Claude API
download_data.py    # one-shot data download from object storage
smoke_test.py       # pre-flight checks for data + imports + API key
demo_cache/         # pre-generated Claude responses for offline demo
vibraint/           # original challenge starter kit + bucket access utilities
data/               # downloaded data files (gitignored)
```

---

## Data Schema

`data/cfos_statistics.csv` — one row per brain region:

| Column | Description |
|--------|-------------|
| `acronym` | Short region identifier (e.g. `NTS`) |
| `region_name` | Full anatomical name |
| `log2_fold_change` | log₂(Semaglutide / Vehicle); positive = higher in Sema |
| `p_value` | Uncorrected p-value |
| `p_corrected` | Multiple-comparison corrected p-value |
| `significant_uncorrected` | Nominally significant (p < 0.05) |
| `significant_corrected` | High-confidence hit (corrected p < 0.05) |
| `mean_A` | Mean c-Fos density, Semaglutide group (cells/mm³) |
| `mean_B` | Mean c-Fos density, Vehicle group |
| `is_lowest_level` | True for leaf regions — always filter on this to avoid double-counting |

---

## Tech Stack

- **[Streamlit](https://streamlit.io)** — UI
- **[Plotly](https://plotly.com/python/)** — interactive charts
- **[SimpleITK](https://simpleitk.org)** — NIfTI brain volume loading
- **[Anthropic Claude](https://www.anthropic.com)** (`claude-opus-4-7`) — region explanations with prompt caching

---

## License

MIT
