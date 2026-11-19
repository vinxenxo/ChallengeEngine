"""Strict A.3 lineage adjudication using the original diagnostic producer's exact field semantics.

The original diagnostic emits legacy-named fields from different identity domains:
old_pointer_expected = whole historical-manifest SHA; old_pointer_actual = old
D9.8 pointer value. The new expected/actual fields are model-file SHA and new
pointer value. They are NOT expected/actual pairs that should be equal.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

BRIDGE_REL = "docs/current/e/C11E_E4C_A3_REVIEW_MANIFEST_LINEAGE_RECONCILIATION_20261110_V2.json"
HIST_REL = "docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json"
CURR_REL = "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"
MODEL_REL = "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"
PROPOSAL_REL = "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
DECISION_REL = "docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json"
BRIDGE_SHA = "aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac"
HIST_SHA = "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470"
CURR_SHA = "5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795"
MODEL_SHA = "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb"
PROPOSAL_SHA = "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"
DECISION_SHA = "49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04"
DIAGNOSTIC_GENERATOR_SHA = "90375a6c21550d67e6aa1f374d5e5c8dcd7c06b630c51b34ad83313fbb7b2fc2"
DIAGNOSTIC_GENERATOR_REL = "reference/diagnose_c11e_e6_loop_policy_v2_receipt.py"
FROZEN_C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_C11C_BYTES = 796318
POINTER = "/source_lineage/6/sha256"
SPECIAL_STATUS = "PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION"

class A3AdjudicationError(ValueError):
    pass

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_json(root: Path, rel: str) -> dict[str, Any]:
    p = root.joinpath(*rel.split("/"))
    try:
        value = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise A3AdjudicationError(f"A3_JSON_INVALID:{rel}:{type(exc).__name__}") from exc
    if not isinstance(value, dict):
        raise A3AdjudicationError(f"A3_JSON_NOT_OBJECT:{rel}")
    return value

def verify_generator_provenance() -> str:
    source = Path(__file__).resolve().parent / DIAGNOSTIC_GENERATOR_REL
    if not source.is_file():
        raise A3AdjudicationError("A3_DIAGNOSTIC_GENERATOR_REFERENCE_MISSING")
    actual = sha256_file(source)
    if actual != DIAGNOSTIC_GENERATOR_SHA:
        raise A3AdjudicationError("A3_DIAGNOSTIC_GENERATOR_REFERENCE_PIN_MISMATCH:" + actual)
    return actual

def verify_single_pointer_postimage(historical: Mapping[str, Any], current: Mapping[str, Any], old_value: str, new_value: str) -> None:
    if not isinstance(historical, Mapping) or not isinstance(current, Mapping):
        raise A3AdjudicationError("A3_MANIFESTS_MUST_BE_OBJECTS")
    hist_lineage = historical.get("source_lineage")
    curr_lineage = current.get("source_lineage")
    if not isinstance(hist_lineage, list) or len(hist_lineage) <= 6:
        raise A3AdjudicationError("A3_HISTORICAL_SOURCE_LINEAGE_INDEX_6_MISSING")
    if not isinstance(curr_lineage, list) or len(curr_lineage) <= 6:
        raise A3AdjudicationError("A3_CURRENT_SOURCE_LINEAGE_INDEX_6_MISSING")
    old_entry, new_entry = hist_lineage[6], curr_lineage[6]
    if not isinstance(old_entry, dict) or not isinstance(new_entry, dict):
        raise A3AdjudicationError("A3_SOURCE_LINEAGE_INDEX_6_NOT_OBJECT")
    if old_entry.get("sha256") != old_value:
        raise A3AdjudicationError("A3_HISTORICAL_POINTER_VALUE_MISMATCH")
    if new_entry.get("sha256") != new_value:
        raise A3AdjudicationError("A3_CURRENT_POINTER_VALUE_MISMATCH")
    expected = copy.deepcopy(dict(historical))
    expected["source_lineage"][6]["sha256"] = new_value
    if dict(current) != expected:
        raise A3AdjudicationError("A3_POSTIMAGE_DIFFERS_BEYOND_SINGLE_POINTER")

def adjudicate_loop_a3(project_root: Path, loop_receipt: dict[str, Any], diagnostic: dict[str, Any]) -> dict[str, Any]:
    generator_pin = verify_generator_provenance()
    checks = loop_receipt.get("checks")
    if not isinstance(checks, list) or len(checks) != 18:
        raise A3AdjudicationError("LOOP_V2_CHECK_LIST_NOT_18")
    statuses = [c.get("status") for c in checks if isinstance(c, dict)]
    literal_pass = statuses.count("PASS")
    special_count = statuses.count(SPECIAL_STATUS)
    unknown = [s for s in statuses if s not in ("PASS", SPECIAL_STATUS)]
    if len(statuses) != 18 or literal_pass != 17 or special_count != 1 or unknown:
        raise A3AdjudicationError("LOOP_V2_STATUS_CLASSIFICATION_MISMATCH")
    if loop_receipt.get("check_count") != 18 or loop_receipt.get("passed_checks") != 17 or loop_receipt.get("failed_checks") != 0:
        raise A3AdjudicationError("LOOP_V2_COUNT_CONTRACT_MISMATCH")
    if loop_receipt.get("status") != "PASS_LOOP_POLICY_DECISIONS_RECONCILED_NOT_COMPOSITOR_ACCEPTANCE":
        raise A3AdjudicationError("LOOP_V2_TOP_LEVEL_STATUS_MISMATCH")
    a3_check = next((c for c in checks if isinstance(c, dict) and c.get("id") == "a3_lineage_single_pointer_reconciliation"), None)
    if not a3_check or a3_check.get("status") != SPECIAL_STATUS:
        raise A3AdjudicationError("LOOP_V2_A3_SPECIAL_STATUS_MISSING")

    active = diagnostic.get("active_a3_lineage", {})
    if not isinstance(active, dict) or active.get("status") != "PASS":
        raise A3AdjudicationError("A3_ACTIVE_LINEAGE_NOT_PASS")
    if active.get("actual_manifest_differences") != [POINTER]:
        raise A3AdjudicationError("A3_SINGLE_POINTER_DIFF_MISMATCH")
    transition = active.get("transition", {})
    if not isinstance(transition, dict) or transition.get("operation") != "PINNED_REPLACE":
        raise A3AdjudicationError("A3_TRANSITION_OPERATION_MISMATCH")
    if transition.get("only_changed_json_pointer") != POINTER:
        raise A3AdjudicationError("A3_TRANSITION_POINTER_MISMATCH")
    if transition.get("historical_bytes_preserved_as_add_only_archive") is not True:
        raise A3AdjudicationError("A3_HISTORY_ARCHIVE_NOT_PRESERVED")

    expected_identities = {
        BRIDGE_REL: BRIDGE_SHA,
        HIST_REL: HIST_SHA,
        CURR_REL: CURR_SHA,
        MODEL_REL: MODEL_SHA,
        PROPOSAL_REL: PROPOSAL_SHA,
        DECISION_REL: DECISION_SHA,
    }
    identity_rows = active.get("identities", [])
    if not isinstance(identity_rows, list) or len(identity_rows) != len(expected_identities):
        raise A3AdjudicationError("A3_IDENTITY_ROW_COUNT_MISMATCH")
    identity_map: dict[str, str] = {}
    for row in identity_rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str) or not isinstance(row.get("sha256"), str):
            raise A3AdjudicationError("A3_IDENTITY_ROW_INVALID")
        if row["path"] in identity_map:
            raise A3AdjudicationError("A3_IDENTITY_DUPLICATE_PATH:" + row["path"])
        identity_map[row["path"]] = row["sha256"]
    for rel, expected_sha in expected_identities.items():
        if identity_map.get(rel) != expected_sha:
            raise A3AdjudicationError("A3_IDENTITY_PIN_MISMATCH:" + rel)
        p = project_root.joinpath(*rel.split("/"))
        if not p.is_file() or sha256_file(p) != expected_sha:
            raise A3AdjudicationError("A3_LIVE_IDENTITY_FILE_PIN_MISMATCH:" + rel)

    bridge = read_json(project_root, BRIDGE_REL)
    if bridge.get("schema") != "C11E-E4C-A3-REVIEW-MANIFEST-LINEAGE-RECONCILIATION-V2":
        raise A3AdjudicationError("A3_BRIDGE_SCHEMA_MISMATCH")
    if bridge.get("status") != "ATTESTED_SINGLE_SOURCE_LINEAGE_POINTER_REFRESH_NO_POLICY_CHANGE":
        raise A3AdjudicationError("A3_BRIDGE_STATUS_MISMATCH")
    frozen = bridge.get("frozen_c11c", {})
    if frozen.get("sha256") != FROZEN_C11C_SHA or frozen.get("bytes") != FROZEN_C11C_BYTES:
        raise A3AdjudicationError("A3_BRIDGE_FROZEN_C11C_PIN_MISMATCH")

    policy = bridge.get("approved_policy", {})
    policy_a3 = policy.get("a3", {}) if isinstance(policy, dict) else {}
    if policy_a3.get("path") != PROPOSAL_REL or policy_a3.get("sha256") != PROPOSAL_SHA or policy_a3.get("decision") != "APPROVE_AS_PROPOSED":
        raise A3AdjudicationError("A3_APPROVED_PROPOSAL_BINDING_MISMATCH")
    policy_ref = policy.get("a3_decision_record", {}) if isinstance(policy, dict) else {}
    if policy_ref.get("path") != DECISION_REL or policy_ref.get("sha256") != DECISION_SHA:
        raise A3AdjudicationError("A3_OPERATOR_POLICY_PIN_MISMATCH")
    decision_record = read_json(project_root, DECISION_REL)
    decisions = {r.get("decision_id"): r for r in decision_record.get("decisions", []) if isinstance(r, dict)}
    accepted = decisions.get("A.3_LOOP_DRILL_EDITORIAL_WINDOWS")
    if not isinstance(accepted, dict) or accepted.get("decision") != "APPROVE_AS_PROPOSED":
        raise A3AdjudicationError("A3_OPERATOR_APPROVAL_MISSING")
    if accepted.get("proposal_sha256") != PROPOSAL_SHA:
        raise A3AdjudicationError("A3_OPERATOR_APPROVAL_PROPOSAL_PIN_MISMATCH")

    lineage = bridge.get("review_manifest_lineage", {})
    if lineage.get("path") != CURR_REL or lineage.get("historical_archive_path") != HIST_REL:
        raise A3AdjudicationError("A3_BRIDGE_MANIFEST_PATH_MISMATCH")
    if lineage.get("historical_sha256") != HIST_SHA or lineage.get("current_sha256") != CURR_SHA:
        raise A3AdjudicationError("A3_BRIDGE_WHOLE_MANIFEST_HASH_MISMATCH")
    if lineage.get("historical_bytes") != 8591 or lineage.get("current_bytes") != 8591:
        raise A3AdjudicationError("A3_BRIDGE_MANIFEST_BYTE_COUNT_MISMATCH")
    if lineage.get("allowed_json_pointer_difference") != [POINTER]:
        raise A3AdjudicationError("A3_BRIDGE_ALLOWED_POINTER_MISMATCH")
    installed_transition = lineage.get("installed_transition", {})
    if installed_transition.get("only_changed_json_pointer") != POINTER:
        raise A3AdjudicationError("A3_BRIDGE_INSTALLED_POINTER_MISMATCH")
    if lineage.get("pointer_target_path") != MODEL_REL:
        raise A3AdjudicationError("A3_BRIDGE_POINTER_TARGET_MISMATCH")
    old_value, new_value = lineage.get("old_pointer_value"), lineage.get("new_pointer_value")
    if not isinstance(old_value, str) or not isinstance(new_value, str):
        raise A3AdjudicationError("A3_BRIDGE_POINTER_VALUES_MISSING")
    if new_value != MODEL_SHA:
        raise A3AdjudicationError("A3_D98_TARGET_POINTER_VALUE_MISMATCH")

    hist_path = project_root.joinpath(*HIST_REL.split("/"))
    curr_path = project_root.joinpath(*CURR_REL.split("/"))
    model_path = project_root.joinpath(*MODEL_REL.split("/"))
    if hist_path.stat().st_size != 8591 or sha256_file(hist_path) != HIST_SHA:
        raise A3AdjudicationError("A3_PREIMAGE_MANIFEST_FILE_PIN_MISMATCH")
    if curr_path.stat().st_size != 8591 or sha256_file(curr_path) != CURR_SHA:
        raise A3AdjudicationError("A3_POSTIMAGE_MANIFEST_FILE_PIN_MISMATCH")
    if transition.get("preimage_sha256") != HIST_SHA:
        raise A3AdjudicationError("A3_PREIMAGE_MANIFEST_SHA256_MISMATCH")
    if transition.get("postimage_sha256") != CURR_SHA:
        raise A3AdjudicationError("A3_POSTIMAGE_MANIFEST_SHA256_MISMATCH")
    if transition.get("preimage_bytes") != 8591 or transition.get("postimage_bytes") != 8591:
        raise A3AdjudicationError("A3_TRANSITION_MANIFEST_BYTE_COUNT_MISMATCH")
    historical, current = read_json(project_root, HIST_REL), read_json(project_root, CURR_REL)
    verify_single_pointer_postimage(historical, current, old_value, new_value)

    # Exact, source-derived diagnostic field mapping. These fields have distinct roles;
    # in particular old_pointer_expected != old_pointer_actual by design.
    diagnostic_field_contract = {
        "old_pointer_expected": HIST_SHA,       # whole historical manifest digest
        "old_pointer_actual": old_value,        # old D9.8 pointer contents
        "bridge_old_pointer_value": old_value,  # bridge's recorded pointer contents
        "new_pointer_expected": MODEL_SHA,      # D9.8 model file digest
        "new_pointer_actual": new_value,        # current manifest pointer contents
        "bridge_new_pointer_value": new_value,  # bridge's recorded pointer contents
        "pointer_target_path": MODEL_REL,
    }
    for key, expected_value in diagnostic_field_contract.items():
        if active.get(key) != expected_value:
            raise A3AdjudicationError("A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:" + key)
    if sha256_file(model_path) != new_value:
        raise A3AdjudicationError("A3_POINTER_TARGET_FILE_MISMATCH")
    d98 = bridge.get("d98_context", {})
    if d98.get("current_model_path") != MODEL_REL or d98.get("current_model_sha256") != MODEL_SHA:
        raise A3AdjudicationError("A3_D98_CONTEXT_PIN_MISMATCH")
    if d98.get("d4_executable_compatibility") is not False or d98.get("renderer_admission") is not False:
        raise A3AdjudicationError("A3_D98_CONTEXT_EXECUTION_LOCK_MISMATCH")

    expected_issues = [
        "UNCLASSIFIED_CHECK_STATUS:PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION",
        "RECEIPT_TOP_LEVEL_STATUS_CONTRADICTS_CHECKS",
        "A3_CHECK_NOT_PASS:PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION",
    ]
    if diagnostic.get("issues") != expected_issues:
        raise A3AdjudicationError("A3_DIAGNOSTIC_ISSUE_SET_UNEXPECTED")
    if diagnostic.get("source_receipt_sha256") != "5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be":
        raise A3AdjudicationError("A3_DIAGNOSTIC_SOURCE_RECEIPT_PIN_MISMATCH")

    return {
        "status": "PASS_SPECIALIZED_A3_PASS_CLASSIFIED",
        "literal_pass_checks": literal_pass,
        "specialized_pass_checks": special_count,
        "normalized_pass_checks": literal_pass + special_count,
        "failed_checks": 0,
        "check_count": 18,
        "a3_lineage": "PASS",
        "manifest_preimage_sha256": HIST_SHA,
        "manifest_postimage_sha256": CURR_SHA,
        "changed_json_pointer": POINTER,
        "old_pointer_value_sha256": old_value,
        "new_pointer_value_sha256": new_value,
        "structural_reconstruction": "PASS_EXACTLY_ONE_POINTER_CHANGED",
        "recognized_specialized_status": SPECIAL_STATUS,
        "diagnostic_generator_sha256": generator_pin,
        "legacy_diagnostic_field_contract": {
            "old_pointer_expected": "WHOLE_HISTORICAL_MANIFEST_SHA256",
            "old_pointer_actual": "HISTORICAL_JSON_POINTER_VALUE_SHA256",
            "new_pointer_expected": "D98_MODEL_FILE_SHA256",
            "new_pointer_actual": "CURRENT_JSON_POINTER_VALUE_SHA256",
        },
    }
