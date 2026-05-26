import numpy as np
import pandas as pd
import SimpleITK as sitk

_cache: dict = {}


def _load(path: str) -> np.ndarray:
    if path not in _cache:
        _cache[path] = sitk.GetArrayFromImage(sitk.ReadImage(path))
    return _cache[path]


def get_slice(acronym: str, axis: int = 1) -> dict:
    """Return coronal (axis=1) 2D slices for anatomy, diff map, and region mask.

    SimpleITK arrays are (Z, Y, X). axis=1 = coronal (anterior-posterior).
    Returns dict with keys: anatomy, diff, mask — all 2D numpy arrays.
    """
    anatomy = _load("data/anatomy.nii.gz")
    diff = _load("data/diff_map.nii.gz")
    regions = _load("data/regions.nii.gz").astype(int)

    hierarchy = pd.read_csv("data/atlas_hierarchy.csv")
    match = hierarchy[hierarchy["acronym"] == acronym]
    if match.empty:
        mask_2d = None
        idx = anatomy.shape[axis] // 2
    else:
        label_id = int(match.iloc[0]["label"])
        region_mask = (regions == label_id)
        counts = region_mask.sum(axis=(0, 2)) if axis == 1 else region_mask.sum(axis=(1, 2))
        idx = int(counts.argmax()) if counts.max() > 0 else anatomy.shape[axis] // 2
        mask_2d = np.take(region_mask, idx, axis=axis)

    return {
        "anatomy": np.take(anatomy, idx, axis=axis),
        "diff": np.take(diff, idx, axis=axis),
        "mask": mask_2d,
    }
