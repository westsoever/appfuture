import anthropic
import streamlit as st


@st.cache_data(show_spinner=False)
def explain_region(region_name, acronym, log2fc, p_value, mean_a, mean_b):
    client = anthropic.Anthropic()
    prompt = f"""Brain region: {region_name} ({acronym})
In a c-Fos mouse study, Semaglutide-treated mice vs Vehicle control:
- Log2 fold change: {log2fc:.2f} (positive = higher neuronal activity in Semaglutide mice)
- Corrected p-value: {p_value:.4f}
- Mean c-Fos density: Vehicle = {mean_a:.1f} cells/mm³, Semaglutide = {mean_b:.1f} cells/mm³

In 3 sentences: what is this brain region's known role, and what might this activation difference mean for understanding how semaglutide (Ozempic) works in the brain? Be accessible to a non-expert."""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
