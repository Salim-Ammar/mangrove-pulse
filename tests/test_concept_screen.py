"""Synthetic mathematical/metadata tests to execute in Colab, not field tests."""
import unittest
from concept_screen import assess, blank_parameters, euler_rhs


def supplied(**values):
    records = blank_parameters()
    for key, value in values.items():
        records[key].update(value=value, kind="assumption", source="synthetic unit test",
                            conditions_and_uncertainty="Artificial values, not any aircraft or site")
    return records


class ConceptTests(unittest.TestCase):
    def test_unknown_is_not_success(self):
        r = assess(blank_parameters())
        self.assertTrue(all(x["status"] == "unknown_missing_inputs" for x in r["screens"].values()))
        self.assertFalse(r["deployment_authorized"])
        self.assertTrue(all(x == "unproven" for x in r["claims"].values()))

    def test_buoyancy_failure(self):
        r = assess(supplied(all_up_wet_mass_kg=10, water_density_kg_m3=1000, displacement_limit_m3=.009))
        self.assertEqual(r["screens"]["buoyancy"]["status"], "fails_necessary_screen")

    def test_boundary_not_pass(self):
        r = assess(supplied(all_up_wet_mass_kg=10, water_density_kg_m3=1000, displacement_limit_m3=.01))
        self.assertEqual(r["screens"]["buoyancy"]["status"], "boundary_no_margin")

    def test_static_thrust(self):
        r = assess(supplied(all_up_wet_mass_kg=1, gravity_m_s2=10, available_thrust_n=9, tilt_deg=0))
        self.assertEqual(r["screens"]["static_vertical_thrust"]["status"], "fails_necessary_screen")

    def test_recovery_reserve_reverse_margin(self):
        r = assess(supplied(usable_battery_wh=100, planned_complete_mission_wh=80, additional_recovery_wh=15, required_reserve_wh=10))
        self.assertEqual(r["screens"]["battery_energy"]["remaining_after_all_costs_wh"], -5)

    def test_peak_power_separate_from_energy(self):
        r = assess(supplied(available_peak_power_w=20, required_peak_power_w=30))
        self.assertEqual(r["screens"]["peak_power"]["status"], "fails_necessary_screen")

    def test_euler_coupling_and_energy(self):
        a = euler_rhs([2, 3, 4], [1, 2, 3], [0, 0, 0])
        self.assertEqual(a, [-3, 2, -.5])
        self.assertEqual(sum(i*w*x for i, w, x in zip([2, 3, 4], [1, 2, 3], a)), 0)

    def test_euler_torque_at_rest(self):
        self.assertEqual(euler_rhs([2, 3, 4], [0, 0, 0], [2, 6, 12]), [1, 2, 3])

    def test_impossible_inertia(self):
        with self.assertRaises(ValueError):
            euler_rhs([1, 1, 3], [0, 0, 0], [0, 0, 0])
        with self.assertRaises(ValueError):
            assess(supplied(principal_inertia_kg_m2=[1, 1, 3]))

    def test_response_requires_applicability(self):
        r = assess(supplied(first_order_response_applicable=False, sensor_tau_s=1, stable_dwell_s=10, residual_error_limit=.05))
        self.assertEqual(r["screens"]["sensor_settling"]["status"], "model_not_applicable")

    def test_settling_failure(self):
        r = assess(supplied(first_order_response_applicable=True, sensor_tau_s=1, stable_dwell_s=1, residual_error_limit=.05))
        self.assertEqual(r["screens"]["sensor_settling"]["status"], "fails_necessary_screen")

    def test_same_acceptance_different_tradeoffs(self):
        r = assess(supplied(hover_complete_energy_wh=10, supported_complete_energy_wh=8, hover_complete_time_s=10,
                           supported_complete_time_s=12, hover_acceptance_fraction=.5, supported_acceptance_fraction=.5))
        f = r["screens"]["accepted_resource_frontier"]
        self.assertTrue(f["energy_improves_under_inputs"])
        self.assertFalse(f["time_improves_under_inputs"])
        self.assertFalse(r["deployment_authorized"])

    def test_zero_acceptance_not_division(self):
        r = assess(supplied(hover_complete_energy_wh=10, supported_complete_energy_wh=8, hover_complete_time_s=10,
                           supported_complete_time_s=12, hover_acceptance_fraction=0, supported_acceptance_fraction=.5))
        self.assertEqual(r["screens"]["accepted_resource_frontier"]["status"], "undefined_per_accepted_comparison_zero_acceptance")

    def test_bad_partial_values(self):
        for value in (True, float("nan"), float("inf"), -1, 0):
            with self.subTest(value=value), self.assertRaises(ValueError):
                assess(supplied(all_up_wet_mass_kg=value))

    def test_missing_provenance_or_wrong_unit(self):
        for field, value in (("source", ""), ("unit", "litres")):
            r = supplied(displacement_limit_m3=.01)
            r["displacement_limit_m3"][field] = value
            with self.assertRaises(ValueError):
                assess(r)

    def test_unknown_recovery_not_zero(self):
        r = assess(supplied(usable_battery_wh=100, planned_complete_mission_wh=80, required_reserve_wh=10))
        self.assertEqual(r["screens"]["battery_energy"]["status"], "unknown_missing_inputs")


if __name__ == "__main__":
    unittest.main()
