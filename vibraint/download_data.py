"""Download all Challenge B data files to data/ directory."""
import os
from bucket_access.bucket_utils import download_file

files = [
    ('challengeB/tabular_data_quantification/cfos_object_density_statistics_G002_vs_G001.csv',
     'cfos_statistics.csv'),
    ('challengeB/tabular_data_quantification/cfos_object_density_quantification.csv',
     'cfos_quantification.csv'),
    ('challengeB/spatial_brain_maps/cfos_group_median_difference_G002_vs_G001.nii.gz',
     'diff_map.nii.gz'),
    ('challengeB/spatial_brain_maps/brain_atlas_regions.nii.gz',
     'regions.nii.gz'),
    ('challengeB/spatial_brain_maps/brain_atlas_anatomy.nii.gz',
     'anatomy.nii.gz'),
    ('challengeB/spatial_brain_maps/cfos_G001_median.nii.gz',
     'cfos_G001.nii.gz'),
    ('challengeB/spatial_brain_maps/cfos_G002_median.nii.gz',
     'cfos_G002.nii.gz'),
    ('challengeB/spatial_brain_maps/atlas_regions.csv',
     'atlas_hierarchy.csv'),
]

os.makedirs('data', exist_ok=True)
for src, dst in files:
    dst_path = f'data/{dst}'
    if os.path.exists(dst_path):
        size_mb = os.path.getsize(dst_path) / 1e6
        print(f'SKIP (exists, {size_mb:.1f}MB): {dst_path}')
        continue
    print(f'Downloading {src} ...')
    download_file(src, dst_path)
    size_mb = os.path.getsize(dst_path) / 1e6
    print(f'  → {dst_path} ({size_mb:.1f} MB)')

print('\nDone. Files in data/:')
for f in sorted(os.listdir('data')):
    size_mb = os.path.getsize(f'data/{f}') / 1e6
    print(f'  {f}: {size_mb:.1f} MB')
