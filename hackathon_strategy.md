# Explainable Brains Hackathon — Competitive Strategy
**Event:** May 26, 2026 · 16:00–20:00 · Copenhagen  
**Build window:** 2.5 hours (16:30–19:00)  
**Demo:** 2 minutes per team

---

## TL;DR verdict

**Pick Challenge B.** The statistics are pre-computed — your job is storytelling and visualization, not ML. You can build something polished and demo-ready in 90 minutes, leaving time to rehearse a strong 2-minute pitch.

---

## Why Challenge B wins over A

| | Challenge A | Challenge B |
|---|---|---|
| Hard part | Must implement diversity/coreset selection | Pre-computed (p-values, fold-changes, all there) |
| Visual wow | Patch grids | Brain anatomy slices + volcano plots |
| Story | "we picked better training data" | "we found where Ozempic rewires the brain" |
| Public hook | None | Ozempic is the most-talked-about drug on Earth |
| Demo clarity | Hard to explain to non-experts | Immediately legible |

Challenge A is more ML-heavy but produces a less compelling demo. Unless your team has a computer vision specialist, go B.

---

## Judging criteria decoded

All 7 criteria are weighted equally:

1. **Usability & UX** — Build for a biologist who has never seen your app. One clear entry point. No config, no error states.
2. **Creativity & Innovation** — The NLP "ask about this region" extension is listed explicitly. Do it.
3. **Communication & Presentation** — Your 2-minute demo IS the product. Script it beforehand.
4. **Quality of Product** — End-to-end. Nothing broken during demo. Load data before demo time starts.
5. **Insight & Interpretability** — Surface a surprising or meaningful finding about Semaglutide vs Vehicle.
6. **Impact on Brain Health** — Frame your tool as accelerating drug discovery. Mention Ozempic.
7. **Feasibility & Scalability** — Mention the tool works for any Vibraint study, not just this one.

**Judges lens:**
- Novo Nordisk Foundation → data trustworthiness, rigour
- Danish Cancer Institute → technical correctness
- Vibraint (data owner) → usefulness to their actual workflow
- Applied Futures → would this be a product?

---

## Winning app: Challenge B blueprint

### The narrative (rehearse this)
> "Semaglutide — the active ingredient in Ozempic — is transforming obesity medicine. But we don't know *how* it rewires the brain. We built a tool that lets any neuroscientist answer that question in 30 seconds."

### App structure (Streamlit, 3 views)

**Page 1 — Volcano Plot (the hook)**
- x-axis: log2 fold change (G002 vs G001)
- y-axis: −log10(p_corrected)
- Colour by significance (corrected vs uncorrected vs ns)
- Hover → region name, stats, quick description
- *The data already has all columns for this. 10 lines of plotly.*

**Page 2 — Brain Region Ranking Table**
- Sortable by fold change, p-value, mean density
- Filter: "only significant (corrected)" toggle
- Click row → opens Page 3 for that region

**Page 3 — Region Deep Dive**
- Bar/violin plot: Vehicle vs Semaglutide per animal for selected region
- NIfTI slice: Show the coronal/axial slice from `cfos_group_median_difference_G002_vs_G001.nii.gz` with the selected region highlighted using `brain_atlas_regions.nii.gz` mask
- "Explain this region" button → Claude API call

### Claude integration (the differentiator)
```python
# Sidebar or button on Page 3
import anthropic

def explain_region(region_name, acronym, log2fc, p_value, mean_a, mean_b):
    client = anthropic.Anthropic()
    prompt = f"""
    Brain region: {region_name} ({acronym})
    In a c-Fos mouse study, Semaglutide-treated mice vs Vehicle:
    - Log2 fold change: {log2fc:.2f} (positive = higher in Semaglutide)
    - Corrected p-value: {p_value:.4f}
    - Mean density Vehicle: {mean_a:.1f} cells/mm³, Semaglutide: {mean_b:.1f} cells/mm³
    
    In 3 sentences: what is this region's known role in the brain, and what might 
    this activation difference mean for understanding how semaglutide works?
    Be accessible to a non-expert.
    """
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

This adds criterion 2 (creativity), criterion 5 (interpretability), and criterion 6 (impact) simultaneously.

---

## File structure to build

```
explainable-brains-hackathon/
├── CLAUDE.md          ← write first, lets Claude Code help you faster
├── data_loader.py     ← download and cache all data files
├── analysis.py        ← volcano prep, region ranking, slice extraction
├── app.py             ← streamlit app, 3 pages
└── llm_explain.py     ← Claude API call wrapper
```

### CLAUDE.md contents (write before the hackathon starts)
```markdown
# Explainable Brains — Challenge B

## Entry point
`streamlit run app.py`

## Data files (downloaded to project root)
- cfos_statistics.csv — one row per brain region, columns: acronym, region_name, log2_fold_change, p_corrected, mean_A, mean_B, etc.
- cfos_quantification.csv — per-animal densities, columns: scan_name, animal_nr, group_nr, [region acronyms...]
- diff_map.nii.gz — NIfTI difference map G002−G001
- regions.nii.gz — NIfTI atlas region labels (integer → atlas_hierarchy.csv)
- atlas_hierarchy.csv — region label ↔ acronym ↔ region_name

## Key functions
- `data_loader.py:load_stats()` returns stats DataFrame
- `data_loader.py:load_quantification()` returns per-animal DataFrame (long format)
- `analysis.py:get_brain_slice(region_acronym, axis='coronal')` returns numpy image array
- `llm_explain.py:explain_region(row)` calls Claude, returns string

## How to add a feature
Edit app.py. Run `streamlit run app.py` to check. Data loading is cached with @st.cache_data.
```

---

## Pre-hackathon checklist (do TODAY)

- [ ] Fork and clone `explainable-brains/explainable-brains-hackathon`
- [ ] `conda env create -f environment.yml && conda activate explainable-brains`
- [ ] Run `python -c "from bucket_access.bucket_utils import list_files; list_files('challengeB/')"` — confirm bucket access works
- [ ] Download the two CSV files and inspect them (understand the columns)
- [ ] Pre-download NIfTI files (they may be slow on event WiFi)
- [ ] Write `CLAUDE.md` as above
- [ ] Write `data_loader.py` skeleton with `load_stats()` and `load_quantification()`
- [ ] Set `ANTHROPIC_API_KEY` and test a small Claude API call
- [ ] Claim hackathon API credits link (goes live at 16:00 — have the page open)
- [ ] Sketch the 2-minute demo narrative on paper

### Quick data download script
```python
from bucket_access.bucket_utils import download_file

files = [
    ('challengeB/tabular_data_quantification/cfos_object_density_statistics_G002_vs_G001.csv', 'cfos_statistics.csv'),
    ('challengeB/tabular_data_quantification/cfos_object_density_quantification.csv', 'cfos_quantification.csv'),
    ('challengeB/spatial_brain_maps/cfos_group_median_difference_G002_vs_G001.nii.gz', 'diff_map.nii.gz'),
    ('challengeB/spatial_brain_maps/brain_atlas_regions.nii.gz', 'regions.nii.gz'),
    ('challengeB/spatial_brain_maps/brain_atlas_anatomy.nii.gz', 'anatomy.nii.gz'),
    ('challengeB/spatial_brain_maps/atlas_hierarchy.csv', 'atlas_hierarchy.csv'),
]

for src, dst in files:
    print(f"Downloading {src}...")
    download_file(src, dst)
    print(f"  → {dst}")
```

---

## Key biology context (helps with the demo narrative)

**Semaglutide (Ozempic/Wegovy)**: GLP-1 receptor agonist. Originally diabetes drug, now weight-loss blockbuster.

**c-Fos**: Immediate early gene. A neuron expressing c-Fos recently fired. High density = recently active region.

**Brain regions likely to show differences** (know these for demo):
- **NTS** (nucleus tractus solitarius) — hunger/satiety signalling, primary GLP-1 target in brainstem
- **ARC / DMH** (hypothalamus) — appetite regulation, energy homeostasis
- **PVT** (paraventricular thalamus) — stress, reward
- **CEA** (central amygdala) — aversive learning, food avoidance
- **VTA / NAc** — dopamine reward circuit

If these regions appear in your top hits, that validates the biology and impresses the Vibraint judge.

---

## Cross-checks vs setup.md research

The setup.md analysis was largely accurate. Key corrections/additions:

1. **Build time is 2.5 hours, not the full 4 hours** — arrival, brief, team formation eat the rest. Plan tighter.
2. **Statistics CSV is richer than expected** — includes `n_A_eff`/`n_B_eff` (effective sample sizes where region was present), confidence intervals, corrected p-values. Use `significant_corrected` as the primary filter.
3. **NIfTI spatial maps are all pre-registered** — they share coordinate space, can be overlaid directly. No registration needed.
4. **`hierarchy_level` and `is_lowest_level` columns** — filter to `is_lowest_level == True` to avoid double-counting parent/child regions in your ranking table.
5. **No GPU needed at all for Challenge B** — purely tabular + NIfTI visualization.
6. **Embeddings in Challenge A use PLIP** (vision model trained on pathology images) — interesting choice for brain data, could be a talking point if you pick A.
7. **API credits claim link goes live at 16:00** — have that tab open ready to paste your org ID.

---

## 2-minute demo script outline

```
0:00 — Hook: "Ozempic changes how the brain works. Today we built a tool to see exactly where."
0:15 — Volcano plot: "This shows all 400+ brain regions. Each dot is a region. Right = more active in Ozempic mice. Up = statistically significant."
0:30 — Click a top hit: "The NTS — the brainstem's hunger centre — is strongly upregulated. Exactly what we'd expect."
0:45 — Click "Explain this region": Claude summarizes in plain English. "Any clinician can now understand this."
1:00 — Scroll to surprising finding: show one unexpected region with high significance.
1:15 — Brain slice: "Here's where that region is, physically, in the brain."
1:30 — Scalability: "This works for any Vibraint study — just swap the CSV."
1:45 — Close: "From raw imaging data to biological insight, for anyone."
2:00 — Done.
```

---

## If you end up on Challenge A (fallback)

Focus on:
1. Load all embeddings (precomputed, 7500 × 512)
2. UMAP to 2D
3. KMeans (k=20) for clusters
4. Coreset selection: pick N patches closest to each cluster centroid
5. Show patch grid viewer by cluster
6. Claude button: "explain why these patches are diverse"

This is harder to make polished in 2.5h but the patch viewer is visually interesting.
