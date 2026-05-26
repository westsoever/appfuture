# Explainable Brains Hackathon — 3-Person, 3-Hour Plan
**Event:** May 26, 2026 · Copenhagen
**Team:** 3 people, parallel streams (P3 owns Claude + Viz + Demo)
**Build window:** 3 hours (T+0:00 → T+3:00)
**Challenge:** B — Guided brain data exploration

---

## Why Challenge B leverages Claude better than Challenge A

| Lever | Challenge A | Challenge B |
|---|---|---|
| Where Claude adds value | Behind-the-scenes (coreset code) | **In-product feature** (region NLP explanations seen by judges) |
| Pre-computed substrate | None — must implement diversity selection | All stats done (p_corrected, log2fc, significant_corrected) — Claude interprets, not computes |
| Claude Code parallelism | ML pipeline is sequential | 4 independent files (data / UI / NIfTI / Claude) — 4 Claude Code agents can build in parallel without merge conflict |
| Demo legibility | "We picked better patches" (abstract) | "Click a region → Claude explains what Ozempic does there" (concrete, 5 sec to grok) |
| Judging criteria 2 (Creativity) | Indirect | Direct hit — NLP explanation extension is named in the brief |
| Judging criteria 5 (Interpretability) | Hard | Trivial — that's literally the feature |

**Verdict:** B wins on Claude leverage. Claude is most useful where (a) the data already has signal and the bottleneck is *narration*, and (b) work can be split across files that don't touch each other.

---

## Phase 0 — Documentation Discovery (VERIFIED 2026-05-25)

Allowed APIs (cite when writing code):

| API | Exact form | Source |
|---|---|---|
| Anthropic SDK | `client.messages.create(model="claude-opus-4-7", max_tokens=N, messages=[...])` → `response.content[0].text` | docs.claude.com/en/api/messages |
| Anthropic streaming | `stream=True`, iterate events, check `event.type == "content_block_delta"` → `event.delta.text` | same |
| Anthropic caching | Add `"cache_control": {"type": "ephemeral"}` to text block | docs.claude.com/en/docs/build-with-claude/prompt-caching |
| Streamlit selection | `event = st.dataframe(df, on_select="rerun", selection_mode="single-row")`; read `event.selection.rows` (list of row indices) | docs.streamlit.io/develop/api-reference/data/st.dataframe |
| Streamlit cache | `@st.cache_data(show_spinner=False)` | docs.streamlit.io/.../caching-and-state/st.cache_data |
| plotly | `px.scatter(df, x=, y=, color=, hover_data=[...], color_discrete_map={...})` | plotly.com/python-api-reference/.../scatter |
| nibabel | `nib.load(path).get_fdata()` → `numpy.ndarray` | nipy.org/nibabel |

**Model ID `claude-opus-4-7` is current and canonical** — do not substitute `claude-3-opus-*` or older aliases.

**Anti-patterns — DO NOT:**
- Invent `client.complete(...)` (deprecated, doesn't exist on current SDK)
- Use `response.completion` (that was the old API)
- Pass `temperature` without setting it intentionally (default is fine for explanations)
- Use `st.experimental_data_editor` or `st.beta_dataframe` (removed)
- Call `nib.load(...).get_data()` (deprecated — use `get_fdata()`)
- Read `event.selection["rows"]` as a dict — it's an attribute object, use `event.selection.rows`

---

## Role assignment (do this in the first 5 minutes)

| Person | Stream | Owns files | Skills needed |
|---|---|---|---|
| **P1 — Data Lead** | Data loading + tabular analysis | `data_loader.py`, `analysis.py` | pandas |
| **P2 — UI Lead** | Streamlit app shell + 3 pages + state | `app.py`, `CLAUDE.md` | streamlit, plotly |
| **P3 — Claude + Viz + Demo Lead** | All Anthropic SDK code, NIfTI rendering, demo script | `llm.py`, `brain_viz.py`, `DEMO.md` | Anthropic SDK, nibabel, matplotlib, presenting |

**No shared-file conflicts.** P1 owns all of `analysis.py` (volcano + ranking + any helpers). P3 owns brain-slice extraction in `brain_viz.py` — kept out of `analysis.py` per current `CLAUDE.md` module map.

Each person runs **one dedicated Claude Code session** in their own branch (`p1-data`, `p2-ui`, `p3-claude-viz`). Merge to `main` at integration gates.

**P3 workload note:** combined role is heavy. Defaults if time-pressed:
- Skip anatomy reference panel (nice-to-have, not in demo script)
- Defer `chat_about_data` streaming — ship `explain_region` first, add chat in Phase 4 only if Phase 2 finishes clean
- P2 wires the chat sidebar UI shell; P3 only supplies the function

---

## Phase 1 — Kickoff & smoke (T+0:00 → T+0:20)

**Goal:** everyone on `main` with working env, data downloaded, API key live.

### Tasks
- [ ] **All:** `git pull`, `conda activate explainable-brains`, `python smoke_test.py`
- [ ] **All:** confirm `echo $ANTHROPIC_API_KEY` is set
- [ ] **P3:** claim hackathon API credits at the link, paste into team channel
- [ ] **P2:** confirm `streamlit run app.py` shows the skeleton
- [ ] **All:** create personal branches: `git checkout -b p<N>-<stream>` (P3 uses `p3-claude-viz`)
- [ ] **All:** open `CLAUDE.md` in your editor — Claude Code reads it as context

### Verification
- `streamlit run app.py` renders three pages with placeholder content
- `python -c "from llm_explain import explain_region; print(explain_region('NTS','NTS',0.8,0.001,100,180))"` returns text
- `python smoke_test.py` exits 0

### Anti-pattern guard
- Do NOT start coding features in Phase 1. If something is broken, fix it first — don't pile new code on a broken base.

---

## Phase 2 — Parallel build (T+0:20 → T+1:30, **70 min**)

Three independent streams. Each person directs their Claude Code session to copy patterns from the existing skeleton and extend.

### P1 — Data Lead

**Copy from:** `PLAN.md` §3b (`data_loader.py`), §3c (`analysis.py` first two functions).

**Tasks:**
1. Verify CSV column names match assumptions (re-run inspect snippet from PLAN.md Phase 2). **If a name is wrong, fix it in `data_loader.py` only — never hardcode renamed columns in `app.py`.**
2. Add `load_atlas()` returning `atlas_hierarchy.csv` as DataFrame, ensure it has columns `label`, `acronym`, `region_name` (rename if needed).
3. Implement `prepare_volcano(df)` and `get_region_ranking(df, only_significant=False)` exactly as in PLAN.md §3c — do not invent extra columns.
4. Add `get_top_regions(df, n=10)` returning top-n by `p_corrected`, lowest-level only — used by Claude prompt context.

**Verification:**
- `pytest -q tests/test_data.py` (P1 writes 3 asserts: `load_stats()` returns >50 rows; `prepare_volcano` adds `neg_log10_p`; `get_region_ranking(only_significant=True)` returns sorted by p_corrected ascending)
- `len(load_stats()) > 50`
- All `is_lowest_level == True` filter is applied — no parent regions leaking through

**Anti-pattern guard:**
- Do NOT call the Anthropic API from `data_loader.py` or `analysis.py`. Keep Claude isolated to `llm_explain.py` / `llm_chat.py`.
- Do NOT mutate input DataFrames in place — always `.copy()`.

### P2 — UI Lead

**Copy from:** `PLAN.md` §3e (`app.py`), §3a (`CLAUDE.md`).

**Tasks:**
1. Implement the 3-page layout exactly as PLAN.md §3e — keep names: "Volcano Plot", "Region Ranking", "Region Deep Dive".
2. Wire Page 2 row-click → Page 3 deep dive via `st.session_state["selected_acronym"]`. Use the verified Streamlit selection pattern:
   ```python
   event = st.dataframe(ranked, on_select="rerun", selection_mode="single-row")
   if event.selection.rows:
       st.session_state["selected_acronym"] = ranked.iloc[event.selection.rows[0]]["acronym"]
   ```
3. Add a top banner: "Semaglutide vs Vehicle · c-Fos mouse brain study · 400+ regions".
4. Add sidebar: number of regions, number significant (corrected), date stamp.
5. Update `CLAUDE.md` with any new entry points you create.

**Verification:**
- Click a row on Page 2 → Page 3 opens with the right acronym pre-selected
- Volcano hover shows region_name + acronym + p_corrected
- No console errors when switching pages

**Anti-pattern guard:**
- Do NOT compute statistics inside `app.py`. Call functions from `analysis.py`.
- Do NOT pass `use_container_width=True` to `st.plotly_chart` AND set explicit `width=` — pick one.

### P3 — Claude + Viz + Demo Lead

**Owns:** `llm.py`, `brain_viz.py`, `DEMO.md`. Single branch `p3-claude-viz`.

**Order tasks by demo-criticality. Ship 1–4 first; 5–7 are stretch.**

**Tasks (in priority order):**

**Block A — Claude wiring (T+0:20 → T+0:55, ~35 min)**
1. **`llm.py::explain_region(row)`** — takes a single stats DataFrame row, returns 3-sentence plain English. Use `client.messages.create(model="claude-opus-4-7", max_tokens=250, messages=[...])`, return `response.content[0].text`. Single module-level `client = anthropic.Anthropic()`. Wrap with `@st.cache_data(show_spinner=False)` — convert row to a tuple of primitives for cache key (DataFrames aren't hashable).
2. **`llm.py::explain_top_findings(top_df)`** — 4-sentence study summary over top-10 ranked regions. Use prompt caching: put the regions context block in `messages[0].content` with `"cache_control": {"type": "ephemeral"}`.

**Block B — Brain viz (T+0:55 → T+1:25, ~30 min)**
3. **`brain_viz.py::get_slice(acronym, axis=1)`** — already declared in `CLAUDE.md` module map. Loads `regions.nii.gz` + `diff_map.nii.gz` + `anatomy.nii.gz` via `@st.cache_resource` (large arrays). Look up integer label by acronym in `atlas_hierarchy.csv` (column is **`id`**, not `label` — see ACTIVE_PLAN data reality). Compute centroid Y-slice for that region's mask, return `{"anatomy": 2D, "diff": 2D, "mask": 2D}`. NIfTI axis 1 = coronal (Z, Y, X shape from SimpleITK).
4. **Matplotlib overlay** — small helper or inline in `app.py` Page 3: `imshow(diff, cmap="RdBu_r", vmin=-3, vmax=3)` with `imshow(mask, cmap="Greens", alpha=0.5)` on top. Crash-safe: if mask sum == 0 return `None`, UI shows "no mask available".

**Block C — Demo (T+1:25 → T+1:30, kick off; finish in Phase 4)**
5. **`DEMO.md` skeleton** — write the 2-min script outline now. Slots for: (a) NTS = "expected, brainstem satiety hub", (b) one *surprising* hit (acronym TBD after Phase 3 integration), (c) closing line "drop in any Vibraint study". Concrete acronym for (b) filled in during Phase 3 once you see real data.

**Stretch (Phase 4 if time):**
6. **`llm.py::chat_about_data(question, context_df)`** — free-text sidebar Q&A. Use `with client.messages.stream(...) as stream: for text in stream.text_stream: yield text`. Wire to `st.write_stream`. Do NOT `@st.cache_data` (free-text input).
7. **Anatomy reference panel** on Page 3 — second axes showing greyscale anatomy slice next to the diff slice.

**Verification:**
- `python -c "from llm import explain_region; from data_loader import load_stats; print(explain_region(load_stats().iloc[0]))"` → ≥50 chars, no exception
- Second identical call ≤50 ms (Streamlit cache hit)
- Page 3 → select "NTS" → slice renders ≤3 s, region mask visibly inside diff signal
- `DEMO.md` exists with timed script before T+1:30
- No API call sends NIfTI bytes or per-animal CSV — only aggregated stats

**Anti-pattern guard:**
- Do NOT use `client.completions.create` / `response.completion` — deprecated API.
- Do NOT hardcode API key — `anthropic.Anthropic()` reads `ANTHROPIC_API_KEY` env var.
- Do NOT use `nib.load(...).get_data()` — use `get_fdata()`.
- Do NOT reload NIfTI on every render — `@st.cache_resource`, not `@st.cache_data`.
- Do NOT pass `temperature=0` to "make it deterministic" then complain explanations are boring — leave default.
- Do NOT split into `llm_explain.py` + `llm_chat.py` — keep one `llm.py` (matches current `CLAUDE.md` module map).
- Do NOT add `get_brain_slice` into `analysis.py` — it lives in `brain_viz.py` per module map.

### Phase 2 integration gate (T+1:30, 5 min hard stop)

All 3 merge to `main`. With combined P3 role, `analysis.py` has only one owner (P1) → no cross-branch conflicts expected. P3's two files (`llm.py`, `brain_viz.py`) are independent of P1/P2 files.

**Definition of done for Phase 2:**
- `streamlit run app.py` works on `main`
- All 3 pages render with real data
- Volcano + ranking + slice + Claude explanation all functional individually

---

## Phase 3 — Integration + first end-to-end demo (T+1:30 → T+2:00, 30 min)

**Goal:** one person clicks through the full 2-minute demo flow on the merged app while the other three watch and call out bugs.

### Tasks
- [ ] **P3 drives the screen** (owns demo), P1/P2 take notes on what's broken
- [ ] **Walk the actual 2-minute demo flow** exactly as scripted in `DEMO.md`
- [ ] **List bugs in shared doc.** Triage into "must fix" / "nice to have"
- [ ] **Identify the surprising finding region** from the real data — P3 updates `DEMO.md` with the actual acronym + a sentence on why it's surprising
- [ ] **Each person fixes their own "must fix" bugs** — back to branches, merge in <20 min. If a Claude/viz bug AND a UI bug both land on P3 simultaneously, P2 picks up the UI side

### Verification
- One full uninterrupted run of the 2-minute demo on `main` with no manual recovery

### Anti-pattern guard
- DO NOT start new features in Phase 3. If it's not in the demo, don't build it.
- DO NOT refactor in Phase 3. If something is ugly but works, leave it.

---

## Phase 4 — Polish & Claude leverage expand (T+2:00 → T+2:30, 30 min)

**Goal:** push the Claude integration from "explain a region" to "this is a thinking partner". This is where the criteria-2 (creativity) and criteria-5 (interpretability) points come from.

### Tasks (parallel)
- [ ] **P3:** Add "Auto-summarize" button on Page 1 — calls `explain_top_findings(top10)`, shows 4-sentence study summary above the volcano. **Ship this first — easier than chat.**
- [ ] **P3:** Rehearse demo **out loud, with a timer**, at least twice. Cut anything past 1:50 (10s buffer). P2 sits next to P3 during rehearsal to catch UI snags live.
- [ ] **P3 (stretch, only if Auto-summarize lands ≤T+2:15):** Wire `chat_about_data` (streaming Q&A) into sidebar — **this is the differentiator**, but skip if running tight.
- [ ] **P2:** Build the chat sidebar UI shell (`st.text_input` + `st.write_stream` placeholder) so P3 can plug in `chat_about_data` with zero UI work if Block C lands.
- [ ] **P2:** Polish — header image/logo, page favicon, title doesn't wrap at 1920×1080.
- [ ] **P1:** Add "Download CSV" button on Page 2 (`st.download_button`) — cheap, scores on usability.
- [ ] **P1:** If P3 is overloaded, pre-cache 5 region explanations to `demo_cache/*.txt` (call `explain_region` from CLI for top-5 hits) as demo backup.

### Verification
- Free-text question in sidebar produces a streaming response with relevant content
- Auto-summary on Page 1 mentions the actual top regions, not generic neuroscience
- One full demo run completes in ≤1:55

### Anti-pattern guard
- DO NOT add features that need new data (e.g., region images from external sources) — too risky 30 min before demo.
- DO NOT ship a feature P4 hasn't rehearsed in the demo flow.

---

## Phase 5 — Demo lock + buffer (T+2:30 → T+3:00, 30 min)

**Goal:** zero-risk final state. App on `main` is locked. Code freeze.

### Tasks
- [ ] **All:** `git status` clean on `main`. Tag: `git tag demo-final && git push --tags`
- [ ] **P3:** present the demo to the team one final time
- [ ] **All:** identify the *single* most likely failure mode and mitigate (e.g., API rate limit → pre-cache 5 region explanations into `demo_cache/`; WiFi flaky → cache more aggressively)
- [ ] **P2:** open `app.py` in browser, leave the tab on Page 1, do NOT close it
- [ ] **P3:** confirm API key still works with a fresh call (credits not exhausted)
- [ ] **P3:** print `DEMO.md` to phone or paper

### Verification
- App is running, on Page 1, ready to demo
- A fresh `explain_region` call to Claude succeeds
- DEMO.md is accessible offline

### Anti-pattern guard
- NO code changes after T+2:45 except hotfix for a demo-blocker.
- If you find a bug in the last 15 minutes, write a workaround into the demo script ("I'll skip this view for time"), don't fix the code.

---

## Final verification — copy-paste at T+2:55

```bash
# Run from project root
python smoke_test.py                                   # data loads
python -c "from llm_explain import explain_region; print(len(explain_region('NTS','NTS',0.8,0.001,100,180)) > 50)"  # Claude works → True
grep -r "client.completions.create" .                  # should be empty (no deprecated API)
grep -r "get_data()" --include="*.py" .                # should be empty (no deprecated nibabel)
grep -r "claude-3-opus" .                              # should be empty (no stale model IDs)
git status                                             # clean
curl -sI http://localhost:8501 | head -1               # 200 OK (streamlit alive)
```

All five greps return nothing AND streamlit responds 200 → ship it.

---

## Risk register

| Risk | Probability | Mitigation |
|---|---|---|
| API credits exhausted mid-demo | Medium | Pre-cache 5 region explanations to disk in Phase 5; fall back to disk if API fails |
| WiFi drops during demo | Medium | All NIfTI files local; cached Claude responses local; only freeform chat needs internet |
| Merge conflict at T+1:30 | Very low | Each person owns disjoint files (P1=`analysis.py`+`data_loader.py`; P2=`app.py`+`CLAUDE.md`; P3=`llm.py`+`brain_viz.py`+`DEMO.md`) |
| P3 overloaded (combined role) | **Medium** | Block C (chat streaming) and anatomy panel are explicit stretch — drop without guilt. P2 absorbs chat sidebar shell; P1 absorbs demo-cache fallback |
| Streamlit selection event broken on a Streamlit version mismatch | Low | Phase 1 smoke test catches this; fallback = `st.selectbox` over acronym list |
| Column names in CSV ≠ assumed | Medium | Fixed in P1's first 10 minutes by re-running inspect snippet from PLAN.md Phase 2 |
| Demo runs over 2:00 | High | Phase 4 ends with two timed rehearsals; cut features, not narration |

---

## What "winning" looks like at the end

A judge sees:
1. A clean volcano plot, 400+ regions, with significance colored — 10 seconds
2. A click on NTS → brain slice + per-animal violin plot + Claude's 3-sentence explanation in plain English — 30 seconds
3. A free-text question typed in the sidebar — "what's the most surprising finding here?" — Claude streams a real answer using actual top-region data — 30 seconds
4. The framing: "This works for any Vibraint study — drop in the CSV"

That hits criteria 1 (usability), 2 (creativity — the chat), 3 (presentation), 4 (quality), 5 (interpretability — Claude narration), 6 (impact — Ozempic framing), 7 (scalability — "any Vibraint study").

7/7 criteria addressed in 2 minutes. That's the bet.
