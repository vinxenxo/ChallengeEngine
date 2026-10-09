from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CASES = (
    ("D9.9", ROOT / "tools/c11d/d9/test_universal_producer.py", "GUI/CLI parity=3/3"),
    ("D9.10", ROOT / "tools/c11d/d9/test_editorial_render_bridge.py", "CLI bridge parity=3/3"),
)


def run_checks() -> dict[str, str]:
    results = {}
    for label, script, marker in CASES:
        completed = subprocess.run(
            [sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=240,
        )
        output = (completed.stdout or "") + "\n" + (completed.stderr or "")
        if completed.returncode != 0:
            raise AssertionError(f"{label} parity suite failed (exit={completed.returncode}):\n{output[-5000:]}")
        if marker not in output:
            raise AssertionError(f"{label} parity marker missing: {marker}\n{output[-2000:]}")
        results[label] = marker
    return results


if __name__ == "__main__":
    result = run_checks()
    print("C11-D D9 GUI/CLI PARITY BUNDLE PASS | " + " | ".join(f"{k}={v}" for k, v in result.items()) + " | renderer=OFF | media_created=false")
