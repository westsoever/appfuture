# Explainable Brains — Active Plan
_Last updated: May 26 · Session: explore_data.py passing, critical data findings_

## Current Focus
`data/` symlink created (→ `vibraint/data/`), explore_data runs clean. Two code fixes before smoke-test: `brain_viz.py` still reads `label` column (use `id`); `significant_corrected` is all-zero in this dataset — need `significant_uncorrected` as the default significance flag everywhere in analysis/UI.

## Tasks

### In Progress
_(nothing)_

### Up Next
- [ ] **Fix `brain_viz.py` label column** — `brain_viz.py:32` change `match.iloc[0]["label"]` → `match.iloc[0]["id"]`
- [ ] **Fix significance flag** — `significant_corrected` is all 0.0 in this dataset (p_corrected range [0.43, 1.0]); replace with `significant_uncorrected` in:
  - `analysis.py:volcano_data` — `significant_corrected == True` → `significant_uncorrected == 1`
  - `app.py` — any "significant only" default filter must use `significant_uncorrected`
  - `CLAUDE.md` data rules note (`significant_corrected` not usable)
- [ ] Run `python smoke_test.py` — verify all checks pass
- [ ] Start `streamlit run app.py` — confirm 3 tabs load with data
- [ ] Wire up region deep dive end-to-end (violin + brain slice + Claude button)
- [ ] Test Claude "Explain this region" button with real API key
- [ ] Pre-load demo data so charts aren't blank on first open
- [ ] Run `/demo` command — pick 3 best regions, rehearse 2-min script

### Done
- [x] Designed folder structure
- [x] Written `CLAUDE.md` (module map + data rules)
- [x] Written `app.py` (3-tab Streamlit skeleton)
- [x] Written `data_loader.py`, `analysis.py`, `brain_viz.py`, `llm.py`
- [x] Written `download_data.py`
- [x] Written `smoke_test.py`
- [x] Written `.claude/settings.json` (pre-approved permissions)
- [x] Written `/run`, `/check`, `/demo`, `/session-context`, `/hackathon` commands
- [x] Written `/plan` and `/wrap-up` commands
- [x] `ANTHROPIC_API_KEY` added to env
- [x] Data downloaded — all 8 files in `vibraint/data/`
- [x] Schema confirmed: stats 1356 rows, hierarchy 1356 rows, quant 12 animals (6/group)
- [x] **Fix data path** — symlink `data/ → vibraint/data/` created; all modules work as-is
- [x] `explore_data.py` fixed (`significant_corrected.astype(bool)`) and passing

## Data Reality (confirmed by explore_data.py)
| Fact | Value |
|------|-------|
| `significant_corrected` hits | **0** — p_corrected range [0.43, 1.0], unusable |
| `significant_uncorrected` hits | use these for rankings/volcano |
| Lowest-level regions | 459 |
| log2FC range | [−3.29, +2.77] |
| Atlas label column | `id` (not `label`, not `region_id`) |
| Atlas name column | `name` (not `region_name`) |
| NIfTI shape | (268, 512, 369) — Z/Y/X |
| Animals | 6×G001, 6×G002 |

## Blockers & Manual Input Needed
- [ ] 👥 **Team size** — if working with others, decide who owns which tab before starting UI work

## Backlog (if time allows, in priority order)
- [ ] Add volcano labels for top 5 uncorrected hits (plotly `text` param)
- [ ] Add "Download results as CSV" button to ranking table
- [ ] NLP query box: "which regions are involved in hunger?" → lookup + highlight
- [ ] Colour brain slice by G001 vs G002 signal side-by-side
- [ ] Add confidence interval bars to violin plot

## Session Log
| When | What happened |
|------|---------------|
| May 25 eve | Set up full folder structure: skeleton app, all modules, commands, smoke test, this plan file |
| May 26 ~17:30 | API key added, data downloaded to `vibraint/data/` (8 files); confirmed schema — `atlas_hierarchy.csv` uses `id` not `label`, data path needs fixing in modules |
| May 26 ~18:00 | `explore_data.py` passing; symlink created for data path; discovered `significant_corrected` all-zero — must use `significant_uncorrected` throughout |
