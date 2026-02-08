import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    print(f"$ {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic local test suite.")
    parser.add_argument(
        "--skip-syntax",
        action="store_true",
        help="Lewati pemeriksaan syntax Python.",
    )
    args = parser.parse_args()

    if not args.skip_syntax:
        syntax_targets = [
            "src",
            "experiments/06_independent_eval",
            "experiments/07_advanced_orchestration",
            "tests",
        ]
        for target in syntax_targets:
            rc = run([sys.executable, "-m", "compileall", "-q", target])
            if rc != 0:
                return rc

    return run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"])


if __name__ == "__main__":
    raise SystemExit(main())
