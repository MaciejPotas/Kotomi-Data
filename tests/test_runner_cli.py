"""Runner contract v1; subprocess execution is replaced with bounded stubs."""
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase, mock
import importlib.util
spec = importlib.util.spec_from_file_location('data_test_runner', Path(__file__).resolve().parents[1]/'tools/run_tests.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class RunnerTests(TestCase):
    def test_pytest_forwards_arguments(self):
        with mock.patch.object(runner, 'find_spec', return_value=object()):
            command = runner.test_command(['tests/test_fixture.py', '--verbose'])
        self.assertEqual(command[-2:], ['tests/test_fixture.py', '--verbose'])
        self.assertIn('pytest', command)

    def test_unittest_group_and_verbosity(self):
        with mock.patch.object(runner, 'find_spec', return_value=None):
            command = runner.test_command(['tests/test_fixture.py', '--verbose'])
            self.assertEqual(command[-2:], ['-v', 'tests.test_fixture'])
            self.assertIn('discover', runner.test_command([]))
            with self.assertRaises(ValueError):
                runner.test_command(['--maxfail=1'])

    def test_exit_status_is_preserved(self):
        with mock.patch.object(runner.subprocess, 'run', return_value=SimpleNamespace(returncode=5)):
            self.assertEqual(runner.main([]), 5)
