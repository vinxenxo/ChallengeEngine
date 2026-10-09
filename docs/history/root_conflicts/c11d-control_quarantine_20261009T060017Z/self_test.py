from __future__ import annotations
import py_compile
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
SUITE = ROOT / "c11c-suite"
MAIN = SUITE / "c11d-control" / "main.py"
py_compile.compile(str(MAIN), doraise=True)
text = MAIN.read_text(encoding="utf-8")
for token in (
    "D4.2 · NORMALIZE", "D5.5 · ACCEPTANCE", "D6.5 · ACCEPTANCE", "D7.5 · ACCEPTANCE",
    "D8.7 · ACCEPTANCE", "D9.4 · CHECKPOINT", "release_authority", "D10",
):
    assert token in text, token
for path in (
    "tools/c11d/d4/run_d4_4_canonical_orchestrator.ps1",
    "tools/c11d/d5/run_d5_5_full_d5_acceptance.ps1",
    "tools/c11d/d6/run_d6_5_full_d6_acceptance.ps1",
    "tools/c11d/d7/run_d7_5_full_acceptance.ps1",
    "tools/c11d/d8/run_d8_7_acceptance_freeze.ps1",
    "tools/c11d/d9/run_d9_4_acceptance_closure.ps1",
):
    assert (ROOT / path).exists(), path
assert "c11c-studio" not in text.lower()
print("C11-D Control Center 0.1.0 STATIC PASS")
