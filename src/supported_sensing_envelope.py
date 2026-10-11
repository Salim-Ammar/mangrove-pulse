"""Conditional static/resource algebra, never a measured aircraft assessment.

SI units except angles in degrees and acceptance probabilities dimensionless.
Unknown inputs stay unknown. No acquisition, fitting, simulation or deployment.
Synthetic verification belongs in the separate Colab companion.
"""
from __future__ import annotations

import math
from numbers import Real


def _number(name, value, lower=None, upper=None, strict_lower=False):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name}: a finite real number is required")
    try:
        value = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name}: representable finite real number required") from exc
    if not math.isfinite(value):
        raise ValueError(f"{name}: a finite real number is required")
    if lower is not None and (value < lower or (strict_lower and value == lower)):
        raise ValueError(f"{name}: invalid lower bound")
    if upper is not None and value > upper:
        raise ValueError(f"{name}: invalid upper bound")
    return value


def _product(name, *factors):
    """Reject overflow and loss of a nonzero product to floating-point zero."""
    result = 1.0
    for factor in factors:
        previous = result
        result *= factor
        _number(name, result)
        if previous != 0 and factor != 0 and result == 0:
            raise ValueError(f"{name}: numerical underflow")
    return result


def _ratio(name, numerator, denominator):
    result = _number(name, numerator / denominator)
    if numerator != 0 and result == 0:
        raise ValueError(f"{name}: numerical underflow")
    return result


def _inputs(spec):
    """Validate supplied values even when a different input is missing."""
    missing, values = [], {}
    for name, (value, lower, upper, strict) in spec.items():
        if value is None:
            missing.append(name)
        else:
            values[name] = _number(name, value, lower, upper, strict)
    return values, missing


def _unknown(missing):
    return {"status": "unknown", "missing_inputs": missing,
            "deployment_authorized": False, "empirical_claims_proven": False}


def static_envelope(m0_kg=None, support_kg=None, displacement_m3=None,
                    water_density_kg_m3=None, usable_thrust_n=None,
                    tilt_deg=None, lift_margin=None, gravity_m_s2=None):
    """Necessary calm-water buoyancy and steady vertical-force intersection.

    The usable thrust is sustained/condition-specific, not catalogue maximum.
    Declare any reserve already applied; do not double-count it in lift_margin.
    Mass/displacement combinations must correspond to a realizable geometry.
    """
    values, missing = _inputs({
        "m0_kg": (m0_kg, 0, None, True),
        "support_kg": (support_kg, 0, None, False),
        "displacement_m3": (displacement_m3, 0, None, True),
        "water_density_kg_m3": (water_density_kg_m3, 0, None, True),
        "usable_thrust_n": (usable_thrust_n, 0, None, True),
        "tilt_deg": (tilt_deg, 0, 90, False),
        "lift_margin": (lift_margin, 1, None, False),
        "gravity_m_s2": (gravity_m_s2, 0, None, True),
    })
    if tilt_deg is not None and values["tilt_deg"] >= 90:
        raise ValueError("tilt_deg must be less than 90")
    if missing:
        return _unknown(missing)
    buoyancy_capacity = _product("computed_buoyancy_capacity_kg",
        values["water_density_kg_m3"], values["displacement_m3"])
    lift_denominator = _product("computed_lift_denominator",
        values["lift_margin"], values["gravity_m_s2"])
    vertical_thrust = _product("computed_vertical_thrust_n",
        values["usable_thrust_n"], math.cos(math.radians(values["tilt_deg"])))
    lift_capacity = _ratio("computed_lift_capacity_kg", vertical_thrust, lift_denominator)
    capacity = min(buoyancy_capacity, lift_capacity)
    total = _number("computed_total_mass_kg", values["m0_kg"] + values["support_kg"], 0, None, True)
    return {"status": "conditional_static_constraints_only",
            "buoyancy_capacity_kg": buoyancy_capacity,
            "vertical_lift_capacity_kg": lift_capacity,
            "maximum_support_mass_kg": capacity - values["m0_kg"],
            "specified_total_mass_kg": total,
            "mass_slack_kg": capacity - total,
            "necessary_constraints_satisfied": total <= capacity,
            "stability_proven": False, "wet_takeoff_proven": False,
            "deployment_authorized": False, "empirical_claims_proven": False}


def restoring_coefficient(mass_kg=None, gravity_m_s2=None, metacentric_height_m=None):
    """For small heel, restoring torque is -k*phi under hydrostatic assumptions.

    Positive k means a restoring sign, not demonstrated dynamic stability.
    Requires an applicable body/geometry, fixed displaced volume and calm water.
    """
    values, missing = _inputs({
        "mass_kg": (mass_kg, 0, None, True),
        "gravity_m_s2": (gravity_m_s2, 0, None, True),
        "metacentric_height_m": (metacentric_height_m, None, None, False),
    })
    if missing:
        return _unknown(missing)
    height = values["metacentric_height_m"]
    sign = "restoring" if height > 0 else "destabilizing" if height < 0 else "neutral_linear_order"
    return {"status": "conditional_small_angle_hydrostatic_sign_only",
            "coefficient_n_m_per_rad": _product("computed_restoring_coefficient",
                values["mass_kg"], values["gravity_m_s2"], height),
            "torque_linearization": "torque = -coefficient * heel_radians",
            "sign": sign, "dynamic_stability_proven": False,
            "deployment_authorized": False, "empirical_claims_proven": False}


def dwell_advantage_interval(hover_fixed_j=None, supported_fixed_j=None,
                             hover_dwell_w=None, supported_dwell_w=None,
                             attempted_tasks=None):
    """Strict supported energy-advantage interval for equal dwell per task.

    EH = hover_fixed_j + n*hover_dwell_w*t, and similarly ES. Fixed energy
    includes transit, transitions, overhead and recovery under the stated model.
    Assumes constant powers/fixed costs and equal accepted observations.
    Power/quality/drift/transition effects that vary with dwell need another model.
    """
    values, missing = _inputs({
        "hover_fixed_j": (hover_fixed_j, 0, None, False),
        "supported_fixed_j": (supported_fixed_j, 0, None, False),
        "hover_dwell_w": (hover_dwell_w, 0, None, False),
        "supported_dwell_w": (supported_dwell_w, 0, None, False),
        "attempted_tasks": (attempted_tasks, 1, 9007199254740991, False),
    })
    if attempted_tasks is not None and not values["attempted_tasks"].is_integer():
        raise ValueError("attempted_tasks must be an integer")
    if missing:
        return _unknown(missing)
    intercept = values["supported_fixed_j"] - values["hover_fixed_j"]
    slope = _product("computed_energy_slope_j_per_s",
        values["attempted_tasks"], values["supported_dwell_w"] - values["hover_dwell_w"])
    interval, boundary = None, None
    if slope == 0:
        if intercept < 0:
            interval = {"lower_s": 0.0, "lower_inclusive": True, "upper_s": None}
    else:
        boundary = _ratio("computed_equality_dwell_s", -intercept, slope)
        if slope < 0:
            interval = {"lower_s": max(0.0, boundary),
                        "lower_inclusive": boundary < 0, "upper_s": None}
        elif boundary > 0:
            interval = {"lower_s": 0.0, "lower_inclusive": True,
                        "upper_s": boundary, "upper_inclusive": False}
    return {"status": "conditional_affine_energy_comparison_only",
            "delta_energy_intercept_j": intercept,
            "delta_energy_slope_j_per_s": slope,
            "algebraic_equality_dwell_s": boundary,
            "strict_supported_advantage_interval": interval,
            "equal_every_dwell": slope == 0 and intercept == 0,
            "acceptance_quality_equal_assumed": True,
            "deployment_authorized": False, "empirical_claims_proven": False}


def accepted_resource_comparison(hover_energy_j=None, supported_energy_j=None,
                                hover_time_s=None, supported_time_s=None,
                                hover_acceptance=None, supported_acceptance=None):
    """Compare ratios of expected whole-mission resources to accepted counts.

    Probability lists describe matched attempted tasks. Linearity of expectation
    gives sum(p_i); independence is not required. Lists are assumptions unless
    separately supported by measurements. Zero expected successes is undefined.
    This is not E[energy / accepted_count] for a single mission.
    """
    values, missing = _inputs({
        "hover_energy_j": (hover_energy_j, 0, None, True),
        "supported_energy_j": (supported_energy_j, 0, None, False),
        "hover_time_s": (hover_time_s, 0, None, True),
        "supported_time_s": (supported_time_s, 0, None, False),
    })
    probabilities = {}
    for name, supplied in (("hover_acceptance", hover_acceptance),
                           ("supported_acceptance", supported_acceptance)):
        if supplied is None:
            missing.append(name)
        elif not isinstance(supplied, (list, tuple)) or not supplied:
            raise ValueError(f"{name}: nonempty probability list required")
        elif any(value is None for value in supplied):
            for i, value in enumerate(supplied):
                if value is not None:
                    _number(f"{name}[{i}]", value, 0, 1)
            missing.append(f"{name}: one or more task probabilities unknown")
        else:
            probabilities[name] = [_number(f"{name}[{i}]", value, 0, 1)
                                   for i, value in enumerate(supplied)]
    if hover_acceptance is not None and supported_acceptance is not None:
        if len(hover_acceptance) != len(supported_acceptance):
            raise ValueError("Acceptance lists must represent the same matched task count")
    if missing:
        return _unknown(missing)
    count_h = math.fsum(probabilities["hover_acceptance"])
    count_s = math.fsum(probabilities["supported_acceptance"])
    result = {"status": "conditional_ratio_of_expectations_only",
              "hover_expected_accepted_count": count_h,
              "supported_expected_accepted_count": count_s,
              "deployment_authorized": False, "empirical_claims_proven": False}
    if count_h == 0 or count_s == 0:
        result.update(status="undefined_zero_expected_accepted_count",
                      energy_advantage=None, time_advantage=None, both_advantages=None)
        return result
    energy_ratio = _ratio("computed_energy_ratio", values["supported_energy_j"], values["hover_energy_j"])
    time_ratio = _ratio("computed_time_ratio", values["supported_time_s"], values["hover_time_s"])
    acceptance_ratio = _ratio("computed_accepted_count_ratio", count_s, count_h)
    result.update(
        expected_accepted_count_ratio=acceptance_ratio,
        energy_ratio=energy_ratio, time_ratio=time_ratio,
        strict_both_advantage_required_count_ratio=max(energy_ratio, time_ratio),
        hover_energy_j_per_expected_accepted=_ratio("computed_hover_energy_per_accepted", values["hover_energy_j"], count_h),
        supported_energy_j_per_expected_accepted=_ratio("computed_supported_energy_per_accepted", values["supported_energy_j"], count_s),
        hover_time_s_per_expected_accepted=_ratio("computed_hover_time_per_accepted", values["hover_time_s"], count_h),
        supported_time_s_per_expected_accepted=_ratio("computed_supported_time_per_accepted", values["supported_time_s"], count_s),
        energy_advantage=acceptance_ratio > energy_ratio,
        time_advantage=acceptance_ratio > time_ratio,
        both_advantages=acceptance_ratio > max(energy_ratio, time_ratio),
        strict_both_advantage_possible_at_hover_count=max(energy_ratio, time_ratio)
            < len(probabilities["supported_acceptance"]) / count_h,
    )
    return result


def unknown_design_assessment():
    """Default output deliberately contains no numerical design assumption."""
    return {"static_envelope": static_envelope(),
            "restoring_sign": restoring_coefficient(),
            "dwell_advantage": dwell_advantage_interval(),
            "accepted_resources": accepted_resource_comparison(),
            "claims": {"aircraft_feasibility": "unproven",
                       "drone_superiority": "unproven",
                       "independent_2018_accuracy": "unproven",
                       "ecological_benefit": "unproven"},
            "deployment_authorized": False}
