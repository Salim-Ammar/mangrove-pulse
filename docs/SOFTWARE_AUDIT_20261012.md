# Software coverage and dependency audit

12 October 2026 · Starting revision `de1cca236980e33065acc382b06c8d4a0624aed5`

[Measurement record](../evidence/software_audit_20261012.json) · [Recorded package versions](../evidence/software_audit_packages_20261012.txt) · [Earlier Colab reproduction](ENGINEERING_CHECKS_20261012.md)

The audit found a JSON-comparison defect and repaired it. All 88 software tests pass. The dated advisory query reported no known vulnerabilities in the 16 Python packages recorded by the isolated baseline Colab run. A separate check of eight additional declared or recorded versions found two distinct advisories, described below. Neither query skipped a package. Scientific inputs, calculations, saved results and licence notices are unchanged.

## Comparison repair

The runner previously accepted Boolean values as equal to numeric zero or one: Python treats `False == 0` and `True == 1` as true. A nested-metadata regression reproduced all four substitutions, in both directions, before the repair. The comparator now rejects Boolean/non-Boolean substitutions while retaining its existing numeric tolerances.

Four added tests cover that regression, matching nested metadata, changed keys/list lengths/values and CSV comparisons. CSV tests preserve small rounding tolerance but reject changed identifiers, scores, row counts and columns. These tests execute the real comparison functions and controlled runner failure fixtures; they do not process satellite rasters.

The [measurement record](../evidence/software_audit_20261012.json) identifies the repaired source and test bytes by SHA-256. The earlier Colab archive identifies its own executed revision `04fa7c1`; it is not execution evidence for this subsequent comparator repair. Saved baseline/audit summary comparisons also pass with the repaired comparator. A fresh raster reproduction of this revision was not performed.

## Coverage measurement

An isolated Windows x86-64 environment used Python 3.13.13, NumPy 2.1.3 and Coverage.py 7.16.2. The complete existing suite ran before the repair (84 tests) and after it (88 tests). Coverage included all eight modules under `src`, including unexecuted ones, with no configured exclusions.

| Measure | Before | After |
| --- | ---: | ---: |
| Covered statements / total | 405 / 849 | 429 / 851 |
| Covered branch destinations / total | 174 / 378 | 200 / 380 |
| Combined statement/branch coverage | 47.19% | 51.10% |

| Module | After: combined coverage |
| --- | ---: |
| `concept_screen.py` | 90.12% |
| `disagreement_audit.py` | 0% |
| `inspection_handoff.py` | 94.34% |
| `offline_context_reader.py` | 0% |
| `reference_baseline.py` | 19.10% |
| `review_sensitivity.py` | 26.71% |
| `run_submission.py` | 74.01% |
| `supported_sensing_envelope.py` | 100% |

The uncovered raster workflows and cached-context reader remain in the denominator. Their separate executed artifacts are not counted as coverage in this measurement. The runner's complete successful raster path was not exercised here. Coverage describes which code this suite executed, not scientific correctness or security; no percentage gate was imposed.

To repeat the measurement from the repository root in a separate diagnostic environment with NumPy 2.1.3 and Coverage.py 7.16.2:

```sh
python -m coverage run --branch --source=src -m unittest discover -s tests -v
python -m coverage report -m
python -m coverage json -o coverage.json
```

## Dependency advisory query

The audited version list matches `packages.log` in [the preserved Colab results archive](../evidence/engineering_04fa7c1_results.zip) exactly. That isolated Linux/Python 3.13.16 reproduction installed the three scientific pins and their Python dependencies. This audit queried those 16 exact versions, not the unrelated packages installed on the local computer.

pip-audit 2.10.1 queried the PyPI service backed by the Python Packaging Advisory Database on 12 October at 00:23 UTC. It returned exit status 0, 16 queried packages, zero skipped packages and zero reported advisories. The complete returned dependency/advisory list is in the measurement record. No dependency was automatically upgraded.

```sh
python -m pip_audit --no-deps --disable-pip \
  -r evidence/software_audit_packages_20261012.txt -f json
```

`--no-deps` is used because this input already lists the recorded transitive Python packages. The list is an environment inventory, not a dependency resolver or hash lock. It does not cover every supplementary-notebook environment, the Python interpreter, operating-system components or bundled native libraries such as GDAL. A zero-advisory result is dated database evidence, not a security clearance. See [pip-audit's security model](https://github.com/pypa/pip-audit#security-model).

### Additional declared and recorded versions

The [additional version list](../evidence/software_additional_packages_20261012.txt) covers five reference-context pins not in the baseline inventory, SymPy 1.14.0, and the Requests/Planetary Computer versions recorded by the original date-comparison archive. It is not a complete transitive inventory of all supplementary environments. The measurement record identifies their source artifacts and preserves the complete advisory response.

At 00:32 UTC, the same advisory service returned exit status 1 for these eight versions: four advisory records, representing **two distinct advisories** because each identifier appeared twice. No packages were skipped.

| Retained version | Advisory and affected operation | Reported fixed version |
| --- | --- | --- |
| GeoPandas 1.1.1 | CVE-2025-69662 / GHSA-6497-prx7-gpmq: SQL injection through the PostGIS database writer, `to_postgis()` | 1.1.2 |
| Requests 2.32.4 | CVE-2026-25645 / GHSA-gc5v-m9x4-r6x2: insecure temporary-file reuse when an application directly calls `extract_zipped_paths()` | 2.33.0 |

The [GeoPandas release notes](https://github.com/geopandas/geopandas/releases/tag/v1.1.2) identify the PostGIS fix. The [Requests maintainers' advisory](https://github.com/psf/requests/security/advisories/GHSA-gc5v-m9x4-r6x2) explicitly distinguishes direct calls to that utility from standard HTTP usage.

A static identifier check found neither affected function in the 42 tracked Python files and notebook code-cell sources, or in `compare_dates.py` preserved in the original date-comparison ZIP. That archived script uses ordinary `requests.get`; the reference-context workflow reads geospatial files rather than writing PostGIS tables. This establishes no direct call in the inspected team sources, not comprehensive dependency reachability or exploit testing.

The historical pins and executed archives remain unchanged for provenance. Neither affected package is in the isolated 16-package baseline inventory. For a new environment using either affected operation, use the reported fixed version or later and qualify that changed environment separately; the retained versions must not be presented as universally safe. No automatic upgrade or security clearance is claimed.

```sh
python -m pip_audit --no-deps --disable-pip \
  -r evidence/software_additional_packages_20261012.txt -f json
```

## Dependency-lock assessment

pip 26.2.1 successfully resolved all 16 recorded versions using wheel metadata for CPython 3.13 and Linux x86-64 manylinux targets, without installing the candidate environment. The resolution selected exactly the recorded version set, and every selected wheel had a published SHA-256. This supports availability and metadata-level compatibility; it does not verify a fresh Linux installation or imported native-library behavior.

We retain the exact recorded package inventory rather than publish a newly generated, untested lock. The three baseline pins in `requirements.txt` remain unchanged. A future optional hash lock needs installation and `pip check` in its named target runtime before being presented as tested. It must remain separate from the different supplementary environments. [pip's lock documentation](https://pip.pypa.io/en/stable/cli/pip_lock/) explicitly limits generated-lock validity to the target Python version and platform.

The audit improves software comparison checks and exposes the dependency/coverage evidence. It adds no independent cover labels, aircraft measurements or ecological outcomes.
