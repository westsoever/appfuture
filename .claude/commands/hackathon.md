---
name: hackathon
description: Full competitive context for Explainable Brains Challenge B — inject when Claude needs the full picture
allowed_tools: []
---

# Explainable Brains — Challenge B competitive context

## What we're building
A 3-tab Streamlit dashboard that lets any neuroscientist see where Semaglutide (Ozempic) rewires the brain in 30 seconds.

## The stack (already built)
- `app.py` — Streamlit, 3 tabs: Volcano Plot / Region Ranking / Region Deep Dive
- `data_loader.py` — cached CSV loaders
- `analysis.py` — rank_regions(), volcano_data()
- `brain_viz.py` — NIfTI slice extractor
- `llm.py` — Claude API explain_region() wrapper
- `download_data.py` — fetch all data files

## The 7 judging criteria (all equal weight)
1. **Usability & UX** — one entry point, works for a biologist, no config needed
2. **Creativity & Innovation** — the "Ask Claude about this region" button is the differentiator
3. **Communication & Presentation** — 2-min demo IS the product, script it
4. **Quality of Product** — nothing broken during demo, data pre-loaded
5. **Insight & Interpretability** — surface a surprising or meaningful finding
6. **Impact on Brain Health** — frame as accelerating drug discovery, mention Ozempic
7. **Feasibility & Scalability** — "works for any Vibraint study, just swap the CSV"

## Judges
- **Novo Nordisk Foundation** → data trustworthiness, rigour
- **Danish Cancer Institute** → technical correctness
- **Vibraint** (data owner) → useful to their actual workflow
- **Applied Futures** → would this be a product?

## Key biology (know for demo)
- **c-Fos** = recently active neurons. High density = active region.
- **G001** = Vehicle (control), **G002** = Semaglutide
- **log2_fold_change > 0** = more active in Semaglutide
- Regions likely to be top hits (validates biology): NTS, ARC/DMH, PVT, CEA, VTA/NAc
- If these appear in top hits → "this validates the known mechanism of GLP-1 agonists"

## 2-minute demo script
```
0:00  "Ozempic changes how the brain works. We built a tool to see exactly where."
0:15  Volcano: "Each dot is a brain region. Right = more active in Ozempic mice."
0:30  Click NTS: "The brainstem hunger centre — strongly upregulated. Expected."
0:45  Click Explain: Claude output live. "Any clinician can understand this now."
1:00  Scroll to one surprising region with high significance
1:15  Brain slice: "Here's where that region is, physically, in the brain."
1:30  "This works for any Vibraint study — just swap the CSV."
1:45  "From raw imaging data to biological insight, for anyone."
2:00  Done.
```

## Build timeline (16:30–19:00)
| By | Goal |
|----|------|
| 16:45 | Volcano tab polished, top-5 labels visible |
| 17:15 | Deep dive working end-to-end + Claude button |
| 17:45 | Brain slice overlay working |
| 18:15 | Buffer / polish / fix broken demo paths |
| 18:30 | Rehearse demo, pick 3 best regions |
| 19:00 | Demos start |

## Data column gotchas
- Filter `is_lowest_level == True` before any ranking — avoids double-counting
- `mean_A` = Semaglutide (G002), `mean_B` = Vehicle (G001)
- `p_corrected` not `p_value` for significance
- NIfTI arrays from SimpleITK are shape (Z, Y, X) — axis=1 is coronal
