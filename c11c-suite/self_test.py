from __future__ import annotations

import ast
import py_compile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "c11c-suite"
CURRENT = "2.19.12"

REQUIRED_FILES = [
    "main.py",
    "common.py",
    "c11c-test/main.py",
    "c11c-test/run.bat",
    "c11c-test/run_all.bat",
    "c11c-test/run_suite.bat",
    "c11c-test/run_c11c_acceptance.bat",
    "c11c-test/run_c11c_complete_review.bat",
    "c11c-test/run_c11c_focused_validation.bat",
    "c11c-test/run_c11c_one_video_each_type.bat",
    "c11c-test/run_c11c_family_coverage_smoke.bat",
    "c11c-test/run_c11c_challenge_smoke.bat",
    "c11c-test/run_c11c_challenge_smoke.ps1",
    "c11c-test/run_c11c_challenge_family_smoke.bat",
    "c11c-test/run_c11c_challenge_family_smoke.ps1",
    "c11c-producer/main.py",
    "c11c-producer/self_test.py",
    "c11c-producer/test_producer_gui_contract.py",
    "c11c-producer/test_gui_contract.bat",
    "c11c-producer/run.bat",
    "c11c-maintenance/main.py",
    "c11c-maintenance/run.bat",
    "c11c-maintenace/run.bat",
    "c11c-catalog/main.py",
    "c11c-catalog/run.bat",
    "c11c-config/main.py",
    "c11c-config/run.bat",
    "run.bat",
    "self_test.py",
    "test_retro_reference_contract.py",
]

for rel in REQUIRED_FILES:
    p = SUITE / rel
    assert p.exists(), f"Missing Suite file: {p}"

for p in sorted(SUITE.rglob("*.py")):
    if p.name == "self_test.py" or "__pycache__" not in p.parts:
        py_compile.compile(str(p), doraise=True)

run_all = (ROOT / "tests" / "run_all.py").read_text(encoding="utf-8-sig")
for marker in (
    "C11CProductionReviewCopySafetyTest.gd",
    "C11A1FactoryIsolationContractTest.gd",
    "C11CVisualLoopLongformSourceArtifactContractTest.gd",
    "C11CParallelReviewWorkerIsolationContractTest.gd",
    "C11CVisualDrillReviewEnvelopePathContractTest.gd",
):
    assert marker in run_all, f"run_all.py missing required contract marker: {marker}"

ui = (SUITE / "c11c-test" / "main.py").read_text(encoding="utf-8")
for command in (
    "C11-C 2.19 CONSOLIDATED ACCEPTANCE",
    "C11-C ACCEPTANCE LAUNCHER",
    "C11-C FOCUSED VALIDATION",
    "C11-C ONE VIDEO EACH TYPE",
    "C11-C FAMILY COVERAGE SMOKE",
    "C11-C CHALLENGE SMOKE",
    "C11-C CHALLENGE FAMILY FAST SMOKE",
    "C11-C COMPLETE VIDEO REVIEW",
    "C11-C SUITE LAUNCHER AUDIT",
    "C11-C PARALLEL WORKER CONTRACT",
    "C11-C VISUAL DRILL ENVELOPE PATH CONTRACT",
    "C11-C DOCS CONSOLIDATION",
    "SEED STRESS 32x2",
):
    assert command in ui, f"Test UI missing command: {command}"
assert "FULL_ACCEPTANCE_C11C_2.19.12.ps1" in ui
assert "run_c11c_family_coverage_smoke.ps1" in ui
assert "run_c11c_challenge_smoke.ps1" in ui
assert "run_c11c_challenge_family_smoke.ps1" in ui
assert "'-Workers', '7', '-All'" in ui
assert "C11-C 2.19.11" not in ui
assert "C11-C 2.19.10" not in ui
assert "C11-C 2.19.4" not in ui

# Every registered UI command must target an existing root file or the canonical direct Godot command.
module = ast.parse(ui)
commands = None
for node in module.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "C11_COMMANDS" for t in node.targets):
        commands = ast.literal_eval(node.value)
        break
assert commands is not None
for name, kind, args, _description in commands:
    if kind in {"ps", "python", "bat"} and args:
        first = str(args[0]).replace("\\", "/")
        if first.startswith("tools/") or first.startswith("c11c-suite/") or first.startswith("FULL_ACCEPTANCE"):
            target = ROOT.joinpath(*first.split("/"))
            assert target.exists(), f"UI command '{name}' targets missing file: {target}"

# Canonical launcher invariants.
launcher_root = SUITE / "c11c-maintenace" / "run.bat"
alias = launcher_root.read_text(encoding="utf-8-sig").lower()
assert "call" in alias and "c11c-maintenance\\run.bat" in alias
for p in sorted((SUITE / "c11c-test").glob("*.bat")) + [SUITE / "run.bat", SUITE / "c11c-producer" / "run.bat", SUITE / "c11c-maintenance" / "run.bat", SUITE / "c11c-catalog" / "run.bat", SUITE / "c11c-config" / "run.bat"]:
    t = p.read_text(encoding="utf-8-sig")
    assert "C11C_PROJECT_ROOT" in t, f"Launcher missing C11C_PROJECT_ROOT: {p}"
    assert "cd /d" in t, f"Launcher missing cd /d root normalization: {p}"

focused = (ROOT / "tools" / "qa" / "c11" / "run_c11c_focused_validation.ps1").read_text(encoding="utf-8-sig")
assert "Join-Path $PSScriptRoot '..\\..\\..'" in focused
smoke = (ROOT / "tools" / "qa" / "c11" / "run_c11c_one_video_each_type.ps1").read_text(encoding="utf-8-sig")
assert "COMPLETE PASS - 3 independent" in smoke
family_smoke = (ROOT / "tools" / "qa" / "c11" / "run_c11c_family_coverage_smoke.ps1")
assert family_smoke.exists()
family_smoke_text = family_smoke.read_text(encoding="utf-8-sig")
for token in ("5 Visual Loops", "4 Visual Drills", "9 Challenges", "5 Longforms", "23", "producer_schema.json", "c11c_visual_loop_longform_schedule.json"):
    assert token in family_smoke_text, f"Family coverage smoke missing contract token: {token}"

# Active PowerShell execution paths must be UTF-8 BOM encoded for Windows PowerShell 5.1 safety.
active_ps1 = [
    ROOT / "tools/qa/c11/verify_c11c_suite_launchers.ps1",
    ROOT / "tools/qa/c11/run_c11c_focused_validation.ps1",
    ROOT / "tools/qa/c11/run_c11c_one_video_each_type.ps1",
    ROOT / "tools/qa/c11/run_c11c_family_coverage_smoke.ps1",
    ROOT / "tools/qa/c11/run_c11c_complete_video_review.ps1",
    ROOT / "tools/qa/c11/run_c11c_challenge_bulk_qa.ps1",
    ROOT / "tools/prototypes/c11c_bulk/C11CProductionBatchCommon.ps1",
    ROOT / "tools/prototypes/c11c_bulk/run_c11c_production.ps1",
    ROOT / "tools/prototypes/c11c_bulk/run_c11c_visual_drill_review.ps1",
    ROOT / "tools/prototypes/c11c_bulk/run_c11c_visual_loop_longform_production.ps1",
    ROOT / "tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1",
    ROOT / "tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1",
    ROOT / "c11c-suite/c11c-producer/run_visual_drill_production.ps1",
    SUITE / "c11c-test/run_c11c_challenge_family_smoke.ps1",
]
for p in active_ps1:
    data = p.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), f"Active PowerShell script is not UTF-8 BOM: {p}"

# Current C11-C revision drift is forbidden inside the active operational Suite and report scripts.
stale_re = re.compile(r"(?:revision\s*=\s*[\"]|\"revision\"\s*:\s*[\"])2\.19\.(?:[0-9]|10|11)(?!\d)", re.IGNORECASE)
scan_roots = [SUITE, ROOT / "tools/qa/c11", ROOT / "tools/prototypes/c11c_bulk"]
ignored_names = {"run_c11c_art_direction_review_v3.ps1"}  # historical 2.16 compatibility runner
stale_hits = []
for base in scan_roots:
    for p in sorted(base.rglob("*")):
        if not p.is_file() or p.name in ignored_names or p.name == "self_test.py" or p.suffix.lower() not in {".py", ".ps1", ".bat", ".cmd", ".json", ".md"}:
            continue
        text = p.read_text(encoding="utf-8-sig", errors="ignore")
        for m in stale_re.finditer(text):
            stale_hits.append(f"{p.relative_to(ROOT)}:{m.group(0)}")
assert not stale_hits, "Stale active 2.19 revision references remain: " + "; ".join(stale_hits[:20])

# Worker isolation contract remains private-root + no mutex.
worker_batch = (ROOT / "tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1").read_text(encoding="utf-8-sig")
worker_helper = (ROOT / "tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1").read_text(encoding="utf-8-sig")
assert "New-C11CReviewWorkerPool" in worker_batch
assert "WorkerRoot" in worker_batch and "WorkerRoot" in worker_helper
assert "Mutex" not in worker_batch and "Mutex" not in worker_helper
assert "$Workers" in worker_batch
assert "Tee-Object -FilePath $bootstrapLog | Out-Null" in worker_helper
assert "$null = Initialize-C11CReviewWorkerProject" in worker_helper
assert "Initialize-C11CReviewWorkerProject" in worker_helper
for marker in ("global_script_class_cache.cfg", "PresentationProfile", "--headless", "--editor", "--quit"):
    assert marker in worker_helper, f"Worker class-cache bootstrap marker missing: {marker}"
assert "c11c-studio" not in worker_helper.lower()

operational_code = "".join(
    p.read_text(encoding="utf-8-sig", errors="ignore")
    for p in sorted(SUITE.rglob("*"))
    if p.is_file()
    and p.name not in {"self_test.py", "test_powershell_parse.py"}
    and p.suffix.lower() in {".py", ".ps1", ".bat", ".cmd"}
)
assert "c11c-studio" not in operational_code.lower()

# Current acceptance and documentation anchors.
assert (ROOT / "FULL_ACCEPTANCE_C11C_2.19.12.ps1").exists()
assert (ROOT / "docs/master-prompts/MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md").exists()
assert (ROOT / "docs/master-prompts/START_PROMPT_C11C_2.19_CONSOLIDATED.md").exists()
assert (ROOT / "docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md").exists()
assert "Revision: 2.19.12" in (ROOT / "docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md").read_text(encoding="utf-8-sig")

print("C11-C Suite 0.1.4 + Producer 0.9.7 + C11-C 2.19.12 hardened contracts STATIC PASS")
