#!/usr/bin/env python3
"""Read-only static guard for isolated V2-B consumer runtime revision 2."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

EXPECTED_FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_DESIGN_SHA = "099da26bf50820fec026f2fe4a764bb78b35b6e1f24306f12a35181f8fa879c4"
EXPECTED_DESIGN_SCHEMA_SHA = "1547efa8f129299354b967b3352847aa79037a0d0068b1ccc9bdd3481aaf1ca4"
EXPECTED_DESIGN_TEST_SHA = "dfa2bd278eaba47a9967fa4b3fbd75249e218123ee10570725e220ec4e7d319c"
EXPECTED_DESIGN_RECEIPT_SHA = "9148ad3dfc21857d7decf5885a3fb0e10a839234ba7672040cfdfa86b57c7bd2"
EXPECTED_DESIGN_STDOUT_SHA = "0e8e75cbd7d749c758657bd20e8b39e9df31047decf71094350cb4ab3f94246d"
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strip_comments(source: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in source.splitlines())


def main() -> int:
    if len(sys.argv) != 3:
        print("USAGE=test_d_renderer_challenge_visual_payload_v2b_allowlisted_coordinate_consumer_runtime_static.py REPO_ROOT DESIGN_RECEIPT_PATH")
        return 2

    root = Path(sys.argv[1]).resolve()
    receipt_path = Path(sys.argv[2]).resolve()
    checks = 0
    failures: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(label)

    def file_hash(relative: str, expected: str, label: str) -> None:
        path = root / relative
        check(path.is_file(), label + "_EXISTS")
        if path.is_file():
            check(sha256(path) == expected, label + "_SHA256")

    contract_rel = "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CONTRACT_V2.json"
    schema_rel = "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CONTRACT_SCHEMA_V2.json"
    module_rel = "tools/c11d/d9/allowlisted_coordinate_consumer_review_only_v2.gd"
    runtime_test_rel = "tools/c11d/d9/test_allowlisted_coordinate_consumer_review_only_runtime_v2.gd"
    design_rel = "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_V1.json"
    design_schema_rel = "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_SCHEMA_V1.json"
    design_test_rel = "tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_allowlisted_coordinate_consumer_implementation_design_v1.py"

    contract_path = root / contract_rel
    schema_path = root / schema_rel
    module_path = root / module_rel
    runtime_test_path = root / runtime_test_rel

    check(root.is_dir(), "REPO_ROOT_EXISTS")
    check(receipt_path.is_file(), "PRIOR_DESIGN_RECEIPT_EXISTS")
    receipt: dict[str, Any] = {}
    if receipt_path.is_file():
        try:
            receipt_value = json.loads(receipt_path.read_text(encoding="utf-8"))
            if isinstance(receipt_value, dict):
                receipt = receipt_value
            else:
                failures.append("PRIOR_DESIGN_RECEIPT_IS_OBJECT")
                checks += 1
        except (OSError, json.JSONDecodeError):
            failures.append("PRIOR_DESIGN_RECEIPT_JSON")
            checks += 1

    check(receipt.get("status") == "PASS_STATIC_DESIGN_TESTS", "PRIOR_DESIGN_RECEIPT_STATUS")
    check(receipt.get("test_count") == 235, "PRIOR_DESIGN_RECEIPT_TEST_COUNT")
    check(receipt.get("planned_negative_runtime_case_count") == 261, "PRIOR_DESIGN_RECEIPT_PLANNED_MATRIX")
    check(receipt.get("negative_runtime_tests_executed") is False, "PRIOR_DESIGN_NEGATIVES_NOT_PRETENDED_EXECUTED")
    check(receipt.get("implementation_design_sha256") == EXPECTED_DESIGN_SHA, "PRIOR_DESIGN_RECEIPT_DESIGN_PIN")
    check(receipt.get("implementation_design_schema_sha256") == EXPECTED_DESIGN_SCHEMA_SHA, "PRIOR_DESIGN_RECEIPT_SCHEMA_PIN")
    check(receipt.get("implementation_design_test_script_sha256") == EXPECTED_DESIGN_TEST_SHA, "PRIOR_DESIGN_RECEIPT_TEST_PIN")
    check(receipt.get("stdout_sha256") == EXPECTED_DESIGN_STDOUT_SHA, "PRIOR_DESIGN_RECEIPT_STDOUT_PIN")
    check(receipt.get("stderr_sha256") == EMPTY_SHA, "PRIOR_DESIGN_RECEIPT_EMPTY_STDERR")
    check(receipt.get("frozen_manifest_sha256") == EXPECTED_FROZEN_SHA, "PRIOR_DESIGN_RECEIPT_C11C_PIN")
    check(receipt.get("renderer") == "OFF", "PRIOR_DESIGN_RECEIPT_RENDERER_OFF")
    check(receipt.get("render_test_authorized") is False, "PRIOR_DESIGN_RECEIPT_RENDER_TEST_DENIED")
    check(receipt.get("candidate_input_admissible") is False, "PRIOR_DESIGN_RECEIPT_CANDIDATE_INPUT_DENIED")

    check(contract_path.is_file(), "RUNTIME_CONTRACT_EXISTS")
    check(schema_path.is_file(), "RUNTIME_SCHEMA_EXISTS")
    check(module_path.is_file(), "RUNTIME_MODULE_EXISTS")
    check(runtime_test_path.is_file(), "GODOT_RUNTIME_TEST_EXISTS")
    check((root / design_rel).is_file(), "PINNED_DESIGN_EXISTS")
    check((root / design_schema_rel).is_file(), "PINNED_DESIGN_SCHEMA_EXISTS")
    check((root / design_test_rel).is_file(), "PINNED_DESIGN_SUITE_EXISTS")

    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        contract = {}
        failures.append("RUNTIME_CONTRACT_JSON")
        checks += 1
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        schema = {}
        failures.append("RUNTIME_SCHEMA_JSON")
        checks += 1

    check(contract.get("schema") == "C11D-V2B-ALLOWLISTED-COORDINATE-CONSUMER-RUNTIME-CONTRACT-V2", "RUNTIME_CONTRACT_ID")
    check(contract.get("schema_version") == "2.0", "RUNTIME_CONTRACT_VERSION")
    check(contract.get("status") == "IMPLEMENTED_NOT_RUNTIME_ACCEPTED", "RUNTIME_CONTRACT_STATUS")
    check(contract.get("source_authority", {}).get("frozen_c11c_manifest_sha256") == EXPECTED_FROZEN_SHA, "RUNTIME_CONTRACT_C11C_PIN")
    check(contract.get("source_authority", {}).get("prior_design_receipt_sha256") == EXPECTED_DESIGN_RECEIPT_SHA, "RUNTIME_CONTRACT_PRIOR_RECEIPT_PIN")
    check(contract.get("implementation", {}).get("runtime_module_path") == module_rel, "RUNTIME_MODULE_PATH")
    check(contract.get("implementation", {}).get("runtime_test_path") == runtime_test_rel, "RUNTIME_TEST_PATH")
    check(contract.get("implementation", {}).get("runtime_module_sha256") == (sha256(module_path) if module_path.is_file() else ""), "RUNTIME_MODULE_HASH_SELF_PIN")
    check(contract.get("implementation", {}).get("runtime_test_sha256") == (sha256(runtime_test_path) if runtime_test_path.is_file() else ""), "RUNTIME_TEST_HASH_SELF_PIN")
    current_static_test = Path(__file__).resolve()
    check(contract.get("implementation", {}).get("runtime_static_test_sha256") == sha256(current_static_test), "RUNTIME_STATIC_TEST_HASH_SELF_PIN")
    check(contract.get("governance_locks", {}).get("renderer") == "OFF", "GOVERNANCE_RENDERER_OFF")
    check(contract.get("governance_locks", {}).get("release_authority") == "NONE", "GOVERNANCE_RELEASE_AUTHORITY_NONE")
    check(contract.get("governance_locks", {}).get("approved_bindings") == 0, "GOVERNANCE_BINDINGS_ZERO")
    check(contract.get("governance_locks", {}).get("approved_custom_data_bindings") == 0, "GOVERNANCE_CUSTOM_BINDINGS_ZERO")
    check(contract.get("governance_locks", {}).get("approved_renderer_projection_bindings") == 0, "GOVERNANCE_RENDERER_BINDINGS_ZERO")
    for name in ("media_created", "payload_materialized", "candidate_input_admissible", "runtime_implementation_authorized_for_production", "render_test_authorized", "whole_custom_data_serialization_allowed"):
        check(contract.get("governance_locks", {}).get(name) is False, "GOVERNANCE_LOCK_" + name)

    check(schema.get("schema") == "C11D-V2B-ALLOWLISTED-COORDINATE-CONSUMER-RUNTIME-CONTRACT-SCHEMA-V2", "RUNTIME_SCHEMA_ID")
    check(schema.get("additionalProperties") is False, "RUNTIME_SCHEMA_CLOSED_ROOT")
    for required_key in contract.get("schema_required_keys", []):
        check(required_key in contract, "RUNTIME_CONTRACT_REQUIRED_" + str(required_key))
    check((root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json").is_file(), "FROZEN_MANIFEST_EXISTS")
    frozen = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    if frozen.is_file():
        check(sha256(frozen) == EXPECTED_FROZEN_SHA, "FROZEN_MANIFEST_UNCHANGED")

    file_hash(design_rel, EXPECTED_DESIGN_SHA, "IMPLEMENTATION_DESIGN")
    file_hash(design_schema_rel, EXPECTED_DESIGN_SCHEMA_SHA, "IMPLEMENTATION_DESIGN_SCHEMA")
    file_hash(design_test_rel, EXPECTED_DESIGN_TEST_SHA, "IMPLEMENTATION_DESIGN_TEST")

    for pin_group in contract.get("source_authority", {}).get("runtime_reference_pins", []):
        relative = str(pin_group.get("path", ""))
        expected = str(pin_group.get("sha256", ""))
        pin_path = root / relative
        check(pin_path.is_file(), "REFERENCE_EXISTS_" + relative)
        if pin_path.is_file():
            check(sha256(pin_path) == expected, "REFERENCE_SHA_" + relative)

    if module_path.is_file():
        source = module_path.read_text(encoding="utf-8")
        code = strip_comments(source)
        check(len(re.findall(r"\.custom_data\s*\.get\s*\(", code)) == 1, "ONE_ALLOWLISTED_CUSTOM_DATA_GET_SITE")
        check(re.search(r"if\s+typeof\(source_value\)\s*==\s*TYPE_OBJECT\s*:\s*\n\s*if\s+source_value\s+is\s+RefCounted\s+and\s+source_value\s*==\s*missing_sentinel:", code) is not None, "SENTINEL_OBJECT_TYPE_GUARD_BEFORE_EQUALITY")
        for forbidden_pattern, label in [
            (r"\.custom_data\s*\.has\s*\(", "CUSTOM_DATA_HAS_FORBIDDEN"),
            (r"\.custom_data\s*\.keys\s*\(", "CUSTOM_DATA_KEYS_FORBIDDEN"),
            (r"\.custom_data\s*\.duplicate\s*\(", "CUSTOM_DATA_DUPLICATE_FORBIDDEN"),
            (r"\.custom_data\s*\[", "CUSTOM_DATA_INDEXING_FORBIDDEN"),
            (r"custom_data\s*\.\s*values\s*\(", "CUSTOM_DATA_VALUES_FORBIDDEN"),
            (r"RenderingServer", "RENDERING_SERVER_FORBIDDEN"),
            (r"ResourceLoader", "RESOURCE_LOADER_FORBIDDEN"),
            (r"\bNode2D\b|\bSprite2D\b|\bTexture2D\b|\bImageTexture\b", "RENDER_NODES_AND_TEXTURES_FORBIDDEN"),
            (r"\bFileAccess\b|\bDirAccess\b", "FILESYSTEM_ACCESS_FORBIDDEN_IN_CONSUMER"),
            (r"\bload\s*\(", "ASSET_LOADING_FORBIDDEN"),
            (r"\bprint\s*\(|\bprinterr\s*\(|\bpush_error\s*\(", "INPUT_LOGGING_FORBIDDEN"),
            (r"JSON\s*\.\s*stringify|JSON\s*\.\s*new", "JSON_SERIALIZATION_FORBIDDEN"),
        ]:
            check(re.search(forbidden_pattern, code) is None, label)

        signature = re.search(r"func\s+project_allowlisted_target_marker_track\s*\(([^)]*)\)", code)
        check(signature is not None, "ENTRYPOINT_EXISTS")
        if signature:
            args = [part.strip().split(":", 1)[0].strip() for part in signature.group(1).split(",") if part.strip()]
            check(args == ["candidate_id", "simulation_result", "upstream_validation"], "ENTRYPOINT_EXACT_THREE_INPUTS_NO_FIELD_ARGUMENT")

        check("CHALLENGE_003" in code and "target_x" in code, "CHALLENGE_003_SINGLE_ALLOWLISTED_FIELD")
        check(code.count('"CHALLENGE_005": "target_position"') == 1, "CHALLENGE_005_ALLOWLIST")
        check(code.count('"CHALLENGE_006": "target_position"') == 1, "CHALLENGE_006_ALLOWLIST")
        check(code.count('"CHALLENGE_007": "target_position"') == 1, "CHALLENGE_007_ALLOWLIST")
        check("CHALLENGE_008" not in code and "CHALLENGE_009" not in code, "BLOCKED_CANDIDATES_ABSENT_FROM_RUNTIME_ALLOWLIST")
        check("winning_frame" not in code, "WINNING_FRAME_NOT_READ_BY_CONSUMER")
        check(re.search(r"\bround\s*\(|\bclamp[fdi]?\s*\(", code) is None, "NO_ROUNDING_OR_CLAMPING")
        check("540.0" in code and "480.0" in code and "1080.0" in code and "1920.0" in code, "COORDINATE_DOMAINS_AND_LOGICAL_CANVAS_PINNED")
        check("PER_RUN_CONSTANT_MISMATCH" in code, "CHALLENGE_005_CONSTANT_GUARD")
        check("MISSING_ALLOWLISTED_FIELD" in code, "MISSING_FIELD_FAIL_CLOSED")
        check("FRAME_CARDINALITY_MISMATCH" in code, "CARDINALITY_FAIL_CLOSED")
        check("return _failure(\"INVALID_VALUE_TYPE\")" in code, "STRICT_TYPE_FAILURE_PRESENT")
        check("return _failure(\"NONFINITE_VALUE\")" in code, "NONFINITE_FAILURE_PRESENT")

    if runtime_test_path.is_file():
        runtime_test = runtime_test_path.read_text(encoding="utf-8")
        runtime_code = strip_comments(runtime_test)
        check("extends SceneTree" in runtime_code, "HEADLESS_RUNTIME_TEST_SCENETREE")
        check("RenderingServer" not in runtime_code and "Sprite2D" not in runtime_code and "Texture2D" not in runtime_code, "RUNTIME_TEST_HAS_NO_RENDERING_CALLS")
        check("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_NEGATIVE_RUNTIME_CASES=%d/241" in runtime_code, "NEGATIVE_DENOMINATOR_241")
        check("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_POSITIVE_RUNTIME_CASES=%d/36" in runtime_code, "POSITIVE_DENOMINATOR_36")
        check("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CASES=%d/277" in runtime_code, "TOTAL_DENOMINATOR_277")
        check("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_IMPLEMENTATION_REVISION=V2_SAFE_SENTINEL_TYPE_GUARD" in runtime_code, "V2_SENTINEL_FIX_REVISION_MARKER")

    # Structural call-graph guard: permit only explicit review and composition test harnesses.
    callsite_paths: list[str] = []
    needle = ".project_allowlisted_target_marker_track("
    for gd_path in root.rglob("*.gd"):
        rel = gd_path.relative_to(root).as_posix()
        if any(part in {".git", ".godot", ".mono", "bin", "obj"} for part in gd_path.parts):
            continue
        try:
            text = gd_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if needle in text:
            callsite_paths.append(rel)
        expected_review_callsites = sorted([
        runtime_test_rel,
        "tools/c11d/d9/test_allowlisted_coordinate_consumer_review_only_runtime.gd",
        "tools/c11d/d9/test_allowlisted_coordinate_consumer_source_composition_runtime.gd",
    ])
    check(sorted(callsite_paths) == expected_review_callsites, "ONLY_REVIEW_AND_COMPOSITION_TESTS_ARE_CALLSITES")

    check(contract.get("negative_matrix_reconciliation", {}).get("negative_runtime_cases_expected") == 241, "RECONCILED_NEGATIVE_MATRIX_241")
    check(contract.get("negative_matrix_reconciliation", {}).get("positive_runtime_cases_expected") == 36, "RECONCILED_POSITIVE_MATRIX_36")
    check(contract.get("negative_matrix_reconciliation", {}).get("total_runtime_cases_expected") == 277, "RECONCILED_TOTAL_MATRIX_277")
    check(contract.get("negative_matrix_reconciliation", {}).get("original_design_261_not_claimed_as_all_negative") is True, "ORIGINAL_NEGATIVE_DENOMINATOR_CORRECTED_TRANSPARENTLY")
    check(contract.get("implementation", {}).get("production_callsite_count") == 0, "CONTRACT_PRODUCTION_CALLSITE_ZERO")
    check(contract.get("implementation", {}).get("production_consumer_code_included") is False, "NO_PRODUCTION_CONSUMER_CODE")

    if failures:
        for failure in failures:
            print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_STATIC_FAILURE=" + failure)
        print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_STATIC_TEST_STATUS=FAIL")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_STATIC_CHECKS_PASSED=%d/%d" % (checks - len(failures), checks))
        return 1

    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_STATIC_CHECKS=%d/%d" % (checks, checks))
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_ONE_CUSTOM_DATA_LOOKUP_SITE=true")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_PRODUCTION_CALLS=0")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RENDERER=OFF")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_STATIC_TEST_STATUS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
