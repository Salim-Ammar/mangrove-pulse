"""Execute notebook setup against controlled package state; no pip download."""
import contextlib
import importlib.machinery
import importlib.metadata
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


class SymPySetupTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        notebook = json.loads((root/'supplementary/Mangrove_Pulse_SymPy_Resource_Audit.ipynb').read_text())
        self.setup = ''.join(next(c for c in notebook['cells'] if c['cell_type'] == 'code')['source'])

    def module(self, version):
        module = types.ModuleType('sympy')
        module.__version__ = version
        module.__spec__ = importlib.machinery.ModuleSpec('sympy', loader=None)
        return module

    def test_wrong_loaded_version_is_rejected_before_installation(self):
        for installed in ['1.13.3', '1.14.0']:
            with self.subTest(installed=installed), patch.dict(sys.modules, {'sympy': self.module('1.13.3')}), \
                 patch('importlib.metadata.version', return_value=installed), \
                 patch('subprocess.check_call', side_effect=AssertionError('Must restart before installing')), \
                 contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(RuntimeError):
                    exec(self.setup, {})

    def test_matching_version_runs_without_installation(self):
        namespace = {}
        with patch.dict(sys.modules, {'sympy': self.module('1.14.0')}), \
             patch('importlib.metadata.version', return_value='1.14.0'), \
             patch('subprocess.check_call', side_effect=AssertionError('Matching version needs no install')), \
             contextlib.redirect_stdout(io.StringIO()):
            exec(self.setup, namespace)
        self.assertEqual(namespace['sp'].__version__, '1.14.0')

    def test_missing_or_different_unloaded_package_installs_exact_version(self):
        for version in [None, '1.13.3']:
            with self.subTest(version=version), tempfile.TemporaryDirectory(dir=os.environ.get('MP_FORMAT_TEST_TMP')) as temp:
                package = Path(temp)/'sympy'
                if version:
                    package.mkdir()
                    (package/'__init__.py').write_text("__version__ = '1.13.3'\n")
                installs = []
                def install(command):
                    installs.append(command)
                    package.mkdir(exist_ok=True)
                    (package/'__init__.py').write_text("__version__ = '1.14.0'\n")
                    importlib.invalidate_caches()
                namespace = {}
                lookup = importlib.metadata.PackageNotFoundError('sympy') if version is None else None
                with patch.dict(sys.modules), patch.object(sys, 'path', [temp]+sys.path), \
                     patch('importlib.metadata.version', return_value=version, side_effect=lookup), \
                     patch('subprocess.check_call', side_effect=install), contextlib.redirect_stdout(io.StringIO()):
                    sys.modules.pop('sympy', None)
                    importlib.invalidate_caches()
                    exec(self.setup, namespace)
                self.assertEqual(installs, [[sys.executable, '-m', 'pip', 'install', 'sympy==1.14.0']])
                self.assertEqual(namespace['sp'].__version__, '1.14.0')


if __name__ == '__main__':
    unittest.main()
