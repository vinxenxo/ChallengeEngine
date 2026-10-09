from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "c11c-suite" / "c11c-maintenance" / "main.py"
BACKEND = ROOT / "tools" / "c11d" / "d9" / "maintenance.py"
POLICY = ROOT / "definitions" / "c11d" / "d9" / "D9_11_MAINTENANCE_POLICY_V1.json"
MANIFEST = ROOT / "c11c-suite" / "c11c-maintenance" / "BUILD_MANIFEST.json"

main_text = MAIN.read_text(encoding="utf-8-sig")
backend_text = BACKEND.read_text(encoding="utf-8-sig")
policy = json.loads(POLICY.read_text(encoding="utf-8-sig"))
manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))

for token in (
    "D9.11 PLAN · DRY RUN",
    "D9.11 DOCS AUDIT · DRY RUN",
    "D9.11 FREEZE PREFLIGHT",
    "D9.11 CLEANUP PREVIEW",
    "D9.11 CONTROL QUARANTINE · DRY RUN",
    "D9.11 CONTROL QUARANTINE · APPLY",
    "D9.11 CONTROL RESTORE · DRY RUN",
    "D9.11 CONTROL RESTORE · APPLY",
    "def run_d9_maintenance",
    "tools/c11d/d9/maintenance.py",
    "QUARANTINE_C11D_CONTROL",
    "RESTORE_C11D_CONTROL",
    "CLEAN_TRANSIENTS_ONLY",
    "RESTORE_CLEANUP_ARCHIVE",
):
    assert token in main_text, f"Maintenance GUI operation/callback missing: {token}"

for token in (
    "def is_protected_path",
    "def is_allowed_quarantine_source",
    "def quarantine_legacy_control",
    "def restore_legacy_control",
    "def cleanup_allowlisted",
    "def restore_cleanup_archive",
    "def docs_audit",
    "def freeze_preflight",
    "PRESERVED_UNMODIFIED_HISTORICAL_EVIDENCE",
    "RECOVERY_REQUIRED",
    "files_deleted",
):
    assert token in backend_text, f"canonical D9.11 backend guard/operation missing: {token}"

assert policy["schema"] == "C11-D-D9.11-MAINTENANCE-POLICY-V1"
assert policy["surface"] == "c11c-maintenance" and policy["version"] == "0.2.0"
assert policy["quarantine_policy"]["only_allowed_source"] == "c11c-suite/c11d-control"
assert policy["quarantine_policy"]["allow_overwrite"] is False
assert policy["cleanup_policy"]["permanent_deletion"] is False
assert policy["historical_manifest"]["rewrite_allowed"] is False
assert policy["freeze_preparation"]["may_create_release_archive"] is False
assert manifest["version"] == "0.2.0"
assert manifest["canonical_backend"] == "tools/c11d/d9/maintenance.py"
assert manifest["release_authority"] == "NONE" and manifest["renderer_activation"] is False
assert manifest["production_execution"] is False and manifest["c11d_control_registered"] is False

# The new panel is an additive control surface inside the existing Maintenance GUI.
tree = ast.parse(main_text)
method_names = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
for name in (
    "d9_plan", "d9_docs_audit", "d9_freeze_preflight", "d9_cleanup_preview", "d9_cleanup_apply",
    "d9_quarantine_preview", "d9_quarantine_apply", "d9_restore_preview", "d9_restore_apply",
    "d9_cleanup_restore_preview", "d9_cleanup_restore_apply",
):
    assert name in method_names, f"GUI action points to missing method: {name}"


# The legacy transient-cleanup button must delegate to the reversible D9.11
# backend; it may not retain any direct file/directory deletion code.
tree = ast.parse(main_text)
clean_method = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "clean_cleanup")
clean_calls = [node for node in ast.walk(clean_method) if isinstance(node, ast.Call)]
assert any(isinstance(call.func, ast.Attribute) and call.func.attr == "d9_cleanup_apply" for call in clean_calls)
assert not any(isinstance(call.func, ast.Attribute) and call.func.attr in {"unlink", "rmdir", "remove", "rmtree"} for call in clean_calls)
assert "ARCHIVAR TRANSITORIOS · REVERSIBLE (D9.11)" in main_text

# Only five canonical apps remain registered; Maintenance is not a sixth suite.
shell = ast.parse((ROOT / "c11c-suite" / "main.py").read_text(encoding="utf-8-sig"))
apps = None
for node in ast.walk(shell):
    if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "APPS" for target in node.targets):
        apps = ast.literal_eval(node.value)
        break
assert apps is not None and len(apps) == 5
assert {row[1] for row in apps} == {
    "c11c-test/main.py", "c11c-producer/main.py", "c11c-catalog/main.py",
    "c11c-config/main.py", "c11c-maintenance/main.py",
}
print("C11C_MAINTENANCE_GUI_CONTRACT PASS | version=0.2.0 | D9.11 canonical backend | confirmations=EXPLICIT | protected roots=ENFORCED | freeze/release=READ_ONLY")
