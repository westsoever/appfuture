import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

_client = anthropic.Anthropic()


@st.cache_data(show_spinner=False)
def _explain_cached(acronym, region_name, log2fc, p_uncorr, mean_a, mean_b):
    direction = "higher" if log2fc > 0 else "lower"
    prompt = (
        f"You are explaining a neuroscience finding to a clinician or drug developer "
        f"who is not a brain expert. Be concrete, vivid, and scientifically accurate. "
        f"No jargon without explanation.\n\n"
        f"Data: In a mouse c-Fos activity study, mice treated with Semaglutide (GLP-1 "
        f"agonist, the active ingredient in Ozempic) showed {direction} neural activity "
        f"in the brain region '{region_name}' ({acronym}) compared to "
        f"vehicle-treated controls. "
        f"Effect size: log₂ fold change = {log2fc:.2f}. "
        f"Statistical confidence: uncorrected p = {p_uncorr:.4f}. "
        f"Mean activity: {mean_a:.1f} cells/mm³ (Semaglutide) vs "
        f"{mean_b:.1f} cells/mm³ (Vehicle).\n\n"
        f"Write exactly 3 sentences:\n"
        f"1. What does {region_name} normally do in the brain?\n"
        f"2. What does this activity change suggest about how Semaglutide works?\n"
        f"3. Why might this matter for treating obesity, addiction, or brain health?\n\n"
        f"Be specific. If this region has known links to appetite, reward, or metabolism, say so."
    )
    response = _client.messages.create(
        model="claude-opus-4-7",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def explain_region(row) -> str:
    """Call Claude to explain a brain region's activation difference in plain English."""
    return _explain_cached(
        row["acronym"],
        row["region_name"],
        float(row["log2_fold_change"]),
        float(row["p_value"]),
        float(row["mean_A"]),
        float(row["mean_B"]),
    )


def explain_top_findings(top_df) -> str:
    """Summarize the top-ranked findings in 4 sentences. Uses prompt caching on the
    LARGE_CONTEXT block so repeated calls (e.g. button mashing during demo) are cheap."""
    rows_text = "\n".join(
        f"- {r['acronym']} ({r['region_name']}): "
        f"log2FC={r['log2_fold_change']:+.2f}, p_uncorr={r['p_value']:.3g}, "
        f"mean Sema={r['mean_A']:.1f} vs Vehicle={r['mean_B']:.1f}"
        for _, r in top_df.iterrows()
    )
    context = (
        "Study: Semaglutide (Ozempic, GLP-1 agonist) vs Vehicle, c-Fos activity mapping "
        "in mouse brain, 6 animals per group, ~459 lowest-level regions. "
        "Top findings by absolute log2 fold-change "
        "(log2FC > 0 ⇒ higher in Semaglutide; < 0 ⇒ higher in Vehicle):\n"
        f"{rows_text}"
    )
    question = (
        "Summarize this study in 4 sentences for a hackathon judge. "
        "Lead with the strongest biological story, name 2-3 specific regions, "
        "and end with what this suggests about Semaglutide's mechanism of action."
    )
    response = _client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": context,
                 "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": question},
            ],
        }],
    )
    return response.content[0].text
