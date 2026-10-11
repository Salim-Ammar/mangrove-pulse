"""Pure metadata tests. No satellite, raster, drone-model or field calculation."""
import copy
import csv
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from inspection_handoff import OBSERVATION_FIELDS, export, read_json, validate


class HandoffTests(unittest.TestCase):
    def setUp(self):
        folder = ROOT / 'examples/inspection'
        self.requests = read_json(folder / 'inspection_requests.json')
        self.targets = read_json(folder / 'inspection_targets.geojson')
        self.returns = read_json(folder / 'observation_return_template.json')

    def verify(self):
        return validate(ROOT, self.requests, self.targets, self.returns)

    def test_original_package(self):
        self.assertEqual(self.verify()['original_centres'], 85)

    def test_duplicate_target_rejected(self):
        self.targets['features'][1] = copy.deepcopy(self.targets['features'][0])
        with self.assertRaises(ValueError): self.verify()

    def test_coordinate_change_rejected(self):
        self.targets['features'][0]['geometry']['coordinates'][0] += 0.001
        with self.assertRaises(ValueError): self.verify()

    def test_original_label_change_rejected(self):
        self.targets['features'][0]['properties']['gmw'] = '1'
        with self.assertRaises(ValueError): self.verify()

    def test_context_change_rejected(self):
        self.targets['features'][0]['properties']['worldcover_v100_2020'] = 80
        with self.assertRaises(ValueError): self.verify()

    def test_date_change_rejected(self):
        self.requests['historical_satellite_dates'][0] = '2026-10-07'
        with self.assertRaises(ValueError): self.verify()

    def test_missing_case_membership_rejected(self):
        self.requests['cases'][0]['cell_ids'].pop()
        with self.assertRaises(ValueError): self.verify()

    def test_flight_waypoint_claim_rejected(self):
        self.targets['features'][0]['properties']['target_semantics'] = 'flight_waypoint'
        with self.assertRaises(ValueError): self.verify()

    def test_populated_measurement_rejected(self):
        self.returns['observation_record_template']['actual_observer_latitude'] = 25
        with self.assertRaises(ValueError): self.verify()

    def test_each_missing_observation_field_rejected(self):
        canonical = copy.deepcopy(self.returns['observation_record_template'])
        for field in canonical:
            with self.subTest(field=field):
                self.returns['observation_record_template'] = canonical.copy()
                del self.returns['observation_record_template'][field]
                with self.assertRaises(ValueError): self.verify()

    def test_unexpected_observation_field_rejected(self):
        self.returns['observation_record_template']['unsupported_measurement'] = None
        with self.assertRaises(ValueError): self.verify()

    def test_missing_or_unsupported_schema_rejected(self):
        for version in (None, '1.1', 1.0):
            with self.subTest(version=version):
                self.returns['schema_version'] = version
                with self.assertRaises(ValueError): self.verify()

    def test_fabricated_conclusion_rejected(self):
        self.returns['cases'][0]['conclusion'] = 'plant_here'
        with self.assertRaises(ValueError): self.verify()

    def test_export_empty_csv_and_source_identity(self):
        with tempfile.TemporaryDirectory(prefix='mp_format_test_', dir=os.environ.get('MP_FORMAT_TEST_TMP')) as temp:
            out = Path(temp) / 'handoff'
            self.assertEqual(export(ROOT, out)['field_observations_collected'], 0)
            with (out / 'observations_UNFILLED.csv').open(newline='', encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 85)
            self.assertEqual(set(rows[0]), set(OBSERVATION_FIELDS) | {'target_longitude', 'target_latitude', 'observation_status'})
            self.assertTrue(all(r['observation_status'] == 'not_collected' and r['acquisition_datetime_with_timezone'] == '' and r['actual_observer_latitude'] == '' for r in rows))
            self.assertEqual((out / 'inspection_targets.geojson').read_bytes(), (ROOT / 'examples/inspection/inspection_targets.geojson').read_bytes())

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='mp_format_test_', dir=os.environ.get('MP_FORMAT_TEST_TMP')) as temp:
            out = Path(temp)
            (out / 'keep.txt').write_text('preserve', encoding='utf-8')
            with self.assertRaises(ValueError): export(ROOT, out)
            self.assertEqual((out / 'keep.txt').read_text(), 'preserve')

    def test_source_hash_mismatch_rejected(self):
        key = next(iter(self.requests['sources']))
        self.requests['sources'][key] = '0' * 64
        with self.assertRaises(ValueError): self.verify()

    def test_source_path_escape_rejected(self):
        self.requests['sources'] = {'../../../../PROJECT_MEMORY.md': '0' * 64, 'bad': '0' * 64}
        with self.assertRaises(ValueError): self.verify()


if __name__ == '__main__':
    unittest.main()
