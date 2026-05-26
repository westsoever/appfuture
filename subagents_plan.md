# P3 Subagent Launch Plan

Self-contained launch sheet for the remaining P3 work. Each section is a ready-to-paste prompt for a single subagent. Launch order at the bottom.

**Branch:** `p3-claude-viz` (already created; Agent 1 landed as commit `77b33e9`)
**Working dir:** `/Users/lyo/aiw/appfuture`
**Required reading for every agent:** `P3_PLAN.md`, `CLAUDE.md`

---

## Pre-flight checklist (state at start of next session)

Verify before launching any agent:

```bash
cd /Users/lyo/aiw/appfuture
git branch --show-current          # → p3-claude-viz
git log --oneline -1               # → 77b33e9 P3 pre-flight: fix atlas id column...
ls data/atlas_hierarchy.csv        # symlink exists
echo $ANTHROPIC_API_KEY            # non-empty
conda activate explainable-brains
python smoke_test.py               # → 19/19 green
```

If `$ANTHROPIC_API_KEY` is empty, export it first or persist it (see Blockers).

---

## Outstanding pre-block fix (do before Agent 2)

`significant_corrected` is all-zero. Replace in:
- `analysis.py:21,23`
- `app.py:37,53`

```bash
grep -n significant_corrected analysis.py app.py
# manually swap to significant_uncorrected, keep semantics (== 1 / .astype(bool))
streamlit run app.py    # confirm volcano + ranking still render
git add analysis.py app.py
git commit -m "P3: switch significance filter to uncorrected (corrected all-zero)"
```

This can be done by hand or as a tiny agent — either way it must land on `p3-claude-viz` before Block A.

---

## Agent 2 — Block A: `llm.py` extensions

```
subagent_type: ruflo-core:coder
description: P3 Block A — add explain_top_findings + cache explain_region

Working dir: /Users/lyo/aiw/appfuture
Branch: p3-claude-viz (verify with `git branch --show-current`)
Read FIRST: P3_PLAN.md §3, §4, §5. CLAUDE.md module map.

Current llm.py already has explain_region using p_value/p_uncorr (Agent 1 fixed
this). Do NOT rewrite — extend.

Tasks:
1. Wrap explain_region with an internal @st.cache_data(show_spinner=False) helper
   keyed on (acronym, region_name, log2fc, p_uncorr, mean_A, mean_B). Pattern in
   P3_PLAN.md §5 A.1.
2. Add explain_top_findings(top_df) per §5 A.2 using prompt caching via
   cache_control: {"type": "ephemeral"} on the LARGE_CONTEXT block.
   - Use `p_value` (NOT p_uncorrected — column doesn't exist).
   - max_tokens=400, model="claude-opus-4-7".
3. Keep `anthropic.Anthropic()` (reads env). NO temperature=0. NO
   client.completions.create. NO claude-3 model IDs.

Verification:
- python -c "from data_loader import load_stats; from llm import explain_region; r=load_stats().iloc[0]; print(len(explain_region(r)))"
  → ≥50, no traceback.
- python -c "from data_loader import load_stats; from analysis import rank_regions; from llm import explain_top_findings; print(explain_top_findings(rank_regions(load_stats()).head(10))[:120])"
  → real text, no traceback.
- grep -n 'client.completions' llm.py  → empty
- grep -n 'claude-3' llm.py            → empty
- grep -n 'p_uncorrected' llm.py       → empty (use p_value)

Commit on p3-claude-viz: "P3-A: cached explain_region + explain_top_findings prompt cache"
Report: commit sha, output char lengths, any anti-pattern grep that wasn't empty.
```

---

## Agent 3 — Block B: `brain_viz.py` extensions (parallel with Agent 2)

```
subagent_type: ruflo-core:coder
description: P3 Block B — st.cache_resource + render_overlay

Working dir: /Users/lyo/aiw/appfuture
Branch: p3-claude-viz
Read FIRST: P3_PLAN.md §3, §4, §6.

Current brain_viz.py uses module-level _cache dict and the `id` lookup (Agent 1
fixed `label`→`id`). Refactor to Streamlit caching + add overlay helper.

Tasks:
1. Replace `_cache: dict = {}` + `_load(path)` with:
     @st.cache_resource
     def _load_volumes():
         anatomy = sitk.GetArrayFromImage(sitk.ReadImage("data/anatomy.nii.gz"))
         regions = sitk.GetArrayFromImage(sitk.ReadImage("data/regions.nii.gz"))
         diff    = sitk.GetArrayFromImage(sitk.ReadImage("data/diff_map.nii.gz"))
         return anatomy, regions, diff
2. Wrap get_slice with @st.cache_data(show_spinner=False). Keep argmax-of-counts
   centroid logic (it's slightly better than mean centroid for thin regions).
3. Return None (not the half-populated dict) when acronym missing OR mask empty.
   App code must handle None.
4. Add render_overlay(slice_dict) per §6 B.2 — matplotlib RdBu_r, vmin=-3,
   vmax=3, mask overlay via np.ma.masked_where, alpha=0.5, ax.axis("off"),
   figsize=(5,4). Return fig.

Anti-patterns to avoid (§4):
- nib.get_data()  (we use SimpleITK already — keep it)
- Streamlit imports inside analysis.py (don't add any)
- @st.cache_data on volume loader (it's @st.cache_resource)

Verification:
- python -c "from brain_viz import get_slice; [print(a, (s:=get_slice(a)) is not None and s['mask'].sum()) for a in ['NTS','ARH','LHA']]"
  → all three: True with mask voxel count > 0.
- python -c "from brain_viz import get_slice, render_overlay; import matplotlib; matplotlib.use('Agg'); render_overlay(get_slice('NTS'))"
  → no error.
- grep -n '\.get_data()' brain_viz.py  → empty.

Commit: "P3-B: st.cache_resource volumes + render_overlay helper"
Report: voxel counts for NTS/ARH/LHA, commit sha.
```

---

## Agent 4 — Block C: `DEMO.md` skeleton (parallel with Agents 2, 3)

```
subagent_type: ruflo-core:coder
description: P3 Block C — write DEMO.md skeleton

Working dir: /Users/lyo/aiw/appfuture
Branch: p3-claude-viz
Read FIRST: P3_PLAN.md §7.

Tasks:
1. Create DEMO.md using the template in P3_PLAN.md §7 verbatim. Keep the
   [SURPRISING_REGION_TBD — fill in during Phase 3] placeholder as-is — Agent 6
   fills it once it has seen the real data.
2. Create directories with .gitkeep:
     demo_cache/.gitkeep
     demo_cache/screenshots/.gitkeep

No code edits. No app.py changes.

Verification:
- test -f DEMO.md && wc -l DEMO.md         (≥ 30 lines)
- test -f demo_cache/.gitkeep
- test -d demo_cache/screenshots

Commit: "P3-C: demo script skeleton + cache dirs"
Report: file size, line count.
```

---

## Agent 5 — Verification & anti-pattern sweep

Run AFTER Agents 2, 3, 4 have all committed. Do not commit fixes — report only.

```
subagent_type: ruflo-core:reviewer
description: P3 §9 integration checklist + anti-pattern grep

Working dir: /Users/lyo/aiw/appfuture
Branch: p3-claude-viz
Read FIRST: P3_PLAN.md §4 (anti-patterns), §9 (integration checklist).

Run every check below, mark PASS/FAIL, and for each FAIL give the exact fix.

A. Functional checks
   1. python -c "from llm import explain_region; from data_loader import load_stats; print(len(explain_region(load_stats().iloc[0])) > 50)"  → True
   2. python -c "from brain_viz import get_slice; r=get_slice('NTS'); print(r is not None and r['mask'].sum() > 0)"  → True
   3. python -c "from data_loader import load_stats; from analysis import rank_regions; from llm import explain_top_findings; print(len(explain_top_findings(rank_regions(load_stats()).head(10))) > 100)"  → True
   4. python smoke_test.py  → exit 0

B. Anti-pattern greps (must all be empty)
   1. grep -rn "client.completions.create" llm.py
   2. grep -rn "response.completion" llm.py
   3. grep -rn "\.get_data()" llm.py brain_viz.py
   4. grep -rn "iloc\[0\]\[\"label\"\]" brain_viz.py
   5. grep -rn "significant_corrected" analysis.py app.py
   6. grep -rn "claude-3" llm.py
   7. grep -rn "p_uncorrected" llm.py        (column doesn't exist; should be p_value)
   8. grep -rn "temperature=0" llm.py

C. Code quality
   - llm.py: cache_control ephemeral present in explain_top_findings?
   - llm.py: explain_region wrapped in @st.cache_data (directly or via helper)?
   - brain_viz.py: @st.cache_resource on volume loader, @st.cache_data on get_slice?
   - brain_viz.py: returns None on missing region / empty mask?
   - DEMO.md: [SURPRISING_REGION_TBD] still a placeholder (will be filled by Agent 6)?

D. Files DEMO.md exists, demo_cache/ dir exists.

Report: structured PASS/FAIL list with remediations. DO NOT auto-fix.
```

---

## Agent 6 — Phase 3/4: surprising region + summarize button + cache prewarm

Only launch AFTER Agent 5 reports all PASS (or all FAILs resolved).

```
subagent_type: ruflo-core:coder
description: P3 Phase 3+4 — surprising region, summarize button, prewarm cache

Working dir: /Users/lyo/aiw/appfuture
Branch: p3-claude-viz
Read FIRST: P3_PLAN.md §7 Phase 3, Phase 4, Phase 5.

Phase 3 — pick surprising region:
1. python -c "from data_loader import load_stats; from analysis import rank_regions; df = rank_regions(load_stats()); print(df.head(30)[['acronym','region_name','log2_fold_change','p_value','significant_uncorrected']].to_string())"
2. Pick a region that:
   - Has large |log2_fold_change|
   - significant_uncorrected == 1
   - is NOT in {NTS, ARC, ARH, PVN, LHA, NAc, AP, DMV}  (obvious satiety/reward)
   - Has a plausible 1-sentence biological story (look up Allen Brain Atlas /
     Wikipedia if unsure)
3. Edit DEMO.md: replace [SURPRISING_REGION_TBD — fill in during Phase 3] with
   the acronym + region name + your 1-sentence story.

Phase 4 — Auto-summarize button:
1. Edit app.py Volcano tab. Add:
     if st.button("Auto-summarize top findings"):
         top10 = rank_regions(load_stats()).head(10)
         with st.spinner("Claude is reading the data…"):
             st.write(explain_top_findings(top10))
   (Adapt to existing imports / tab layout; do not break other tabs.)
2. Verify: `python -c "import app"` — no error.
3. If possible, `streamlit run app.py`, click the button once, confirm output.

Phase 5 — Prewarm demo_cache:
1. Write a one-shot script (or inline python -c) that, for each of NTS, ARH, LHA,
   plus the top 2 by |log2FC| from rank_regions, calls explain_region(row) and
   writes the text to demo_cache/<ACRONYM>.txt.
2. Verify: ls demo_cache/*.txt → 5 files, each non-empty.

Commit: "P3 Phase 3-4: surprising region picked, summarize button, demo cache prewarm"
Report: region chosen + 1-line rationale, app.py button location, list of cache files.
```

---

## Agent 7 — Merge `p3-claude-viz` → `main`

```
subagent_type: ruflo-core:coder
description: P3 merge gate

Working dir: /Users/lyo/aiw/appfuture
Pre-conditions:
  - Agent 5 final pass = all PASS
  - Agent 6 complete

Tasks:
1. git checkout p3-claude-viz
2. Re-run the §9 integration checklist (full grep + python -c suite from
   Agent 5 Section A + B). If any fail, STOP and report.
3. git checkout main
4. git pull --rebase  (skip if no remote configured — `git remote -v` empty)
5. git merge --no-ff p3-claude-viz -m "Merge P3: Claude explanations + brain viz + demo"
6. git log --oneline -5
7. git push  (only if remote exists)

Report: merge commit sha, files changed, any conflicts.
```

---

## Launch order summary

```
[done] Agent 1   — preflight (commit 77b33e9)
[next] handfix  — significant_corrected → significant_uncorrected
       Agent 2 ∥ Agent 3 ∥ Agent 4   (parallel)
       Agent 5   — verification gate
       Agent 6   — phase 3+4 (only if Agent 5 PASS)
       Agent 7   — merge to main
```

Total expected wall time after handfix: ~45–60 min of real work, parallelized.
