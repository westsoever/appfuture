# P3 — Claude + Viz + Demo Lead · Persistent Plan

> **Self-contained.** A fresh Claude Code session can read ONLY this file plus `CLAUDE.md` and execute the entire P3 stream. Other plan files are reference, not required.

**Branch:** `p3-claude-viz`
**Files owned:** `llm.py`, `brain_viz.py`, `DEMO.md`
**Build window:** ~70 min in Phase 2 (T+0:20 → T+1:30), then integration + demo work in Phases 3–5

---

## 1. Setup (do once, T+0:00 → T+0:20)

Pre-condition: the two `main`-level bugfixes are merged (see ACTIVE_PLAN.md "Up Next — on `main` BEFORE branching"). If they are not done, do them first, on `main`, then come back.

```bash
git checkout main && git pull
conda activate explainable-brains
python smoke_test.py           # must exit 0 before forking
echo $ANTHROPIC_API_KEY        # must be non-empty
git checkout -b p3-claude-viz
```

---

## 2. Data Reality (memorize — drives every implementation decision)

| Fact | Value | Implication |
|---|---|---|
| Stats rows | 1356 | Filter `is_lowest_level == True` → 459 regions |
| `significant_corrected` hits | **0** (p_corrected ∈ [0.43, 1.0]) | **Do NOT use this column.** Use `significant_uncorrected` for any "is significant" check |
| log2FC range | [−3.29, +2.77] | Centroid colormap at 0; `vmin=-3, vmax=3` for diff slices |
| Atlas label column | **`id`** (NOT `label`, NOT `region_id`) | When mapping acronym → integer voxel value, look up `id` |
| Atlas name column | **`name`** (NOT `region_name`) | Use `name` for human-readable region label |
| NIfTI shape | (268, 512, 369) — (Z, Y, X) from SimpleITK | Coronal slice = axis 1 (Y). `regions.nii.gz` voxel values = atlas `id` |
| Animals | 6×G001 (Vehicle), 6×G002 (Semaglutide) | `log2_fold_change > 0` ⇒ higher in Semaglutide |
| Data location | `data/` symlink → `vibraint/data/` | Just use `data/<file>` paths everywhere |

Files in `data/`:
- `cfos_statistics.csv` — one row per region (use this for explanations)
- `cfos_quantification.csv` — per-animal density (wide → long after `load_quant_long()`)
- `atlas_hierarchy.csv` — `id` ↔ `acronym` ↔ `name`
- `anatomy.nii.gz`, `regions.nii.gz`, `diff_map.nii.gz`, `cfos_G001.nii.gz`, `cfos_G002.nii.gz`

---

## 3. Allowed APIs (cite — do not invent)

### Anthropic SDK (`anthropic>=0.40`)
```python
import anthropic
client = anthropic.Anthropic()                          # reads ANTHROPIC_API_KEY

response = client.messages.create(
    model="claude-opus-4-7",                            # canonical, current
    max_tokens=250,
    messages=[{"role": "user", "content": "..."}],
)
text = response.content[0].text                         # NOT response.completion
```

**Prompt caching** (for `explain_top_findings` — the top-10 context block is reused):
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "text", "text": LARGE_CONTEXT,
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": QUESTION},
    ],
}]
```

**Streaming** (for stretch `chat_about_data`):
```python
with client.messages.stream(model="claude-opus-4-7", max_tokens=500,
                            messages=[...]) as stream:
    for text in stream.text_stream:
        yield text
```

Docs: docs.claude.com/en/api/messages, docs.claude.com/en/docs/build-with-claude/prompt-caching

### Streamlit
- `@st.cache_data(show_spinner=False)` — deterministic inputs (explain_region with same row → cached)
- `@st.cache_resource` — large objects (nibabel image handles, numpy arrays)
- `st.write_stream(generator)` — pipe streaming generator into the page

### nibabel
```python
import nibabel as nib
img = nib.load("data/regions.nii.gz")
arr = img.get_fdata()                                   # NOT .get_data() (deprecated)
```

### matplotlib
```python
fig, ax = plt.subplots()
ax.imshow(diff_slice, cmap="RdBu_r", vmin=-3, vmax=3)
ax.imshow(np.ma.masked_where(mask_slice == 0, mask_slice),
          cmap="Greens", alpha=0.5)
ax.axis("off")
st.pyplot(fig)
```

---

## 4. Anti-patterns (DO NOT)

- ❌ `client.completions.create(...)` or `response.completion` — old API, deprecated
- ❌ `nib.load(...).get_data()` — deprecated, use `get_fdata()`
- ❌ Hardcoding API key in source — use `anthropic.Anthropic()`, reads env
- ❌ Splitting into `llm_explain.py` + `llm_chat.py` — keep single `llm.py` (matches `CLAUDE.md` module map)
- ❌ Putting `get_brain_slice` in `analysis.py` — it lives in `brain_viz.py`
- ❌ Reloading NIfTI on every render — `@st.cache_resource`, not `@st.cache_data`
- ❌ Filtering on `significant_corrected` — all zero, use `significant_uncorrected`
- ❌ Looking up acronym → voxel via `label` or `region_id` column — it's `id`
- ❌ Sending raw NIfTI bytes / per-animal CSV to the API — only aggregated stats
- ❌ `temperature=0` "for determinism" then complaining outputs are dry — leave default
- ❌ `claude-3-opus-*` model IDs — use `claude-opus-4-7`

---

## 5. Block A — Claude wiring (T+0:20 → T+0:55, ~35 min) · `llm.py`

Current `llm.py` already has a skeleton — extend, don't rewrite.

### A.1 — `explain_region(row)` (already declared in `CLAUDE.md` module map)

Signature: takes a single Series/dict-like row from `load_stats()`. Returns 3-sentence string.

```python
import anthropic
import streamlit as st

_client = anthropic.Anthropic()

@st.cache_data(show_spinner=False)
def _explain_cached(acronym, name, log2fc, p_uncorr, mean_a, mean_b):
    direction = "higher in Semaglutide" if log2fc > 0 else "higher in Vehicle"
    prompt = (
        f"Region: {name} ({acronym}). "
        f"c-Fos signal is {direction} (log2FC={log2fc:.2f}, "
        f"uncorrected p={p_uncorr:.3g}). "
        f"Mean activity — Vehicle group: {mean_a:.1f}, Semaglutide group: {mean_b:.1f}.\n\n"
        "Explain in 3 plain-English sentences for a non-neuroscientist: "
        "what this region does, what the change might mean for appetite/satiety, "
        "and one caveat about interpreting a single c-Fos study."
    )
    resp = _client.messages.create(
        model="claude-opus-4-7",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text

def explain_region(row):
    return _explain_cached(
        row["acronym"], row["region_name"] if "region_name" in row else row["name"],
        float(row["log2_fold_change"]), float(row["p_uncorrected"]),
        float(row["mean_A"]), float(row["mean_B"]),
    )
```

**Note on column name:** if `data_loader.load_stats()` already renames `name` → `region_name`, use `region_name`. Otherwise use `name`. Check `data_loader.py` once before writing this — don't guess.

### A.2 — `explain_top_findings(top_df)`

4-sentence study summary. `top_df` = output of `analysis.rank_regions(...).head(10)`.

```python
def explain_top_findings(top_df):
    rows_text = "\n".join(
        f"- {r['acronym']} ({r['region_name']}): "
        f"log2FC={r['log2_fold_change']:+.2f}, p_uncorr={r['p_uncorrected']:.3g}"
        for _, r in top_df.iterrows()
    )
    context = (
        "Study: Semaglutide (Ozempic) vs Vehicle, c-Fos activity mapping in mouse brain, "
        "6 animals per group, ~459 lowest-level regions. Top 10 by absolute log2 fold-change:\n"
        f"{rows_text}"
    )
    resp = _client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": context,
                 "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text":
                    "Summarize this study in 4 sentences for a hackathon judge. "
                    "Lead with the strongest biological story, name 2-3 specific regions, "
                    "and end with what this suggests about Semaglutide's mechanism."},
            ],
        }],
    )
    return resp.content[0].text
```

### A.3 — Verification
```bash
python -c "from data_loader import load_stats; from llm import explain_region; print(explain_region(load_stats().iloc[0]))"
# expect ≥50 chars, no traceback
# run twice — second call should return in <50ms (cache hit)
```

---

## 6. Block B — Brain viz (T+0:55 → T+1:25, ~30 min) · `brain_viz.py`

Current `brain_viz.py` already has a skeleton. After the pre-branch bugfix, `match.iloc[0]["id"]` should be the lookup — confirm before extending.

### B.1 — `get_slice(acronym, axis=1)` (already in module map)

Returns `{"anatomy": 2D ndarray, "diff": 2D ndarray, "mask": 2D ndarray}` or `None` if region has no voxels.

```python
import numpy as np
import SimpleITK as sitk        # OR nibabel — match whatever data_loader uses
import streamlit as st
from data_loader import load_atlas      # or pd.read_csv if no helper

@st.cache_resource
def _load_volumes():
    anatomy = sitk.GetArrayFromImage(sitk.ReadImage("data/anatomy.nii.gz"))
    regions = sitk.GetArrayFromImage(sitk.ReadImage("data/regions.nii.gz"))
    diff    = sitk.GetArrayFromImage(sitk.ReadImage("data/diff_map.nii.gz"))
    return anatomy, regions, diff

@st.cache_data(show_spinner=False)
def get_slice(acronym, axis=1):
    anatomy, regions, diff = _load_volumes()
    atlas = load_atlas()
    match = atlas[atlas["acronym"] == acronym]
    if match.empty:
        return None
    region_id = int(match.iloc[0]["id"])              # `id`, NOT `label`
    mask_vol = (regions == region_id)
    if mask_vol.sum() == 0:
        return None
    # centroid index along chosen axis
    coords = np.argwhere(mask_vol)
    centroid_idx = int(np.round(coords[:, axis].mean()))
    sl = [slice(None)] * 3
    sl[axis] = centroid_idx
    sl = tuple(sl)
    return {
        "anatomy": anatomy[sl],
        "diff":    diff[sl],
        "mask":    mask_vol[sl].astype(np.uint8),
    }
```

### B.2 — Overlay helper (inline in `app.py` Page 3 is fine — coordinate with P2)

```python
def render_overlay(slice_dict):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(slice_dict["diff"], cmap="RdBu_r", vmin=-3, vmax=3)
    ax.imshow(np.ma.masked_where(slice_dict["mask"] == 0, slice_dict["mask"]),
              cmap="Greens", alpha=0.5)
    ax.axis("off")
    return fig
```

### B.3 — Verification
- Streamlit page 3 with acronym=`NTS` → slice renders in <3 s; mask overlay sits inside obvious negative (blue) diff signal (NTS = brainstem satiety hub, should be visibly active)
- Pick 2 more acronyms (e.g. `ARH`, `LHA`) — mask not zero, no exceptions

---

## 7. Block C — Demo (start T+1:25, finish T+2:30 over Phases 3–4) · `DEMO.md`

Phase 2 ends with **skeleton only**. The surprising region is filled in during Phase 3 once you see the real data.

### `DEMO.md` template — write this in Block C

```markdown
# Explainable Brains — 2-Minute Demo Script

## 0:00 — Setup (presenter says before clicking)
"Vibraint shared a real c-Fos study: Semaglutide — Ozempic — versus Vehicle, in mice. 12 animals, 459 brain regions. The data is here. The question is: what does Ozempic do to the brain, and can we see it in 2 minutes?"

## 0:15 — Volcano (Page 1)
Click Page 1. Point at the colored points.
"Each dot is a brain region. Right side: higher activity on Semaglutide. Left: higher on Vehicle. Color = uncorrected significance."
Click "Auto-summarize" → Claude streams a 4-sentence summary live.

## 0:45 — Ranking → Deep dive (Page 2 → Page 3)
Click Page 2. Click NTS row.
"NTS — nucleus of the solitary tract — brainstem satiety hub. We expect to see this. There it is, lit up."
Page 3 opens with NTS pre-selected. Show brain slice + violin.

## 1:15 — The surprising finding
Go back to Page 2. Click [SURPRISING_REGION_TBD — fill in during Phase 3].
"This one we did NOT expect. [one-sentence biological reason it's surprising]"
Click "Explain this region" → Claude streams 3 sentences.

## 1:50 — Close
"Volcano, ranking, brain slice, Claude narration. Drop in any Vibraint study CSV — same app, new biology, ten seconds."

## Backup plan
- API stalls → cached responses in `demo_cache/<acronym>.txt`. Read with `Path("demo_cache/NTS.txt").read_text()`.
- Streamlit dies → screenshots in `demo_cache/screenshots/`
```

### Phase 3 — fill in `[SURPRISING_REGION_TBD]`
You drive the screen. Walk the real data. Pick a region that:
- Has large `|log2_fold_change|`
- Is NOT in the obvious satiety/reward circuit (NTS, ARC/ARH, PVN, LHA, NAc)
- Has a biologically coherent one-sentence story (look it up — Allen Brain Atlas / Wikipedia is fine)

### Phase 4 — Auto-summarize button + rehearsal
- Wire `explain_top_findings(top10)` into a button on Page 1 (`st.button` → `st.write_stream` is fine even without true streaming; just call and `st.write`)
- Rehearse 2× with phone stopwatch. If you hit 2:00, cut narration not features

### Phase 5 — Lock
- Pre-cache 5 region explanations to `demo_cache/*.txt` (P1 can help)
- Print `DEMO.md` to phone

---

## 8. Stretch (only if everything above ships by T+2:15)

### Stretch 1 — `chat_about_data(question, context_df)` streaming

```python
def chat_about_data(question, context_df):
    context = "Study context: ...top regions...\n" + context_df.to_string()
    with _client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": context,
                 "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": question},
            ],
        }],
    ) as stream:
        for text in stream.text_stream:
            yield text
```
Wire into a sidebar `st.text_input` + `st.write_stream(chat_about_data(q, top10))`. **Do NOT `@st.cache_data` this.** P2 has the sidebar shell ready.

### Stretch 2 — Anatomy reference panel
Side-by-side: `slice_dict["anatomy"]` as greyscale on left, diff+mask overlay on right. Two-column layout via `st.columns(2)`.

---

## 9. Integration checklist (T+1:30 merge gate)

Before merging to `main`:
```bash
python -c "from llm import explain_region; from data_loader import load_stats; print(len(explain_region(load_stats().iloc[0])) > 50)"   # True
python -c "from brain_viz import get_slice; r = get_slice('NTS'); print(r is not None and r['mask'].sum() > 0)"                          # True
grep -n "client.completions.create" llm.py    # empty
grep -n "get_data()" brain_viz.py             # empty (must be get_fdata or SimpleITK)
grep -n 'significant_corrected' .             # only in CLAUDE.md as a "do not use" note
```

Then:
```bash
git add llm.py brain_viz.py DEMO.md
git commit -m "P3: explain_region, get_slice, demo script skeleton"
git checkout main && git pull --rebase
git merge --no-ff p3-claude-viz
git push
```

---

## 10. Quick reference — file/function map

| File | Function | Purpose |
|---|---|---|
| `llm.py` | `explain_region(row)` | 3-sentence region explanation, cached |
| `llm.py` | `explain_top_findings(top_df)` | 4-sentence study summary, prompt-cached |
| `llm.py` | `chat_about_data(q, df)` *(stretch)* | streaming free-text Q&A |
| `brain_viz.py` | `get_slice(acronym, axis=1)` | `{anatomy, diff, mask}` 2D arrays at region centroid |
| `brain_viz.py` | `render_overlay(slice_dict)` | matplotlib figure for Streamlit |
| `DEMO.md` | — | 2-min demo script, region picks, backup plan |
