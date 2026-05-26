import anthropic
from dotenv import load_dotenv

load_dotenv()


def explain_region(row) -> str:
    """Call Claude to explain a brain region's activation difference in plain English."""
    client = anthropic.Anthropic()
    direction = "higher" if row["log2_fold_change"] > 0 else "lower"
    p_uncorr = row["p_value"]
    prompt = (
        f"You are explaining a neuroscience finding to a clinician or drug developer "
        f"who is not a brain expert. Be concrete, vivid, and scientifically accurate. "
        f"No jargon without explanation.\n\n"
        f"Data: In a mouse c-Fos activity study, mice treated with Semaglutide (GLP-1 "
        f"agonist, the active ingredient in Ozempic) showed {direction} neural activity "
        f"in the brain region '{row['region_name']}' ({row['acronym']}) compared to "
        f"vehicle-treated controls. "
        f"Effect size: log₂ fold change = {row['log2_fold_change']:.2f}. "
        f"Statistical confidence: uncorrected p = {p_uncorr:.4f}. "
        f"Mean activity: {row['mean_A']:.1f} cells/mm³ (Semaglutide) vs "
        f"{row['mean_B']:.1f} cells/mm³ (Vehicle).\n\n"
        f"Write exactly 3 sentences:\n"
        f"1. What does {row['region_name']} normally do in the brain?\n"
        f"2. What does this activity change suggest about how Semaglutide works?\n"
        f"3. Why might this matter for treating obesity, addiction, or brain health?\n\n"
        f"Be specific. If this region has known links to appetite, reward, or metabolism, say so."
    )
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
