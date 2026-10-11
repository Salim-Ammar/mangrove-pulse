"""Analytical sensitivity model, not a flight or ecological simulation.

All mission/design inputs are hypothetical. No satellite data or external packages
are used. Run with Python 3.10+; see the Colab bundle's EVIDENCE_AND_MODEL.md.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import hashlib
from itertools import product
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    baseline_mass_kg: float = 8.0  # Includes battery and shared sampling payload.
    added_support_mass_kg: float = 2.0  # Complete additional kit, not just floats.
    disk_area_m2: float = 0.8  # Equal effective non-overlapping area for both.
    loss_multiplier: float = 1.6  # Hypothetical lumped factor, NOT an efficiency.
    common_air_load_w: float = 25.0
    supported_total_power_w: float = 40.0  # Includes the shared sampling loads.
    travel_time_s: float = 300.0  # Complete round trip/inter-site flight budget.
    sites: int = 3
    dwell_per_site_s: float = 150.0  # Equal accepted-observation time assumption.
    transition_per_site_s: float = 30.0  # Additional landing + takeoff air time.
    additional_support_overhead_wh: float = 0.0  # Extra energy sensitivity term.
    battery_nominal_wh: float = 240.0  # Included in baseline mass; NOT mass-sized.
    battery_usable_fraction: float = 0.8  # Withhold 20%; do not also add 20% energy.
    air_density_kg_m3: float = 1.225
    gravity_m_s2: float = 9.81


def validate(scenario: Scenario) -> None:
    """Reject invalid/nonfinite inputs instead of emitting misleading results."""
    for name, value in asdict(scenario).items():
        if isinstance(value, bool) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite and numeric")
        if value < 0:
            raise ValueError(f"{name} cannot be negative")
    for name in ("baseline_mass_kg", "disk_area_m2", "battery_nominal_wh",
                 "air_density_kg_m3", "gravity_m_s2"):
        if getattr(scenario, name) <= 0:
            raise ValueError(f"{name} must be positive")
    if not isinstance(scenario.sites, int) or scenario.sites <= 0:
        raise ValueError("sites must be a positive integer")
    if scenario.loss_multiplier < 1:
        raise ValueError("loss_multiplier must be at least 1")
    if not 0 < scenario.battery_usable_fraction <= 1:
        raise ValueError("battery_usable_fraction must be in (0, 1]")


def induced_power_w(mass_kg: float, disk_area_m2: float,
                    air_density_kg_m3: float = 1.225,
                    gravity_m_s2: float = 9.81) -> float:
    """Ideal, static, out-of-ground-effect induced power; omits real losses."""
    for value in (mass_kg, disk_area_m2, air_density_kg_m3, gravity_m_s2):
        if not math.isfinite(value) or value <= 0:
            raise ValueError("power-model inputs must be positive and finite")
    return (mass_kg * gravity_m_s2) ** 1.5 / math.sqrt(
        2 * air_density_kg_m3 * disk_area_m2
    )


def evaluate(scenario: Scenario) -> dict:
    """Compare equal dwell tasks and derive the per-site break-even duration."""
    validate(scenario)
    s = scenario
    p0_ideal = induced_power_w(s.baseline_mass_kg, s.disk_area_m2,
                             s.air_density_kg_m3, s.gravity_m_s2)
    p1_ideal = induced_power_w(s.baseline_mass_kg + s.added_support_mass_kg,
                             s.disk_area_m2, s.air_density_kg_m3, s.gravity_m_s2)
    p0 = s.loss_multiplier * p0_ideal + s.common_air_load_w
    p1 = s.loss_multiplier * p1_ideal + s.common_air_load_w
    total_dwell_s = s.sites * s.dwell_per_site_s
    total_transition_s = s.sites * s.transition_per_site_s
    hover_travel_wh = p0 * s.travel_time_s / 3600
    hover_dwell_wh = p0 * total_dwell_s / 3600
    support_travel_wh = p1 * s.travel_time_s / 3600
    support_transition_wh = p1 * total_transition_s / 3600
    support_dwell_wh = s.supported_total_power_w * total_dwell_s / 3600
    hover_wh = hover_travel_wh + hover_dwell_wh
    support_wh = (support_travel_wh + support_transition_wh + support_dwell_wh
                  + s.additional_support_overhead_wh)
    saving_wh = hover_wh - support_wh
    numerator_ws = ((p1 - p0) * s.travel_time_s + p1 * total_transition_s
                    + 3600 * s.additional_support_overhead_wh)
    denominator_w = s.sites * (p0 - s.supported_total_power_w)
    threshold_s = numerator_ws / denominator_w if denominator_w > 0 else None
    usable_wh = s.battery_nominal_wh * s.battery_usable_fraction
    # A budget pass is not a flight, transition, access, quality or safety pass.
    return {
        "baseline_ideal_induced_power_w": p0_ideal,
        "supported_ideal_induced_power_w": p1_ideal,
        "baseline_air_power_w": p0,
        "supported_air_power_w": p1,
        "hover_segments_wh": {"round_trip_travel": hover_travel_wh,
                              "sampling_hover": hover_dwell_wh},
        "supported_segments_wh": {"round_trip_travel": support_travel_wh,
                                  "land_takeoff": support_transition_wh,
                                  "supported_sampling": support_dwell_wh,
                                  "additional_overhead": s.additional_support_overhead_wh},
        "hover_energy_wh": hover_wh,
        "supported_energy_wh": support_wh,
        "saving_wh": saving_wh,
        "saving_percent_of_hover": 100 * saving_wh / hover_wh if hover_wh else None,
        "break_even_dwell_per_site_s": threshold_s,
        "supported_energy_lower": saving_wh > 1e-9,
        "usable_battery_wh": usable_wh,
        "hover_within_energy_budget": hover_wh <= usable_wh + 1e-9,
        "supported_within_energy_budget": support_wh <= usable_wh + 1e-9,
        "hover_accounted_duration_s": s.travel_time_s + total_dwell_s,
        "supported_accounted_duration_s": s.travel_time_s + total_dwell_s + total_transition_s,
        "duration_note": "Subtotal; additional-overhead duration is unspecified if nonzero",
        "operational_feasibility_established": False,
        "observation_equivalence_verified": False,
    }


def original_report_arithmetic() -> dict:
    """Reproduce and correct the report's explicit arithmetic, not its design."""
    area = 4 * math.pi * 0.4 ** 2
    segments_wh = [1600 * 100 / 3600, 1800 * 300 / 3600,
                   200 * 100 / 3600, 100 * 60 / 3600, 1800 * 300 / 3600]
    subtotal = sum(segments_wh)
    return {
        "report_sha256": "d8da47734a872a7408b741119fa576cc167011ef65d84366bc244fbba47fe224",
        "four_rotor_disk_area_m2": area,
        "hover_table": [{"total_mass_kg": m, "ideal_induced_power_w":
                         induced_power_w(m, area)} for m in (23, 27, 31, 35, 43)],
        "area_of_50_by_100_m_km2": 50 * 100 / 1_000_000,
        "two_20_by_5_cm_contact_patches_m2": 2 * 0.2 * 0.05,
        "contact_pressure_30_kg_kpa": 30 * 9.81 / (2 * 0.2 * 0.05) / 1000,
        "segment_energy_subtotal_wh": subtotal,
        "segment_energy_with_10_percent_addition_wh": subtotal * 1.1,
        "fraction_of_750_wh_after_addition": subtotal * 1.1 / 750,
        "flight_segment_duration_min": (100 + 300 + 300) / 60,
        "20_percent_added_mass_ideal_power_ratio": 1.2 ** 1.5,
        "23_to_27_kg_added_mass_percent": 100 * (27 / 23 - 1),
        "23_to_27_kg_ideal_power_ratio": (27 / 23) ** 1.5,
    }


def build_results() -> dict:
    base = Scenario()
    cases = {
        "short_dwell": replace(base, dwell_per_site_s=30),
        "illustrative_main": base,
        "long_dwell": replace(base, dwell_per_site_s=300),
        "long_route_energy_only_win": replace(base, travel_time_s=1200,
                                               dwell_per_site_s=300),
        "extra_80_wh_overhead": replace(base, additional_support_overhead_wh=80),
    }
    axes = {
        "added_support_mass_kg": [1.0, 2.0, 4.0],
        "travel_time_s": [300.0, 600.0, 1200.0],
        "sites": [1, 3, 5],
        "dwell_per_site_s": [30.0, 60.0, 150.0, 300.0],
        "supported_total_power_w": [40.0, 150.0],
        "loss_multiplier": [1.3, 1.8],
        "transition_per_site_s": [15.0, 60.0],
    }
    rows = []
    for values in product(*axes.values()):
        scenario = replace(base, **dict(zip(axes, values)))
        rows.append({"inputs": asdict(scenario), "result": evaluate(scenario)})
    return {
        "model_version": "1.0",
        "evidence_status": "Analytical scenario estimates, not measured drone performance",
        "input_provenance": {
            "mission_and_design_values": "Hypothetical sensitivity inputs; no component specifications",
            "air_density_and_gravity": "Chosen reference constants, not measured Khor Kalba conditions",
            "power_equation": "Ideal actuator-disk momentum theory; Johnson (2004), pp. 2–3",
            "power_source_url": "https://rotorcraft.arc.nasa.gov/Publications/files/Johnson_AHS-SF2004.pdf",
            "loss_multiplier": "Uncalibrated lumped scenario factor, not a published motor efficiency",
            "observation_equivalence": "Assumed; no sensor quality, depth or stability measurements",
            "published_18_percent_MEDUSA_result": "Context only; NOT a model calibration or input",
        },
        "original_report_arithmetic_checks": original_report_arithmetic(),
        "illustrative_cases": {name: {"inputs": asdict(s), "result": evaluate(s)}
                               for name, s in cases.items()},
        "sweep_axes": axes,
        "sweep_summary": {
            "scenarios": len(rows),
            "energy_lower": sum(r["result"]["supported_energy_lower"] for r in rows),
            "energy_lower_and_supported_budget_pass": sum(
                r["result"]["supported_energy_lower"] and
                r["result"]["supported_within_energy_budget"] for r in rows),
            "interpretation": "Grid counts are not probabilities or evidence of real mission success",
        },
        "sweep": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("sampling_energy_results.json"))
    args = parser.parse_args()
    results = build_results()
    results["model_source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()),
                      "sweep_summary": results["sweep_summary"],
                      "illustrative_cases": {name: case["result"] for name, case in
                                             results["illustrative_cases"].items()}}, indent=2))


if __name__ == "__main__":
    main()
