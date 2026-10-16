"""Real GeoTIFF/ROI regressions for new and legacy integer outputs."""
import numpy as np
import pytest
import rasterio
from affine import Affine
from shapely.geometry import box, mapping

from getpak.automation import Pipelines
from getpak.commons import Utils
from getpak.output import Raster


@pytest.mark.parametrize('dtype', ['uint16', 'uint32'])
def test_zero_encoding_boundaries_and_diagnostics(dtype):
    maximum = np.iinfo(dtype).max
    encoded, metadata = Utils.to_uint_scaled(
        np.array([0, .004, .006, np.nan, -1, maximum / 100, maximum / 100 + 1]),
        scale=100, dtype=dtype, return_metadata=True)
    assert encoded.tolist() == [0, 0, 1, 0, 0, maximum, 0]
    assert metadata['nodata'] == 0
    assert metadata['zero_nodata_count'] == 2
    assert metadata['valid_zero_count'] == 0
    assert metadata['valid_min'] == .01
    assert metadata['overflow_count'] == 1


@pytest.mark.parametrize('dtype,nodata', [('uint16', 0), ('uint32', 0),
                                          ('uint16', 65535), ('uint32', 4294967295)])
@pytest.mark.parametrize('embedded_scale', [True, False])
def test_real_roi_respects_file_nodata_and_multiplier(tmp_path, dtype, nodata, embedded_scale):
    target = tmp_path / 'product.tif'
    transform = Affine(1, 0, 0, 0, -1, 1)
    with rasterio.open(target, 'w', driver='GTiff', width=4, height=1,
                       count=1, dtype=dtype, transform=transform,
                       crs='EPSG:4326', nodata=nodata) as dst:
        dst.write(np.array([[0, 100, 200, nodata]], dtype=dtype), 1)
        if embedded_scale:
            dst.scales = (.1,)
            dst.update_tags(STORED_MULTIPLIER='10', DECODE_MULTIPLIER='.1',
                            GETPAK_ENCODING_VERSION='GETPAK-ENC-2')
    # A conflicting setting must not override the file's scale or NoData.
    result = Pipelines._parse_tifs(target, [mapping(box(0, 0, 4, 1))], prefix='Turb',
                                 encoding_settings={'output_encoding': {'turbidity_multiplier': 100}})
    assert result['Turb_status'] == 'success'
    assert result['Turb_nodata'] == nodata
    assert result['Turb_count'] == (2 if nodata == 0 else 3)
    factor = .1 if embedded_scale else .01
    assert result['Turb_mean'] == pytest.approx((150 if nodata == 0 else 100) * factor)
    assert result['Turb_min'] == (100 * factor if nodata == 0 else 0)
    assert result['Turb_decode_source'] == ('embedded_metadata' if embedded_scale else 'settings_fallback')


def test_new_categorical_geotiff_masks_zero(tmp_path):
    encoded, metadata = Utils.to_uint8_categorical(
        np.array([[0, 1, 7, 255, np.nan]]), return_metadata=True)
    target = tmp_path / 'owt.tif'
    Raster.array2tiff(encoded, target, Affine(1, 0, 0, 0, -1, 1), 'EPSG:4326', metadata=metadata)
    with rasterio.open(target) as src:
        assert src.nodata == 0
        assert src.tags()['NODATA'] == '0'
        assert src.read_masks(1).tolist() == [[0, 255, 255, 255, 0]]


def test_settings_and_example_use_zero():
    for path in ('settings.ini', 'examples/example_settings.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read(path)
        settings = Utils.resolve_encoding_settings({s: dict(config[s]) for s in config.sections()})
        assert settings['output_encoding']['continuous_nodata'] == 0
        assert settings['output_encoding']['categorical_nodata'] == 0


def test_all_nodata_roi_is_empty(tmp_path):
    target = tmp_path / 'empty.tif'
    Raster.array2tiff(np.zeros((1, 2), dtype='uint32'), target,
                      Affine(1, 0, 0, 0, -1, 1), 'EPSG:4326',
                      metadata={'stored_multiplier': 100})
    result = Pipelines._parse_tifs(target, [mapping(box(0, 0, 2, 1))], prefix='Turb')
    assert result['Turb_count'] == 0
    assert result['Turb_mean'] is None
    assert result['Turb_status'] == 'empty_overlap'


def test_file_metadata_does_not_validate_obsolete_output_settings(tmp_path):
    target = tmp_path / 'legacy.tif'
    with rasterio.open(target, 'w', driver='GTiff', width=2, height=1,
                       count=1, dtype='uint16', transform=Affine(1, 0, 0, 0, -1, 1),
                       crs='EPSG:4326', nodata=65535) as dst:
        dst.write(np.array([[0, 100]], dtype='uint16'), 1)
        dst.scales = (.1,)
        dst.update_tags(PHYSICAL_UNIT='legacy-unit')
    result = Pipelines._parse_tifs(target, [mapping(box(0, 0, 2, 1))], prefix='Turb',
        encoding_settings={'output_encoding': {'continuous_nodata': 65535}})
    assert result['Turb_count'] == 2
    assert result['Turb_mean'] == 5
    assert result['Turb_decode_source'] == 'embedded_metadata'
    assert result['Turb_physical_unit'] == 'legacy-unit'
