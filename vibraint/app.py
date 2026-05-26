import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from data_loader import load_stats, load_quantification, load_atlas
from analysis import prepare_volcano, get_region_ranking, get_brain_slice
from llm_explain import explain_region

st.set_page_config(
    page_title="Explainable Brains",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Explainable Brains")
st.caption("Where does Semaglutide (Ozempic) rewire the mouse brain?")

stats = load_stats()
quant = load_quantification()
atlas = load_atlas()

page = st.sidebar.radio(
    "View",
    ["Volcano Plot", "Region Ranking", "Region Deep Dive"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**G001** = Vehicle (control)  \n**G002** = Semaglutide (Ozempic)")
st.sidebar.markdown("c-Fos = recently active neurons  \n↑ density = more brain activity")

# ── Page 1: Volcano Plot ─────────────────────────────────────────────────────
if page == "Volcano Plot":
    st.header("All Brain Regions: Semaglutide vs Vehicle")
    st.markdown(
        "Each dot = one brain region. **Right** = more active in Semaglutide. "
        "**Up** = more statistically significant."
    )

    volcano_df = prepare_volcano(stats)

    color_map = {
        "significant (corrected)": "#e74c3c",
        "significant (uncorrected)": "#f39c12",
        "not significant": "#bdc3c7",
    }
    fig = px.scatter(
        volcano_df,
        x="log2_fold_change",
        y="neg_log10_p",
        color="significance",
        color_discrete_map=color_map,
        hover_data=["region_name", "acronym", "p_corrected", "mean_A", "mean_B"],
        labels={
            "log2_fold_change": "Log2 Fold Change (Semaglutide / Vehicle)",
            "neg_log10_p": "−log10(corrected p-value)",
        },
        height=600,
    )
    fig.add_vline(x=0, line_dash="dash", line_color="#7f8c8d", line_width=1)
    fig.add_hline(y=-np.log10(0.05), line_dash="dot", line_color="#e74c3c",
                  line_width=1, annotation_text="p=0.05 (corrected)")
    st.plotly_chart(fig, use_container_width=True)

    sig_count = (volcano_df["significant_corrected"] == True).sum()
    st.metric("Significantly different regions (corrected)", sig_count)

# ── Page 2: Region Ranking ───────────────────────────────────────────────────
elif page == "Region Ranking":
    st.header("Brain Regions Ranked by Statistical Significance")

    col1, col2 = st.columns([1, 3])
    with col1:
        only_sig = st.toggle("Only corrected-significant", value=True)
        direction = st.radio("Direction", ["All", "↑ Semaglutide higher", "↓ Vehicle higher"])

    ranked = get_region_ranking(stats, only_significant=only_sig)
    if direction == "↑ Semaglutide higher":
        ranked = ranked[ranked["log2_fold_change"] > 0]
    elif direction == "↓ Vehicle higher":
        ranked = ranked[ranked["log2_fold_change"] < 0]

    display_cols = ["region_name", "acronym", "log2_fold_change", "p_corrected",
                    "mean_A", "mean_B", "n_A_eff", "n_B_eff"]
    st.dataframe(
        ranked[display_cols].rename(columns={
            "region_name": "Region",
            "acronym": "Acronym",
            "log2_fold_change": "Log2FC",
            "p_corrected": "p (corrected)",
            "mean_A": "Mean Vehicle",
            "mean_B": "Mean Sema",
            "n_A_eff": "n Vehicle",
            "n_B_eff": "n Sema",
        }),
        use_container_width=True,
        height=500,
    )
    st.caption(f"{len(ranked)} regions shown")

# ── Page 3: Region Deep Dive ─────────────────────────────────────────────────
elif page == "Region Deep Dive":
    st.header("Region Deep Dive")

    sig_regions = get_region_ranking(stats, only_significant=True)
    all_regions = get_region_ranking(stats, only_significant=False)

    region_options = sig_regions["acronym"].tolist()
    selected_acronym = st.selectbox(
        "Select region (sorted by significance)",
        region_options,
        format_func=lambda a: f"{a} — {stats[stats['acronym']==a].iloc[0]['region_name']}",
    )

    row = stats[stats["acronym"] == selected_acronym].iloc[0]

    col_stats, col_plot = st.columns([1, 2])

    with col_stats:
        st.subheader(row["region_name"])
        st.metric("Acronym", row["acronym"])
        direction_label = "↑ Higher in Semaglutide" if row["log2_fold_change"] > 0 else "↓ Lower in Semaglutide"
        st.metric("Log2 Fold Change", f"{row['log2_fold_change']:.3f}", delta=direction_label,
                  delta_color="normal")
        st.metric("Corrected p-value", f"{row['p_corrected']:.4f}")
        st.metric("Mean density (Vehicle / Sema)",
                  f"{row['mean_A']:.0f} / {row['mean_B']:.0f} cells/mm³")
        st.metric("Effective n (Vehicle / Sema)",
                  f"{int(row['n_A_eff'])} / {int(row['n_B_eff'])}")

    with col_plot:
        region_quant = quant[quant["region"] == selected_acronym].dropna(subset=["density"])
        if len(region_quant) > 0:
            fig2 = px.violin(
                region_quant,
                x="group", y="density",
                box=True, points="all",
                color="group",
                color_discrete_map={"Vehicle": "#3498db", "Semaglutide": "#e74c3c"},
                title=f"c-Fos density: {row['region_name']}",
                labels={"density": "c-Fos density (cells/mm³)", "group": ""},
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No per-animal data available for this region.")

    # Brain slice
    st.subheader("Brain location")
    axis_choice = st.radio("Slice orientation", ["coronal", "axial", "sagittal"], horizontal=True)
    with st.spinner("Loading brain slice..."):
        slice_data = get_brain_slice(selected_acronym, atlas, axis=axis_choice)

    if slice_data:
        fig3, axes = plt.subplots(1, 2, figsize=(10, 4))
        vmax = np.percentile(np.abs(slice_data["diff_slice"]), 99)
        axes[0].imshow(slice_data["anatomy_slice"], origin="lower", cmap="gray")
        axes[0].imshow(
            np.where(slice_data["mask_slice"], slice_data["diff_slice"], np.nan),
            origin="lower", cmap="RdBu_r", vmin=-vmax, vmax=vmax, alpha=0.7,
        )
        axes[0].set_title(f"{selected_acronym} — difference map overlay")
        axes[0].axis("off")

        axes[1].imshow(slice_data["anatomy_slice"], origin="lower", cmap="gray")
        mask_rgba = np.zeros((*slice_data["mask_slice"].shape, 4))
        mask_rgba[slice_data["mask_slice"]] = [0.2, 0.8, 0.2, 0.6]
        axes[1].imshow(mask_rgba, origin="lower")
        axes[1].set_title(f"{selected_acronym} — region mask")
        axes[1].axis("off")

        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
    else:
        st.info("Region not found in atlas or no voxels detected.")

    # Claude explanation
    st.subheader("What does this mean?")
    if st.button("Explain this region with Claude 🤖", type="primary"):
        with st.spinner("Asking Claude..."):
            explanation = explain_region(
                str(row["region_name"]),
                str(row["acronym"]),
                float(row["log2_fold_change"]),
                float(row["p_corrected"]),
                float(row["mean_A"]),
                float(row["mean_B"]),
            )
        st.info(explanation)
        st.caption("Generated by Claude claude-opus-4-7 (Anthropic)")
