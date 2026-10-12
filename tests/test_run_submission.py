"""Runner failure fixtures; no satellite processing or real analysis engine."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from run_submission import run, compare, compare_csv
import run_submission


class CoveragePolicyTests(unittest.TestCase):
    def report(self, tp=2, fp=1, fn=1, tn=6, excluded_positive=2, excluded_negative=3):
        summary = {'held_out': {'test-date': {
            'all_eligible_southern_cells': {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn},
            'evaluation_coverage': {'total': tp+fp+fn+tn, 'mapped_mangrove': tp+fn, 'not_mapped': fp+tn},
            'evaluation_excluded': {'total': excluded_positive+excluded_negative,
                                   'mapped_mangrove': excluded_positive, 'not_mapped': excluded_negative}}}}
        self.assertTrue(callable(getattr(run_submission, 'coverage_policy_report', None)),
                        'Runner must derive the explicit coverage-policy report')
        return run_submission.coverage_policy_report(summary)

    def test_exclusions_are_negative_predictions_not_worst_case(self):
        report = self.report()
        self.assertEqual(report['policy'], 'excluded_cells_as_negative_predictions')
        row = report['dates']['test-date']
        self.assertEqual(row['eligible_cells'], 10)
        self.assertEqual(row['excluded_cells'], 5)
        self.assertEqual(row['population_cells'], 15)
        self.assertAlmostEqual(row['eligible_f1'], 2/3)
        self.assertEqual(row['policy_counts'], {'tp': 2, 'fp': 1, 'fn': 3, 'tn': 9})
        self.assertEqual(row['policy_f1'], 0.5)
        self.assertEqual(row['policy_recall'], 0.4)
        self.assertEqual(row['eligible_fraction'], 2/3)

    def test_no_exclusions_preserves_f1(self):
        row = self.report(excluded_positive=0, excluded_negative=0)['dates']['test-date']
        self.assertEqual(row['eligible_f1'], row['policy_f1'])
        self.assertEqual(row['eligible_fraction'], 1.0)

    def test_undefined_metrics_are_null_not_perfect_scores(self):
        row = self.report(0, 0, 0, 0, 0, 0)['dates']['test-date']
        self.assertIsNone(row['eligible_f1'])
        self.assertIsNone(row['policy_f1'])
        self.assertIsNone(row['policy_recall'])
        self.assertIsNone(row['eligible_fraction'])

    def test_saved_date_counts_reproduce_documented_scores(self):
        self.assertTrue(callable(getattr(run_submission, 'coverage_policy_report', None)))
        root = Path(__file__).resolve().parents[1]
        summary = json.loads((root/'examples/baseline/baseline_summary.json').read_text())
        report = run_submission.coverage_policy_report(summary)
        self.assertAlmostEqual(report['dates']['2018-11-20']['policy_f1'], 0.8194444444444444)
        self.assertAlmostEqual(report['dates']['2018-11-30']['policy_f1'], 0.8228176318063959)

    def test_invalid_or_unreconciled_counts_are_rejected(self):
        self.assertTrue(callable(getattr(run_submission, 'coverage_policy_report', None)))
        root = Path(__file__).resolve().parents[1]
        for field, value in [('total', 469), ('mapped_mangrove', -1), ('not_mapped', True)]:
            summary = json.loads((root/'examples/baseline/baseline_summary.json').read_text())
            summary['held_out']['2018-11-20']['evaluation_excluded'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                run_submission.coverage_policy_report(summary)

    def test_runner_emits_report_after_verified_summary_without_rasters(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=os.environ.get('MP_FORMAT_TEST_TMP')) as temp:
            out = Path(temp)
            baseline = out/'baseline'
            baseline.mkdir()
            for name in ['baseline_summary.json','frozen_experiment_plan.json','frozen_threshold.json','split_and_coverage.json']:
                (baseline/name).write_bytes((root/'examples/baseline'/name).read_bytes())
            (baseline/'run_status.json').write_text('{"status":"succeeded"}')
            def reproduced_baseline(command, **kwargs):
                target = Path(command[-1])
                target.mkdir()
                for source in baseline.iterdir():
                    (target/source.name).write_bytes(source.read_bytes())
                return subprocess.CompletedProcess(command, 0)
            # Existing baseline files stand in for the scientific child; imports stop before raster I/O.
            with patch('run_submission.verify_manifest'), patch('importlib.metadata.version', return_value='fixture'), \
                 patch('run_submission.subprocess.run', side_effect=reproduced_baseline), \
                 patch.dict(sys.modules, {'rasterio': None}), contextlib.redirect_stdout(io.StringIO()):
                staging = out/'run'
                staging.mkdir()
                self.assertFalse(run(root, staging))
            report = json.loads((staging/'coverage_policy_summary.json').read_text())
            self.assertEqual(report['dates']['2018-11-20']['excluded_cells'], 468)
            self.assertAlmostEqual(report['dates']['2018-11-20']['policy_f1'], 0.8194444444444444)


class ComparisonTests(unittest.TestCase):
    def test_boolean_numeric_type_drift_is_rejected(self):
        for saved, new in [(False, 0), (0, False), (True, 1), (1, True)]:
            with self.subTest(saved=saved, new=new):
                with self.assertRaises(ValueError):
                    compare({'flags': [saved]}, {'flags': [new]})

    def test_matching_nested_metadata_retains_numeric_tolerance(self):
        compare({'values': [1, 0.49, None, 'Kalba', False]},
                {'values': [1.0, 0.49 + 1e-12, None, 'Kalba', False]})

    def test_changed_nested_metadata_is_rejected(self):
        for saved, new in [({'a': 1}, {'b': 1}), ([1], [1, 2]),
                           ([1], {'a': 1}), ('Kalba', 'Tarif'),
                           (0.49, 0.50), (False, True), (1, '1')]:
            with self.subTest(saved=saved, new=new):
                with self.assertRaises(ValueError):
                    compare(saved, new)

    def test_csv_numeric_tolerance_does_not_hide_changed_records(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('MP_FORMAT_TEST_TMP')) as temp:
            saved, new = Path(temp) / 'saved.csv', Path(temp) / 'new.csv'
            saved.write_text('case,score\nC001,0.49\n', encoding='utf-8')
            new.write_text('case,score\nC001,0.490000000001\n', encoding='utf-8')
            compare_csv(saved, new)
            for changed in ['case,score\nC001,0.50\n', 'case,score\nC017,0.49\n',
                            'case,score\n', 'case,value\nC001,0.49\n']:
                with self.subTest(changed=changed):
                    new.write_text(changed, encoding='utf-8')
                    with self.assertRaises(ValueError):
                        compare_csv(saved, new)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=os.environ.get('MP_FORMAT_TEST_TMP'))
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.root = self.base / 'repo'
        (self.root / 'src').mkdir(parents=True)
        self.out = self.base / 'out'
        self.out.mkdir()
        self.child = self.root / 'src/reference_baseline.py'
        self.child.write_text(
            "from pathlib import Path\nimport sys\n"
            "(Path(__file__).resolve().parents[1] / 'child_ran.txt').write_text('yes')\n"
            "sys.exit(7)\n", encoding='utf-8')
        (self.root / 'payload.txt').write_bytes(b'original')
        self.manifest = {
            name: hashlib.sha256((self.root / name).read_bytes()).hexdigest()
            for name in ['src/reference_baseline.py', 'payload.txt']
        }

    def execute(self):
        (self.root / 'SHA256SUMS.json').write_text(json.dumps(self.manifest), encoding='utf-8')
        # Dependency version lookup is unavailable in this metadata-only fixture.
        with patch('importlib.metadata.version', return_value='fixture'), contextlib.redirect_stdout(io.StringIO()):
            result = run(self.root, self.out)
        return result, json.loads((self.out / 'run_status.json').read_text())

    def assert_rejected_before_child(self):
        result, status = self.execute()
        self.assertFalse(result)
        self.assertEqual(status['status'], 'failed')
        self.assertFalse((self.root / 'child_ran.txt').exists())
        self.assertEqual(json.loads((self.out / 'checks.json').read_text()), [])

    def test_changed_payload_stops_before_child(self):
        (self.root / 'payload.txt').write_bytes(b'changed')
        self.assert_rejected_before_child()

    def test_missing_payload_stops_before_child(self):
        (self.root / 'payload.txt').unlink()
        self.assert_rejected_before_child()

    def test_parent_manifest_path_stops_before_child(self):
        outside = self.base / 'outside.txt'
        outside.write_bytes(b'outside')
        self.manifest['../outside.txt'] = hashlib.sha256(b'outside').hexdigest()
        self.assert_rejected_before_child()

    def test_absolute_manifest_path_stops_before_child(self):
        outside = self.base / 'outside.txt'
        outside.write_bytes(b'outside')
        self.manifest[outside.as_posix()] = hashlib.sha256(b'outside').hexdigest()
        self.assert_rejected_before_child()

    def test_empty_manifest_stops_before_child(self):
        self.manifest = {}
        self.assert_rejected_before_child()

    def test_invalid_hash_stops_before_child(self):
        self.manifest['payload.txt'] = 'not a SHA-256 digest'
        self.assert_rejected_before_child()

    def test_unmanifested_source_stops_before_child(self):
        (self.root / 'src/extra.py').write_bytes(b'# unexpected source\n')
        self.assert_rejected_before_child()

    def test_runtime_cache_and_log_do_not_reject_valid_payloads(self):
        cache = self.root / 'src/__pycache__'
        cache.mkdir()
        (cache / 'unused.cpython-313.pyc').write_bytes(b'not imported')
        (self.root / 'local.log').write_bytes(b'local log')
        self.execute()
        self.assertTrue((self.root / 'child_ran.txt').exists())

    def test_nonzero_child_is_recorded_as_failure(self):
        result, status = self.execute()
        self.assertFalse(result)
        self.assertEqual(status['status'], 'failed')
        self.assertTrue((self.root / 'child_ran.txt').exists())
        self.assertIn('RuntimeError', (self.out / 'failure_log.txt').read_text())
        self.assertEqual(len(json.loads((self.out / 'checks.json').read_text())), 1)

    def test_timeout_is_recorded_as_failure(self):
        # Exercising timeout handling does not require waiting the 300-second limit.
        with patch('run_submission.subprocess.run', side_effect=subprocess.TimeoutExpired(['fixture'], 300)):
            result, status = self.execute()
        self.assertFalse(result)
        self.assertEqual(status['status'], 'failed')
        self.assertIn('TimeoutExpired', (self.out / 'failure_log.txt').read_text())

    def test_unsuccessful_stage_status_is_recorded_as_failure(self):
        self.child.write_text(
            "from pathlib import Path\nimport json, sys\n"
            "out = Path(sys.argv[2]); out.mkdir()\n"
            "(out / 'run_status.json').write_text(json.dumps({'status': 'failed'}))\n",
            encoding='utf-8')
        self.manifest['src/reference_baseline.py'] = hashlib.sha256(self.child.read_bytes()).hexdigest()
        result, status = self.execute()
        self.assertFalse(result)
        self.assertEqual(status['status'], 'failed')
        self.assertIn('RuntimeError', (self.out / 'failure_log.txt').read_text())

    def test_missing_stage_status_is_recorded_as_failure(self):
        self.child.write_text('pass\n', encoding='utf-8')
        self.manifest['src/reference_baseline.py'] = hashlib.sha256(self.child.read_bytes()).hexdigest()
        result, status = self.execute()
        self.assertFalse(result)
        self.assertEqual(status['status'], 'failed')
        self.assertIn('FileNotFoundError', (self.out / 'failure_log.txt').read_text())

    def test_nonempty_output_is_preserved(self):
        keep = self.out / 'keep.txt'
        keep.write_bytes(b'preserve')
        with self.assertRaises(ValueError):
            self.execute()
        self.assertEqual(keep.read_bytes(), b'preserve')


if __name__ == '__main__':
    unittest.main()
