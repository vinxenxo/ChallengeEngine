import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Discover all test suites in the tests directory
def discover_test_suites():
    tests_dir = PROJECT_ROOT / "tests"
    suites = []
    
    # Find all .gd test files
    for root, dirs, files in os.walk(str(tests_dir)):
        for file in files:
            if file.endswith(".gd") and not file.startswith("."):
                suite_path = Path(root) / file
                # Use the file name as the suite name
                suite_name = file.replace(".gd", "").upper()
                # Use a default pass marker
                pass_marker = f"[{suite_name}_SUITE] PASS"
                suites.append((suite_name, suite_path, pass_marker))
    
    return suites

SUITES = discover_test_suites()

FATAL_PATTERNS = [
    "SCRIPT ERROR:",
    "Parse Error:",
    "Failed to load script",
    "Invalid access",
    "Invalid assignment",
    "Cannot call method",
    "CrashHandlerException",
]


def run_suite(name: str, suite_path: Path, pass_marker: str) -> bool:
    print(f"\n[RUNNER] Ejecutando {name}: {suite_path}")

    if not suite_path.exists():
        print(f"[RUNNER-FAIL] Suite inexistente: {suite_path}")
        return False

    cmd = [
        "godot",
        "--headless",
        "--path",
        str(PROJECT_ROOT),
        "--script",
        str(suite_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            timeout=60,
            cwd=str(PROJECT_ROOT),
        )
    except subprocess.TimeoutExpired:
        print(f"[RUNNER-FAIL] Timeout ejecutando {name}.")
        return False
    except OSError as exc:
        print(f"[RUNNER-FAIL] No se pudo iniciar Godot: {exc}")
        return False

    stdout = result.stdout
    stderr = result.stderr
    combined = f"{stdout}\n{stderr}"

    for pattern in FATAL_PATTERNS:
        if pattern in combined:
            print(
                f"[RUNNER-FAIL] {name}: detectado patrón fatal: {pattern}"
            )
            if stdout.strip():
                print(f"--- STDOUT ---\n{stdout.strip()}")
            if stderr.strip():
                print(f"--- STDERR ---\n{stderr.strip()}")
            return False

    if result.returncode != 0:
        print(
            f"[RUNNER-FAIL] {name}: exit code {result.returncode}"
        )
        if stderr.strip():
            print(f"--- STDERR ---\n{stderr.strip()}")
        return False

    if pass_marker not in stdout:
        print(
            f"[RUNNER-FAIL] {name}: falta marcador de éxito "
            f"'{pass_marker}'."
        )
        if stdout.strip():
            print(f"--- STDOUT ---\n{stdout.strip()}")
        return False

    print(f"[RUNNER-PASS] {name}")
    return True


def main() -> None:
    print("=== PYTHON TEST RUNNER — HARDENING 0.7.0-A ===")
    args = sys.argv[1:]
    
    if "--all" in args:
        SUITES = discover_test_suites()
    else:
        # Use default discovered suites
        pass

    results = []

    for name, suite_path, pass_marker in SUITES:
        passed = run_suite(name, suite_path, pass_marker)
        results.append((name, passed))

    failed = [name for name, passed in results if not passed]

    if failed:
        print(
            "\n[BATCH-RUNNER] FAIL — "
            f"{len(failed)} suite(s) fallaron."
        )
        for name in failed:
            print(f"  - {name}")
        sys.exit(1)

    print(
        f"\n[BATCH-RUNNER] PASS — "
        f"{len(results)} suite(s) superaron la auditoría."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()