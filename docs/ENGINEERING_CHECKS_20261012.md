# Software checks and repaired-runner reproduction

The subsequent [coverage and dependency audit](SOFTWARE_AUDIT_20261012.md) records measured coverage, a dated advisory query and a separate comparator repair. The 84-test Colab execution below remains tied to its original candidate.

12 October 2026 | Candidate `04fa7c18ccc39e6cf5656686b39b53ca82a81ce5`

[Executed notebook](../supplementary/Mangrove_Pulse_Engineering_Checks_Executed.ipynb) · [Results and logs](../evidence/engineering_04fa7c1_results.zip) · [Source notebook](../supplementary/Mangrove_Pulse_Engineering_Checks.ipynb) · [Hosted software check](https://github.com/Salim-Ammar/mangrove-pulse/actions/runs/38183276594)

## Changes and checks

Three test modules now import independently. The runner rejects unsafe or malformed manifest entries, missing or changed payloads and unlisted Python source under `src/`; runtime caches and logs remain allowed. The baseline reader validates required ZIP names and declared sizes before reading or writing: 50,000,000 bytes per member and 100,000,000 bytes in total.

Nineteen added fixtures cover these boundaries, subprocess failures and preservation of nonempty output directories. All 84 software tests passed locally, in the hosted job and in Colab. Scientific calculations, inputs, threshold and split are unchanged.

## Colab execution

The notebook reconstructed the 170-payload candidate in an empty directory, reusing 125 matching files from the previously uploaded archive and fetching only 45 changed public files. Every payload hash matched; no EO imagery was reacquired.

Drive mounting initially failed, then succeeded. Environment creation next failed at `ensurepip`, before scientific execution. The source was repaired using the release notebook's existing `venv --without-pip` and kernel `pip --python` pattern, also documented by [pip](https://pip.pypa.io/en/stable/topics/python-option/).

The affected setup/reproduction path then passed using the verified cache, a new isolated environment and fresh output directories. This was not another acquisition or a sequential-from-scratch execution of the revised source notebook. The executed notebook retains the initial setup failure and successful recovery; the recovery uses a literal `exec` expression to avoid editor auto-indentation.

| Check | Recorded result |
| --- | --- |
| Environment | Python 3.13.16; NumPy 2.1.3, Rasterio 1.5.1, Matplotlib 3.10.0 |
| Dependency installation | Succeeded; 22.4956 seconds |
| Software suite | 84 tests passed |
| Baseline/audit reproduction | Succeeded; 7.0464 seconds |
| Equality checks | Summaries, frozen plan/threshold/split, decoded prediction grids, audit cell/cluster records and three curated cases matched |
| Returned archive | 66 files; CRC passed; 1,687,436 bytes |

Archive SHA-256: `6ef393329fdd3564d85b5794ca6715ecc63e6a8aee93f336aa47c5e752519a04`. Packaging ran twice during navigation; the downloaded archives are byte-identical. Scientific reproduction succeeded once. The notebook and archive were preserved before ending the completed runtime.

The hosted job succeeded in 14 seconds, checking 170 payload hashes, 21 notebook structures, Python syntax and the software suite. It uses read-only repository permissions and runs no raster analysis. GitHub reported Node/action and Ubuntu-image migration notices. Later documentation, notebook and evidence additions are not reruns of this candidate.

## Remaining limits and decisions

Direct package pins and installed-package records are not a complete transitive hash lock. Supplementary studies retain separate environments. Coverage percentage and dependency vulnerability status remain unmeasured: no coverage or vulnerability-audit tool was installed. A future audit needs a separately qualified environment, recorded tool/database versions and interpreted findings before imposing gates or changing packages.

The unsigned manifest checks consistency, not publisher authentication or broad security. No arbitrary coverage gate, package migration, Docker requirement or general-purpose site configuration was added. Existing licence notices and attribution are unchanged. Computational consistency does not establish independent cover accuracy, measured drone advantage or ecological benefit.
