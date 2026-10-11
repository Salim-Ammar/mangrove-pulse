"""Controlled ZIP-reader fixtures; no raster execution or large payloads."""
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import reference_baseline


class RequiredArchiveTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=os.environ.get('MP_FORMAT_TEST_TMP'))
        self.addCleanup(temp.cleanup)
        self.destination = Path(temp.name) / 'extracted'
        self.destination.mkdir()

    def archive(self, entries):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            for name, data in entries:
                archive.writestr(name, data)
        buffer.seek(0)
        archive = zipfile.ZipFile(buffer)
        self.addCleanup(archive.close)
        return archive

    def test_required_members_are_read_without_extracting_unrelated_paths(self):
        archive = self.archive([('nested/input.txt', b'input'), ('../outside.txt', b'unused')])
        reference_baseline.extract_required_members(archive, self.destination, ['nested/input.txt'])
        self.assertEqual((self.destination / 'nested/input.txt').read_bytes(), b'input')
        self.assertEqual([p.name for p in self.destination.iterdir()], ['nested'])

    def test_missing_required_member_rejected_before_any_write(self):
        archive = self.archive([('present.txt', b'input')])
        with self.assertRaises(ValueError):
            reference_baseline.extract_required_members(archive, self.destination, ['present.txt', 'missing.txt'])
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_duplicate_required_member_rejected(self):
        with self.assertWarns(UserWarning):
            archive = self.archive([('input.txt', b'one'), ('input.txt', b'two')])
        with self.assertRaises(ValueError):
            reference_baseline.extract_required_members(archive, self.destination, ['input.txt'])
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_unsafe_required_path_rejected(self):
        archive = self.archive([('../outside.txt', b'outside')])
        with self.assertRaises(ValueError):
            reference_baseline.extract_required_members(archive, self.destination, ['../outside.txt'])
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_member_limit_rejected_before_reading_payload(self):
        archive = self.archive([('input.txt', b'small')])
        archive.getinfo('input.txt').file_size = 50_000_001
        with patch.object(archive, 'read', side_effect=AssertionError('payload must not be read')):
            with self.assertRaises(ValueError):
                reference_baseline.extract_required_members(archive, self.destination, ['input.txt'])
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_cumulative_limit_rejected_before_reading_payload(self):
        names = ['one.txt', 'two.txt', 'three.txt']
        archive = self.archive([(name, b'small') for name in names])
        for info in archive.infolist():
            info.file_size = 40_000_000
        with patch.object(archive, 'read', side_effect=AssertionError('payload must not be read')):
            with self.assertRaises(ValueError):
                reference_baseline.extract_required_members(archive, self.destination, names)
        self.assertEqual(list(self.destination.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
