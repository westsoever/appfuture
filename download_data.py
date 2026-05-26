"""Run once before the hackathon to cache all data files locally."""
import os
from vibraint.bucket_access.bucket_utils import download_file

os.makedirs("data", exist_ok=True)

files = [
    ("challengeB/tabular_data_quantification/cfos_object_density_statistics_G002_vs_G001.csv",
     "data/cfos_statistics.csv"),
    ("challengeB/tabular_data_quantification/cfos_object_density_quantification.csv",
     "data/cfos_quantification.csv"),
    ("challengeB/spatial_brain_maps/atlas_hierarchy.csv",
     "data/atlas_hierarchy.csv"),
    ("challengeB/spatial_brain_maps/brain_atlas_anatomy.nii.gz",
     "data/anatomy.nii.gz"),
    ("challengeB/spatial_brain_maps/brain_atlas_regions.nii.gz",
     "data/regions.nii.gz"),
    ("challengeB/spatial_brain_maps/cfos_group_median_difference_G002_vs_G001.nii.gz",
     "data/diff_map.nii.gz"),
    ("challengeB/spatial_brain_maps/cfos_G001_median.nii.gz",
     "data/cfos_G001.nii.gz"),
    ("challengeB/spatial_brain_maps/cfos_G002_median.nii.gz",
     "data/cfos_G002.nii.gz"),
]

for src, dst in files:
    if os.path.exists(dst):
        print(f"  skip {dst} (already exists)")
        continue
    print(f"downloading {src} ...")
    download_file(src, dst)
    print(f"  → {dst}")

print("done.")
