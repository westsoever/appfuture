import numpy as np
import pandas as pd
import SimpleITK as sitk
import streamlit as st


@st.cache_resource
def _load_volumes():
    anatomy = sitk.GetArrayFromImage(sitk.ReadImage("data/anatomy.nii.gz"))
    regions = sitk.GetArrayFromImage(sitk.ReadImage("data/regions.nii.gz"))
    diff    = sitk.GetArrayFromImage(sitk.ReadImage("data/diff_map.nii.gz"))
    return anatomy, regions, diff


@st.cache_data(show_spinner=False)
def get_slice(acronym: str, axis: int = 1) -> dict | None:
    """Return coronal (axis=1) 2D slices for anatomy, diff map, and region mask.

    SimpleITK arrays are (Z, Y, X). axis=1 = coronal (anterior-posterior).
    Returns dict with keys: anatomy, diff, mask — all 2D numpy arrays.
    Returns None if acronym is not found or region mask is empty.
    """
    hierarchy = pd.read_csv("data/atlas_hierarchy.csv")
    match = hierarchy[hierarchy["acronym"] == acronym]
    if match.empty:
        return None

    anatomy, regions, diff = _load_volumes()
    regions_int = regions.astype(int)

    label_id = int(match.iloc[0]["id"])
    region_mask = (regions_int == label_id)

    counts = region_mask.sum(axis=(0, 2)) if axis == 1 else region_mask.sum(axis=(1, 2))
    if counts.max() == 0:
        return None

    idx = int(counts.argmax())
    mask_2d = np.take(region_mask, idx, axis=axis)

    return {
        "anatomy": np.take(anatomy, idx, axis=axis),
        "diff":    np.take(diff, idx, axis=axis),
        "mask":    mask_2d,
    }


def render_overlay(slice_dict: dict):
    """Render diff map with region mask overlay as a matplotlib figure."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(slice_dict["diff"], cmap="RdBu_r", vmin=-3, vmax=3)
    ax.imshow(
        np.ma.masked_where(slice_dict["mask"] == 0, slice_dict["mask"]),
        cmap="Greens",
        alpha=0.5,
    )
    ax.axis("off")
    return fig
