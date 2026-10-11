# Conditional resource gates for a proposed contact-sensing task

8 October 2026 | Executed algebra, not measured aircraft performance

A free-CPU [Colab run](https://colab.research.google.com/drive/1rmDLv560DydPXqOXs9QGF6VlMhEh-CXp) verified seven zero-residual identities and two rational identities. The [executed notebook](../supplementary/Mangrove_Pulse_SymPy_Resource_Audit_Executed.ipynb), [returned JSON/README ZIP](../supplementary/Mangrove_Pulse_SymPy_Results.zip) and [artifact review](../evidence/sympy_resource_audit_colab_review.json) preserve the results. These checks establish consistency of the declared accounting equations. They are neither a formal proof-assistant certificate nor validation of a physical model.

## Connection to Khor Kalba

C001/C017 need dated photographic cover/alignment evidence; those questions do not establish a need for amphibious hardware. C027 records historical optical exclusion rather than a water-quality problem. Historical local sources motivate the separate [water-contact question](WATER_CONTACT_RATIONALE.md), which needs its own current decision, authorized stations and [measurement acceptance rule](OBSERVABLES_AND_MEASUREMENT_CHAIN.md). If that task is justified, use the bounds below to compare delivery methods, including simpler alternatives. The 85 historical centres specify neither the number of sensing tasks nor approved waypoints. Present measurements cannot directly label 2018 cover.

## Model, units and assumptions

The preserved [source model](../examples/inspection/energy_source/sampling_energy_model.py) supplies the accounting, not empirical inputs. Its SHA-256 is recorded in the returned JSON. It uses ideal induced hover power with an assumed loss multiplier, equal rotor area/common airborne load and a nonnegative added support burden. Wind, hydrodynamics, wet takeoff, recovery, disturbance and measurement quality are not validated by this model.

Let `P > 0` be baseline airborne power, `D >= 0` extra airborne power, and `W > 0` supported power, all in watts. `T >= 0` is travel time, `N` a positive integer count of comparable attempted tasks, `d >= 0` equal dwell per task and `tau >= 0` extra airborne transition time per task, all times in seconds. `O >= 0` is extra supported energy overhead and `B > 0` a common usable battery budget, both in Wh. Unknown inputs remain unknown.

Scaled energies `H` and `S` are watt-seconds; divide by 3600 for Wh:

```text
H = P(T + Nd)
S = (P + D)(T + N tau) + WNd + 3600O
K = DT + (P + D)N tau + 3600O
A = 3600B - (P + D)(T + N tau) - 3600O
H - S = N(P - W)d - K
```

## General rejection and comparison rules

| Question | Conditional rule | Meaning |
|---|---|---|
| Can support save energy? | If `W >= P`, no strict saving under the nonnegative penalties. If `P > W`, require `d > K/[N(P-W)]`. | Equality is break-even, not superiority. Short dwell or added burden can remove the modeled advantage. |
| Does support fit the battery? | Require `0 <= d <= A/(NW)`. | Negative `A` leaves no nonnegative dwell; sufficient total energy is not a peak-power, lift or recovery guarantee. |
| Can both methods fit the same battery while support saves energy? | For `P > W`, require `K/[N(P-W)] < min(A/(NW), (3600B-PT)/(NP))`. | A nonempty interval is conditional on the same usable `B`, task count and dwell. It does not establish a feasible mission. |
| Does support improve energy per expected accepted record? | For positive energies and `0 < pH,pS <= 1`, require `pS/pH > S/H`. | Acceptance uses one predeclared quality rule; neither fraction is measured here. |
| Does support improve accounted time per expected accepted record? | With positive `TH = T+Nd`, `TS = TH+N tau`, require `pS/pH > TS/TH`. | Positive `tau` and equal acceptance preclude a subtotal time benefit. Unspecified overhead duration is not zero. |

The both-battery interval is equivalently nonempty when both `A(P-W) > WK` and `(3600B-PT)(P-W) > PK`, with `P > W`. Positive denominators and strict inequalities are required; SymPy residual checks alone cannot establish inequality direction or applicable input domains. The original numerical model uses a small floating-point battery tolerance. These exact algebraic bounds do not reproduce that boundary predicate bit for bit.

The acceptance comparison divides expected resource totals by expected accepted count for equal attempted tasks. It is not the expectation of a per-mission realized ratio. Zero-success missions remain part of resource/reliability evidence, even when that realized ratio is undefined. For unequal task counts or heterogeneous acceptance, specify the corresponding expected accepted counts before comparing.

The [saved hypothetical example](../examples/inspection/energy_scenario_excerpt.json) uses less energy but takes longer at equal acceptance. It is not a matched comparison with a UAE product. The symbolic rules generalize its accounting assumptions without turning assumed inputs into measurements.

## What remains to test

First define the useful observation and verify its calibration, position/depth, timing and acceptance against an appropriate reference. Then compare complete measured energy, elapsed time, failures, recovery and habitat disturbance against the simplest suitable shore/boat/logger/USV/ordinary-drone method. The algebra supplies no craft, accepted observations, independent historical labels or ecological outcomes. Planting suitability, survival and carbon benefit need separate evidence. The frozen EO source, thresholds, split and executed results are unchanged; this work required neither a new EO transfer nor local scientific execution.

[SymPy documentation](https://docs.sympy.org/latest/tutorials/intro-tutorial/simplification.html) describes the algebra tool used in the saved notebook. The calculations test conditional relationships, not aircraft measurements. The [Colab register](COLAB_LINKS.md#repository-notebooks-in-the-teams-drive) links the team-owned viewer copy.
