# Bundled example validation — GET-Pak 1.0.3

Validated on 16 October 2026. Both notebooks were executed from their first code cell through their final comparison cell using Python 3.10 in the local `gpk310` environment, with Matplotlib's noninteractive Agg backend. Notebook source cells were executed by `validate_examples.py`; no Jupyter frontend was required. Each notebook independently ran the actual batch pipeline as its reference.

Source: bundled GRS v2.1.9 scene dated 7 September 2023, tile 31TCJ, and its bundled WaterDetect mask. Full 5,490 × 5,490 scene; no spatial subset. GRS and mask files were unchanged.

- `Notebook_single_image_tutorial.ipynb`: passed in 555.70 seconds.
- `l2b_workflow.ipynb`: passed in 541.98 seconds.
- All 13 products: exactly equal valid masks and decoded physical values, matching CRS, transform, dimensions, NoData, multipliers, units and encoding profile/version.
- Pixel-count reports and all pre-QC per-band diagnostics also matched batch exactly.
- Full regression suite: 129 passed. Package metadata reports 1.0.3.

The two notebook comparisons produced the same counts below. Different product counts are expected from their respective retrieval limits, input-band validity and encoding rules.

| Product | Valid pixels in notebook and batch | Maximum absolute physical difference |
| --- | ---: | ---: |
| OWT | 179,877 | 0 |
| OWTSPM | 179,877 | 0 |
| Chla | 133,055 | 0 |
| Turb | 134,781 | 0 |
| HySPM | 136,460 | 0 |
| Aerosol | 163,342 | 0 |
| Blue | 173,457 | 0 |
| Green | 179,875 | 0 |
| Red | 179,877 | 0 |
| RedEdge1 | 179,658 | 0 |
| RedEdge2 | 178,887 | 0 |
| RedEdge3 | 179,350 | 0 |
| Nir2 | 179,037 | 0 |

The water-mask count was 186,564; the negative-Red counter was 6,671 and the low-reflectance counter was 16. Both notebooks use current quality filtering; higher Rrs storage precision does not bypass it.

## Reproduce

From the repository root in an environment with GET-Pak and Matplotlib installed:

```sh
python examples/validate_examples.py examples/Notebook_single_image_tutorial.ipynb
python examples/validate_examples.py examples/l2b_workflow.ipynb
python -m pytest -q
```

Every run creates its own `examples/Outputs/<notebook>_<timestamp>/` folder, containing manual and batch outputs plus `comparison.json`. Notebook saved outputs are intentionally cleared to avoid stale results and embedded local paths.

This verifies one bundled scene, not all sensor/processor combinations. No ROI vectors are bundled, so these scene runs do not generate ROI workbooks; synthetic legacy/zero-NoData ROI regressions remain part of the test suite. A headless Matplotlib warning that figures cannot be shown is expected during command-line validation. The separate experimental `blended_turb` route is unchanged; both notebooks use the current batch `turb(alg="owt")` route.
