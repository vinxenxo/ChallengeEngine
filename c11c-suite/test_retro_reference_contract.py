from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "tests" / "reference" / "c11a1"
MANIFEST = REF / "C11A1_CHALLENGE_BULK_MANIFEST.json"
RUNS = REF / "runs"
assert MANIFEST.is_file(), MANIFEST
payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
executions = payload.get("executions")
assert isinstance(executions, list) and len(executions) == 54
for item in executions:
    run_id = str(item["run_id"])
    path = RUNS / run_id / "challenge_definition.json"
    assert path.is_file(), path
print("C11A1_REFERENCE_CONTRACT_SUITE PASS — 54/54 runs present")
