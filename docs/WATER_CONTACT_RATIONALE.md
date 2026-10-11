# A locally grounded EO-to-contact-sensing question

Updated 8 October 2026 | Proposed contact-sensing task; water observations and aircraft tests remain uncollected

## The concrete connection

How do water-column conductivity and temperature vary between authorized open-channel and accessible interior-water locations, with depth and tidal context recorded?

The proposed task has its own observation date, separate from the historical cover analysis. [Khor Kalba's official Ramsar record](https://rsis.ramsar.org/RISapp/files/RISrep/AE2125RIS.pdf), completed 1 September 2012, page 5, reports historical salinity differences between beach water (34-38 ppt) and the mangrove interior (38-44 ppt), with temperature variation. The section gives no measurement dates or sample count. These reports motivate investigation but cannot diagnose current harm or set a planting threshold.

| Link | What it supplies | What it does not supply |
|---|---|---|
| Frozen 2018 EO/reference review | Demonstrated evidence/date/quality handling and traceable unresolved cover questions | Current cover, current water properties or independent historical truth |
| Separate dated EO context | Actual 24 September 2026 provider RGB display and native SCL labels, with explicit interpretation limits | Mangrove field truth, water-column conductivity, sensor depth, navigable water or landing permission |
| Contact observation | Proposed calibrated conductivity/temperature, position, time, depth and tide/water-level records | Root-zone porewater, stress cause, carbon or planting suitability |
| Platform comparison | Proposed quality-matched whole-mission energy/time/cost and recovery comparison | A predetermined amphibious winner |
| Qualified evidence review | A future interpretation of accepted measurements against a defined question | Automatic intervention or established ecological benefit |

The local motivation applies to the site, not automatically to C027's historical excluded centres. Those 42 centres are not present sampling stations. C001/C017 photographic questions still have photographic comparators; contact sensing answers a different observable. No contemporary station or route is specified.

The [historical Kalba workbook](HISTORICAL_KALBA_FIELD_CONTEXT.md) contains November 2014 plot records and related soil-carbon/tree tables. Its dates, repeated/outside-AOI or missing coordinates, unspecified salinity scale and conflicting method scope prevent validation of individual review cases. It adds local field context, not current chemistry. A channel-water probe cannot substitute for borehole porewater, sediment cores or laboratory carbon measurements.

<a id="which-data-and-tools-earn-a-place"></a>

## Data selection and access

- **Use:** the already demonstrated Sentinel-2/GMW baseline and saved WorldCover context, preserving dates and shared-reference limitations.
- **Completed separate EO context:** native SCL and provider TCI windows from Planetary Computer item `S2C_MSIL2A_20260924T064621_R020_T40RDN_20260924T114716` (24 September 2026; PB 05.13) were acquired once in free Colab. The [dated figures, exact report and retained cache](DATED_EO_CONTEXT.md) supply display/product-label context, not a calibrated index, mangrove classifier or chemical measurement. Per-band provider encoding remains unresolved for the separate reflectance experiment; scene cloud percentage is not local quality. Reuse the cache, not another acquisition.
- **Hyperspectral candidate:** DLR's [EnMAP catalogue](https://geoservice.dlr.de/eoc/ogc/stac/) returns item `ENMAP01-____L2A-DT0000152124_20250911T072327Z_006_V010502_20250914T181224Z`, acquired 11 September 2025: 224 advertised bands, 30 m grid, scene cloud 19%. This establishes a catalogue intersection, not valid local pixels or a useful hyperspectral result. Data-asset requests returned login HTML, not the image/product XML. Authenticate lawfully and check correction/QA/rights before an experiment. The [public ARD default](https://www.enmap.org/data_access/) is land-mode correction, not an automatically valid aquatic product.
- **Do not substitute unrelated training data:** none of the 43 individual bboxes in the checked [Planet coastal-water collection](https://www.planet.com/data/stac/tanager-core-imagery/coastal-water-bodies/collection.json) intersects this AOI. Its union bbox and the starter notebook's UAE wording do not establish Kalba coverage. Other Planet collections were not ruled out.
- **Keep optional:** Landsat for a defined longer-term contextual question; GBIF for appropriate biodiversity context, not absence/species/health truth at these cells; geojson.io for geometry inspection, not navigation validation. Add them only where they change the evidence or decision.

The 2025 hyperspectral scene, recent EO and 2018 cover address different dates and questions. They cannot be combined into one accuracy or change result. Any future EnMAP analysis must follow the [data licence](https://geoservice.dlr.de/resources/licenses/enmap/EnMAP-Data_License_v1_1.pdf).

An anonymous image-URL request on 8 October returned HTTP 200 with `text/html;charset=UTF-8` and an HTML prefix, not raster bytes. The official [no-registration examples](https://www.enmap.org/data_tools/exampledata/) cover Tyrol, Groningen and Nevada, not this site. The [EnMAP-Box access documentation](https://enmap-box.readthedocs.io/en/latest/general/data_access.html) describes a registration exemption request through `enmap_registration@dlr.de` for people without institutional email. The team has not sent a request, received an exemption or created an account. Public metadata and unrelated samples cannot substitute for local spectral observations.

<a id="why-amphibious-support-is-a-testable-improvement-not-a-decorative-feature"></a>

## Testing water-supported sensing

The candidate mechanism is water-supported dwell: transport a suitable contact probe by air, obtain stationary accepted observations while supported, then recover it. This might reduce airborne dwell, but support mass, drift, transitions, sensing bias and failed recovery can offset the benefit. The team has not implemented this mechanism.

An [ordinary drone/boat comparison published in 2026](https://doi.org/10.1007/s10661-026-15473-0) covered three Irish lakes and 27 paired sonde comparisons. It estimated sampling times of 28 versus 45 minutes, with higher initial drone cost and variable-specific discrepancies. This freshwater study was neither an amphibious nor a Khor Kalba trial. Nonsignificant differences do not prove equivalence. Ordinary hovering probe delivery belongs in our comparison; ordinary drones can collect more than photographs.

Compare shore/boat probes, fixed loggers, USVs, ordinary hover delivery and supported delivery against the same observation contract. Prefer the least burdensome method that meets its acceptance and habitat/access constraints. Permissions, payload calibration and safe water operation still require qualification.

## One refutable task comparison

**Proposed task:** return quality-accepted, dated water-column conductivity/temperature records for an authorized open-channel station and an accessible interior-water station, with depth and tidal context. Test whether the observations resolve the specified station-scale question, not whether a canopy cell is damaged. Station selection, the required detectable difference and the complete uncertainty allowance must be fixed by the question and qualified measurement procedure before a trial; they are not populated here.

C027 is a historical locator and source-quality question, not either station's coordinates or a reason to expect a chemical anomaly. Current EO can help assess visibility and candidate access, but cannot certify navigability, safe water contact or permission. Use existing imagery for C001/C017's photographic questions; do not add contact hardware to answer cover alone.

**Mission unit:** one paired station visit, not an arbitrary tour of disagreement centres. Collect the open-channel and interior-water records close in time at a common specified depth, retaining actual sampling times and tidal/water-level context. A separate time-matched reference and repeated visits are needed where natural variation prevents interpreting the pair; one pair is not an estimate of an ecosystem-wide gradient. Stations and numerical tolerances remain unassigned pending site and measurement qualification. The primary UAE study's borehole porewater is a different sampling medium, not a calibration target for this visit. This mission can inform whether further water investigation is justified; it cannot authorize planting or diagnose mangrove stress by itself.

The [concrete sensor precedent](OBSERVABLES_AND_MEASUREMENT_CHAIN.md#a-concrete-sensor-precedent--not-a-selected-payload) separates a commercially available observable from an unbuilt delivery platform. Its response metric does not justify the illustrative model's favourable 150-second dwell. Start the comparison with an independently justified observation and measure its actual time to acceptance.

| Comparison step | Control that makes it discriminating | Outcome that attacks the proposed advantage |
|---|---|---|
| Controlled-water measurement-chain test | Same complete calibrated probe/logger assembly, depth and predefined acceptance procedure; independent reference and checks for immersion/thermal response, contamination and craft disturbance | Supported delivery cannot provide equivalent accepted observations, even if it uses less propulsion energy. |
| Authorized site comparison | Same qualified stations where methods can safely reach them; interleave/randomize method order where practicable, retain actual time/tide/depth and a time-matched reference to diagnose natural variation | A station/time/access difference explains an apparent platform difference. Do not compare easy shore water with different interior water and call it a quality comparison. |
| Complete resource comparison | First include shore/boat or fixed logging where it answers the question, then ordinary hover delivery versus supported delivery; record transit, placement, stabilization, retries, retrieval, preparation/operator effort and all relevant energy sources | A simpler method meets the same contract with lower burden, or support fails to improve the predeclared outcome once rejects and recovery are included. |

A fixed logger's time series answers temporal variability differently from a mobile spatial visit; compare only an explicitly common information requirement. A method that cannot safely reach a station fails that access requirement; do not invent its measurements or a favorable cost. Battery energy, operator effort, elapsed time and habitat disturbance remain separate outcomes, not an arbitrary weighted score. A task with zero accepted records is a failed mission, not a division-by-zero value omitted from evaluation.

Before any trial, define the conditions for retaining the amphibious branch: it must pass access/habitat and measurement-quality checks and demonstrate the stated task-specific advantage against a suitable simpler comparator. If short accepted dwell applies, the saved short-dwell counterexample challenges the energy rationale. If sustained contact is required, test whether the measured benefit survives mass, transitions, drift and recovery. Duration alone does not determine whether support succeeds. Neither outcome validates 2018 cover, mangrove health, planting need or ecological benefit. These trials have not been performed.

<a id="conditional-analytical-claims-that-withstand-scrutiny"></a>

## Conditional design and resource bounds

With aircraft/payload mass `m0`, support mass `mf`, allowable displacement `Vallow`, water density `rho_w`, condition-specific usable thrust `Tusable`, tilt `theta`, declared lift margin `gamma >= 1`, and gravity `g`, simultaneous static buoyancy and vertical-lift constraints imply:

`mf <= min(rho_w * Vallow, Tusable * cos(theta) / (gamma * g)) - m0`.

This is a necessary design envelope, not a selected craft's performance. Inputs are unknown here, support geometry/mass are coupled, and any reserve already included in `Tusable` must not be counted twice. [Buoyancy](https://openstax.org/books/university-physics-volume-1/pages/14-4-archimedes-principle-and-buoyancy) does not establish [small-angle restoring stability](https://farside.ph.utexas.edu/teaching/336L/Fluidhtml/node29.html), wet takeoff or recovery. An empty envelope rejects that specified design; a nonempty envelope does not validate it.

For equal attempted tasks, common per-attempt acceptance rates `pH,pS > 0`, and expected whole-mission resources `EH,ES,TH,TS`, supported sensing improves both aggregate energy and time per accepted record only if:

`pS/pH > max(ES/EH, TS/TH)`.

This follows directly from comparing ratios of expectations; it is not an expected per-mission ratio. For heterogeneous tasks use the expected accepted count `sum(p_i)`. The earlier illustrative main case saves energy but takes longer at equal assumed acceptance. No measured acceptance rates, resource advantage or superiority over a UAE product are supplied.

The separate [supported-sensing envelope source](../supplementary/Mangrove_Pulse_Supported_Sensing_Envelope.ipynb) implements these conditional screens, strict dwell-advantage boundaries and explicit counterexamples using standard-library Python only. The [actual downloaded executed companion](../supplementary/Mangrove_Pulse_Supported_Sensing_Envelope_Executed.ipynb) completed on free CPU Colab on 8 October: 26 synthetic tests passed, three cells executed and no error outputs. The [results ZIP](../supplementary/Mangrove_Pulse_Supported_Sensing_Envelope_Results.zip) and [61-check returned-artifact review](../evidence/supported_envelope_colab_review.json) verify exact sources, hashes, empty records and unknown inputs. The source and preparation rationale were preserved as run, so their earlier unexecuted wording is historical preparation context, not the current run status. No additional dataset upload was required. Software/algebra verification is not physical validation; default aircraft inputs remain unknown.

## Acceptance before interpretation

The [blank water-context question contract](../examples/inspection/water_context_question.json) requires a separate date, authorized station definition, selected calibrated sensor, units/conversion, depth/time/position/tidal context, rejection rules and matched comparator. Its station list and observations are empty. No arbitrary success tolerance is populated without a sensor specification and decision requirement.

The [observable and measurement-chain audit](OBSERVABLES_AND_MEASUREMENT_CHAIN.md) distinguishes our EO outputs from station-scale contact observations, and in-situ conductivity from temperature-compensated specific conductance. Version 1.1 requires declarations for calibration, pressure/depth, salinity scale/conversion domain and uncertainty; their values and an acceptance validator remain unspecified. Historical "ppt" cannot automatically be interpreted as dimensionless Practical Salinity or Absolute Salinity in g/kg. Earlier executed companions retain their original preparation snapshots.

Water-column salinity is not porewater salinity. A colour/index is not chlorophyll concentration, harmful bloom toxicity or ecological damage. A measurement is useful only if it meets the contract and helps a qualified interpretation. Any planting or ecological-benefit claim still needs the [separate evidence protocol](VALIDATION_AND_BENEFIT_TESTS.md).

The completed work provides a sourced local research question, separately dated Sentinel-2 SCL/TCI context, verified candidate catalogue records and conditional inequalities. Calibrated reflectance indices, usable local hyperspectral pixels, accepted water observations, aircraft feasibility, independent 2018 accuracy and ecological improvement remain unestablished.
