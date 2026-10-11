# Provenance and scope of reproduction

## Sensor lineage and radiometry qualification (12 October 2026)

The item metadata inside [the cached comparison ZIP](../data/Khor_Kalba_Date_Comparison_Results.zip) records processing baseline **02.12** for both Sentinel-2B dates; the B04/B08 asset paths also identify `N0212`, relative orbit `R020` and tile `T40RDN`. These are the exact cached products, not another reprocessing of the same acquisition.

Copernicus [Level-2A documentation](https://sentiwiki.copernicus.eu/web/s2-products) describes surface-reflectance products and the additive BOA offset introduced with baseline 04.00. For unmodified pre-offset red/NIR values with a common multiplicative scale, that scale cancels in `(mean NIR - mean red) / (mean NIR + mean red)`: the ratio equals NDVI of the mean reflectances. This is not the mean of four pixel-level NDVI values. The [baseline source](../src/reference_baseline.py) averages four native pixels per band and rejects nonpositive, nonfinite or nodata subpixels before calculating the ratio. The archived comparison source preserves November 30 DN values during window extraction, filling masked values with zero; display stretching is separate.

The cache does not retain the original baseline-02.12 product XML for either date or the complete first-date crop-extraction source. Exact product quantification and the first-date transformation chain are therefore not independently verified here. We retain the feature name **normalized red/NIR DN contrast**, with the common-scale NDVI equivalence conditional on those checks. Neither interpretation establishes mangrove identity, health or ecological change. The smallest remaining radiometry check is to obtain only the two exact product metadata files and qualify the original first-date crop preparation; no imagery reacquisition or threshold change is needed.

GMW v3's annual maps use L-band SAR-based change mapping from the GMW v2.5 baseline, whose development combined optical and radar evidence. The source mosaics have 25 m spacing. Our optical 20 m diagnostic cells and the reference differ in measurement physics, spatial support and preparation; disagreements do not identify which source is wrong. See the [GMW v3 dataset](https://doi.org/10.5281/zenodo.6894273) and [methods paper](https://doi.org/10.3390/rs14153657).

The separate comparison uses **GMW v4.1.12 2018 vector membership**, not an independently labelled 10 m truth image. The [versioned provider record](https://doi.org/10.5281/zenodo.21346457) describes a timeseries built from the v4.0 10 m baseline, optical classifications, L-band SAR evidence and temporal filtering. A baseline's resolution is not the diagnostic grid or proof of local accuracy. Shared lineage, product construction and vector-versus-raster sampling remain relevant transfer limits.

The [WorldCover 2020 v100 manual, page 10](https://esa-worldcover.s3.eu-central-1.amazonaws.com/v100/2020/docs/WorldCover_PUM_V1.0.pdf#page=10) explicitly includes GMW among auxiliary datasets used in expert rules that modulate class probabilities. WorldCover's later date and shared auxiliary lineage prevent treating its mangrove class as independent November 2018 truth.

The [official hackathon description](https://spaceacademy-hackathons.space.gov.ae/) permits multiple EO data types and describes demonstrated hyperspectral added value as a bonus rather than a requirement. Our Tarif qualification shows bounded spectral-data access, not a mangrove improvement; it does not establish that bonus result.

## Notebook presentation revision (10 October 2026)

`Mangrove_Pulse_Review.ipynb` is the main output-bearing reading copy. Its Markdown explains the recorded 7 October run; code, embedded inputs, execution counts and outputs remain from that run. The executed notebook also has presentation-only Markdown revisions. Neither copy is a new execution or incorporates later code repairs into the historical run.

The reproduction source, `Mangrove_Pulse.ipynb`, has Markdown-only presentation edits. Its executable cells, metadata and empty output records are unchanged. The original source remains in the team's local archive; the revised notebook is not a new execution.

The [SymPy source notebook](../supplementary/Mangrove_Pulse_SymPy_Resource_Audit.ipynb) has revised explanatory Markdown and omits one setup print. Its mathematical and export code are unchanged. The original prepared source remains in the team's local archive; the [executed notebook](../supplementary/Mangrove_Pulse_SymPy_Resource_Audit_Executed.ipynb) and [returned results](../supplementary/Mangrove_Pulse_SymPy_Results.zip) remain intact. The source revision has no saved outputs and is not presented as a new execution.

The connected-concept and supported-sensing source notebooks also have revised explanatory Markdown. Their code, embedded preparation notes, metadata and empty output records are unchanged. Those dated notes are labelled as archival and linked to current interpretation guides; the original executed companions retain their recorded wording and outputs.

Claim-validation, inspection-handoff and cache-replay source notebooks have Markdown-only presentation edits. Claim-validation wording explicitly distinguishes ratios of expected totals from expected per-mission ratios; its calculations are unchanged. The handoff points to the executed main demonstration, and replay documentation describes retained inputs without narrating an earlier upload. Original sources remain preserved; no execution outputs were added or rewritten.

The energy-study, reference-context and end-to-end source notebooks also have Markdown-only edits. The reference companion retains its existing-session recovery instructions and distinguishes the repaired source from the completed earlier experiment. The end-to-end source corrects the old wording that treated choosing a code licence as mandatory. All calculation code, embedded inputs and original executed records remain unchanged.

The C001 reading notebook has revised prose and standard anchor links. Its embedded figures, data blocks and source-fingerprint table retain the original preparation snapshot. It links to the current Markdown decision contract and separate Tarif results without merging their evidence. The original remains in the team's local archive.

The earlier HTML viewers are retained in the team's local archive. They are not part of this repository; the review briefs cite the recorded metadata and qualitative notes.

The baseline/audit input is [Khor_Kalba_Date_Comparison_Results.zip](../data/Khor_Kalba_Date_Comparison_Results.zip), identified in [source_archives.json](../evidence/source_archives.json). It contains the small November 20 and November 30 crops, source item metadata, fixed GMW mask, previous input hashes, grid/quality comparison and attribution. This cached input archive was not regenerated during repository assembly; it is distinct from the later run-result archives.

The two src analysis engines were recovered byte-for-byte from the successful returned result ZIPs. The baseline module docstring uses team-facing wording; both engines retain their original execution logic. The run_submission.py runner and main notebook orchestrate those engines and check their outputs against saved examples. Initial static checks were followed by a successful 2026-09-28 cached reproduction. See `evidence/verified_run/` for the recorded status, checks and original package manifest.

Original acquisition sequence: pixel inspection → GMW overlay → November 20/30 comparison → northern threshold calibration/southern evaluation → disagreement audit → three-point Wayback metadata query → visual review. Computational reproduction begins with the cached comparison ZIP. It does not retest remote satellite acquisition, regenerate source preprocessing or requery Wayback.

The baseline reproduction repeats the original deterministic northern-only selection rule and must return 0.49. This is reproduction of the frozen experiment, not permission to retune it. It checks all saved baseline summary values, the experiment plan and the audit summary, the audit cell/cluster tables, and decoded prediction/split rasters. Plot bytes may differ by environment and are not an accuracy test.

The assembled runner uses fresh output directories. The original case checks predate visual review; [CASES.md](CASES.md) and the case-review records retain the qualified observations.

Observed Python for baseline/audit: 3.13.15; NumPy 2.1.3, Rasterio 1.5.1, Matplotlib 3.10.0. The three direct package versions are pinned in requirements.txt; the Python patch version is an environment observation, not enforced by that file. The original assembled cached run passed; this does not guarantee installation in every future runtime. Provider changes can affect browser basemap loading. No new screenshots, field labels or ecological validation were produced during this documentation revision.

The source archive hashes identify the original inputs. `SHA256SUMS.json` covers the repository files. Verification uses file hashes, JSON/CSV values and syntax checks, not a new satellite analysis.

<a id="recovery-and-documentation-revision--2026-09-29"></a>

## Recovery and documentation revision (2026-09-29)

The original repository was recovered from a locally saved archive and extracted copies. All 59 files in the successful run's package manifest matched before editing. The original archive SHA-256 is `fa52ed26680d2a6e543e2e4ad7e15deb86540c8461c2ac389cdd0e54628432d7`; an unchanged backup is preserved outside this submission folder.

That revision updated the README, notebook Markdown, scope documentation and runner module description, and added an inspection brief. Every executable notebook cell retained its original contents. Analysis-engine execution logic, data, thresholds, split, reference labels and saved predictions were unchanged. The current `SHA256SUMS.json` describes this repository, while the manifest under `evidence/verified_run/` identifies the earlier tested bytes.

<a id="separate-reference-supplement--2026-10-02"></a>

## Separate reference supplement (2026-10-02)

Experiment MP-REFERENCE-SENSITIVITY-01 completed in the team's Colab session on 2026-10-01. Eighteen exact returned files are included under `examples/reference_context/`, including tables, per-centre context, maps, source, tests, methods, attribution, environment and run checks. `INCLUDED_PAYLOADS.json` identifies their source archive and byte hashes. The original archive is preserved outside the submission; its duplicate/self-hashed manifest and stale failure note are excluded from the curated supplement. The completed status supersedes the returned method plan's pre-run wording. See [the supplement review](REFERENCE_SENSITIVITY.md).

The [reference-context source notebook](../supplementary/Mangrove_Pulse_Reference_Context.ipynb) includes plotting-backend and packaging repairs made after the successful 1 October run, and has no stored execution outputs. That run used a plotting-backend environment workaround. Its exact returned calculation source is [reference_context.py](../examples/reference_context/reference_context.py); the subsequent repairs did not change scientific sampling. Reproducing this supplementary study requires its own inputs and dependencies, separate from the core baseline runner; this does not make its reference maps scientifically independent.

The 13,401-centre full-AOI reference comparison does not update the original southern baseline metrics or establish field truth. WorldCover represents 2020 and uses GMW auxiliary input. Existing data, original model examples, main notebook and baseline/audit/runner source remain unchanged by this integration. Local checks cover byte preservation, JSON consistency, notebook syntax, links and manifests only. No local geospatial analysis or new field evidence was produced.
