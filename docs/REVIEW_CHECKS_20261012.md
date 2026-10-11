# Edge population, reverse split and standalone reproduction

12 October 2026 | Separate exploratory check of commit `a5131ce0b702b6018274c7d20af1346eee43654d`

[Executed notebook](../supplementary/Mangrove_Pulse_Review_Checks_Executed.ipynb) · [Results and logs](../evidence/review_checks_a5131ce_results.zip) · [Machine-readable result](../examples/baseline/review_sensitivity_20261012.json) · [Source notebook](../supplementary/Mangrove_Pulse_Review_Checks.ipynb)

## Population edge comparison

The rule is unchanged from the original audit: a cell touches a transition if any of its eight neighbouring 20 m cells has a different 0/1 GMW label. Neighbours outside the AOI, coded 255, are ignored. The population is the 5,653 eligible southern cells on 20 November 2018.

| Population | Cells | Transition-touching cells | Transition share |
| --- | ---: | ---: | ---: |
| All eligible southern cells | 5,653 | 334 | 5.91% |
| Disagreements | 121 | 96 | 79.34% |
| Agreements | 5,532 | 238 | 4.30% |

Disagreements are descriptively concentrated near reference-label transitions, rather than simply reflecting the population's edge share. This does not identify a cause. Sensor response, mixed pixels, map error and alignment remain possible contributors. The cells are spatially dependent; these proportions are not independent-trial accuracy estimates or evidence of physical positional error.

## Exploratory split reversal

The original split and 200 m gap are unchanged. For this separate check only, the southern November 20 cells select an F1-maximizing threshold from the original 201 candidates, with the original higher-threshold tie rule. The selected value is approximately 0.45. It is then applied to the north.

| Direction | Threshold | Calibration F1 | Evaluation F1 |
| --- | ---: | ---: | ---: |
| Original: north to south | 0.49 | 0.6652 | 0.8864 |
| Exploratory reverse: south to north | 0.45 | 0.8881 | 0.6577 |

Reverse northern TP/FP/FN/TN are 317/211/119/4,971. Reversal does not remove the geographic performance difference. It therefore strengthens the warning against presenting the favorable southern score as regional generalization, but does not isolate why the halves differ. Both halves were already inspected: this is not a fresh independent holdout, and the reverse threshold does not replace the frozen 0.49 threshold.

## What executed and what was checked

A newly created CPU Colab runtime cloned the public repository, fetched and checked out the exact candidate above, installed its pinned requirements, and ran `src/run_submission.py` with a fresh empty output directory. No pre-existing result could satisfy that runner. The cached input package was obtained as part of the checkout; no data-provider imagery request was made.

The runner verified all 162 candidate payload hashes, matched baseline summaries, plan, threshold and split, compared decoded prediction grids, matched every audit cell/cluster record, and confirmed the three curated case sizes and ranks. The sensitivity check additionally required reconstructed eligibility and original predictions to match exactly, and required the original 121 disagreements and 96 edge-touching disagreements to reconcile before reporting new values. Six local synthetic tests covered the new helper logic; the full local software suite passed 65 tests. Synthetic tests are separate from this actual raster execution.

| Environment / step | Recorded value |
| --- | --- |
| Python | 3.13.16 |
| NumPy / rasterio / matplotlib | 2.1.3 / 1.5.1 / 3.10.0 |
| Dependency installation | 8.74 s |
| Standalone reproduction | 7.56 s |
| Sensitivity analysis | 0.37 s |
| Stage return codes | All zero |

Timings are observations from this runtime, not performance guarantees. The archive contains 26 returned files, including logs, runtime records, summaries and the sensitivity result. Its 21,423 bytes have SHA-256 `2363e4e96c6e49483199fefb1deb5b5af4fe034d1d3cc463058c623b3ba715b9`, matching the executed notebook's export record. The sensitivity result records hashes of its reproduced inputs. Original execution artifacts remain unchanged.

The scientific cell executed once. The packaging cell was repeated after the browser's download-event hook did not report the first successful download; both downloaded archives are byte-identical. No scientific rerun or repeated imagery acquisition resulted. The executed notebook was saved in Drive and downloaded before its completed task runtime was deleted. Later documentation commits are not new executions of the candidate.

These checks establish reproducibility and descriptive sensitivity. They do not establish independent cover accuracy, aircraft performance, contact-measurement quality, ecological benefit or hyperspectral improvement.
