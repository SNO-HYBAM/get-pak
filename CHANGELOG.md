# Changelog

## 1.0.3

- Standardize new unsigned continuous and categorical raster outputs on zero NoData.
- Increase the default Rrs multiplier to 10,000,000; continuous outputs remain uint32 by default.
- Preserve existing files' embedded multipliers, units and NoData when decoding and computing ROI statistics.
- Align both bundled notebooks with the current batch quality rules, retrievals and metadata-aware raster writers. Each notebook verifies its outputs against a real batch run of the bundled scene.

### Migration

Update nonzero `continuous_nodata` and `categorical_nodata` output settings to zero. New integer outputs cannot represent valid physical zero; values rounding to stored zero also become NoData. Negative values and overflow remain masked. Existing low-Rrs quality filtering is unchanged.

Older files remain readable with their embedded encoding metadata. For files lacking multiplier metadata, explicitly configure the original product multiplier; the new Rrs default must not be assumed for old untagged files. Files without embedded NoData remain rejected. `GETPAK-ENC-2` is unchanged, so inspect each file's actual metadata rather than inferring its sentinel from the encoding version.

Signed custom Float32 products retain NaN NoData. No change to the separate `blended_turb` algorithm is included in this release.
