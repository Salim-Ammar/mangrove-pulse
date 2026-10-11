"""Synthetic equation/domain verification only; not aircraft or field tests."""
import math
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from supported_sensing_envelope import (
    accepted_resource_comparison, dwell_advantage_interval,
    restoring_coefficient, static_envelope, unknown_design_assessment,
)


class SupportedEnvelopeTests(unittest.TestCase):
    def test_unknown_defaults_remain_unknown(self):
        result = unknown_design_assessment()
        for key in ("static_envelope", "restoring_sign", "dwell_advantage", "accepted_resources"):
            self.assertEqual(result[key]["status"], "unknown")
            self.assertTrue(result[key]["missing_inputs"])
        self.assertFalse(result["deployment_authorized"])
        self.assertTrue(all(value == "unproven" for value in result["claims"].values()))

    def test_buoyancy_limited_envelope(self):
        result = static_envelope(2, 1, .004, 1000, 100, 0, 1, 10)
        self.assertEqual(result["maximum_support_mass_kg"], 2)
        self.assertEqual(result["mass_slack_kg"], 1)
        self.assertTrue(result["necessary_constraints_satisfied"])
        self.assertFalse(result["stability_proven"])

    def test_lift_limited_envelope(self):
        result = static_envelope(2, 1, .020, 1000, 40, 0, 2, 10)
        self.assertEqual(result["maximum_support_mass_kg"], 0)
        self.assertFalse(result["necessary_constraints_satisfied"])

    def test_boundary_is_only_necessary_equality(self):
        result = static_envelope(2, 2, .004, 1000, 100, 0, 1, 10)
        self.assertEqual(result["mass_slack_kg"], 0)
        self.assertTrue(result["necessary_constraints_satisfied"])
        self.assertFalse(result["wet_takeoff_proven"])
        self.assertFalse(result["deployment_authorized"])

    def test_tilt_and_margin_reduce_lift_capacity(self):
        result = static_envelope(1, 0, .020, 1000, 100, 60, 2, 10)
        self.assertAlmostEqual(result["vertical_lift_capacity_kg"], 2.5)

    def test_empty_envelope_rejects_specified_design(self):
        result = static_envelope(5, 0, .004, 1000, 100, 0, 1, 10)
        self.assertEqual(result["maximum_support_mass_kg"], -1)
        self.assertFalse(result["necessary_constraints_satisfied"])

    def test_invalid_domains_and_nonfinite(self):
        for bad in (True, "1", math.inf, math.nan):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                static_envelope(m0_kg=bad)
        for key, bad in (("support_kg", -1), ("lift_margin", .9),
                         ("gravity_m_s2", 0), ("tilt_deg", 90), ("tilt_deg", -1)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                static_envelope(**{key: bad})

    def test_missing_input_does_not_hide_invalid_input(self):
        with self.assertRaises(ValueError):
            dwell_advantage_interval(hover_fixed_j=None, supported_dwell_w=-1)

    def test_numerical_overflow_cannot_be_reported_as_a_design_result(self):
        with self.assertRaises(ValueError):
            static_envelope(1, 0, 1e308, 1e308, 100, 0, 1, 10)
        with self.assertRaises(ValueError):
            restoring_coefficient(1e308, 1e308, .1)
        with self.assertRaises(ValueError):
            dwell_advantage_interval(100, 200, 1e308, 0, 100)
        with self.assertRaises(ValueError):
            accepted_resource_comparison(1e308, 50, 100, 50, [1e-308], [1])
        with self.assertRaises(ValueError):
            static_envelope(m0_kg=10 ** 1000)

    def test_numerical_underflow_does_not_create_a_false_tie(self):
        with self.assertRaises(ValueError):
            restoring_coefficient(1e-200, 1e-200, .1)
        with self.assertRaises(ValueError):
            accepted_resource_comparison(1e308, 1e-308, 100, 50, [1], [1])

    def test_restoring_sign_and_dimensions(self):
        result = restoring_coefficient(2, 10, .1)
        self.assertEqual(result["coefficient_n_m_per_rad"], 2)
        self.assertEqual(result["sign"], "restoring")
        self.assertFalse(result["dynamic_stability_proven"])

    def test_neutral_and_destabilizing_are_not_passes(self):
        self.assertEqual(restoring_coefficient(2, 10, 0)["sign"], "neutral_linear_order")
        self.assertEqual(restoring_coefficient(2, 10, -.1)["sign"], "destabilizing")

    def test_positive_break_even_dwell(self):
        result = dwell_advantage_interval(100, 400, 10, 2, 3)
        self.assertEqual(result["algebraic_equality_dwell_s"], 12.5)
        self.assertEqual(result["strict_supported_advantage_interval"],
                         {"lower_s": 12.5, "lower_inclusive": False, "upper_s": None})

    def test_short_dwell_can_win_when_supported_power_is_higher(self):
        result = dwell_advantage_interval(400, 100, 2, 10, 3)
        self.assertEqual(result["strict_supported_advantage_interval"],
                         {"lower_s": 0.0, "lower_inclusive": True,
                          "upper_s": 12.5, "upper_inclusive": False})

    def test_all_nonnegative_dwell_advantage(self):
        result = dwell_advantage_interval(400, 100, 10, 2, 3)
        self.assertEqual(result["strict_supported_advantage_interval"],
                         {"lower_s": 0.0, "lower_inclusive": True, "upper_s": None})

    def test_same_power_offset_and_tie(self):
        self.assertTrue(dwell_advantage_interval(100, 100, 2, 2, 1)["equal_every_dwell"])
        self.assertIsNone(dwell_advantage_interval(100, 200, 2, 2, 1)["strict_supported_advantage_interval"])
        self.assertIsNotNone(dwell_advantage_interval(200, 100, 2, 2, 1)["strict_supported_advantage_interval"])

    def test_zero_boundary_is_not_strict_advantage_at_zero(self):
        result = dwell_advantage_interval(100, 100, 10, 2, 1)
        self.assertFalse(result["strict_supported_advantage_interval"]["lower_inclusive"])
        self.assertIsNone(dwell_advantage_interval(100, 100, 2, 10, 1)["strict_supported_advantage_interval"])

    def test_attempt_count_is_positive_integer(self):
        for bad in (0, -1, 1.5, True):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                dwell_advantage_interval(attempted_tasks=bad)

    def test_interval_matches_direct_energy_on_synthetic_grid(self):
        for eh0, es0, ph, ps, n in ((100, 400, 10, 2, 3), (400, 100, 2, 10, 3),
                                   (100, 100, 2, 2, 1), (200, 100, 2, 2, 2),
                                   (100, 100, 10, 2, 1), (400, 100, 10, 2, 3)):
            interval = dwell_advantage_interval(eh0, es0, ph, ps, n)["strict_supported_advantage_interval"]
            for dwell in (0, 1, 12.5, 13, 100):
                expected = es0 + n * ps * dwell < eh0 + n * ph * dwell
                inside = False
                if interval:
                    inside = dwell > interval["lower_s"] or (
                        interval["lower_inclusive"] and dwell == interval["lower_s"])
                    if interval["upper_s"] is not None:
                        inside = inside and dwell < interval["upper_s"]
                self.assertEqual(inside, expected)

    def test_energy_advantage_need_not_be_time_advantage(self):
        result = accepted_resource_comparison(100, 75, 100, 112, [.8, .8], [.8, .8])
        self.assertTrue(result["energy_advantage"])
        self.assertFalse(result["time_advantage"])
        self.assertFalse(result["both_advantages"])

    def test_heterogeneous_probabilities_use_expected_counts(self):
        result = accepted_resource_comparison(100, 50, 100, 50, [.1, .9], [.4, .4])
        self.assertAlmostEqual(result["hover_expected_accepted_count"], 1)
        self.assertAlmostEqual(result["supported_expected_accepted_count"], .8)
        self.assertAlmostEqual(result["supported_energy_j_per_expected_accepted"], 62.5)
        self.assertTrue(result["both_advantages"])

    def test_probability_ceiling_can_make_both_advantages_impossible(self):
        result = accepted_resource_comparison(100, 75, 100, 112, [.95, .95], [1, 1])
        self.assertFalse(result["strict_both_advantage_possible_at_hover_count"])
        self.assertFalse(result["both_advantages"])

    def test_zero_success_is_undefined_not_zero_resource(self):
        for ph, ps in (([0], [0]), ([0], [.5]), ([.5], [0])):
            result = accepted_resource_comparison(100, 50, 100, 50, ph, ps)
            self.assertEqual(result["status"], "undefined_zero_expected_accepted_count")
            self.assertIsNone(result["both_advantages"])

    def test_invalid_and_mismatched_probability_records(self):
        for ph, ps in (([], []), ([1], [1, 1]), ([1.1], [1]), ([True], [1]),
                       ([-.1], [1]), ([math.nan], [1]), ("bad", [1])):
            with self.subTest(ph=ph), self.assertRaises(ValueError):
                accepted_resource_comparison(100, 50, 100, 50, ph, ps)

    def test_unknown_probability_cannot_be_filled_with_success(self):
        result = accepted_resource_comparison(100, 50, 100, 50, [.5, None], [.5, .5])
        self.assertEqual(result["status"], "unknown")
        self.assertNotIn("both_advantages", result)

    def test_resource_comparison_matches_direct_ratios(self):
        for es, ts, ph, ps in ((75, 112, .8, .8), (150, 75, .5, .8), (50, 50, .9, .2)):
            result = accepted_resource_comparison(100, es, 100, ts, [ph], [ps])
            self.assertEqual(result["energy_advantage"], es / ps < 100 / ph)
            self.assertEqual(result["time_advantage"], ts / ps < 100 / ph)
            self.assertFalse(result["empirical_claims_proven"])


if __name__ == "__main__":
    unittest.main()
