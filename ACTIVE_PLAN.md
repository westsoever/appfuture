# Explainable Brains — Active Plan
_Last updated: May 25 evening · Session: initial setup_

## Current Focus
All skeleton files written. Waiting for bucket credentials (go live at 16:00 May 26) to download data and smoke-test the app.

## Tasks

### In Progress
_(nothing — pre-hackathon, waiting for credentials)_

### Up Next
- [ ] Fork + clone `explainable-brains/explainable-brains-hackathon`
- [ ] Copy app files into the forked repo
- [ ] Run `python download_data.py` (do on good WiFi, not event WiFi)
- [ ] Run `python smoke_test.py` — verify columns match expected schema
- [ ] Fix `brain_viz.py` if `atlas_hierarchy.csv` label column name differs
- [ ] Start `streamlit run app.py` — confirm 3 tabs load with data
- [ ] Polish volcano tab: add labels on top 5 hits
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

## Blockers & Manual Input Needed
- [ ] 🔑 **API credits** — link goes live at 16:00. Have Claude Console open. Paste `ANTHROPIC_API_KEY` into env immediately.
- [ ] 🌐 **Bucket credentials** — check `bucket_access/config.py` in the starter repo for how to authenticate. May need a token from organizers.
- [ ] ❓ **atlas_hierarchy.csv label column** — `brain_viz.py` assumes column named `label`. Run `python -c "import pandas as pd; print(pd.read_csv('data/atlas_hierarchy.csv').columns.tolist())"` after download and update line ~30 of `brain_viz.py` if different.
- [ ] 🧪 **smoke_test.py first run** — will reveal any schema mismatches. Fix before building UI.
- [ ] 👥 **Team size** — if working with others, decide who owns which tab before 16:30.

## Backlog (if time allows, in priority order)
- [ ] Add volcano labels for top 5 significant hits (plotly `text` param)
- [ ] Add "Download results as CSV" button to ranking table
- [ ] NLP query box: "which regions are involved in hunger?" → lookup + highlight
- [ ] Colour brain slice by G001 vs G002 signal side-by-side
- [ ] Add confidence interval bars to violin plot

## Session Log
| When | What happened |
|------|---------------|
| May 25 eve | Set up full folder structure: skeleton app, all modules, commands, smoke test, this plan file |
