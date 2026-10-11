"""Unit, conservation, boundary and sensitivity checks for the analytical model."""

from dataclasses import replace
import math
import unittest

from sampling_energy_model import (Scenario, build_results, evaluate,
                                   induced_power_w, original_report_arithmetic)


class SamplingEnergyTests(unittest.TestCase):
    def test_original_hover_table(self):
        area = 4 * math.pi * 0.4 ** 2
        self.assertAlmostEqual(induced_power_w(23, area), 1527.0290516837522)
        self.assertAlmostEqual(induced_power_w(43, area), 3903.5363591526134)

    def test_mass_and_area_scaling(self):
        self.assertAlmostEqual(induced_power_w(9.6, 0.8) / induced_power_w(8, 0.8),
                               1.2 ** 1.5)
        self.assertAlmostEqual(induced_power_w(8, 3.2), induced_power_w(8, 0.8) / 2)

    def test_independent_hand_case_and_unit_conversion(self):
        s = replace(Scenario(), baseline_mass_kg=1, added_support_mass_kg=0,
                    disk_area_m2=0.5, air_density_kg_m3=1, gravity_m_s2=1,
                    loss_multiplier=1, common_air_load_w=0, supported_total_power_w=0,
                    travel_time_s=3600, sites=1, dwell_per_site_s=3600,
                    transition_per_site_s=0)
        result = evaluate(s)  # Ideal power = 1 W, independent of production equation.
        self.assertAlmostEqual(result["hover_energy_wh"], 2)
        self.assertAlmostEqual(result["supported_energy_wh"], 1)

    def test_segment_conservation(self):
        result = evaluate(Scenario())
        self.assertAlmostEqual(sum(result["hover_segments_wh"].values()),
                               result["hover_energy_wh"])
        self.assertAlmostEqual(sum(result["supported_segments_wh"].values()),
                               result["supported_energy_wh"])
        self.assertAlmostEqual(result["saving_wh"], result["hover_energy_wh"] -
                               result["supported_energy_wh"])

    def test_break_even_and_both_sides(self):
        base = Scenario()
        threshold = evaluate(base)["break_even_dwell_per_site_s"]
        self.assertGreater(threshold, 0)
        self.assertAlmostEqual(evaluate(replace(base, dwell_per_site_s=threshold))["saving_wh"], 0)
        self.assertLess(evaluate(replace(base, dwell_per_site_s=threshold / 2))["saving_wh"], 0)
        self.assertGreater(evaluate(replace(base, dwell_per_site_s=threshold * 2))["saving_wh"], 0)

    def test_identical_power_no_benefit(self):
        base = replace(Scenario(), added_support_mass_kg=0, transition_per_site_s=0)
        p = evaluate(base)["baseline_air_power_w"]
        result = evaluate(replace(base, supported_total_power_w=p))
        self.assertIsNone(result["break_even_dwell_per_site_s"])
        self.assertAlmostEqual(result["saving_wh"], 0)
        self.assertFalse(result["supported_energy_lower"])

    def test_supported_power_above_hover_never_wins(self):
        base = Scenario()
        p = evaluate(base)["baseline_air_power_w"]
        result = evaluate(replace(base, supported_total_power_w=p + 1))
        self.assertIsNone(result["break_even_dwell_per_site_s"])
        self.assertLess(result["saving_wh"], 0)

    def test_free_support_zero_penalty(self):
        base = replace(Scenario(), added_support_mass_kg=0, transition_per_site_s=0)
        self.assertEqual(evaluate(base)["break_even_dwell_per_site_s"], 0)
        self.assertTrue(evaluate(base)["supported_energy_lower"])

    def test_sensitivity_directions(self):
        base = Scenario()
        threshold = evaluate(base)["break_even_dwell_per_site_s"]
        for change in ({"added_support_mass_kg": 4}, {"travel_time_s": 600},
                       {"transition_per_site_s": 60}, {"supported_total_power_w": 150},
                       {"additional_support_overhead_wh": 80}):
            self.assertGreater(evaluate(replace(base, **change))["break_even_dwell_per_site_s"],
                               threshold)
        self.assertLess(evaluate(replace(base, sites=5))["break_even_dwell_per_site_s"], threshold)

    def test_budget_gate_is_not_savings_gate(self):
        result = evaluate(replace(Scenario(), travel_time_s=1200, dwell_per_site_s=300))
        self.assertTrue(result["supported_energy_lower"])
        self.assertFalse(result["supported_within_energy_budget"])
        self.assertFalse(result["operational_feasibility_established"])

    def test_reserve_withheld_not_double_counted(self):
        result = evaluate(Scenario())
        self.assertAlmostEqual(result["usable_battery_wh"], 192)
        s = replace(Scenario(), battery_usable_fraction=1)
        self.assertEqual(evaluate(s)["hover_energy_wh"], result["hover_energy_wh"])

    def test_time_accounts_for_transitions(self):
        result = evaluate(Scenario())
        self.assertEqual(result["supported_accounted_duration_s"] -
                         result["hover_accounted_duration_s"], 90)

    def test_report_arithmetic(self):
        result = original_report_arithmetic()
        self.assertAlmostEqual(result["area_of_50_by_100_m_km2"], 0.005)
        self.assertAlmostEqual(result["contact_pressure_30_kg_kpa"], 14.715)
        self.assertAlmostEqual(result["segment_energy_with_10_percent_addition_wh"], 386.8333333333333)
        self.assertAlmostEqual(result["flight_segment_duration_min"], 11 + 2 / 3)

    def test_invalid_inputs(self):
        for changes in ({"sites": 0}, {"sites": 1.5}, {"sites": True},
                        {"added_support_mass_kg": -1}, {"disk_area_m2": 0},
                        {"battery_usable_fraction": 0}, {"battery_usable_fraction": 1.1},
                        {"loss_multiplier": 0.9}, {"travel_time_s": math.nan},
                        {"dwell_per_site_s": math.inf}, {"supported_total_power_w": -1}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                evaluate(replace(Scenario(), **changes))
        with self.assertRaises(ValueError):
            induced_power_w(0, 1)

    def test_sweep_and_determinism(self):
        results = build_results()
        self.assertEqual(results, build_results())
        self.assertEqual(results["sweep_summary"]["scenarios"], 864)
        statuses = {row["result"]["supported_energy_lower"] for row in results["sweep"]}
        self.assertEqual(statuses, {False, True})
        for row in results["sweep"]:
            s, result = row["inputs"], row["result"]
            threshold = result["break_even_dwell_per_site_s"]
            if threshold is not None and abs(s["dwell_per_site_s"] - threshold) > 1e-6:
                self.assertEqual(result["supported_energy_lower"], s["dwell_per_site_s"] > threshold)


if __name__ == "__main__":
    unittest.main()
