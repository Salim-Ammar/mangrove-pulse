# Connected concept assessment: observation first, aircraft second

Updated 9 October 2026 | Proposed engineering assessment, not a prototype or deployment plan

## The complete connection

Historical satellite evidence -> unresolved question -> dated observation contract -> simplest suitable method -> physical and measurement checks -> accepted evidence -> qualified decision -> separately tested ecological outcome.

The completed PoC supplies the first two links and a traceable [observation handoff](DRONE_KHOR_KALBA_HANDOFF.md). Flight performance, independent 2018 truth and ecological outcomes remain unmeasured. The team reconfirmed on 7 October that the drone is still concept-only. Mathematics can identify necessary conditions and reject inconsistent assumptions, but cannot supply missing observations.

| Evidence branch | Decision-relevant observation | Appropriate first comparison | Amphibious connection |
|---|---|---|---|
| C001, 11 original centres | Dated identifiable canopy and edge alignment | Licensed near-date imagery for 2018; separately, shore/boat imagery or ordinary RGB aerial imagery for current cover | Contact sensing does not answer the photographic question. No amphibious requirement established. |
| C017, 32 centres | Mixed-cover composition, visibility and qualified interpretation | The same photographic alternatives, with adequate coverage of the whole cell and surroundings | A spectral or water reading is not a cover fraction or species label. |
| C027, 42 centres | Historical optical quality/cover uncertainty; separately, a justified current channel observation | Source-quality review first; current photography if warranted. For a separately justified contact task, compare shore/boat probe, USV and hovering or floating platforms | Sustained contact is a candidate use, not a consequence of the exclusion flag. Sampling positions require a fresh site assessment. |

The 85 centres are historical references, not sampling stations, routes or landing coordinates. These selected cases are not an accuracy sample. A current visit cannot directly validate the 2018 map. [Site-specific published context](KHOR_KALBA_SITE_EVIDENCE.md) confirms older drone mapping and sediment sampling at Khor Kalba, not the performance of our concept.

The [water-contact rationale](WATER_CONTACT_RATIONALE.md) asks a separate local question about dated, depth- and tide-referenced water-column conductivity/temperature across suitable channel/interior-water locations. The historical official site record motivates this question; C027's exclusion flag does not. Stations, current water properties, sensor requirements and the best delivery method remain to be established. A separate Colab run supplies [24 September 2026 native SCL/provider TCI context](DATED_EO_CONTEXT.md), which cannot establish water chemistry, mangrove field truth, change or aircraft need. EnMAP remains a catalogue candidate because asset access returned a login page. The analytical notebook and returned ZIP retain the note used at preparation time.

## What must enter the assessment

The assessment needs the following parameter families, though they do not cover every environmental interaction. Each value needs units, provenance, date/conditions and an uncertainty range. Leave unknown inputs unknown, and distinguish literature or assumed design values from team measurements.

| Family | Required information | What changes the conclusion |
|---|---|---|
| Observation and dates | Intended decision, observable, historical/current date, acceptance rule, independent reference lineage | A useful current observation can still be invalid for historical accuracy. No information benefit is established without a decision and acceptance rule. |
| Access and habitat | Permissions, protected habitats, seasonal wildlife, launch/retrieval, qualified operator, lawful flight/contact constraints | A resource advantage cannot override a habitat or access constraint. Neither coordinates nor this assessment authorize deployment. |
| Mass and flight | All-up wet mass, payload/float/battery mass, air density, thrust at conditions, rotor/actuator limits, peak power, centre of mass | A heavier float kit can erase energy savings or exceed lift/battery limits. Payload must fit the same aircraft budget. |
| Water support and dynamics | Displacement/freeboard, hull geometry, centre of buoyancy, restoring stability, inertia, wind/waves/current, wet takeoff, net torque, drag, tether | Enough buoyancy does not imply upright stability, station keeping or recoverability. A tether can add forces and contaminate the measurement. |
| Sensing and optical quality | Sensor calibration/response, depth, tide, positioning/alignment, coverage/occlusion, GSD, illumination, vibration, contamination and craft-induced disturbance | A longer dwell helps only if it yields an accepted measurement; rotor wash, stirred sediment or probe drift can bias it. Conductivity is not automatically calibrated salinity. |
| Whole mission and reliability | Transit and all transitions, sampling, electronics, retries, recovery, battery derating, reserve, operator effort, failed/zero-success attempts | Compare complete costs, not motor-off dwell alone. Failures and recovery can reverse a nominal advantage. |
| Navigation and links | Actual positioning error, antenna height, line of sight, logged packet delivery, loss-of-link behaviour, onboard recording and safe recovery | Satellite target coordinates are not measured aircraft positions; a relay aircraft adds its own energy, operator and disturbance costs. |
| Ecology and economics | Baseline habitat/recruitment, hydrology/sediment, alternatives including no action, repeated controls, disturbance, cost, maintenance and lifecycle | More measurements or planted seedlings are not automatically better ecological outcomes. Carbon needs separate accounting. |

Hyperspectral, mud mobility, planting, solar, fleet coordination and communications are separate hypotheses. Add each only if it solves a defined observation or operational requirement and survives a matched simpler baseline. The [separate Tarif source/crop run](TARIF_SCENE_QUALIFICATION.md) does not demonstrate mangrove classification or hyperspectral improvement; no implemented drone payload is claimed.

## Mathematics that is useful now

### Demonstrated components and the proposed integration

Published prototypes establish some component precedents. Their demonstrations remain separate from our implemented software and unbuilt aircraft:

| Component | Published physical precedent | What our integration must still establish |
|---|---|---|
| Drone-assisted seedling placement | [SkyPlanter](https://portal.findresearcher.sdu.dk/en/publications/skyplanter-aerial-reforestation-with-an-ultralight-seedling-plant/), developed by NIBIO/SDU, reports terrestrial planting trials with a pneumatic insertion/soil-compaction mechanism. [NIBIO's prototype account](https://nibio.no/en/news/can-drone-mounted-tree-planting-replace-manual-tree-planting) records pilot operation and hard-soil/capacity limitations. | This is **seedling** placement, not our original **bio-seed-pod** proposal. No pod-to-seedling design change is adopted here. Mangrove planting need, substrate compatibility, placement quality and establishment remain separate questions; these trials are not our results. |
| Amphibious sensing | The separately cited Japanese pond study below physically tested amphibious sensing and relay links, reporting consequential flight, communications and sensor limitations. | Saltwater compatibility, wet transitions, station keeping, recovery and an accepted local observation under UAE conditions. Do not combine capabilities from separate prototypes and call the combined craft demonstrated. |
| EO-to-observation handoff | Our executed Kalba workflow preserves historical evidence and exports case-specific requests with blank returns. | Connecting an actual permitted observation to the request, then comparing decision usefulness and complete mission resources. This software output is not aircraft performance. |

Can flight access plus water-supported sensing deliver a specified, quality-accepted mangrove-channel observation more usefully than shore/boat, fixed logger, USV or ordinary-drone alternatives? The proposed contribution is an evaluated integration for a defined task. Drone planting and amphibious sensing have precedents; this review establishes neither novelty nor superiority for our concept.

### UAE comparison: monitoring already exists

The [2023 ADNOC/Distant Imagery conference paper](https://doi.org/10.2118/215963-MS) describes a drone-restoration pilot on the Abu Dhabi coast. The review checked its identity and Crossref abstract, but could not retrieve full methods/results; the publisher page returned 403. That abstract alone cannot establish survival or efficiency.

ADNOC's [2024 sustainability report, Mangroves section, p. 93](https://reports.adnoc.ae/e/sustainability-report-2024) describes aerial seed dispersal alongside machine-learning/NDVI monitoring and replenishment. Its summary/body use inconsistent seeds/mangroves wording; no matched survival cohort or method comparator is supplied in that section. Do not divide its program totals into a survival rate or infer why replenishment occurred.

The UAE baseline already includes monitoring. Gaps in published detail do not establish gaps in capability. Our proposed improvement must therefore demonstrate a task-specific contact observation under matched quality requirements, with complete resource and habitat tradeoffs. Adding monitoring, spectral bands or planted units would not establish that improvement. The historical Kalba cases demonstrate a traceable handoff, not an advantage over the UAE program. Its Abu Dhabi outcomes cannot be transferred to Khor Kalba or our aircraft.

**Optical component precedent, not our payload:** [Yang et al. (2024), Methods 2.2.2 and Results 3.2](https://www.mdpi.com/2072-4292/16/16/3093) used UAV multispectral/hyperspectral imagery with 2023 field surveys in Guangxi. They report LightGBM overall accuracy of 80.96%/97.15%, respectively. Different aircraft/sensor packages prevent attributing that contrast solely to spectral richness. Their abstract says all hyperspectral models exceed 91%, while the body gives AdaBoost 82.96%; retain the conflict. Indexed primary text was inspected; full tables, validation separation and raw-data access were not verified. This supports a tested optical component, not our craft, UAE transfer, independent 2018 accuracy or ecological benefit. For C001/C017, first establish what RGB cannot resolve; a multi-species study does not automatically justify hyperspectral hardware for Kalba.

Historical soil cores, borehole porewater, soil redox and laboratory carbon measurements require their own acquisition methods. A floating channel probe cannot reproduce them simply by measuring water-column conductivity/temperature. Neither type of observation supplies a planting prescription by itself. Present-day sensing also cannot validate the historical measurements or the 2018 cover cells.

A [2024 Japanese pond study](https://mdpi-res.com/d_attachment/drones/drones-08-00038/article_deploy/drones-08-00038.pdf) tested amphibious sensing and relay links. Floats impaired flight; vegetation disrupted communications; an oxygen-consuming DO electrode made longer settling inappropriate in its test. Data are available by author request, not an established downloaded dataset. This supports selected component feasibility, not our design, Khor Kalba transfer or matched energy superiority.

### Measured third-party tradeoffs

[Suetsugu et al. (2024), Methods 2.5.1 and Table 1](https://www.mdpi.com/2504-446X/8/2/38/xml), report seconds before lateral deviation exceeded ±1.5 m, without aileron correction:

| Configuration | Beaufort 1-2 | Beaufort 2-3 |
|---|---:|---:|
| Polystyrene bar floats | 41 ± 26 | 14 ± 1 |
| PET-bottle floats | 43 ± 25 | 34 ± 6 |
| Drone-only | >180 | 90 ± 47 |

These values describe hover stability, not battery endurance, mission duration or sensing accuracy. Trials included manual throttle/elevator adjustment, with a cutoff of 180 seconds. The prose gives >180 for the higher wind band, conflicting with the table. That discrepancy prevents a definitive effect estimate; the extraction also does not establish replicate counts or the meaning of ±.

The disc-float design could not reach the 1.5 m test height. Section 3.2.1 compares relay communications rather than water-sensing platforms. These findings make loaded flight and complete recovery necessary tests alongside buoyancy. The Japanese craft results do not calibrate our energy model or establish UAE performance. The review used indexed publisher text because direct HTML/XML access was blocked; it downloaded neither a new PDF nor a raw dataset.

### Buoyancy and static lift: necessary, not sufficient

For a freely floating body at rest without other vertical forces, buoyancy balances weight: `rho_water * g * V_displaced = m * g`, hence `V_required = m / rho_water`. Compare this with a documented displacement limit that preserves the intended freeboard. Geometry, leaks, loading and restoring stability still require separate assessment. This follows [Archimedes' principle](https://openstax.org/books/university-physics-volume-1/pages/14-4-archimedes-principle-and-buoyancy).

For an idealized steady airborne state with no other vertical force, `T_available * cos(tilt) >= m * g`. Equality gives no upward thrust margin. This is a necessary static screen, not proof of controllability, flight endurance or wet takeoff. Use thrust and battery capability under the actual anticipated conditions, not an unrelated catalogue maximum.

### Euler: where it genuinely belongs

In constant-mass rigid-body principal axes, the forced Euler equation is:

`I * omega_dot + omega cross (I * omega) = torque_net`.

For example, `omega_dot_x = (torque_x + (I_y - I_z) * omega_y * omega_z) / I_x`, with cyclic counterparts. Angular velocity is in rad/s, inertia in kg m² and torque in N m. The [MIT Press mechanics text, section 2.9](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/9579/sicm_edition_2.zip/chapter002.html) derives the forced equation and distinguishes angular dynamics from orientation kinematics.

This equation identifies the inertia and torque inputs needed to assess attitude during contact and transitions. Instantaneous acceleration alone cannot establish stability. A future model needs orientation, translational dynamics, controller/actuator limits, hydrodynamic forces, restoring torques and measured validation. Moving payloads, rotor angular momentum, variable mass and added-water effects require an expanded model or justified approximation. No such calibrated model exists here. Euler's differential equations differ from a numerical Euler integration method; selecting an integrator does not validate the physics.

### Dwell, measurement quality and resource advantage

The optional notebook includes a declared first-order response assumption: if a sensor's normalized step-error obeys `e(t) = exp(-t / tau)`, with `tau > 0` and `0 < epsilon < 1`, a residual error limit `epsilon` requires `t >= -tau * ln(epsilon)`. This is the team's elementary model derivation, not a specification for any selected sensor. Test applicability; settling alone excludes calibration bias, fouling and spatial drift.

For the same `n` comparable attempted observation tasks with a common per-attempt acceptance probability `p > 0`, long-run aggregate energy per accepted observation is `E / (n*p)` and time is `T / (n*p)`, with `E,T` expected whole-mission resources. The probabilities are unknown here. For heterogeneous tasks use expected accepted count `sum(p_i)` instead. These are ratios of expectations, not the expected per-mission ratio; a mission can return zero accepted records. With equal attempted tasks, supported mode improves energy only if `p_S/p_H > E_S/E_H`, and time only if `p_S/p_H > T_S/T_H`. Acceptance must use the same predeclared quality rule, not different standards for each platform.

The [saved illustrative scenario](../examples/inspection/energy_scenario_excerpt.json) already shows approximately 170.7 versus 128.0 Wh but 750 versus 840 s. Those rounded hypothetical results imply an energy threshold near 0.749854 and a time threshold of 1.12; equal acceptance cannot improve both. A 30 s dwell or extra recovery overhead can reverse the energy advantage. These are not measured probabilities or UAE product comparisons. Unmeasured recovery costs must not silently become zero.

The [commercial response-time check and task-specific comparison](WATER_CONTACT_RATIONALE.md#one-refutable-task-comparison) challenge the assumed dwell duration. The observation requirement must justify sustained contact; choosing it to favour support would bias the comparison. Catalog response is not field settling, and the full measurement chain and matched reference remain untested. The saved scenario is illustrative, not a sensor-specified Kalba mission.

### Executed symbolic bounds, not additional hardware evidence

The [SymPy resource gates](SYMBOLIC_RESOURCE_GATES.md) generalize the saved accounting model: minimum dwell for strict energy saving, upper dwell from each battery budget, a nonempty joint window and quality-matched expected-acceptance thresholds. One actual free-CPU Colab run verified seven zero residuals and two rational identities. These let us reject inconsistent energy claims without inventing power or acceptance measurements. The model and executed snapshots remain preserved, and the completed temporary runtime was saved and terminated. They do not establish that any actual Khor Kalba task falls within the conditional window.

## Choosing the next experiment, not the most elaborate aircraft

Select a method for each evidence gap instead of assigning every satellite flag to the same drone. First ask which observation could change a decision and whether an existing source can answer it. Disagreement frequency does not give a probability of damage. Compare information quality, habitat safeguards, energy, time, operator effort and money separately rather than combining them in an arbitrary weighted score.

For engineering, the smallest decisive future experiment is a permitted controlled-water comparison of the same specified sensor observation: establish calibration, depth/position/settling and bias against a reference probe; then measure complete energy, elapsed time, rejected attempts, transitions and recovery against the simplest suitable method. Include a no-amphibious baseline. Tank performance would be an early engineering result, not Khor Kalba field suitability or ecological benefit. No tank test is claimed or scheduled.

For accuracy, first establish reusable independent sufficiently detailed near-date evidence, then draw the frozen held-out probability sample and perform blind interpretation. For ecology, first establish current need and suitability, with no action/protection/natural regeneration as genuine alternatives; any intervention requires the [separate outcome protocol](VALIDATION_AND_BENEFIT_TESTS.md). The three evidence tracks cannot substitute for each other.

## Reproducible companion and status

[Connected concept Colab notebook](../supplementary/Mangrove_Pulse_Connected_Concept.ipynb) embeds the unchanged saved requests, this note, exact screening code/tests and blank parameter records. It needs no dataset upload, package installation or accelerator, and exports a downloadable assessment ZIP when run in Colab. Source is [concept_screen.py](../src/concept_screen.py). Default engineering inputs are unknown; saved energy/time values remain explicitly hypothetical. It never returns deployment authorization, independent accuracy, superiority or ecological-benefit proof. Synthetic tests test equations and record handling only.

The [executed Colab copy](https://colab.research.google.com/drive/19mTP4c0HW3WDptV_4er8T6PVZhxz4j2S) records the 7 October CPU run: three code cells, sixteen passing synthetic tests, zero error outputs. The [repository notebook](../supplementary/Mangrove_Pulse_Connected_Concept_Executed.ipynb), [results ZIP](../supplementary/Mangrove_Pulse_Connected_Concept_Results.zip) and [execution review](../evidence/connected_concept_colab_review.json) preserve the evidence. The source and returned ZIP retain the preparation-time version of this note. Six physical screens remain unknown and acceptance fractions remain unmeasured. The run verifies equations, record handling and conditional algebra, not physical or ecological performance.

The frozen EO inputs, threshold, split, predictions, scores and previously executed notebooks are unchanged. This assessment adds no field observations or local scientific runs. Its 7 October notebook run did not test anonymous access; the later team-owned repository copy has link-viewer access as recorded in the [Colab register](COLAB_LINKS.md#repository-notebooks-in-the-teams-drive). No platform submission or PDF is claimed.
