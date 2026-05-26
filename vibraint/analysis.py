import numpy as np
import SimpleITK as sitk
import pandas as pd

REGIONS_PATH = "data/regions.nii.gz"
DIFF_PATH = "data/diff_map.nii.gz"
ANATOMY_PATH = "data/anatomy.nii.gz"


def prepare_volcano(df):
    out = df.copy()
    out["neg_log10_p"] = -np.log10(out["p_corrected"].clip(lower=1e-10))
    out["significance"] = "not significant"
    out.loc[out["significant_uncorrected"] == True, "significance"] = "significant (uncorrected)"
    out.loc[out["significant_corrected"] == True, "significance"] = "significant (corrected)"
    return out


def get_region_ranking(df, only_significant=False):
    result = df.copy()
    if only_significant:
        result = result[result["significant_corrected"] == True]
    return result.sort_values("p_corrected").reset_index(drop=True)


def get_brain_slice(region_acronym, atlas_df, axis="coronal"):
    regions_img = sitk.ReadImage(REGIONS_PATH)
    diff_img = sitk.ReadImage(DIFF_PATH)
    anatomy_img = sitk.ReadImage(ANATOMY_PATH)

    # sitk.GetArrayFromImage returns (Z, Y, X)
    regions = sitk.GetArrayFromImage(regions_img).astype(int)
    diff = sitk.GetArrayFromImage(diff_img)
    anatomy = sitk.GetArrayFromImage(anatomy_img)

    match = atlas_df[atlas_df["acronym"] == region_acronym]
    if match.empty:
        return None
    label = int(match.iloc[0]["label"])

    mask = (regions == label)
    if not mask.any():
        return None

    coords = np.argwhere(mask)
    center = coords.mean(axis=0).astype(int)  # (z, y, x)

    axis_map = {"axial": 0, "coronal": 1, "sagittal": 2}
    ax = axis_map.get(axis, 1)
    idx = center[ax]

    slices = [slice(None)] * 3
    slices[ax] = idx

    return {
        "diff_slice": diff[tuple(slices)],
        "mask_slice": mask[tuple(slices)],
        "anatomy_slice": anatomy[tuple(slices)],
        "center": center,
        "axis": axis,
        "label": label,
    }
