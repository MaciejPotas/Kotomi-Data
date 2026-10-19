"""Run the actual Data suite with pytest, or the standard-library fallback."""
from importlib.util import find_spec
from pathlib import Path
import subprocess
import sys
from time import perf_counter


def test_command(arguments):
    if find_spec('pytest') is not None:
        return [sys.executable, '-m', 'pytest', '-q', '--durations=10', *arguments]
    verbose = any(arg in {'-v', '--verbose'} for arg in arguments)
    paths = [arg for arg in arguments if arg not in {'-v', '--verbose'}]
    if any(arg.startswith('-') for arg in paths):
        raise ValueError('Install pytest for advanced flags; unittest fallback accepts file paths and --verbose.')
    modules = [str(Path(arg).with_suffix('')).replace('\\', '.').replace('/', '.') for arg in paths]
    return [sys.executable, '-m', 'unittest', *(['-v'] if verbose else []), *modules] if modules else [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', *(['-v'] if verbose else [])]


def main(argv=None):
    start = perf_counter()
    try:
        command = test_command(sys.argv[1:] if argv is None else argv)
        result = subprocess.run(command, cwd=Path(__file__).resolve().parents[1]).returncode
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        result = 2
    print(f'Test runner: exit={result}, elapsed={perf_counter()-start:.2f}s')
    return result


if __name__ == '__main__':
    raise SystemExit(main())
