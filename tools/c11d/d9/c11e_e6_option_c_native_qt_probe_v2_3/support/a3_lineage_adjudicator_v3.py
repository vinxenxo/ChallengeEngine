"""Strict A.3 single-pointer lineage adjudication for the V2.2 native Qt probe.

Legacy *_pointer_expected/actual field names do not reliably identify the SHA scope.
This module constrains each expected/actual pair to exactly one of two pinned values
for that side (whole manifest or JSON pointer), requires the pair to agree, validates
explicit bridge pointer fields, and reconstructs the exact postimage.
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
BRIDGE_SHA = "aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac"
HIST_SHA = "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470"
CURR_SHA = "5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795"
MODEL_SHA = "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb"
POLICY_SHA = "49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04"
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

def verify_single_pointer_postimage(historical: Mapping[str, Any], current: Mapping[str, Any], old_value: str, new_value: str) -> None:
    """Prove current == historical except source_lineage[6].sha256.

    This is structural proof. It must not compare a whole-document digest with a
    pointer's digest; they are separate scopes and are verified independently.
    """
    if not isinstance(historical, Mapping) or not isinstance(current, Mapping):
        raise A3AdjudicationError("A3_MANIFESTS_MUST_BE_OBJECTS")
    hist_lineage = historical.get("source_lineage")
    curr_lineage = current.get("source_lineage")
    if not isinstance(hist_lineage, list) or len(hist_lineage) <= 6:
        raise A3AdjudicationError("A3_HISTORICAL_SOURCE_LINEAGE_INDEX_6_MISSING")
    if not isinstance(curr_lineage, list) or len(curr_lineage) <= 6:
        raise A3AdjudicationError("A3_CURRENT_SOURCE_LINEAGE_INDEX_6_MISSING")
    old_entry = hist_lineage[6]
    new_entry = curr_lineage[6]
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

    bridge_path = project_root.joinpath(*BRIDGE_REL.split("/"))
    hist_path = project_root.joinpath(*HIST_REL.split("/"))
    curr_path = project_root.joinpath(*CURR_REL.split("/"))
    model_path = project_root.joinpath(*MODEL_REL.split("/"))
    identity_rows = active.get("identities", [])
    identities = {r.get("path"): r.get("sha256") for r in identity_rows if isinstance(r, dict)}
    expected_identities = {BRIDGE_REL: BRIDGE_SHA, HIST_REL: HIST_SHA, CURR_REL: CURR_SHA, MODEL_REL: MODEL_SHA}
    for rel, expected_sha in expected_identities.items():
        if identities.get(rel) != expected_sha:
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
    if frozen.get("sha256") != "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953" or frozen.get("bytes") != 796318:
        raise A3AdjudicationError("A3_BRIDGE_FROZEN_C11C_PIN_MISMATCH")
    policy = bridge.get("approved_policy", {})
    policy_a3 = policy.get("a3", {}) if isinstance(policy, dict) else {}
    proposal_rel = "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
    if policy_a3.get("path") != proposal_rel or policy_a3.get("sha256") != "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc" or policy_a3.get("decision") != "APPROVE_AS_PROPOSED":
        raise A3AdjudicationError("A3_APPROVED_PROPOSAL_BINDING_MISMATCH")
    proposal_path = project_root.joinpath(*proposal_rel.split("/"))
    if not proposal_path.is_file() or sha256_file(proposal_path) != "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc":
        raise A3AdjudicationError("A3_APPROVED_PROPOSAL_FILE_PIN_MISMATCH")
    policy_ref = policy.get("a3_decision_record", {}) if isinstance(policy, dict) else {}
    if policy_ref.get("sha256") != POLICY_SHA:
        raise A3AdjudicationError("A3_OPERATOR_POLICY_PIN_MISMATCH")
    policy_path = policy_ref.get("path")
    if not isinstance(policy_path, str) or sha256_file(project_root.joinpath(*policy_path.split("/"))) != POLICY_SHA:
        raise A3AdjudicationError("A3_OPERATOR_POLICY_FILE_PIN_MISMATCH")
    decision_record = read_json(project_root, policy_path)
    decisions = {r.get("decision_id"): r for r in decision_record.get("decisions", []) if isinstance(r, dict)}
    accepted = decisions.get("A.3_LOOP_DRILL_EDITORIAL_WINDOWS")
    if not isinstance(accepted, dict) or accepted.get("decision") != "APPROVE_AS_PROPOSED":
        raise A3AdjudicationError("A3_OPERATOR_APPROVAL_MISSING")
    if accepted.get("proposal_sha256") != "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc":
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
    if not isinstance(lineage.get("old_pointer_value"), str) or not isinstance(lineage.get("new_pointer_value"), str):
        raise A3AdjudicationError("A3_BRIDGE_POINTER_VALUES_MISSING")
    old_value = lineage["old_pointer_value"]
    new_value = lineage["new_pointer_value"]
    if new_value != MODEL_SHA:
        raise A3AdjudicationError("A3_D98_TARGET_POINTER_VALUE_MISMATCH")

    # Check *whole-document* preimage/postimage hashes against pinned manifest files.
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
    historical = read_json(project_root, HIST_REL)
    current = read_json(project_root, CURR_REL)
    verify_single_pointer_postimage(historical, current, old_value, new_value)

    # Legacy diagnostic labels are not reliable evidence of hash scope. For each
    # side, constrain expected/actual to the two independently verified identities
    # that are valid for that side (whole-file manifest SHA OR the one JSON-pointer
    # value), require exact expected==actual agreement, and expose the classification.
    def verify_legacy_pair(label: str, expected_key: str, actual_key: str,
                           whole_manifest_sha: str, pointer_value_sha: str) -> str:
        expected_claim = active.get(expected_key)
        actual_claim = active.get(actual_key)
        if not isinstance(expected_claim, str) or not isinstance(actual_claim, str):
            raise A3AdjudicationError("A3_LEGACY_DIAGNOSTIC_HASH_MISSING:" + label)
        if expected_claim != actual_claim:
            raise A3AdjudicationError("A3_LEGACY_DIAGNOSTIC_EXPECTED_ACTUAL_MISMATCH:" + label)
        if expected_claim == whole_manifest_sha:
            return "WHOLE_MANIFEST_SHA256"
        if expected_claim == pointer_value_sha:
            return "JSON_POINTER_VALUE_SHA256"
        raise A3AdjudicationError("A3_LEGACY_DIAGNOSTIC_HASH_OUTSIDE_PINNED_DOMAINS:" + label)

    old_diagnostic_hash_domain = verify_legacy_pair(
        "old", "old_pointer_expected", "old_pointer_actual", HIST_SHA, old_value)
    new_diagnostic_hash_domain = verify_legacy_pair(
        "new", "new_pointer_expected", "new_pointer_actual", CURR_SHA, new_value)

    # These two explicitly scoped bridge fields must always contain pointer values.
    pointer_domain_pairs = {
        "bridge_old_pointer_value": old_value,
        "bridge_new_pointer_value": new_value,
    }
    for key, expected_value in pointer_domain_pairs.items():
        if key in active and active.get(key) != expected_value:
            raise A3AdjudicationError("A3_POINTER_DOMAIN_VALUE_MISMATCH:" + key)
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
        "legacy_diagnostic_hash_domains": {
            "old_expected_actual": old_diagnostic_hash_domain,
            "new_expected_actual": new_diagnostic_hash_domain,
        },
    }
