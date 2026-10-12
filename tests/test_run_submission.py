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
