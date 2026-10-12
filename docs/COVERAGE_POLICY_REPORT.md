# Coverage-policy reporting and SymPy setup

12 October 2026

The standalone runner now writes `coverage_policy_summary.json` after the reproduced baseline summary matches the frozen record. This is a separate reporting output; the original baseline engine, threshold, eligibility mask and scores are unchanged. The [example report](../examples/baseline/coverage_policy_summary.json) was derived from the stored summary without processing rasters and records that summary's SHA-256.

## Explicit exclusion policy

The report gives each date's eligible, excluded and total southern cell counts, eligible fraction, eligible-cell F1 and the full confusion counts, recall and F1 under **excluded cells as negative predictions**. Excluded GMW-positive cells become additional false negatives; excluded GMW-negative cells become additional true negatives. This is GMW agreement under a declared reporting policy, not independent cover accuracy or a general worst-case bound.

| Date | Eligible / population | Excluded | Eligible F1 | Policy F1 | Policy recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| 20 November 2018 | 5,653 / 6,121 | 468 | 0.8864 | 0.8194 | 0.7457 |
| 30 November 2018 | 5,310 / 6,121 | 811 | 0.8889 | 0.8228 | 0.7520 |

The helper rejects negative, non-integer and unreconciled counts. Undefined ratios are JSON `null`, not perfect scores. Six software tests cover literal synthetic counts, no exclusions, empty populations, malformed counts, both stored dates and actual runner report emission using a controlled child fixture. That fixture deliberately stops before raster imports; it does not establish a new complete scientific execution.

## SymPy version

The [source notebook](../supplementary/Mangrove_Pulse_SymPy_Resource_Audit.ipynb) requires SymPy 1.14.0, matching the [original executed record](../supplementary/Mangrove_Pulse_SymPy_Resource_Audit_Executed.ipynb). Setup installs that version when absent or different and checks the imported version. A conflicting already-loaded module requires restarting the runtime before continuing, rather than mixing old in-memory code with a replaced installation.

Three tests execute the real setup cell against controlled package states: matching, missing, different and stale loaded versions. Installation is replaced by a fixture operation, so these tests do not download packages or establish a fresh Colab installation. Symbolic calculation cells and the original executed notebook remain unchanged.

The current software suite passes 97 tests. The [earlier coverage measurement](SOFTWARE_AUDIT_20261012.md) remains tied to its 88-test source snapshot; it is not a measurement of these later changes. No field observations, aircraft performance or ecological outcomes are added by either repair.
