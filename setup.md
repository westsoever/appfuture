<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# How to setup claude code for reading and inteprating ai brain data.

Scan git repositories and skills that are relevant for it, the provide a list of skills that I should implement to solve one of these problems:

[https://appliedfutures.io/hackathons/explainable-brains](https://appliedfutures.io/hackathons/explainable-brains)

Here’s a concrete way to think about this: you’re not “reading AI brain data” in the abstract — you’re wiring Claude Code into a small, opinionated toolkit that (1) loads Vibraint’s brain imaging data, (2) computes or uses embeddings, and (3) exposes a couple of interaction patterns that make this interpretable for a scientist in 2.5 hours of hacking.[^1]

Below is:

1. A quick mental model of the two challenges
2. How to set up Claude Code for this repo
3. A list of specific “skills” (in the Claude Code / MCP sense + Python utilities) that you could implement to solve **one** of the challenges

***

## 1. Understand the hackathon framing

From the brief:

- Data: real mouse brain imaging from a c‑Fos study comparing **Vehicle vs Semaglutide**.[^1]
- Repo: `explainable-brains-hackathon` starter repo with:
    - `CHALLENGE_A.md`, `CHALLENGE_B.md`
    - Python 3.11 env with `h5py`, `SimpleITK`, `plotly`, `dash`, `streamlit`, `scikit-learn`, `umap-learn`, Anthropic SDK
    - Bucket helpers for listing files, downloading, and reading patches/embeddings
    - Claude Code setup steps.[^1]

Two core problems:[^1]

- **Challenge A – Smart image data selection**
“Pick the most informative subset of mouse brain imaging patches and build an interface to inspect and validate the selection for AI model training.”
- **Challenge B – Guided brain data exploration**
“Build a dashboard that surfaces the brain regions where Vehicle vs Semaglutide differences are most pronounced or biologically interesting.”

Given your background, Challenge B is probably the best “product + data + storytelling” fit, but both are feasible once Claude Code can traverse the repo and call some utilities.[^1]

***

## 2. Setting up Claude Code for this project

You’ll get a GitHub starter repo with Claude Code instructions; at high level, your setup should look like:

1. **Fork and clone the repo**
    - Fork `github.com/explainable-brains/explainable-brains-hackathon` with your GitHub account, then `git clone` locally so Claude Code can index it.[^1]
2. **Create a dedicated Claude Code workspace**
    - Open the project folder in VS Code / your editor with Claude Code enabled.
    - Let Claude index the repo (it will read `CHALLENGE_A.md`, `CHALLENGE_B.md`, env files, and `bucket_access/` helpers).[^1]
3. **Follow the included “Claude Code install steps”**
    - Configure Claude Code with either:
        - The **free hackathon API credits** via Claude Console, or
        - Your own Claude subscription key.[^1]
    - Make sure Claude Code can:
        - Read and edit files
        - Run shell commands (e.g., `poetry run`, `pip install`, `streamlit run`)
        - Interact with Git (branching, commits)
4. **Set up the Python environment**
    - Use the provided environment (likely a `requirements.txt` or `pyproject.toml`) with `h5py`, `SimpleITK`, `plotly`, `dash` or `streamlit`, `scikit-learn`, `umap-learn`.[^1]
    - Ask Claude Code to generate a small smoke test that:
        - Imports the bucket helpers
        - Lists files in the S3 bucket
        - Reads a small subset of patches/embeddings and prints their shape.

Once this works, Claude Code essentially becomes your “co-pilot” to wire together data → embeddings → dashboard in very few manual keystrokes.

***

## 3. Concrete skills to implement (for one challenge)

Think of “skills” at two levels:

- **Python utilities** in the repo (functions / modules)
- **Claude Code usage patterns / MCP-like skills** (e.g., instructions in `CLAUDE.md` that tell Claude how to operate in this repo, or external MCP servers)

Below is a focused skill list for **Challenge B (Guided brain data exploration)** first, then a shorter list for Challenge A.

***

### Skills for Challenge B: Guided brain data exploration

The goal: a dashboard where a biologist can **interactively see where Vehicle vs Semaglutide differ**, ideally at region level and patch level, with clear explanations.[^1]

#### A. Data access \& abstraction skills

1. **`load_metadata_and_embeddings` utility**
    - Skill: Functions that, given the bucket path, return a tidy DataFrame with columns like:
        - `mouse_id`, `treatment` (Vehicle vs Semaglutide), `brain_region`, coordinates, embedding vector, maybe c-Fos intensity
    - Purpose: One line to get “analysis-ready” data for Claude Code to work with.
2. **Region hierarchy mapper**
    - Skill: A small module that maps region IDs or coordinates to named brain regions (e.g., hippocampus, cortex subregions), using whatever atlas info is provided in the challenge brief.
    - Purpose: Turn low-level coordinates into concepts that neuroscientists recognise.

#### B. Statistical \& ML analysis skills

3. **Treatment difference scoring per region**
    - Skill: A function `compute_region_differences(df)` that:
        - Aggregates embeddings or activation values per region per treatment
        - Computes effect size (e.g., Cohen’s d), p-values (e.g., t-test), or a simple ranking metric for differences between Vehicle and Semaglutide.
    - Purpose: Provide a ranked list of “interesting regions” to drive the dashboard.
4. **Dimensionality reduction \& clustering**
    - Skill: A utility that uses `umap-learn` + `scikit-learn` to:
        - Reduce high-dimensional patch embeddings to 2D/3D
        - Optionally cluster them (KMeans / DBSCAN)
        - Return embedding coordinates, cluster labels, and treatment labels for each patch.
    - Purpose: Enable an interactive scatter plot coloured by treatment, region, or cluster.

#### C. Visualization \& dashboard skills

5. **Region overview dashboard (Streamlit or Dash)**
    - Skill: A minimal app skeleton, e.g. `app_region_overview.py`, that:
        - Shows a sortable table of brain regions with “difference score” and simple metrics
        - Allows filtering (e.g., only show regions with strong Semaglutide response)
        - Shows a bar or violin plot of activation/embedding projection per region and treatment.
    - Purpose: A clear “entry point” for non-experts to see where Semaglutide seems to matter.
6. **Interactive embedding explorer**
    - Skill: A second view in the same app that:
        - Plots UMAP embeddings coloured by treatment, region, or cluster
        - Provides hover tooltips with metadata (mouse, region, treatment)
        - Lets the user filter to a specific region from the overview table and see only those points.
    - Purpose: Make the “latent space” interpretable and explorable.
7. **Brain-region map integration (even simple)**
    - Skill: Given the brief likely contains atlas info, a simple visual (even schematic) that:
        - Highlights top N regions with highest difference
        - Optionally shows them layered on a reference slice or a geometry approximation.
    - Purpose: Connect numeric differences to brain anatomy.

#### D. Interpretability \& explanation skills using Claude

8. **Natural-language explanation generator**
    - Skill: A small REST endpoint or script that:
        - Takes as input: region name, difference metrics, maybe a small summary of the plot state
        - Calls Claude (via Anthropic SDK already in the env) to produce:
            - A short, non-technical explanation like:
“In this region, Semaglutide-treated mice show higher c-Fos activation than Vehicle, which may suggest increased neuronal activity associated with X.”
    - Purpose: Turn charts into narrative summaries a clinician or non-ML person can understand.
9. **“Ask about a region” text box in the dashboard**
    - Skill: From the dashboard, let the user:
        - Select a region
        - Click “Explain this” to call the explanation generator
    - Optionally: let them type a freeform question (“What could this pattern mean biologically?”) that’s answered using Claude + an inline description of the data (without sending raw data).

#### E. Project / Claude Code workflow skills

10. **`CLAUDE.md` with repo-specific instructions**
    - Skill: Write a `CLAUDE.md` that tells Claude Code:
        - Where the main entry points are (e.g., `data_loading.py`, `analysis.py`, `dashboard/`)
        - How to run the app (`streamlit run dashboard/app.py`)
        - Naming conventions for functions and modules
    - Purpose: Make Claude Code more “agentic” in this repo so you can just say “add a filter to the region table for minimum effect size” and it edits the right files.
11. **Automated test and smoke-check scripts**
    - Skill: Very lightweight tests (e.g., `pytest` or even a `python scripts/smoke_test.py`) that ensure:
        - Data loading still works
        - The difference computation runs end-to-end
    - Purpose: Let Claude refactor safely during the 2.5h build without breaking core functionality.

***

### Skills for Challenge A: Smart image data selection

If you decide to focus on A instead, here are high-impact skills that pair nicely with Claude Code:

1. **Patch quality / artifact detection**
    - Functions that score patches by signal-to-noise, presence of artefacts, or basic QC flags using image stats or simple models.
2. **Redundancy and diversity selection**
    - Use embeddings to select a diverse but informative subset of patches (e.g., via clustering + sampling from each cluster, or coreset-like methods).
3. **Label-stratified sampling**
    - Ensure balance across Vehicle vs Semaglutide, mice, and regions so model training is not biased.
4. **Patch inspection interface**
    - A viewer where users can:
        - See raw patch images
        - See their metadata and selection scores
        - Accept/reject or tag patches, feeding back into selection.
5. **Claude-assisted rationale summaries**
    - Given a set of selected patches and some statistics, call Claude to generate a short explanation:
        - “This subset covers all major regions, balances treatments, and includes high-variance patches likely to be informative for training.”

***

## 4. Minimal concrete “first implementation” you could aim for

To keep this hackathon-proof and Claude Code–friendly, a realistic target for Challenge B would be:

- A **Streamlit app** with:
    - Page 1: Region table ranked by Vehicle vs Semaglutide difference, with a plot per region on click.
    - Page 2: UMAP scatter of embeddings, coloured by treatment and filterable by region.
    - “Explain this view” button that calls Claude via Anthropic SDK to generate 2–3 sentences of interpretation, shown in a sidebar.
- Under the hood:
    - `data_loading.py` with `load_data()` returning a tidy DataFrame
    - `analysis.py` with `compute_region_differences` and `compute_umap`
    - `dashboard/app.py` which wires it up
    - `CLAUDE.md` that orients Claude Code to these files
    - A short `README_DEV.md` that describes run commands.

This gives you something that looks like a **real product** and scores strongly on usability, interpretability, and impact, which are all explicit judging criteria.[^1]

***

If you describe your current comfort level with Streamlit/Dash, UMAP, and basic stats, a next step could be to pick **one challenge (A or B)** and then define the exact file structure and first function you want Claude Code to write; what feels like the most natural starting point for you?
<span style="display:none">[^10][^11][^12][^13][^14][^15][^2][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://appliedfutures.io/hackathons/explainable-brains

[^2]: https://www.linkedin.com/posts/jlangvad_the-brain-remains-largely-a-mystery-neurological-activity-7454749953064767489-sgql

[^3]: https://luma.com/aes5eyzk

[^4]: https://www.linkedin.com/posts/alicia-parra_explainable-brains-hackathon-brain-imaging-activity-7455181902623277056-C0GU

[^5]: https://appliedfutures.io/hackathons

[^6]: https://www.centreforbrainhealth.ca/news/hackathon-explores-the-use-of-artificial-intelligence-tools-for-brain-health-research/

[^7]: https://www.deeplearning.ai/courses/claude-code-a-highly-agentic-coding-assistant

[^8]: https://appliedfutures.io/impact-lab

[^9]: https://www.linkedin.com/posts/alljoined_introducing-alljoined-uncovering-thoughts-activity-7311409825496633345-S3N9

[^10]: https://www.anthropic.com/research/natural-language-autoencoders

[^11]: https://www.explainable-brains-hackathon.com

[^12]: https://github.com/explainable-brains

[^13]: https://code.claude.com/docs/en/overview

[^14]: https://aiforgood.itu.int/the-future-leaders-in-quantum-hackathon/

[^15]: https://www.instagram.com/reel/DOaiDgUgO5l/

