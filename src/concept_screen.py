"""Conditional analytic screens; no flight simulation, accuracy or ecology claim."""
import math


PARAMETER_UNITS = {
    "all_up_wet_mass_kg": "kg", "water_density_kg_m3": "kg/m^3",
    "displacement_limit_m3": "m^3", "gravity_m_s2": "m/s^2",
    "available_thrust_n": "N", "tilt_deg": "degree",
    "principal_inertia_kg_m2": "three kg*m^2 components",
    "angular_velocity_rad_s": "three rad/s components",
    "net_body_torque_nm": "three N*m components",
    "usable_battery_wh": "Wh", "planned_complete_mission_wh": "Wh",
    "additional_recovery_wh": "Wh", "required_reserve_wh": "Wh",
    "available_peak_power_w": "W", "required_peak_power_w": "W",
    "first_order_response_applicable": "boolean declaration",
    "sensor_tau_s": "s", "stable_dwell_s": "s",
    "residual_error_limit": "fraction of initial step error",
    "hover_complete_energy_wh": "Wh", "supported_complete_energy_wh": "Wh",
    "hover_complete_time_s": "s", "supported_complete_time_s": "s",
    "hover_acceptance_fraction": "fraction", "supported_acceptance_fraction": "fraction",
}


def blank_parameters():
    return {key: {"value": None, "unit": unit, "kind": "unknown",
                  "source": None, "conditions_and_uncertainty": None}
            for key, unit in PARAMETER_UNITS.items()}


def finite(value, name, minimum=None, maximum=None, strict_min=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name}: finite number required")
    if minimum is not None and (value < minimum or (strict_min and value == minimum)):
        raise ValueError(f"{name}: outside lower bound")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name}: outside upper bound")
    return value


def values_from_records(records):
    if set(records) != set(PARAMETER_UNITS):
        raise ValueError("Parameter keys must match the documented register")
    values = {}
    for key, unit in PARAMETER_UNITS.items():
        record = records[key]
        if record.get("unit") != unit:
            raise ValueError(f"{key}: wrong unit declaration")
        value = record.get("value")
        if value is None:
            if record.get("kind") != "unknown":
                raise ValueError(f"{key}: null must remain unknown")
        else:
            if record.get("kind") not in {"assumption", "declared_measurement", "saved_hypothetical_result"}:
                raise ValueError(f"{key}: evidence kind required")
            for field in ("source", "conditions_and_uncertainty"):
                if not isinstance(record.get(field), str) or not record[field].strip():
                    raise ValueError(f"{key}: {field} required")
        values[key] = value
    return values


def vector3(value, name, positive=False):
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError(f"{name}: three components required")
    return [finite(v, name, minimum=0 if positive else None, strict_min=positive) for v in value]


def euler_rhs(inertia, omega, torque):
    """Instantaneous derivative about CM in body principal axes, not stability."""
    ix, iy, iz = vector3(inertia, "inertia", positive=True)
    largest = max(ix, iy, iz)
    others = sorted((ix, iy, iz))[:2]
    if largest / 2 > others[0] / 2 + others[1] / 2:
        raise ValueError("Principal moments violate the physical inertia triangle")
    wx, wy, wz = vector3(omega, "angular velocity")
    tx, ty, tz = vector3(torque, "net body torque")
    result = [(tx + (iy - iz) * wy * wz) / ix,
              (ty + (iz - ix) * wz * wx) / iy,
              (tz + (ix - iy) * wx * wy) / iz]
    return [finite(x, "angular acceleration") for x in result]


def margin_status(value):
    finite(value, "derived margin")
    return "fails_necessary_screen" if value < 0 else ("boundary_no_margin" if value == 0 else "conditional_margin_only")


def assess(records):
    v = values_from_records(records)
    # Validate supplied values even if another input in the same group is missing.
    signed = {"tilt_deg", "principal_inertia_kg_m2", "angular_velocity_rad_s", "net_body_torque_nm", "first_order_response_applicable"}
    zero_allowed = {"additional_recovery_wh", "required_reserve_wh", "stable_dwell_s", "hover_acceptance_fraction", "supported_acceptance_fraction"}
    for key, value in v.items():
        if value is not None and key not in signed:
            finite(value, key, minimum=0, strict_min=key not in zero_allowed)
    for key in ("hover_acceptance_fraction", "supported_acceptance_fraction", "residual_error_limit"):
        if v[key] is not None:
            finite(v[key], key, minimum=0, maximum=1, strict_min=key == "residual_error_limit")
    if v["residual_error_limit"] == 1:
        raise ValueError("Residual error limit must be strictly less than one")
    if v["tilt_deg"] is not None:
        finite(v["tilt_deg"], "tilt", minimum=0, maximum=89.999999)
    for key in ("principal_inertia_kg_m2", "angular_velocity_rad_s", "net_body_torque_nm"):
        if v[key] is not None:
            vector3(v[key], key, positive=key == "principal_inertia_kg_m2")
    if v["principal_inertia_kg_m2"] is not None:
        # Reject an impossible declared inertia even if velocities/torques are absent.
        euler_rhs(v["principal_inertia_kg_m2"], [0, 0, 0], [0, 0, 0])
    if v["first_order_response_applicable"] is not None and not isinstance(v["first_order_response_applicable"], bool):
        raise ValueError("Response applicability must be boolean or unknown")
    def ready(*keys):
        return all(v[key] is not None for key in keys)
    report = {"status": "conditional_analytic_assessment_not_field_validation",
              "deployment_authorized": False,
              "claims": {key: "unproven" for key in ("independent_2018_accuracy", "drone_superiority", "ecological_benefit")},
              "source_declarations_independently_verified": False,
              "screens": {key: {"status": "unknown_missing_inputs"} for key in
                          ("buoyancy", "static_vertical_thrust", "battery_energy", "peak_power", "sensor_settling", "euler_dynamics", "accepted_resource_frontier")},
              "unassessed": ["task utility and acceptance rule", "independent dated reference truth", "permissions and habitat disturbance",
                             "float restoring stability and freeboard", "wind waves current and station keeping", "water transitions and recovery",
                             "closed-loop orientation and translational dynamics", "sensor bias calibration contamination and positioning",
                             "ecological outcomes and lifecycle costs"]}
    s = report["screens"]
    if ready("all_up_wet_mass_kg", "water_density_kg_m3", "displacement_limit_m3"):
        required = finite(v["all_up_wet_mass_kg"] / v["water_density_kg_m3"], "required displacement")
        margin = v["displacement_limit_m3"] - required
        s["buoyancy"] = {"status": margin_status(margin), "required_displacement_m3": required, "volume_margin_m3": margin}
    if ready("all_up_wet_mass_kg", "gravity_m_s2", "available_thrust_n", "tilt_deg"):
        margin = v["available_thrust_n"] * math.cos(math.radians(v["tilt_deg"])) - v["all_up_wet_mass_kg"] * v["gravity_m_s2"]
        s["static_vertical_thrust"] = {"status": margin_status(margin), "vertical_margin_n": margin}
    if ready("usable_battery_wh", "planned_complete_mission_wh", "additional_recovery_wh", "required_reserve_wh"):
        margin = v["usable_battery_wh"] - v["planned_complete_mission_wh"] - v["additional_recovery_wh"] - v["required_reserve_wh"]
        s["battery_energy"] = {"status": margin_status(margin), "remaining_after_all_costs_wh": margin}
    if ready("available_peak_power_w", "required_peak_power_w"):
        margin = v["available_peak_power_w"] - v["required_peak_power_w"]
        s["peak_power"] = {"status": margin_status(margin), "power_margin_w": margin}
    if v["first_order_response_applicable"] is False:
        s["sensor_settling"] = {"status": "model_not_applicable"}
    elif v["first_order_response_applicable"] is True and ready("sensor_tau_s", "stable_dwell_s", "residual_error_limit"):
        required = -v["sensor_tau_s"] * math.log(v["residual_error_limit"])
        margin = v["stable_dwell_s"] - required
        s["sensor_settling"] = {"status": margin_status(margin), "required_stable_dwell_s": finite(required, "settling time")}
    if ready("principal_inertia_kg_m2", "angular_velocity_rad_s", "net_body_torque_nm"):
        s["euler_dynamics"] = {"status": "instantaneous_derivative_only_not_stability", "omega_dot_rad_s2":
                               euler_rhs(v["principal_inertia_kg_m2"], v["angular_velocity_rad_s"], v["net_body_torque_nm"])}
    if ready("hover_complete_energy_wh", "supported_complete_energy_wh", "hover_complete_time_s", "supported_complete_time_s"):
        er = finite(v["supported_complete_energy_wh"] / v["hover_complete_energy_wh"], "energy ratio")
        tr = finite(v["supported_complete_time_s"] / v["hover_complete_time_s"], "time ratio")
        f = {"status": "conditional_thresholds_acceptance_unknown", "strict_energy_ratio_threshold": er,
             "strict_time_ratio_threshold": tr, "strict_joint_ratio_threshold": max(er, tr),
             "assumptions": "Identical attempted tasks and quality rules; complete expected costs across repeated missions, including failures/recovery"}
        if ready("hover_acceptance_fraction", "supported_acceptance_fraction"):
            ph, ps = v["hover_acceptance_fraction"], v["supported_acceptance_fraction"]
            if ph == 0 or ps == 0:
                f["status"] = "undefined_per_accepted_comparison_zero_acceptance"
            else:
                ratio = finite(ps / ph, "acceptance ratio")
                f.update(status="conditional_comparison_only", declared_acceptance_ratio=ratio,
                         energy_improves_under_inputs=ratio > er, time_improves_under_inputs=ratio > tr)
        s["accepted_resource_frontier"] = f
    return report
