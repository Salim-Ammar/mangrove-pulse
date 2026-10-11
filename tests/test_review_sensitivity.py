import unittest
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from review_sensitivity import edge_mask, agreement, select_threshold


class ReviewSensitivityTests(unittest.TestCase):
    def test_diagonal_transition_counts_but_outside_does_not(self):
        ref = np.array([[255, 0, 0], [0, 0, 0], [0, 0, 1]])
        np.testing.assert_array_equal(edge_mask(ref),
                                      [[False, False, False],
                                       [False, True, True],
                                       [False, True, True]])

    def test_unknown_cells_are_not_transition_edges(self):
        np.testing.assert_array_equal(edge_mask(np.array([[255, 0], [0, 0]])),
                                      np.zeros((2, 2), bool))

    def test_masked_cells_do_not_enter_confusion_counts(self):
        result = agreement(np.array([1, 1, 0, 0, 1], bool),
                           np.array([1, 0, 1, 0, 0], bool),
                           np.array([1, 1, 1, 1, 0], bool))
        self.assertEqual(result, dict(tp=1, fp=1, fn=1, tn=1,
                                     precision=.5, recall=.5, f1=.5, iou=1/3))

    def test_empty_positive_denominators_are_unknown_not_perfect(self):
        result = agreement(np.array([False]), np.array([False]), np.array([True]))
        self.assertEqual(result['tn'], 1)
        self.assertIsNone(result['f1'])
        self.assertIsNone(result['recall'])

    def test_threshold_tie_chooses_highest_and_uses_only_calibration(self):
        # Calibration: 50 positives at .605 and 50 negatives at .20.
        # An excluded positive at -1 must not change threshold selection.
        x = np.array([.605]*50 + [.2]*50 + [-1.])
        y = np.array([True]*50 + [False]*50 + [True])
        mask = np.array([True]*100 + [False])
        threshold, scores = select_threshold(x, y, mask)
        self.assertAlmostEqual(threshold, .6)
        self.assertEqual(scores['f1'], 1.)

    def test_small_class_stops_without_moving_split(self):
        with self.assertRaisesRegex(ValueError, '50'):
            select_threshold(np.array([.6, .2]), np.array([True, False]),
                             np.array([True, True]))


if __name__ == '__main__':
    unittest.main()
