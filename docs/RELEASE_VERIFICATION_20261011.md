# Release verification: 11 October 2026

The team reproduced release `cb4b400dd67aa79c7f5800006a14db4637926467` in a fresh Colab Python 3 CPU runtime. The run verified 178 input hashes and matched the frozen baseline summaries, threshold, split, decoded predictions, disagreement audit and case records. The observation handoff passed 17 format tests and retained C001/C017/C027 counts of 11/32/42.

- [View the executed notebook](../supplementary/Mangrove_Pulse_Release_cb4b400_Executed.ipynb)
- [Open the repository copy in Colab](https://colab.research.google.com/drive/1DSr8g_p2pEhOVD4bVvGkW1hhB8l9VLMb)
- [Download the results and logs](../evidence/release_cb4b400_results.zip)

## What ran

The wrapper adds input extraction, timing and environment records around the seven unchanged analysis cells. It recomputed the baseline and audit. It displayed the separate reference-map context and hypothetical drone-energy examples from saved results; those examples were not recomputed.

Python was 3.13.16, with NumPy 2.1.3, Matplotlib 3.10.0 and Rasterio 1.5.1. The ZIP includes the full package list and command logs.

| Operation | Wall time |
| --- | ---: |
| Environment creation and dependency installation | 14.3315 s |
| Baseline and disagreement-audit reproduction | 8.1099 s |
| Handoff test command | 0.1641 s |
| Inspection export command | 0.0451 s |

These timings describe this runtime. They are not aircraft performance measurements.

## Artifact integrity

The executed repository copy contains ten code cells with execution counts 3 through 12, six PNG outputs and no saved errors. Its code, outputs, execution counts and timing metadata match the downloaded execution; only explanatory Markdown and cell metadata differ. The original downloaded notebook remains in the team's local archive.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Original downloaded notebook | 846240 | `ee437ee8fc6ba15a0d557263e438aef1bc776e0ee72354ba823990e5308490be` |
| Repository reading copy | 846205 | `b5f4a7ec103c080c00890e7b2c428de434c2c3afa9c785527caeed7b1d3ed112` |
| Results ZIP | 2103306 | `ca8c84c157194b948b0600d4438080e2365370add803dcc8b6d5805e2669a398` |
| Input release ZIP | 15182259 | `28aa20c925b8ddccf327f30e5e1408e716aa397960e7e7b7e1da7b2ddff6ccc6` |

All 91 result payload hashes match the ZIP manifest. There are no duplicate entries. Two earlier administrative attempts failed before analysis: an editor indentation error and unsuccessful Drive credential propagation. After repair and approved Drive access, the analysis completed. The team saved and verified the artifacts before deleting only this completed runtime.

## Limits

This run establishes computational reproduction of the identified release, not independent cover accuracy, drone advantage or ecological benefit. Collected field observations remain zero. The older 7 October notebook's code and saved outputs remain unchanged, although presentation Markdown has been revised; its unrecovered results ZIP is not this archive. Later documentation and evidence additions do not constitute another scientific execution.
