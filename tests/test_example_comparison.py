"""Ensure the example verification rejects scientifically meaningful differences."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest
from affine import Affine
from getpak.commons import Utils
from getpak.output import Raster

spec = importlib.util.spec_from_file_location('example_support', Path(__file__).parents[1] / 'examples' / 'example_support.py')
example = importlib.util.module_from_spec(spec)
spec.loader.exec_module(example)


def write(path, values, scale=100):
    encoded, metadata = Utils.to_uint_scaled(np.array([values]), scale=scale, return_metadata=True)
    Raster.array2tiff(encoded, path, Affine(1, 0, 0, 0, -1, 1), 'EPSG:4326', metadata=metadata)


@pytest.mark.parametrize('values,scale', [([0, 1, 2], 100), ([0, 1, 3], 100),
                                          ([1, 1, 2], 100), ([0, 1, 2], 10)])
def test_comparison_checks_masks_values_and_encoding(tmp_path, values, scale):
    a, b = tmp_path / 'a.tif', tmp_path / 'b.tif'
    write(a, [0, 1, 2])
    write(b, values, scale)
    if values == [0, 1, 2] and scale == 100:
        assert example.compare_products({'Red': a}, {'Red': b})['Red']['valid_pixels'] == 2
    else:
        with pytest.raises(AssertionError):
            example.compare_products({'Red': a}, {'Red': b})
