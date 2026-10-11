<a id="poc-logic-and-next-step--7-october-2026"></a>

# PoC logic and next step (7 October 2026)

## Defensible claim

Mangrove Pulse turns historical satellite/reference uncertainty at Khor Kalba into traceable observation requests. An amphibious drone is a candidate platform for a separately justified contact-sensing task, not the implemented result or an automatic response to a flagged cell.

The frozen baseline and audit were reproduced, and the reference-sensitivity study completed separately in Colab. The three cases have 85 exact historical centre records, observation questions and unfilled return records. Independent historical cell truth, practitioner usefulness, field access and platform benefit remain unknown. Packaging tests cannot resolve them.

## Evidence-to-decision chain

| Evidence already available | Question it supports | Next evidence / method | Drone gate |
|---|---|---|---|
| C001: 11 prediction-positive/v3-unmapped centres; v4 maps 7; later WorldCover maps 11 | What cover and boundary alignment can actually be supported at a specified date? | Dated, aligned imagery and qualified vegetation identification | Existing imagery or ordinary photography may suffice; amphibious need unestablished |
| C017: 32 prediction-negative/v3-mapped centres; v4 maps 6; later WorldCover includes mixed classes | Is the mapped patch dense canopy, mixed cover or something else? | Dated per-cell cover composition, uncertainty and independent labels | Do not turn reference disagreement into a health diagnosis or planting demand |
| C027: 42 quality-excluded/v3-mapped centres; v4 maps 36; later WorldCover includes water and vegetation | Why is optical evidence inadequate, and what observation would answer the task? | Visibility/cover evidence first; a separate current water-context task only if justified | Contact sensing might motivate amphibious research, but exclusions alone do not establish that need |

All coordinates remain diagnostic centres, not an approved flight/sampling/landing plan. Current observations cannot directly validate November 2018 cover. WorldCover 2020 and related GMW releases are not independent historical field truth. Preserve the original threshold, split, categories and denominators.

## External checks that constrain our claims

Ramsar describes Khor Kalba's protected wetland as a mixture of mangroves, mud, tidal channels and other habitats. This historical description supports a limit on our interpretation: open/non-mangrove cover is not automatically a restoration deficit. Our rectangle is not the official protected-area boundary, and access/aircraft/contact permission remains unestablished. [Ramsar site announcement](https://www.ramsar.org/news/third-ramsar-site-united-arab-emirates).

EAD's January 2023 announcement describes UAE restoration drones performing planting, growth monitoring, habitat mapping and 3D imaging. It documents a comparator, not a complete current product specification. Adding a drone or monitoring alone therefore cannot establish novelty. The PoC contains no head-to-head performance evidence. [EAD project announcement](https://www.ead.gov.ae/en/Media-Centre/News/0-plants-one-million-mangrove).

The primary-source follow-up on 9 October verified that ADNOC's report also describes dispersal plus monitoring. The [comparison audit](CONNECTED_CONCEPT_ASSESSMENT.md#uae-comparison-monitoring-already-exists) records source-access and reporting limits. Those sources cannot justify a planting-only baseline, survival ratio or missing-capability claim.

Wetlands International's discussion recommends site-specific restoration under suitable ecological conditions, with selective rather than default planting. Planting therefore stays outside our present observation workflow; a salinity measurement alone would establish neither ecological need nor a treatment. [To Plant or Not to Plant?](https://www.mangrovealliance.org/news/to-plant-or-not-to-plant). EAD also announced national restoration guidance in 2024; the PoC has not undergone a full compliance assessment against that document. [EAD national-guidelines announcement](https://www.ead.gov.ae/en/Media-Centre/News/MANGROVE-INITIATIVE-GUIDELINES).

Sources checked on 7 October 2026. Ramsar's HTML was inaccessible on direct opening; the primary publisher's indexed description supports only the historical habitat context above. EAD's 2022 project page timed out on direct opening; no claim depends on treating that failed page load as a current product test. Search-index text is not a substitute for local measurements.

Later checks retrieved the official Ramsar PDF and visually inspected its complete relevant page. Its historical water-property description motivates the [separate water-contact rationale](WATER_CONTACT_RATIONALE.md). A separate free-Colab run produced [24 September 2026 Sentinel-2 SCL/TCI context](DATED_EO_CONTEXT.md), supplying dated product labels/display rather than historical truth, chemistry, change or aircraft need. A 2025 EnMAP candidate remains catalogue-only because asset requests returned a login page. The earlier failed HTML retrieval records that attempt, not the extent of the later PDF review.

## What would count as a proposed improvement?

The hypothesis is that satellite-guided selection plus supported contact sensing could reduce energy per accepted observation for a particular permitted task, after accounting for support mass, transitions, dwell, overhead and observation quality. The theoretical study includes favourable and unfavourable scenarios. It supplies neither a Khor Kalba mission simulation, mapped route, physical feasibility test nor proof of superiority over the UAE comparator.

Before a comparison, define one observation task, its date, permissible access and a measurable acceptance rule. Compare the same required observations with licensed imagery, shore/boat methods and an ordinary drone as appropriate. Predeclare measurement quality/positioning, rejected observations, total energy and time, payload/transition overhead, safety and habitat-disturbance gates. Report energy and time per accepted observation rather than idle/hover savings alone. Supported operation requires permissions and a justified safe protocol. Reject or redesign the concept if it fails those gates or produces no useful advantage.

## Integrated run completed; next step

The authorized 7 October CPU Colab run succeeded. The [actual executed notebook](../Mangrove_Pulse_End_to_End_Executed.ipynb) is included with seven executed cells, six PNG figures, no error outputs and 14 passing handoff tests. [Evidence](../evidence/final_colab_review.json) records the exact 109-file input snapshot and limits. The run fulfilled the following computational gates:

1. Verify the repository fingerprints and reproduce the original baseline/audit without tuning.
2. Display reproduced metrics/figures, with saved reference context explicitly labelled as a prior result.
3. Pass the handoff metadata tests and export the exact 85-centre requests plus empty observation records.
4. Produce a diagnostic/result ZIP with explicit success status, logs and a non-self-referential manifest.

The executed portable copy embeds the exact snapshot used for the run and does not recursively contain itself. The smaller source notebook remains unexecuted on disk; its seven common analysis/export code bodies match those actually run. Outputs were not fabricated or copied into the untouched original. The automatic ZIP transfer stalled. On 8 October, the original reported ZIP remains unrecovered locally and its finished runtime has ended; local archive integrity is unverified, not an ongoing transfer. The retained executed notebook establishes the recorded run, not independent possession or integrity of that ZIP. Do not reconstruct another archive and call it the original.

The priorities recorded on 8 October are to retain the frozen workflow and reuse the completed [dated context and cache](DATED_EO_CONTEXT.md) without another acquisition. Keep historical cover validation, contemporary photographic inspection and the separately justified water-contact question distinct. The next drone test needs an authorized observation contract, a quality-matched comparator and measurements. More product-label counts or hypothetical energy grids cannot supply those measurements. EnMAP needs lawful access, correction/QA and rights checks before a local hyperspectral result.

Drone superiority, independent cell truth and ecological benefit remain unestablished. The next scientific steps are the independent cover-label study, a matched observation-method comparison and a separately controlled ecological intervention test.
