# Evidence gaps and decisions

10 October 2026 | Bounded evidence review

The [implemented results](WHAT_THE_POC_ESTABLISHES.md) remain reproducible. The review below asks what additional evidence could establish H1-H4 in the [claim register](CLAIM_EVIDENCE_MAP.md). It reuses the saved source qualifications, actual records and proposed tests. No new field observations, aircraft missions or ecological outcomes were obtained.

## Independent historical accuracy: H2 remains unresolved

The target is the frozen 20 November 2018 southern eligible population, not three selected cases or mangroves anywhere in the UAE. A usable source must support independently interpreted whole-cell cover, with dates, relative alignment, lineage, unknown-label rules and known sampling probabilities. Image interpretation would establish accuracy against that reference, not automatically field accuracy.

The strongest near-date candidate is GE01 imagery metadata dated 5 October 2018. Its [saved records](../examples/review/confirmed_metadata.json) state 1.2 m resolution and 8.47 m positional accuracy. These are different quantities; the latter is not measured relative alignment to our grid. The selected screenshots support qualitative review, but not blind interpretation or a representative accuracy estimate. Their selection already depends on the audit.

The [historical workbook](HISTORICAL_KALBA_FIELD_CONTEXT.md) supplies 2014 or undated field records, not 2018 whole-cell labels. The dated Abu Dhabi species-presence lead does not supply absence observations or canopy footprints. Related GMW representations and WorldCover cannot replace an independent reference.

A targeted follow-up of the [Northern Emirates mapping paper](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2020.00102/full) checked its Training Data Collections and Data availability sections. It reports 536 imagery-derived samples, split 375/161, but the inspected page exposed no usable dated-label download or scene identifiers resolving the previously documented acquisition-date conflict. This does not establish that additional data do not exist.

Decision: keep the frozen experiment as a reference-agreement result. Do not generate an accuracy score from selected screenshots, undated training points or present observations. Follow the [independent-reference protocol](VALIDATION_AND_BENEFIT_TESTS.md#2-independently-assess-the-historical-map) only after a qualified source is available. Any new endpoint or site needs a separately frozen method and untouched evaluation evidence; renaming an inspected holdout does not restore independence.

## Useful observations and aircraft tradeoffs: H3 remains unresolved

C001/C017 ask photographic questions. Licensed imagery, shore or boat photography, or a conventional drone may suffice. C027 records historical optical exclusion; it does not identify a current chemical anomaly or a permitted water station. The connection is an evidence request, not a route selected for an amphibious aircraft.

A separate current water question needs a named decision, authorized locations, depth and tide context, a calibrated sensor assembly and acceptance tolerances. Historical borehole porewater, sediment cores and calculated carbon stocks cannot be reproduced by channel-water conductivity and temperature alone. See the [measurement chain](OBSERVABLES_AND_MEASUREMENT_CHAIN.md) and [water-task rationale](WATER_CONTACT_RATIONALE.md).

The [physical precedents](CONNECTED_CONCEPT_ASSESSMENT.md#measured-third-party-tradeoffs) support testing components and also expose limitations: floats can impair flight, vegetation can interrupt links, and sensor disturbance can invalidate readings. Manufacturer response time is not complete field stabilization. It does not justify choosing the favorable hypothetical dwell in our energy example.

The [conditional example](../examples/inspection/energy_scenario_excerpt.json) permits lower energy with longer elapsed time; short dwell or additional overhead can reverse the energy result. Neither that example nor the static buoyancy/Euler checks establishes a working craft. Mass, thrust, usable battery, loaded stability, wet transitions, station keeping, observation quality, failures and recovery remain unmeasured.

Decision: keep amphibious collection as a candidate, not the default. First test the complete sensor against a reference using the simplest feasible delivery method. Compare aircraft modes only after both return observations under the same quality rule. Count complete setup-to-recovery time, energy, unsuccessful attempts, operator effort and habitat disturbance. A logger is a fair comparator only for the same information need. A controlled tank trial could qualify a component; it would not establish field or ecological performance.

## Ecological benefit: H4 remains unresolved

The [historical field context](HISTORICAL_KALBA_FIELD_CONTEXT.md) supports investigating hydrology and root-zone conditions. It does not identify present damage, prescribe planting, or measure the team's benefit. Carbon stock is not carbon gain. External planted-site comparisons cannot supply the missing baseline, controls and follow-up for our intervention.

The [ecological protocol and UAE guidance](VALIDATION_AND_BENEFIT_TESTS.md#3-establish-benefit-without-converting-valuable-habitat) require current need and suitability, permissions, protection of mudflat/saltmarsh, and replicated outcomes. Protection, natural regeneration or no intervention may be preferable to planting. More measurements and more seedlings are not ecological endpoints by themselves.

Decision: do not prescribe planting from satellite disagreement or a water reading. If an intervention is justified, predeclare outcomes and stopping rules before collecting baseline/control/follow-up observations. Carbon additionality needs separate accounting. Software and physical identities cannot close this gap.

## Practitioner usefulness: H1 remains unresolved

The briefs preserve evidence and questions, but [completed practitioner reviews](STAKEHOLDER_FEEDBACK.md) remain zero. Internal critique can improve clarity; it cannot substitute for intended practitioners using the brief. Unanswered outreach is neither feedback nor evidence of workflow improvement.

Decision: retain the handoff as a working format. The proposed neutral review asks practitioners to choose an action without coaching, records criticism and accepts simpler alternatives. A time-saving claim would need a separate matched task comparison. No external messages were sent during this review.

## Where further effort changes the decision

The next empirical steps are source qualification for historical cover, a defined and authorized current observation task, and real practitioner use. Aircraft comparison follows measurement acceptance; ecological intervention follows established need and suitability. Switching to Abu Dhabi or Tarif is allowed, but the qualified evidence currently does not close these gates. The [Tarif crop](TARIF_SCENE_QUALIFICATION.md) demonstrates spectral access, not classification improvement.

This review completes a bounded attempt, not the empirical claims. H1-H4 remain unresolved. Further acquisition should follow a concrete lead that can pass a stated gate, rather than repeat the same searches, downloads or synthetic checks.

## Additional source qualification — 12 October 2026

Two narrow research checks examined new leads while the [computational checks](REVIEW_CHECKS_20261012.md) ran. The sources below change what to test, not the status of team field, aircraft or ecological claims.

### UAE labels and restoration-planning data

The [Bellone dataset record](https://zenodo.org/records/21275271), published 9 July 2026, accompanies a submitted paper about UAV restoration planning in the UAE. Its description identifies five-class training points and example vegetation/tidal rasters. It does not establish point observation dates, annotation method, independent evaluation status, Kalba footprint or reuse terms; the displayed licence field is blank. The publication date is not the observation date, and model-generated vegetation maps are not reference labels.

**TEST:** qualify the source paper and point metadata before acquiring the files. Require dated, interpretable cover labels, footprint/alignment, label lineage and permission. External training labels are not automatically unusable for a different method, but their independence from that method and reference must be established. If qualified contemporary labels support a better UAE task, freeze a separate experiment; do not apply them retrospectively to the 2018 score. No dataset was downloaded or evaluated in this check.

### A simpler aerial water-sampling comparator

A [2026 primary study](https://link.springer.com/article/10.1007/s10661-026-15473-0) compares tethered drone sampling with a boat at three Irish lakes on three dates in 2023. It used the same sonde at three depths, plus bottle samples. It reports no significant method difference for nine of ten tested variables, but a pH difference; reported workflow durations are 28 minutes for the drone and 45 for the boat. The cost model excludes repairs and travel and assumes comparable useful life and maintenance.

**DEFEND:** conventional aerial delivery is a substantive comparator, not just photography. **TEST:** compare accepted measurements before mission resources. Nonsignificant differences do not establish equivalence within a useful tolerance. Depth readings and repeated seconds are not independent missions. The study does not measure our platform, water-supported delivery, UAE tidal channels, whole-mission energy per accepted observation or net habitat disturbance. It therefore supplies a simpler-method precedent and design warnings, not an amphibious advantage.

### Ecological outcomes beyond planting counts

A [2023 Sulawesi study](https://doi.org/10.1111/rec.13963) compared monoculture restoration, mixed-species regeneration and nearby reference stands 14–16 years after restoration. It measured structure, abundance, biomass and canopy, with 18 comparison plots at one site and 17 at the other. Some mixed-regeneration structure measures were closer to reference stands, while other deficits remained. This was an observational comparison, not randomized allocation or a team intervention.

**DEFEND:** an ecological endpoint must extend beyond planted counts or survival alone. **TEST:** use site-appropriate reference conditions and controls. Tropical species-diversity targets do not transfer automatically to naturally species-poor UAE mangroves, and the study does not justify adding species, planting at Kalba or claiming carbon gain. Current need, suitability, permissions, independent plots and follow-up remain required.

### Resulting decisions

The original metrics and conditional model are retained with the completed sensitivity checks. H2 needs qualified independent dated labels; H3 needs a defined accepted observation and measured matched missions; H4 needs a justified intervention and controlled ecological outcomes. These are specific external evidence dependencies, not problems solved by another simulated score. The new UAE source is a qualification lead, not proof that no better site exists. No new hardware, fieldwork, ecological intervention or stakeholder contact is claimed.
