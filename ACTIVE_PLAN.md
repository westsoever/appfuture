# Explainable Brains — Active Plan
_Last updated: May 26 ~18:40 · Handfix landed (96d9688); Agent 4 (Block C) landed (50fe81e); Agents 2 & 3 in-flight in parallel terminals_

## Current Focus
On branch `p3-claude-viz`. Pre-flight (77b33e9), Block C DEMO.md (50fe81e), significance handfix + Styler.map (96d9688) all shipped. Agent 2 (Block A llm.py) running in user's other terminal; Agent 3 (Block B brain_viz) in flight. **Next:** wait for 2 & 3 to commit → run Agent 5 verification gate.

## Tasks

### In Progress
- [ ] **Agent 2 — Block A `llm.py`** — cached `explain_region` + `explain_top_findings` with prompt cache. (running in user's other terminal)
- [ ] **Agent 3 — Block B `brain_viz.py`** — `st.cache_resource` volumes, `@st.cache_data` get_slice, return None on missing/empty, `render_overlay` helper. (in-flight as ruflo-core:coder)

### Up Next — P3 subagent launch queue
5. Agent 5 — verification + anti-pattern grep sweep (§9 integration checklist) — after Agents 2 & 3 land
6. Agent 6 — Phase 3/4 surprising-region pick + summarize button wire-up + `demo_cache/*.txt` prewarm
7. Agent 7 — merge `p3-claude-viz` → `main`

### Up Next — after branching (per role)
- [ ] **P1** (`p1-data`): see PLAN_4PERSON.md §Phase 2 P1
- [ ] **P2** (`p2-ui`): see PLAN_4PERSON.md §Phase 2 P2
- [ ] **P3** (`p3-claude-viz`): see `P3_PLAN.md` — self-contained, has everything needed for a fresh session
- [ ] Integration gate T+1:30 → merge all to `main` → end-to-end demo walk-through
- [ ] Run `/demo` — pick 3 best regions, rehearse 2-min script

### Done
- [x] **Significance handfix (May 26 ~18:38, commit 96d9688)** — `significant_corrected` → `significant_uncorrected` in `analysis.py:21,23` and `app.py:37,53`. Also fixed `Styler.applymap` → `.map` (pandas 3.x rename) so Ranking tab renders.
- [x] **Agent 4 — Block C (May 26 ~18:35, commit 50fe81e)** — `DEMO.md` skeleton from P3_PLAN §7 template (26 lines, [SURPRISING_REGION_TBD] placeholder preserved); `demo_cache/.gitkeep` + `demo_cache/screenshots/.gitkeep` created
- [x] **Agent 1 — Pre-flight (May 26 ~18:20, commit 77b33e9)** — branched `p3-claude-viz`; `data/` symlink restored; `brain_viz.py` `label`→`id` (NTS mask 772 voxels); `llm.py` `p_corrected`→`p_value`+`p_uncorr`; smoke 19/19 green; streamlit running
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
- [x] ~~**Fix data path** — symlink `data/ → vibraint/data/` created~~ (REVERTED — symlink no longer present, re-create)
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

## Team (3-person split — see `PLAN_4PERSON.md` for full role plan)
- **P1 — Data:** `data_loader.py`, `analysis.py`
- **P2 — UI:** `app.py`, `CLAUDE.md`
- **P3 — Claude + Viz + Demo:** `llm.py`, `brain_viz.py`, `DEMO.md` — branch `p3-claude-viz`. Heaviest role; chat-streaming + anatomy panel are stretch-only.

## Blockers & Manual Input Needed
- [ ] 🔑 **`ANTHROPIC_API_KEY` shell persistence** — currently exported in current shell only. Add to `~/.zshrc` or project `.env` (gitignored) before next session so subagents don't trip the smoke test.

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
| May 26 evening | Team finalized at 3: P3 = Claude + Viz + Demo (merged former P3 Claude Lead + P4 Brain Viz + Demo Lead). `PLAN_4PERSON.md` updated accordingly. P3 branch = `p3-claude-viz` |
| May 26 ~21:00 (wrap-up) | Created `P3_PLAN.md` — fully self-contained role spec (data reality, allowed APIs, anti-patterns, Block A/B/C tasks, verification, demo script template) so any fresh session can execute P3 work without re-reading other plan files. Updated ACTIVE_PLAN Up Next to split pre-branch (`main`) fixes from per-role branch work |
| May 26 ~22:00 (agents session) | Audited current code vs `P3_PLAN.md`. Found: (a) `data/` symlink missing despite being marked Done; (b) `llm.py` uses `p_corrected` and plan's `p_uncorrected` column doesn't exist — real col is `p_value`. Split P3 into 7 launchable subagent prompts (setup → A/B/C parallel → verify → phase3-4 → merge) ready to fire one-by-one next session |
| May 26 ~18:25 (this session) | Agent 1 (ruflo-core:coder) executed pre-flight on branch `p3-claude-viz` (77b33e9): restored `data/` symlink, `brain_viz.py` `label`→`id` (NTS mask 772 voxels, was 0), `llm.py` switched to `p_value`/`p_uncorr`. API key exported, smoke test 19/19 green, streamlit launched. Significance-flag fix still pending; Agents 2–4 queued. |
| May 26 ~18:30 (wrap-up) | Wrote `subagents_plan.md` — self-contained launch sheet for the remaining 6 agents (handfix + Agents 2/3/4 parallel + 5 verify + 6 phase3-4 + 7 merge). Each section is a paste-ready prompt with verification + commit message. |
| May 26 ~18:35 | Agent 4 (ruflo-core:coder) landed Block C on `p3-claude-viz` (50fe81e): `DEMO.md` 26 lines from P3_PLAN §7 template + `demo_cache/{,screenshots/}.gitkeep`. [SURPRISING_REGION_TBD] placeholder preserved for Agent 6. |
| May 26 ~18:38 (this session) | Significance handfix (96d9688): `significant_corrected` → `significant_uncorrected` in analysis.py + app.py. Bonus: fixed pandas 3.x `Styler.applymap` removal → `.map` so Ranking tab no longer errors on import. Agent 2 reported already running in user's other terminal → not double-launched here. |
