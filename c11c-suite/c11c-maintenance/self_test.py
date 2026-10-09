from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
checks = [
    (ROOT / "c11c-suite" / "c11c-maintenance" / "test_cleanup_contract.py", "C11C_CLEANUP_FREEZE_TOOLING_CONTRACT PASS"),
    (ROOT / "c11c-suite" / "c11c-maintenance" / "test_root_organization_contract.py", "C11C_ROOT_ORGANIZATION_CONTRACT PASS"),
    (ROOT / "tools" / "c11d" / "d9" / "test_maintenance.py", "C11-D D9.11 MAINTENANCE PASS"),
    (ROOT / "c11c-suite" / "c11c-maintenance" / "test_d9_maintenance_contract.py", "C11C_MAINTENANCE_GUI_CONTRACT PASS"),
]
for script, token in checks:
    result = subprocess.run([sys.executable, str(script)], cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    if result.returncode != 0 or token not in result.stdout:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"Maintenance self-test failed: {script.relative_to(ROOT).as_posix()}")
print("C11-C Maintenance 0.2.0 + C11-D D9.11 self-test PASS | dry-run-first | reversible allowlists | quarantine/restore | manifest-preserved | release_authority=NONE")
