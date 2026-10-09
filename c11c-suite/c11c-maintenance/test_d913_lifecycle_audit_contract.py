from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
main=(ROOT/"c11c-suite/c11c-maintenance/main.py").read_text(encoding="utf-8")
manifest=json.loads((ROOT/"c11c-suite/c11c-maintenance/BUILD_MANIFEST.json").read_text(encoding="utf-8"))
backend=(ROOT/"tools/c11d/d9/maintenance.py").read_text(encoding="utf-8")
assert "D9.13 LIFECYCLE AUDIT · READ ONLY" in main and "audit-lifecycle" in main
assert "def audit_cross_suite_lifecycle" in backend
assert manifest["version"]=="0.2.0" and manifest["release_authority"]=="NONE"
assert manifest["d9_13_lifecycle_audit"]=="READ_ONLY" and manifest["d9_13_side_effects"] is False
print("C11C_MAINTENANCE_D9_13_AUDIT_CONTRACT PASS | receipt audit=READ_ONLY | media=false | release_authority=NONE")
