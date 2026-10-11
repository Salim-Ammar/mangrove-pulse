# What the PoC establishes

Mangrove Pulse demonstrates a reproducible way to turn historical satellite/reference disagreements into inspection questions. It also tests conditional engineering arguments for a proposed amphibious observation platform. The aircraft and its ecological outcomes have not been measured.

## Demonstrated results

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| [Saved execution](../Mangrove_Pulse_End_to_End_Executed.ipynb) and [run record](../evidence/final_colab_review.json) | The frozen cached workflow reproduced its recorded results. The notebook retains seven executed cells, six figures and 14 passing handoff tests. | Independent truth, successful execution of every later revision or public evaluator access. The separately reported integrated results ZIP was not recovered locally. |
| [Baseline](../examples/baseline/baseline_summary.json) and [audit](../examples/audit/audit_summary.json) | On 20 November 2018, 5,653 eligible southern cells gave F1 0.8864 and IoU 0.7960 against GMW. There were 121 disagreements and 87 excluded GMW-mapped cells. | Field accuracy or ecological damage. GMW informed calibration; the raw-DN contrast is not calibrated NDVI. |
| [Reference comparison](../examples/reference_context/comparison_summary.json) | Two GMW 2018 representations differ at 614 of 13,401 full-AOI centres; mapped Jaccard is 0.6150. Reference choice affects interpretation. | Which reference is correct. Later WorldCover 2020 context is not an independent 2018 label source. |
| [Inspection briefs](CASES.md), [requests](../examples/inspection/inspection_requests.json) and [blank returns](../examples/inspection/observation_return_template.json) | The handoff preserves 85 historical centres across three cases and states evidence questions and proposed decisions. | Collected observations, an authorized route, an accuracy sample or a demonstrated improvement in a practitioner's work. |
| [Dated EO context](DATED_EO_CONTEXT.md) and [Tarif spectral qualification](TARIF_SCENE_QUALIFICATION.md) | Separately dated scene context can be retained and reused; actual hyperspectral channels were accessed in a fixed Tarif window. | Water chemistry, historical cover truth, hyperspectral improvement or a better mangrove demonstration site. The inspected Tarif window shows open water. |
| [Symbolic resource gates](SYMBOLIC_RESOURCE_GATES.md) and [saved energy scenarios](../examples/inspection/energy_scenario_excerpt.json) | Under stated assumptions, supported sensing can save energy at sufficiently long dwell, but can lose with short dwell or added overhead. Energy and time can favor different methods. | Measured aircraft feasibility or superiority. Observation quality is assumed rather than verified, and craft inputs remain unknown. |

## Claims still requiring evidence

Independent 2018 accuracy needs qualified, independently interpreted near-date labels with appropriate sampling, alignment and uncertainty. Present-day observations cannot directly label historical cover. The already inspected evaluation set is not an untouched confirmatory set for future method selection. See the [accuracy protocol](VALIDATION_AND_BENEFIT_TESTS.md).

Drone advantage needs accepted observations and measured whole-mission comparisons against appropriate alternatives, including failures, recovery and habitat disturbance. Photographic cover review does not establish an amphibious requirement. The [separate water-contact task](WATER_CONTACT_RATIONALE.md) has no assigned stations or accepted measurements.

Ecological or carbon benefit needs a justified present need, suitable intervention, permissions, baseline, controls and follow-up outcomes. Neither disagreement counts nor planting counts establish that benefit. The [ecological protocol](VALIDATION_AND_BENEFIT_TESTS.md) describes the missing evaluation.

Practitioner usefulness needs actual use and criticism from relevant people. The [stakeholder protocol](STAKEHOLDER_FEEDBACK.md) is proposed; unanswered outreach is not completed validation. Published planting and amphibious-sensing precedents support investigating components, not treating another team's results as measurements of our combined design.

The [claim map](CLAIM_EVIDENCE_MAP.md) records the scope of each result and hypothesis. Repository access and presentation delivery are separate from scientific evidence.
