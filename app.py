import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from data_loader import load_stats, load_quant_long
from analysis import rank_regions, volcano_data
from brain_viz import get_slice
from llm import explain_region

st.set_page_config(page_title="Explainable Brains", layout="wide")
st.title("Explainable Brains — Semaglutide vs Vehicle")

stats = load_stats()
ranked = rank_regions(stats)

tab1, tab2, tab3 = st.tabs(["Volcano Plot", "Region Ranking", "Region Deep Dive"])

# ── Tab 1: Volcano ────────────────────────────────────────────────────────────
with tab1:
    vdf = volcano_data(stats)
    color_map = {"corrected": "#e41a1c", "uncorrected": "#ff7f00", "ns": "#aaaaaa"}
    fig = px.scatter(
        vdf,
        x="log2_fold_change",
        y="neg_log10_p",
        color="significance",
        color_discrete_map=color_map,
        hover_data=["region_name", "acronym", "p_corrected"],
        labels={"log2_fold_change": "log₂ fold change (Sema / Vehicle)",
                "neg_log10_p": "−log₁₀(p corrected)"},
        title="All brain regions — Semaglutide vs Vehicle",
    )
    fig.add_vline(x=0, line_dash="dash", line_color="gray")

    # Label top-5 hits by effect size
    top5 = (vdf[vdf["significant_corrected"] == True]
            .assign(abs_fc=lambda d: d["log2_fold_change"].abs())
            .nlargest(5, "abs_fc"))
    for _, r in top5.iterrows():
        fig.add_annotation(
            x=r["log2_fold_change"], y=r["neg_log10_p"],
            text=r["acronym"], showarrow=True, arrowhead=2,
            arrowsize=0.8, ax=20, ay=-25, font=dict(size=11, color="#222"),
        )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("Red = statistically significant (corrected) · Orange = nominally significant · Top-5 hits labelled")

# ── Tab 2: Ranking table ──────────────────────────────────────────────────────
with tab2:
    sig_only = st.toggle("Show significant (corrected) only", value=True)
    df = ranked[ranked["significant_corrected"] == True] if sig_only else ranked
    display = df[["acronym", "region_name", "log2_fold_change", "p_corrected",
                  "mean_A", "mean_B", "n_A_eff", "n_B_eff"]].copy()
    display.columns = ["Acronym", "Region", "log₂FC (Sema/Veh)", "p (corrected)",
                       "Mean Sema", "Mean Veh", "n Sema", "n Veh"]
    st.dataframe(
        display.reset_index(drop=True).style.applymap(
            lambda v: "color: #d6604d; font-weight:bold" if isinstance(v, float) and v > 0 else
                      ("color: #4393c3; font-weight:bold" if isinstance(v, float) and v < 0 else ""),
            subset=["log₂FC (Sema/Veh)"],
        ),
        use_container_width=True,
        height=500,
    )
    st.caption("Red = higher in Semaglutide · Blue = higher in Vehicle")

# ── Tab 3: Deep dive ──────────────────────────────────────────────────────────
with tab3:
    region_options = ranked["acronym"].tolist()
    selected = st.selectbox("Select brain region", region_options)

    row = stats[stats["acronym"] == selected].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{row['region_name']} ({selected})")
        quant = load_quant_long()
        region_data = quant[quant["region"] == selected]
        if not region_data.empty:
            fig2 = px.violin(
                region_data,
                x="group_nr",
                y="density",
                box=True,
                points="all",
                color="group_nr",
                color_discrete_map={"G001": "#4393c3", "G002": "#d6604d"},
                labels={"group_nr": "Group", "density": "c-Fos density (cells/mm³)"},
                title=f"{selected} — per-animal density",
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No per-animal data for this region.")

    with col2:
        st.subheader("Brain slice")
        try:
            slices = get_slice(selected)
            fig3 = go.Figure()
            fig3.add_trace(go.Heatmap(z=slices["anatomy"], colorscale="gray", showscale=False))
            fig3.add_trace(go.Heatmap(z=slices["diff"], colorscale="RdBu_r",
                                      opacity=0.6, showscale=True,
                                      colorbar=dict(title="Diff")))
            if slices["mask"] is not None:
                mask_overlay = np.where(slices["mask"], 1.0, np.nan)
                fig3.add_trace(go.Heatmap(z=mask_overlay, colorscale=[[0, "yellow"], [1, "yellow"]],
                                          opacity=0.4, showscale=False))
            fig3.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig3, use_container_width=True)
        except FileNotFoundError:
            st.warning("NIfTI files not downloaded yet. Run `python download_data.py`.")

    st.divider()
    if st.button("Explain this region (Claude)"):
        with st.spinner("Asking Claude..."):
            explanation = explain_region(row.to_dict())
        st.info(explanation)
