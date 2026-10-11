# Mangrove Pulse: Khor Kalba to proposed drone inspection

7 October 2026 | Historical evidence handoff | No flight, field visit or planting performed

<a id="what-the-poc-now-connects"></a>

## Observation handoff

The satellite workflow identifies questions for review, rather than confirming damaged sites. This companion turns three Khor Kalba cases into observation requests for a future inspection platform, including the team's amphibious "hyper drone" concept. Locations and evidence come from saved analysis outputs. Observation methods are proposed, and return fields are empty.

Satellite evidence -> case-specific question -> observation-method selection -> quality-checked observations -> human review.

The machine-readable [requests](../examples/inspection/inspection_requests.json), [85 original cell-centre points](../examples/inspection/inspection_targets.geojson) and [blank return template](../examples/inspection/observation_return_template.json) make the handoff traceable. The optional [Colab handoff notebook](../supplementary/Mangrove_Pulse_Inspection_Handoff.ipynb) exports these and an 85-row blank observation CSV without new data uploads, package installation or satellite processing. This is a format/export demonstration, not drone control or the main scientific notebook.

The implemented work includes the frozen satellite analysis, reference sensitivity, review briefs and structured handoff. Collection and return of observations remain proposed. Their usefulness, aircraft capability, hyperspectral sensing, safe field access, restoration and comparative advantage remain unvalidated.

## Three different questions, not one generic drone mission

| Case | Existing evidence | Requested observation | Why a drone might help / what it cannot prove |
|---|---|---|---|
| C001: canopy-edge ambiguity, 11 centres | Prediction positive/GMW v3 unmapped; v4 maps 7; WorldCover 2020 classifies 11 as mangroves | Dated cover evidence, canopy boundaries, qualified vegetation identification and measured alignment | Overhead RGB could document current boundaries if lawful and safe. An ordinary aerial platform or existing imagery may suffice. Today's photographs cannot determine November 2018 truth. |
| C017: mixed/open cover, 32 centres | Prediction negative/v3 mapped; v4 maps 6; WorldCover 2020 has 21 mangrove, 7 bare/sparse and 4 wetland centres | Cover composition across each cell and surroundings, with visibility and uncertainty; fractions only where supported | Detailed, aligned photographs could support mixed-cover interpretation. Colour or a spectral response alone does not establish species, health, loss or planting need. |
| C027: channel-margin coverage gap, 42 centres | Quality excluded/v3 mapped; 40 still excluded on Nov 30; v4 maps 36; WorldCover 2020 includes 28 mangrove and 9 water centres | Inspect source quality and historical cover separately; a future current visit could document channel-edge visibility | An aerial view could address current observation gaps. Water-supported contact sensing is a separate conditional task, not evidence that exclusions were caused by tides or that water landing is possible. |

The counts describe map labels at centres, not mapped hectares, confirmed vegetation or damaged cells. Original categories remain unchanged. GMW releases share lineage; WorldCover is later-date/shared-source context, not independent 2018 validation. [Full case evidence](CASES.md).

## Where amphibious capability could earn its place

The [connected concept assessment](CONNECTED_CONCEPT_ASSESSMENT.md) links each observation question to simpler alternatives, physical screens (including forced Euler dynamics), measurement acceptance, full mission costs and a separate ecological decision. Its optional no-upload Colab companion leaves unknown engineering inputs unfilled. Mathematical conditions cannot establish a working drone, historical truth or deployment approval.

[Published local evidence](KHOR_KALBA_SITE_EVIDENCE.md) documents earlier drone mapping and field sampling at Khor Kalba. Those studies inform method selection but cannot validate the historical cells, establish current ecological need or prove that our platform improves on prior work.

For C001/C017 photographic questions, compare existing licensed imagery, shore photography, boat-based observation and an ordinary RGB drone before requiring amphibious hardware. No evidence currently establishes the proposed platform as the best option.

A practitioner might define a separate current water-contact task in the C027 channel context, such as recording conductivity/salinity, temperature and sampling depth at justified sites. These candidate measurements would provide local context, not diagnoses of canopy condition or proof of restoration suitability. The PoC has no selected or calibrated sensor and no water measurements. A canopy-cell centre is not automatically a safe or scientifically suitable water-sampling location.

These water-column readings are distinct from soil-core, borehole-porewater and laboratory carbon measurements in historical field studies. A channel probe cannot reproduce those measurements or validate their historical values; they require a separate access/sampling method and measurement chain.

The [locally sourced water-contact rationale](WATER_CONTACT_RATIONALE.md) grounds this branch in an official historical Khor Kalba water-property description, rather than the optical exclusion alone. Its [empty contract](../examples/inspection/water_context_question.json) defines the question without inventing stations, tolerances, permissions or observations. The separate [actual 24 September 2026 SCL/TCI context](DATED_EO_CONTEXT.md) adds dated site display/product labels, not current chemistry, mangrove truth, change or a causal explanation of the historical exclusions. EnMAP access remains unresolved; no local hyperspectral result or ecological diagnosis is claimed.

A water-supported platform could be useful if an agreed observation requires sustained contact and simpler access methods cannot deliver equivalent accepted measurements safely. It must first demonstrate safe transitions, stable sensing, retrieval and comparable data quality. Mud movement and planting are not needed to demonstrate this handoff and remain separate research hypotheses.

### Existing analytical energy evidence: conditional, not site validation

The team already ran MP-DRONE-ENERGY-01 in Colab on 30 September. A [selected verbatim result extract](../examples/inspection/energy_scenario_excerpt.json) preserves all five illustrative cases, assumptions and source/archive hashes; no model was rerun for this integration.

The unchanged [calculation source](../examples/inspection/energy_source/sampling_energy_model.py), [15-test source](../examples/inspection/energy_source/test_sampling_energy_model.py) and [original delivered Colab notebook](../supplementary/Mangrove_Pulse_Drone_Sampling_Energy.ipynb) support inspection and optional separate Colab reproduction. They use hypothetical parameters, not the 85 geographic targets. The packaged notebook copy does not establish a new verified execution.

| Hypothetical task | Hover energy | Water-supported energy | Meaning under assumed inputs |
|---|---:|---:|---|
| 30 s contact sampling per site | 88.8 Wh | 124.0 Wh | Added mass/transitions make support worse. |
| 150 s per site | 170.7 Wh | 128.0 Wh | About 25.0% lower energy, if equal-quality contact observations are possible. |
| Main case plus 80 Wh extra overhead | 170.7 Wh | 208.0 Wh | The advantage reverses. |

Main assumptions: 8 kg baseline plus 2 kg support kit; 0.8 m² effective rotor area; uncalibrated loss factor 1.6; 25 W common airborne load; 40 W total supported load; 300 s hover-equivalent travel; 3 hypothetical sites; 150 s dwell/site; 30 extra airborne transition seconds/site; zero other overhead; 240 Wh nominal battery, 80% usable; reference air density 1.225 kg/m³. None is a measured Khor Kalba mission requirement. The three assumed sites are **not** the three review clusters or a route between them.

The saved break-even dwell is 84.2 s/site for those assumptions only. Accounted mission duration increases from 750 to 840 s. Equivalent observation quality, mass/battery compatibility, waves, drift, corrosion, failed transitions, recovery and full mission costs remain untested. The 864 arbitrary sensitivity combinations are not success probabilities. This result neither proves the full concept feasible nor establishes superiority over any UAE drone or restoration programme.

<a id="hyper-and-hyperspectral-separate-claims"></a>

## "Hyper" and hyperspectral: separate claims

"Hyper drone" names the team's concept, which has no working hyperspectral payload. The implemented EO inputs are multispectral Sentinel-2, GMW reference maps and later WorldCover context. No hyperspectral scene covering Khor Kalba or drone spectral measurements have been processed.

A future hyperspectral experiment must first verify local coverage, acquisition date, usable spatial/spectral detail, quality and redistribution rights. It must test added information against a matched simpler baseline using appropriate independent labels and a fresh spatial evaluation. Do not attach generic Indian Pines training results or an unrelated scene as evidence of Khor Kalba capability. EO remains the PoC core; a drone supplements it.

<a id="observation-contract-and-acceptance-gates--proposed"></a>

## Proposed observation contract and acceptance gates

1. **Before deployment:** establish current inspection purpose, access permission, operational authorization, habitat protection, safe launch/recovery and a qualified responsible operator. All are currently unconfirmed. Refresh current EO and assess whether the historical locator remains relevant. Choose safe observation positions separately; never import these centres as autopilot waypoints or landing targets.
2. **At collection:** retain case/cell IDs; record actual acquisition time with timezone, actual sensor position in WGS84, measured/estimated positioning uncertainty, method, visibility/occlusion, instrument/calibration details where applicable, evidence file and redistribution permission. Original cell-centre coordinates are target references, not measurements of the sensor's location. For photographs, distinguish the camera/aircraft position from the observed organism and area: record camera direction/pose, mapped ground footprint and registration uncertainty where available. A ground/oblique image or geotag without that spatial support cannot label an entire 20 m cell; retain the label as unresolved when footprint or visibility is insufficient. These are proposed collection requirements, not fields enforced by the existing exporter or a surveyed aircraft result. The [dated occurrence review](HISTORICAL_KALBA_FIELD_CONTEXT.md#a-dated-alternative-site-field-presence-lead) demonstrates this failure mode using an actual third-party photograph.
3. **At interpretation:** relate observations to the original 20 m cells only when visibility and measured alignment justify it. Report position uncertainty and assess it for the particular task; no universal GNSS tolerance is specified. Qualified identification is required before asserting mangrove identity. Fractions require adequate coverage and a documented labelling method.
4. **At return:** keep unobserved, rejected and unresolved distinct. The template contains nulls rather than fabricated values. No absence inference from missing observations. Record a cell-specific conclusion, supporting evidence, reviewer and remaining uncertainty before accepting an interpretation.
5. **Temporal gate:** contemporary observations describe their own date. Independent 2018 evidence is required to interpret historical truth; today's inspection alone cannot resolve it. A new current-date experiment must not change the frozen historical scores.

A future method comparison should measure accepted observations per attempted target, positional/visibility quality, total mission energy and time, recovery failures, operator effort and habitat disturbance. Include a shore/boat or ordinary-drone comparator appropriate to the observation. Specify success criteria before testing; do not infer performance from this export's 85 rows.

<a id="what-this-improvement-claim-actually-means"></a>

## Demonstrated contribution and remaining tests

The demonstrated contribution is a traceable PoC output: each proposed observation has an EO-derived reason, exact original identifiers and an explicit uncertainty/return contract. Its usefulness to practitioners remains a hypothesis. Amphibious sensing is a candidate extension whose advantage over existing restoration platforms remains unestablished. Planting, survival and carbon benefit require separate ecological and intervention evidence.

<a id="current-checkout-schema-hardening--9-october"></a>

## Blank-template validation

The [validator](../src/inspection_handoff.py) requires schema `1.0`, exactly the canonical 20 observation fields and null values. It rejects unsupported schemas, missing/extra fields and populated templates. This is a blank-package exporter, not an importer or validator of collected observations. An earlier version accepted a nonempty subset of null fields and could omit required CSV columns; the canonical request/return files themselves are unchanged.

The [17 local metadata tests](../tests/test_inspection_handoff.py) passed, including deletion of every required field and complete CSV-header/source-identity checks. [Test provenance](../evidence/inspection_handoff_unit_tests.json) preserves the earlier 14-test record separately from this recheck. No satellite processing, aircraft calculation or field validation ran locally. The original 7 October executed notebook and embedded historical snapshots are unchanged and do not contain this fix; no new Colab execution is claimed. The additional proposed camera-footprint and contact-measurement acceptance requirements above remain outside this template validator.

## Evidence and attribution

Coordinates and original audit fields are copied from [the frozen register](../examples/audit/all_audit_cells.csv); added map labels come from [the completed reference-context records](../examples/reference_context/audit_cells_with_context.json). No new spatial inference, route, flight plan or priority ranking is made. Cases were previously selected as the largest cluster per audit category, not by ecological urgency.

The energy extract identifies the preserved returned ZIP SHA-256 `02f81a56f34b7c8d9f92e5e830567207a748c6e483d97773158f6663806393b5`. Its theoretical calculation source is cited in the extract; a literature citation does not calibrate our hypothetical parameters. Original scientific sources and the main notebook remain unchanged.

Contains modified Copernicus Sentinel data (2018). GMW v3/v4.1.12 and WorldCover-derived context retain [attribution and modifications](../ATTRIBUTION.md). Original-code rights are described in [the rights notice](../LICENSE_NOTICE.md).
