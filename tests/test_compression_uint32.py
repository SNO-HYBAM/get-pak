import numpy as np
import pytest
import rasterio
from affine import Affine
from getpak.commons import Utils
from getpak.output import Raster


def test_uint32_retains_high_concentrations_and_zero(tmp_path):
    values = np.array([[0, 600, 655.35, 1200.12, 3000, 7000.01, np.nan, -1]])
    encoded, tags = Utils.to_uint_scaled(values, scale=100, return_metadata=True)
    target = tmp_path / 'high_spm.tif'
    Raster.array2tiff(encoded, target, Affine(20, 0, 300000, 0, -20, 9100000),
                      'EPSG:32720', no_data=4294967295, metadata=tags)
    with rasterio.open(target) as src:
        assert src.compression.value == 'LZW'
        assert src.dtypes == ('uint32',)
        assert src.nodata == 4294967295
        assert np.array_equal(src.read(1), encoded)
        assert np.array_equal(src.read(1)[0, :6], np.rint(values[0, :6] * 100))
        assert np.allclose(src.read(1)[0, :6] * src.scales[0], values[0, :6])
        assert tags['overflow_count'] == 0
        assert src.read(1)[0, 6] == src.read(1)[0, 7] == src.nodata


@pytest.mark.parametrize('dtype', ['uint16', 'uint32'])
def test_encoding_boundary_has_no_integer_wraparound(dtype):
    nodata = int(np.iinfo(dtype).max)
    maximum = (nodata - 1) / 100
    data, tags = Utils.to_uint_scaled(np.array([maximum, maximum + 1, 1.23456]),
                                     dtype=dtype, scale=100, return_metadata=True)
    assert data.tolist() == [nodata - 1, nodata, 123]
    assert tags['overflow_count'] == 1
    assert abs(data[-1] / 100 - 1.23456) <= 0.005


def test_float64_writer_does_not_reduce_precision(tmp_path):
    values = np.array([[1.23456789012345, np.nan]], dtype='float64')
    target = tmp_path / 'precise.tif'
    Raster.array2tiff(values, target, Affine(20, 0, 300000, 0, -20, 9100000),
                      'EPSG:32720', no_data=np.nan)
    with rasterio.open(target) as src:
        assert src.dtypes == ('float64',)
        assert src.compression.value == 'LZW'
        assert np.array_equal(values, src.read(1), equal_nan=True)


def test_presentation_switch_does_not_change_encoding():
    turb = Utils.resolve_encoding_settings({'processing': {'owt_product': 'turbidity'}})
    spm = Utils.resolve_encoding_settings({'processing': {'owt_product': 'spm'}})
    assert turb['output_encoding']['owt_unit'] == 'NTU'
    assert spm['output_encoding']['owt_unit'] == 'mg L-1'
    values = np.array([1200.1234])
    a, atags = Utils.to_uint_scaled(values, scale=100, unit=turb['output_encoding']['owt_unit'], return_metadata=True)
    b, btags = Utils.to_uint_scaled(values, scale=100, unit=spm['output_encoding']['owt_unit'], return_metadata=True)
    assert np.array_equal(a, b)
    assert atags['physical_unit'] != btags['physical_unit']
    with pytest.raises(ValueError, match='owt_product'):
        Utils.resolve_encoding_settings({'processing': {'owt_product': 'invalid'}})


def test_legacy_uint16_settings_remain_supported():
    output = Utils.resolve_encoding_settings({'output_encoding': {
        'continuous_dtype': 'uint16', 'continuous_nodata': 65535,
        'hyspm_multiplier': 10, 'turbidity_multiplier': 10,
    }})['output_encoding']
    assert output['maximum_physical_value']['hyspm_multiplier'] == 6553.4
