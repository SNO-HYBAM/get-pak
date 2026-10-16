"""Shared setup, output writing and verification for the bundled notebooks.

Scientific processing remains visible in each notebook. These helpers use the
current pipeline's discovery and writers so metadata and encoding do not drift.
"""
from configparser import ConfigParser
from pathlib import Path
import shutil

import numpy as np
import rasterio

from getpak.automation import Pipelines
from getpak.commons import Utils

BANDS = ('Aerosol', 'Blue', 'Green', 'Red', 'RedEdge1', 'RedEdge2', 'RedEdge3', 'Nir2')


def prepare_pipeline(repo_root, run_folder):
    """Resolve example-relative paths and stage the batch tile-folder layout."""
    root = Path(repo_root).resolve()
    run = Path(run_folder).expanduser().resolve()
    config = ConfigParser()
    config.read(root / 'examples' / 'example_settings.ini')
    tile = config['processing']['s2_tile']
    source = (root / 'examples' / config['client_folder']['inputs']).resolve()
    staged = run / 'inputs' / tile
    staged.mkdir(parents=True, exist_ok=True)
    files = sorted(source.rglob('*.nc'))
    if not files:
        raise FileNotFoundError(f'No bundled GRS inputs under {source}')
    for path in files:
        target = staged / path.name
        if not target.exists():
            # Copying also works on Windows without symlink privileges.
            shutil.copy2(path, target)
    masks = (root / 'examples' / config['client_folder']['wmask_folder']).resolve()
    config['client_folder'].update(inputs=str(run / 'inputs'),
                                  output=str(run / 'products'), wmask_folder=str(masks))
    config_path = run / 'settings.ini'
    with config_path.open('w') as handle:
        config.write(handle)
    pipeline = Pipelines(config_path=str(config_path))
    pipeline.get_matchups()
    return pipeline


def write_products(pipeline, scene_key, grs, products, rrs_bands, pixels):
    """Use the batch writers, including identity, units, scale and NoData tags."""
    for folder in ('OWT', 'OWTSPM', 'Chla', 'Turb', 'HySPM', 'npix', *BANDS):
        (Path(pipeline.output_folder) / pipeline.tile_id / folder).mkdir(parents=True, exist_ok=True)
    pipeline.grid_by_uid[scene_key] = grs.attrs['grid_validation']
    transform, projection = grs.attrs['trans'], grs.attrs['proj']
    written = {}
    for product, prefix in (('OWT', 'OWTs_'), ('OWTSPM', 'OWTSPM_')):
        written[product] = pipeline._write_categorical_raster(
            products[product], product, prefix, scene_key,
            transform=transform, projection=projection)
    encoding = pipeline.encoding_settings['output_encoding']
    units = {'Chla': 'mg m-3', 'Turb': encoding['owt_unit'], 'HySPM': 'mg L-1'}
    continuous = {name: products[name] for name in units}
    if pipeline.report_rrs:
        continuous.update(rrs_bands)
    for product, values in continuous.items():
        path, _ = pipeline._write_scaled_raster(
            values, product, f'{product}_', scene_key,
            scale=encoding[Utils.product_multiplier_key(product)],
            unit=units.get(product, 'sr-1'), transform=transform, projection=projection)
        written[product] = path
    pixel_path = pipeline._output_target('npix', 'npixels_', scene_key, '.txt')
    np.savetxt(pixel_path, pixels, fmt='%s', delimiter=';')
    return written


def compare_products(reference, candidate):
    """Compare masks and decoded physical values, failing on any mismatch."""
    summary = {}
    for product, path in reference.items():
        with rasterio.open(path) as a, rasterio.open(candidate[product]) as b:
            assert a.crs == b.crs and a.transform == b.transform, product
            assert a.shape == b.shape, product
            valid_a, valid_b = a.read_masks(1) > 0, b.read_masks(1) > 0
            assert np.array_equal(valid_a, valid_b), f'{product}: valid masks differ'
            decoded_a = a.read(1).astype(float) * a.scales[0] + a.offsets[0]
            decoded_b = b.read(1).astype(float) * b.scales[0] + b.offsets[0]
            assert np.array_equal(decoded_a[valid_a], decoded_b[valid_b]), product
            assert a.nodata == b.nodata == 0, product
            for tag in ('STORED_MULTIPLIER', 'DECODE_MULTIPLIER', 'PHYSICAL_UNIT',
                        'GETPAK_ENCODING_VERSION', 'ENCODING_PROFILE'):
                assert a.tags().get(tag) == b.tags().get(tag), (product, tag)
            summary[product] = {'valid_pixels': int(valid_a.sum()), 'max_absolute_difference': 0.0}
    return summary
