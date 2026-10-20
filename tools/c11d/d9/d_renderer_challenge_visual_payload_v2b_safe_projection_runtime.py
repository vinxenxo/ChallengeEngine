#!/usr/bin/env python3
"""V2-B source-state seed-sensitivity acceptance harness. Runtime gate is receipt-controlled."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

sys.dont_write_bytecode = True

RUNTIME_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json")
DESIGN_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json")
SEED_MATRIX_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json")
HARNESS_REL = Path("tools/c11d/d9/challenge_visual_payload_v2b_safe_projection_runtime_in_memory.gd")
RECEIPT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_RECEIPT_SCHEMA_V1.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_REPORT_SCHEMA_V1.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_SCHEMA_V1.json")
V2C_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json")
V2C_CONTRACT_SHA = "6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c"
IMPLEMENTATION_TEST_REL = Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py")
RUNTIME_RUNNER_REL = Path("tools/c11d/d9/d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py")
HARNESS = "res://" + HARNESS_REL.as_posix()
FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
DESIGN_SHA = "e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc"
MATRIX_SHA = "d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a"
RUNTIME_CONTRACT_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-CONTRACT-V1"
DESIGN_CONTRACT_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-VISUAL-PROJECTION-DESIGN-CONTRACT-V1"
RECEIPT_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-RECEIPT-V1"
REPORT_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-REPORT-V1"
TEST_RECEIPT_ID = "C11D-V2B-RUNTIME-IMPLEMENTATION-TEST-RECEIPT-V1"
IDS = [f"CHALLENGE_{i:03d}" for i in range(1, 10)]
ROLES = ["BASELINE_R1", "BASELINE_R2", "GAMEPLAY_SEED_MUTATION", "MUSIC_SEED_MUTATION", "EDITORIAL_MUTATION"]
GOVERNANCE = {
    "renderer": "OFF", "media_created": False, "payload_materialized": False,
    "candidate_input_admissible": False, "seed_domains_complete_for_candidate_input": False,
    "automatic_seed_generation": False, "master_seed": "NOT_ADOPTED", "D4.8": "BLOCKED",
    "D9.10": "PREPARE_ONLY", "D9.14": "BLOCKED", "D9.16": "BLOCKED",
    "D9.17": "BLOCKED_NO_GO", "D10": "BLOCKED_FOR_PROMOTION",
    "baseline_approval": "MISSING", "freeze_eligible": False, "release_authority": "NONE",
    "visual_seed_sensitivity": "NOT_TESTED_UNTIL_V2B_RUNTIME_ACCEPTED",
    "challenge_008_009_phase_timeline_acceptance": "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY",
    "challenge_004_v1_fixture": "IMMUTABLE"
}

class ContractError(ValueError):
    pass

class PlannerInvocationFailed(ContractError):
    pass


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def is_sha(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def dump_json(path: Path, value: Any) -> str:
    data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    path.write_bytes(data)
    return sha_bytes(data)


def exact(value: Any, fields: set[str], label: str) -> None:
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be an object")
    if set(value) != fields:
        raise ContractError(f"{label} fields mismatch: missing={sorted(fields-set(value))}; unknown={sorted(set(value)-fields)}")


def safe_child(root: Path, rel: str) -> Path:
    p = Path(rel)
    if not rel or p.is_absolute() or ".." in p.parts or "\\" in rel:
        raise ContractError(f"unsafe repository-relative path: {rel!r}")
    full = (root / p).resolve()
    if root.resolve() not in full.parents:
        raise ContractError(f"path escapes repository: {rel}")
    return full


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} unreadable/invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise ContractError(f"{label} must be an object")
    return data


def validate_runtime_contract(contract: Any, contract_sha: str) -> None:
    fields = {
        "schema", "schema_version", "status", "scope", "design_contract_path", "design_contract_sha256",
        "seed_test_matrix_path", "seed_test_matrix_sha256", "frozen_c11c_manifest_sha256",
        "expected_selector_count", "selector_ids", "variants_per_selector", "variant_roles",
        "canonical_planner_invocations_per_selector", "godot_processes_per_selector",
        "canonical_planner_invocations_expected", "godot_processes_expected", "gameplay_seed_mutation_rule",
        "baseline_music_seed", "music_seed_mutation", "seed_limits", "identity_model", "safe_projection",
        "candidate_observation", "planner_route", "variant_policy", "comparison_rules", "implementation",
        "expected_selector_count_matches_design_contract", "source_pin_count", "authority_input_pin_count",
        "approved_bindings", "approved_custom_data_bindings", "payload_materialized", "media_created", "renderer",
        "governance_locks", "godot_version_required", "godot_process_timeout_seconds", "first_failure_stop",
        "runtime_status", "next_gate"
    }
    exact(contract, fields, "runtime contract")
    if contract.get("schema") != RUNTIME_CONTRACT_ID or contract.get("schema_version") != "1.0" or contract.get("status") != "IMPLEMENTED_NOT_RUNTIME_ACCEPTED":
        raise ContractError("runtime contract identity/status mismatch")
    if not is_sha(contract_sha) or int(contract["expected_selector_count"]) != 9 or contract["selector_ids"] != IDS:
        raise ContractError("selector denominator/order mismatch")
    if contract["variant_roles"] != ROLES or int(contract["variants_per_selector"]) != 5:
        raise ContractError("variant matrix role/order mismatch")
    if int(contract["canonical_planner_invocations_expected"]) != 45 or int(contract["godot_processes_expected"]) != 45:
        raise ContractError("45/45 runtime denominator mismatch")
    if contract["design_contract_sha256"] != DESIGN_SHA or contract["seed_test_matrix_sha256"] != MATRIX_SHA or contract["frozen_c11c_manifest_sha256"] != FROZEN_SHA:
        raise ContractError("upstream source hash pin mismatch")
    if int(contract["source_pin_count"]) != 81 or int(contract["authority_input_pin_count"]) != 9:
        raise ContractError("upstream source/authority pin denominator mismatch")
    if contract["approved_bindings"] != 0 or contract["approved_custom_data_bindings"] != 0:
        raise ContractError("approved binding counts must stay zero")
    if contract["payload_materialized"] is not False or contract["media_created"] is not False or contract["renderer"] != "OFF":
        raise ContractError("prohibited side effects must stay disabled")
    if contract["governance_locks"] != GOVERNANCE:
        raise ContractError("governance locks differ from frozen policy")
    if contract["safe_projection"].get("allowlisted_frame_fields") != ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"]:
        raise ContractError("safe projection allowlist changed")
    if "custom_data" not in contract["safe_projection"].get("forbidden_frame_fields", []):
        raise ContractError("custom_data must remain forbidden in base projection")
    if contract["candidate_observation"].get("whole_custom_data_map_access") != "PROHIBITED" or contract["candidate_observation"].get("raw_values_in_receipt") is not False:
        raise ContractError("candidate observation policy broadened")
    impl = contract["implementation"]
    for k in ("harness_sha256", "receipt_schema_sha256", "report_schema_sha256", "contract_schema_sha256", "runtime_runner_sha256"):
        if not is_sha(impl.get(k)):
            raise ContractError(f"implementation.{k} missing/invalid")
    if (impl.get("harness_path") != HARNESS_REL.as_posix() or impl.get("receipt_schema_path") != RECEIPT_SCHEMA_REL.as_posix() or impl.get("report_schema_path") != REPORT_SCHEMA_REL.as_posix() or impl.get("contract_schema_path") != CONTRACT_SCHEMA_REL.as_posix() or impl.get("runtime_runner_path") != RUNTIME_RUNNER_REL.as_posix()):
        raise ContractError("implementation paths changed")


def load_upstream(root: Path, contract: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    design_path = safe_child(root, str(contract["design_contract_path"]))
    matrix_path = safe_child(root, str(contract["seed_test_matrix_path"]))
    if not design_path.is_file() or sha_file(design_path) != DESIGN_SHA:
        raise ContractError("V2-B design contract SHA mismatch")
    if not matrix_path.is_file() or sha_file(matrix_path) != MATRIX_SHA:
        raise ContractError("V2-B seed matrix SHA mismatch")
    design = load_json(design_path, "V2-B design contract")
    matrix = load_json(matrix_path, "V2-B seed test matrix")
    if design.get("schema") != DESIGN_CONTRACT_ID or design.get("status") != "DESIGN_ONLY_NOT_IMPLEMENTED":
        raise ContractError("V2-B design contract identity/status mismatch")
    if matrix.get("schema") != "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SEED-TEST-MATRIX-V1" or matrix.get("status") != "DESIGN_ONLY_NOT_EXECUTED":
        raise ContractError("V2-B seed matrix identity/status mismatch")
    if design.get("authority", {}).get("approved_bindings") != 0 or design.get("authority", {}).get("approved_custom_data_bindings") != 0:
        raise ContractError("design authority bindings are not zero")
    if len(design.get("source_pins", [])) != 81 or int(design.get("source_pin_count", -1)) != 81:
        raise ContractError("source pin denominator not 81")
    if len(design.get("authority_input_pins", [])) != 9 or int(design.get("authority_input_pin_count", -1)) != 9:
        raise ContractError("authority input pin denominator not 9")
    errors: list[str] = []
    for label, pins in (("source", design["source_pins"]), ("authority", design["authority_input_pins"])):
        seen: set[str] = set()
        for pin in pins:
            if not isinstance(pin, dict) or not isinstance(pin.get("path"), str) or not is_sha(pin.get("sha256")):
                errors.append(f"{label}: malformed pin row")
                continue
            rel = pin["path"]
            if rel in seen:
                errors.append(f"{label}: duplicate pin path {rel}")
                continue
            seen.add(rel)
            path = safe_child(root, rel)
            if not path.is_file():
                errors.append(f"{label}: missing pinned source {rel}")
            elif sha_file(path) != pin["sha256"]:
                errors.append(f"{label}: SHA mismatch {rel}")
    manifest = safe_child(root, "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    if not manifest.is_file() or sha_file(manifest) != FROZEN_SHA:
        errors.append("frozen C11-C manifest SHA mismatch")
    return design, matrix, errors


def validate_implementation_test_receipt(root: Path, receipt_path: Path, contract_sha: str, contract: Mapping[str, Any]) -> dict[str, Any]:
    receipt = load_json(receipt_path, "implementation test receipt")
    fields = {
        "schema", "status", "runtime_contract_sha256", "design_contract_sha256", "frozen_manifest_sha256",
        "source_pin_count", "authority_input_pin_count", "test_count", "implementation_test_sha256",
        "runtime_runner_sha256", "runtime_harness_sha256", "receipt_schema_sha256", "report_schema_sha256", "contract_schema_sha256",
        "contract_file_sha256", "test_stdout_sha256", "test_stderr_sha256", "overlay_manifest_sha256"
    }
    exact(receipt, fields, "implementation test receipt")
    if receipt["schema"] != TEST_RECEIPT_ID or receipt["status"] != "PASS_IMPLEMENTATION_STATIC_TESTS":
        raise ContractError("implementation tests have not produced an accepted receipt")
    if receipt["runtime_contract_sha256"] != contract_sha or receipt["contract_file_sha256"] != contract_sha:
        raise ContractError("implementation test receipt contract SHA mismatch")
    if receipt["design_contract_sha256"] != DESIGN_SHA or receipt["frozen_manifest_sha256"] != FROZEN_SHA:
        raise ContractError("implementation test receipt upstream pin mismatch")
    if receipt["source_pin_count"] != 81 or receipt["authority_input_pin_count"] != 9 or receipt["test_count"] < 60:
        raise ContractError("implementation test receipt counts incomplete")
    if not is_sha(receipt["overlay_manifest_sha256"]) or not is_sha(receipt["test_stdout_sha256"]) or not is_sha(receipt["test_stderr_sha256"]):
        raise ContractError("implementation test evidence hashes malformed")
    impl = contract["implementation"]
    expected_file_hashes = {
        "implementation_test_sha256": IMPLEMENTATION_TEST_REL,
        "runtime_runner_sha256": RUNTIME_RUNNER_REL,
        "runtime_harness_sha256": HARNESS_REL,
        "receipt_schema_sha256": RECEIPT_SCHEMA_REL,
        "report_schema_sha256": REPORT_SCHEMA_REL,
        "contract_schema_sha256": CONTRACT_SCHEMA_REL,
        "contract_file_sha256": RUNTIME_CONTRACT_REL,
    }
    for receipt_key, rel in expected_file_hashes.items():
        p = safe_child(root, rel.as_posix())
        if not p.is_file() or sha_file(p) != receipt[receipt_key]:
            raise ContractError(f"implementation test receipt does not match active file: {receipt_key}")
    if (receipt["runtime_harness_sha256"] != impl["harness_sha256"] or receipt["receipt_schema_sha256"] != impl["receipt_schema_sha256"] or receipt["report_schema_sha256"] != impl["report_schema_sha256"] or receipt["contract_schema_sha256"] != impl["contract_schema_sha256"] or receipt["runtime_runner_sha256"] != impl["runtime_runner_sha256"]):
        raise ContractError("implementation test receipt implementation pin mismatch")
    return receipt


def resolve_godot(explicit: str | None) -> str | None:
    candidates = [explicit, os.environ.get("C11D_GODOT_EXECUTABLE", "").strip(), shutil.which("godot.exe"), shutil.which("godot")]
    for item in candidates:
        if not item:
            continue
        val = item.strip('"')
        p = Path(val)
        if p.is_file():
            return str(p.resolve())
        found = shutil.which(val)
        if found:
            return found
    return None


def version_probe(exe: str) -> tuple[str, int, str, str]:
    try:
        p = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=20, check=False)
        out = (p.stdout or "")
        err = (p.stderr or "")
        combined = (out + "\n" + err).strip()
        ver = combined.splitlines()[0].strip() if combined else ""
        return ver, int(p.returncode), sha_bytes(out.encode("utf-8")), sha_bytes(err.encode("utf-8"))
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"PROBE_ERROR:{type(exc).__name__}:{exc}", 127, sha_bytes(b""), sha_bytes(str(exc).encode("utf-8"))


def read_source_seed(root: Path, selector: Mapping[str, Any]) -> int:
    source_path = safe_child(root, str(selector["challenge_source_path"]))
    source = load_json(source_path, str(selector["challenge_id"]))
    generation = source.get("generation")
    if not isinstance(generation, dict):
        raise ContractError(f"{selector['challenge_id']}: explicit generation object missing")
    seed = generation.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 1 <= seed <= 2147483646:
        raise ContractError(f"{selector['challenge_id']}: explicit gameplay seed invalid")
    return seed


def next_gameplay_seed(source_seed: int) -> int:
    """Deterministic next valid integer with wrap; no RNG and no automatic seed selection."""
    if isinstance(source_seed, bool) or not isinstance(source_seed, int) or not 1 <= source_seed <= 2147483646:
        raise ContractError("invalid source seed for deterministic mutation")
    return 1 if source_seed >= 2147483646 else source_seed + 1


def family_for_selector(root: Path, selector: Mapping[str, Any]) -> str:
    """Resolve family identity from the separately pinned V2-C selector authority."""
    path = safe_child(root, V2C_CONTRACT_REL.as_posix())
    if not path.is_file() or sha_file(path) != V2C_CONTRACT_SHA:
        raise ContractError("pinned V2-C selector/family authority contract SHA mismatch")
    data = load_json(path, "V2-C selector/family authority contract")
    if data.get("schema") != "C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-CONTRACT-V1":
        raise ContractError("pinned V2-C selector/family authority contract identity mismatch")
    matches = [item for item in data.get("selectors", []) if isinstance(item, dict) and item.get("challenge_id") == selector.get("challenge_id")]
    if len(matches) != 1:
        raise ContractError(f"pinned V2-C contract selector cardinality mismatch for {selector.get('challenge_id')}")
    item = matches[0]
    family_id = item.get("family_id")
    if (item.get("mechanic") != selector.get("mechanic") or
        item.get("source_path") != selector.get("challenge_source_path") or
        item.get("source_sha256") != selector.get("challenge_source_sha256") or
        not isinstance(family_id, str) or not family_id):
        raise ContractError(f"pinned selector/family lineage mismatch for {selector.get('challenge_id')}")
    return family_id


def make_planner(root: Path, selector: Mapping[str, Any], role: str, source_seed: int) -> dict[str, Any]:
    d9 = str(root / "tools" / "c11d" / "d9")
    if d9 not in sys.path:
        sys.path.insert(0, d9)
    import universal_producer as planner
    import universal_editorial_model as editorial
    import d_renderer_dynamic_request_payload_binding as binder
    from editorial_render_bridge import build_bridge_planning_record
    from d_render_adapter import prepare_d_only_adapter_envelope

    cid = str(selector["challenge_id"])
    family_id = family_for_selector(root, selector)
    selection_resolved = editorial.resolve_selection({"content_type": "challenges", "family_id": None, "subtype_id": None, "variant_id": cid}, root)
    selection = {k: selection_resolved.get(k) for k in ("content_type", "family_id", "subtype_id", "variant_id")}
    expected = {"content_type": "challenges", "family_id": family_id, "subtype_id": None, "variant_id": cid}
    if selection != expected:
        raise ContractError(f"canonical selection route mismatch for {cid}")
    raw = binder._base_request(selection, f"C11D-V2B-{cid}")
    gameplay_seed = next_gameplay_seed(source_seed) if role == "GAMEPLAY_SEED_MUTATION" else source_seed
    music_seed = 840002 if role == "MUSIC_SEED_MUTATION" else 840001
    raw["seed"] = gameplay_seed
    raw["music_seed"] = music_seed
    if role == "EDITORIAL_MUTATION":
        override = dict(raw.get("production_override", {}))
        override["title"] = str(override.get("title", "Review title")) + " · V2B EDITORIAL MUTATION"
        override["subtitle"] = str(override.get("subtitle", "Review subtitle")) + " · V2B EDITORIAL MUTATION"
        override["call_to_action"] = str(override.get("call_to_action", "Continue")) + " · V2B EDITORIAL MUTATION"
        raw["production_override"] = override
    # Count this as a planner invocation only after the canonical planner function is entered.
    try:
        result = planner.evaluate_universal_request(raw, root)
        if result.get("status") != "PLANNED":
            raise ContractError(f"canonical planner returned {result.get('status')}")
        bridge = build_bridge_planning_record(result, root)
        adapter = prepare_d_only_adapter_envelope(result, bridge, root)
        plan = result.get("plan", {})
        if bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE" or adapter.get("status") != "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED":
            raise ContractError("D9.10 planning-only route boundary mismatch")
        if plan.get("renderer_activation") is not False or plan.get("production_execution") is not False or plan.get("d4_8") != "BLOCKED" or plan.get("release_authority") != "NONE":
            raise ContractError("planner governance gate mismatch")
        canonical_request = result.get("canonical_request", {})
        if canonical_request.get("seed") != gameplay_seed or canonical_request.get("music_seed") != music_seed:
            raise ContractError("canonical planner seed domains do not match variant input")
        editorial_values = canonical_request.get("editorial", {})
        required_editorial = {"title", "subtitle", "call_to_action"}
        if not required_editorial.issubset(editorial_values):
            raise ContractError("canonical editorial variant fields missing")
        return {
            "role": role, "status": "PLANNED", "request_hash": result["request_hash"],
            "plan_hash": result["plan_hash"], "editorial_hash": result["editorial_hash"],
            "gameplay_seed": gameplay_seed, "music_seed": music_seed,
            "bridge_status": bridge["status"], "adapter_status": adapter["status"],
            "request_id": canonical_request.get("request_id"),
            "editorial_mutation_applied": role == "EDITORIAL_MUTATION",
        }
    except Exception as exc:
        raise PlannerInvocationFailed(f"{cid}:{role}:{type(exc).__name__}:{exc}") from exc


def validate_receipt(receipt: Any, contract: Mapping[str, Any], selector: Mapping[str, Any], planner: Mapping[str, Any], role: str, run_id: str, pid: int) -> None:
    if not isinstance(receipt, dict):
        raise ContractError("receipt must be an object")
    fields = {"schema", "schema_version", "status", "selector", "process", "runtime", "lineage", "identity", "seeds", "simulation_input_sha256", "source_frames", "source_timebase", "source_asset_pins", "candidate_field_observations", "authority"}
    exact(receipt, fields, "receipt")
    if (receipt["schema"], receipt["schema_version"], receipt["status"]) != (RECEIPT_ID, "1.0", "SAFE_PROJECTION_RECEIPT"):
        raise ContractError("receipt identity/status mismatch")
    exact(receipt["selector"], {"challenge_id", "mechanic"}, "receipt.selector")
    if receipt["selector"] != {"challenge_id": selector["challenge_id"], "mechanic": selector["mechanic"]}:
        raise ContractError("receipt selector mismatch")
    exact(receipt["process"], {"run_id", "process_id", "variant_role", "exit_code"}, "receipt.process")
    if receipt["process"] != {"run_id": run_id, "process_id": pid, "variant_role": role, "exit_code": 0}:
        raise ContractError("receipt process identity mismatch")
    exact(receipt["lineage"], {"runtime_contract_sha256", "design_contract_sha256", "frozen_manifest_sha256", "challenge_source_sha256", "mechanic_source_sha256", "runtime_bridge_sha256", "frame_snapshot_sha256", "verified_source_pin_count", "verified_authority_input_pin_count"}, "receipt.lineage")
    for key in ("runtime_contract_sha256", "design_contract_sha256", "frozen_manifest_sha256", "challenge_source_sha256", "mechanic_source_sha256", "runtime_bridge_sha256", "frame_snapshot_sha256"):
        if not is_sha(receipt["lineage"].get(key)):
            raise ContractError(f"receipt lineage {key} malformed")
    if receipt["lineage"]["runtime_contract_sha256"] != contract["_actual_sha256"] or receipt["lineage"]["design_contract_sha256"] != DESIGN_SHA or receipt["lineage"]["frozen_manifest_sha256"] != FROZEN_SHA:
        raise ContractError("receipt lineage contract pins mismatch")
    if receipt["lineage"]["challenge_source_sha256"] != selector["challenge_source_sha256"] or receipt["lineage"]["mechanic_source_sha256"] != selector["mechanic_source_sha256"]:
        raise ContractError("receipt challenge/mechanic source identity mismatch")
    if receipt["lineage"]["verified_source_pin_count"] != 81 or receipt["lineage"]["verified_authority_input_pin_count"] != 9:
        raise ContractError("receipt does not verify all source/authority pins")
    exact(receipt["identity"], {"canonical_request_hash", "canonical_plan_hash", "editorial_hash", "projection_instance_identity_sha256", "safe_projection_state_sha256", "candidate_field_probe_sha256", "payload_identity"}, "receipt.identity")
    for key in ("canonical_request_hash", "canonical_plan_hash", "editorial_hash", "projection_instance_identity_sha256", "safe_projection_state_sha256"):
        if not is_sha(receipt["identity"].get(key)):
            raise ContractError(f"receipt identity {key} malformed")
    if receipt["identity"]["canonical_request_hash"] != planner["request_hash"] or receipt["identity"]["canonical_plan_hash"] != planner["plan_hash"] or receipt["identity"]["editorial_hash"] != planner["editorial_hash"]:
        raise ContractError("receipt planner identity mismatch")
    probe_hash = receipt["identity"]["candidate_field_probe_sha256"]
    if probe_hash is not None and not is_sha(probe_hash):
        raise ContractError("candidate probe aggregate hash malformed")
    if receipt["identity"]["payload_identity"] != "NOT_CREATED":
        raise ContractError("payload identity must not be created")
    if receipt["seeds"].get("requested_gameplay_seed") != planner["gameplay_seed"] or receipt["seeds"].get("music_seed_request_domain") != planner["music_seed"] or receipt["seeds"].get("music_seed_copied_into_simulation") is not False:
        raise ContractError("receipt seed-domain identity mismatch")
    if receipt["simulation_input_sha256"] and not is_sha(receipt["simulation_input_sha256"]):
        raise ContractError("simulation input digest malformed")
    if receipt["source_frames"].get("count") != receipt["source_frames"].get("expected_game_frames"):
        raise ContractError("source frame cardinality mismatch")
    if receipt["source_frames"].get("coordinate_transform") != "NONE" or receipt["source_frames"].get("resampling") != "PROHIBITED":
        raise ContractError("projection transform/resampling policy changed")
    if receipt["source_frames"].get("projection_sha256") != receipt["identity"]["safe_projection_state_sha256"]:
        raise ContractError("projection digest aliases do not agree")
    conflict = selector["challenge_id"] in ("CHALLENGE_008", "CHALLENGE_009")
    expected_phase = "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY" if conflict else "NOT_EVALUATED_SOURCE_FRAME_ONLY"
    if receipt["source_timebase"].get("known_conflict") is not conflict or receipt["source_timebase"].get("phase_timeline_acceptance") != expected_phase:
        raise ContractError("source timebase governance mismatch")
    expected_candidate = selector.get("custom_data_candidate_field")
    observations = receipt["candidate_field_observations"]
    if not isinstance(observations, list):
        raise ContractError("candidate observations must be a list")
    if expected_candidate is None:
        if observations or probe_hash is not None:
            raise ContractError("selector without candidate emitted candidate observations")
    else:
        if len(observations) != 1:
            raise ContractError("candidate field observation cardinality mismatch")
        obs = observations[0]
        exact(obs, {"field", "semantic_type", "present_frames", "type_histogram", "value_stream_sha256", "raw_values_emitted", "renderer_binding_approved"}, "candidate observation")
        semantic_types = {"target_x": "float", "target_position": "Vector2", "active_selection": "int", "displayed_count": "int"}
        if obs["field"] != expected_candidate or obs["semantic_type"] != semantic_types.get(str(expected_candidate)) or obs["raw_values_emitted"] is not False or obs["renderer_binding_approved"] is not False or not is_sha(obs["value_stream_sha256"]):
            raise ContractError("candidate observation policy/type mismatch")
        if obs["present_frames"] != receipt["source_frames"]["count"] or obs["type_histogram"] != {obs["semantic_type"]: obs["present_frames"]}:
            raise ContractError("candidate field missing, mistyped, or inconsistent in one or more frames")
        if not is_sha(probe_hash):
            raise ContractError("candidate aggregate hash absent")
    exact(receipt["authority"], {"approved_bindings", "approved_custom_data_bindings", "renderer", "payload_materialized", "media_created", "release_authority"}, "receipt.authority")
    if receipt["authority"] != {"approved_bindings": 0, "approved_custom_data_bindings": 0, "renderer": "OFF", "payload_materialized": False, "media_created": False, "release_authority": "NONE"}:
        raise ContractError("receipt authority lock changed")


def run_godot(exe: str, version: str, root: Path, ev: Path, contract_sha: str, contract: Mapping[str, Any], selector: Mapping[str, Any], planner: Mapping[str, Any], role: str) -> tuple[dict[str, Any], str | None]:
    cid = str(selector["challenge_id"])
    suffix = "R1" if role == "BASELINE_R1" else "R2" if role == "BASELINE_R2" else role
    run_id = f"{cid}_{suffix}"
    prefix = ev / f"{cid}_{suffix}"
    source_seed = read_source_seed(root, selector)
    cmd = [
        exe, "--headless", "--path", str(root), "--script", HARNESS, "--",
        f"--challenge-id={cid}", f"--contract-sha256={contract_sha}", f"--run-id={run_id}",
        f"--variant-role={role}", f"--godot-version={version}",
        f"--planner-request-hash={planner['request_hash']}", f"--planner-plan-hash={planner['plan_hash']}",
        f"--editorial-hash={planner['editorial_hash']}", f"--gameplay-seed={planner['gameplay_seed']}",
        f"--music-seed={planner['music_seed']}", f"--source-gameplay-seed={source_seed}"
    ]
    pid = 0; code = 127; out = ""; err = ""; timed_out = False
    try:
        proc = subprocess.Popen(cmd, cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        pid = int(proc.pid or 0)
        try:
            out, err = proc.communicate(timeout=int(contract.get("godot_process_timeout_seconds", 180)))
            code = int(proc.returncode if proc.returncode is not None else 127)
        except subprocess.TimeoutExpired:
            timed_out = True; proc.kill(); out, err = proc.communicate(); code = int(proc.returncode if proc.returncode is not None else 124)
            err += "\nV2B_TIMEOUT: Godot exceeded the configured process timeout.\n"
    except OSError as exc:
        err = f"V2B_PROCESS_START_ERROR:{type(exc).__name__}:{exc}"
    ob = out.encode("utf-8"); eb = err.encode("utf-8")
    (prefix.with_suffix(".out")).write_bytes(ob); (prefix.with_suffix(".err")).write_bytes(eb)
    marker = "C11D_V2B_SAFE_PROJECTION_RECEIPT="
    hits = [line[len(marker):] for line in out.splitlines() if line.startswith(marker)]
    receipt = None; failure = None
    if timed_out:
        failure = "GODOT_PROCESS_TIMEOUT"
    elif code != 0:
        failure = f"GODOT_EXIT_NONZERO:{code}"
    elif len(hits) != 1:
        failure = f"GODOT_RECEIPT_MARKER_COUNT:{len(hits)}"
    else:
        try:
            receipt = json.loads(hits[0])
            validate_receipt(receipt, contract, selector, planner, role, run_id, pid)
        except (json.JSONDecodeError, ContractError, KeyError, TypeError, ValueError) as exc:
            receipt = None; failure = f"GODOT_RECEIPT_INVALID:{type(exc).__name__}:{exc}"
    run = {
        "role": role, "run_id": run_id, "process_id": pid, "exit_code": code,
        "stdout_sha256": sha_bytes(ob), "stderr_sha256": sha_bytes(eb),
        "receipt_sha256": sha_bytes(canonical_bytes(receipt)) if receipt is not None else None,
        "receipt": receipt
    }
    return run, failure


def candidate_hash_map(receipt: Mapping[str, Any]) -> dict[str, str]:
    return {str(x["field"]): str(x["value_stream_sha256"]) for x in receipt["candidate_field_observations"]}


def compare_selector_runs(selector: Mapping[str, Any], planners: list[dict[str, Any]], runs: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    reasons: list[str] = []
    if [p.get("role") for p in planners] != ROLES or [r.get("role") for r in runs] != ROLES:
        return {"status": "INCOMPLETE_VARIANT_MATRIX"}, ["VARIANT_MATRIX_INCOMPLETE"]
    receipts = [r.get("receipt") for r in runs]
    if any(not isinstance(x, dict) for x in receipts):
        return {"status": "MISSING_RUNTIME_RECEIPT"}, ["RUNTIME_RECEIPT_MISSING"]
    r0, r1, gameplay, music, editorial = receipts
    id0 = r0["identity"]; id1 = r1["identity"]
    probe0 = candidate_hash_map(r0); probe1 = candidate_hash_map(r1)
    same_probe = probe0 == probe1
    baseline_repeat = (
        planners[0]["request_hash"] == planners[1]["request_hash"]
        and planners[0]["plan_hash"] == planners[1]["plan_hash"]
        and planners[0]["editorial_hash"] == planners[1]["editorial_hash"]
        and planners[0].get("request_id") == planners[1].get("request_id") == f"C11D-V2B-{selector['challenge_id']}"
        and all(p.get("request_id") == f"C11D-V2B-{selector['challenge_id']}" for p in planners)
        and id0["projection_instance_identity_sha256"] == id1["projection_instance_identity_sha256"]
        and id0["safe_projection_state_sha256"] == id1["safe_projection_state_sha256"]
        and same_probe
        and runs[0]["process_id"] != runs[1]["process_id"]
        and runs[0]["run_id"] != runs[1]["run_id"]
    )
    if not baseline_repeat:
        reasons.append("BASELINE_REPEAT_IDENTITY_OR_STATE_MISMATCH")
    gameplay_changed = gameplay["identity"]["safe_projection_state_sha256"] != id0["safe_projection_state_sha256"]
    if not gameplay_changed:
        reasons.append("GAMEPLAY_SEED_DID_NOT_CHANGE_SAFE_STATE_HASH")
    music_unchanged = (
        music["identity"]["safe_projection_state_sha256"] == id0["safe_projection_state_sha256"]
        and candidate_hash_map(music) == probe0
        and music["simulation_input_sha256"] == r0["simulation_input_sha256"]
    )
    if not music_unchanged:
        reasons.append("MUSIC_SEED_CHANGED_SIMULATION_STATE_OR_CANDIDATE")
    editorial_unchanged = (
        editorial["identity"]["safe_projection_state_sha256"] == id0["safe_projection_state_sha256"]
        and candidate_hash_map(editorial) == probe0
        and editorial["simulation_input_sha256"] == r0["simulation_input_sha256"]
    )
    if not editorial_unchanged:
        reasons.append("EDITORIAL_MUTATION_CHANGED_SIMULATION_STATE_OR_CANDIDATE")
    if planners[2]["gameplay_seed"] == planners[0]["gameplay_seed"] or planners[2]["music_seed"] != planners[0]["music_seed"]:
        reasons.append("GAMEPLAY_VARIANT_DOMAIN_ISOLATION_FAILED")
    if planners[3]["music_seed"] == planners[0]["music_seed"] or planners[3]["gameplay_seed"] != planners[0]["gameplay_seed"]:
        reasons.append("MUSIC_VARIANT_DOMAIN_ISOLATION_FAILED")
    if planners[4]["editorial_hash"] == planners[0]["editorial_hash"] or planners[4]["gameplay_seed"] != planners[0]["gameplay_seed"] or planners[4]["music_seed"] != planners[0]["music_seed"]:
        reasons.append("EDITORIAL_VARIANT_IDENTITY_OR_DOMAIN_FAILED")
    for i in (2, 3, 4):
        if planners[i]["request_hash"] == planners[0]["request_hash"] or planners[i]["plan_hash"] == planners[0]["plan_hash"]:
            reasons.append(f"{ROLES[i]}_DID_NOT_CHANGE_CANONICAL_REQUEST_AND_PLAN_IDENTITY")
    probe_relations: dict[str, Any] = {}
    for field_name, base_hash in probe0.items():
        game_hash = candidate_hash_map(gameplay).get(field_name)
        music_hash = candidate_hash_map(music).get(field_name)
        editorial_hash = candidate_hash_map(editorial).get(field_name)
        if music_hash != base_hash:
            reasons.append(f"{field_name}_MUSIC_SEED_ORTHOGONALITY_FAILED")
        if editorial_hash != base_hash:
            reasons.append(f"{field_name}_EDITORIAL_ORTHOGONALITY_FAILED")
        if field_name == "target_x":
            gameplay_relation = game_hash == base_hash
            if not gameplay_relation:
                reasons.append("PILOT_TARGET_X_EXPECTED_INVARIANCE_FAILED")
        else:
            gameplay_relation = game_hash != base_hash
            if not gameplay_relation:
                reasons.append(f"{field_name}_GAMEPLAY_SEED_CANDIDATE_CHANGE_NOT_OBSERVED")
        probe_relations[field_name] = {
            "baseline_sha256": base_hash, "gameplay_variant_sha256": game_hash,
            "music_variant_sha256": music_hash, "editorial_variant_sha256": editorial_hash,
            "gameplay_relation_pass": gameplay_relation,
            "music_invariant_pass": music_hash == base_hash,
            "editorial_invariant_pass": editorial_hash == base_hash,
        }
    return {
        "baseline_repeat_agreement": baseline_repeat,
        "gameplay_seed_safe_state_changed": gameplay_changed,
        "music_seed_safe_state_and_candidates_invariant": music_unchanged,
        "editorial_safe_state_and_candidates_invariant": editorial_unchanged,
        "candidate_probe_relations": probe_relations,
        "status": "PASS" if not reasons else "BLOCKED",
    }, reasons


def blank_row(selector: Mapping[str, Any], status: str = "NOT_RUN_AFTER_FIRST_FAILURE", reason: str = "NOT_RUN_AFTER_FIRST_FAILURE") -> dict[str, Any]:
    return {
        "selector": {"challenge_id": selector.get("challenge_id", "UNKNOWN"), "mechanic": selector.get("mechanic", "UNKNOWN")},
        "status": status, "block_reasons": [reason], "planner_variants": [], "runtime_runs": [], "comparison": None
    }


def evidence_hashes(ev: Path) -> dict[str, str]:
    return {p.name: sha_file(p) for p in sorted(ev.iterdir()) if p.is_file() and p.name != "report.json"}


def validate_report(report: Any) -> None:
    fields = {"schema", "schema_version", "status", "runtime_contract_sha256", "design_contract_sha256", "frozen_manifest_sha256", "selector_count_expected", "selectors", "planner_invocations", "planner_invocations_expected", "godot_version_probe_invocations", "godot_runtime_process_invocations", "godot_runtime_processes_expected", "payload_materialized", "media_created", "approved_bindings", "approved_custom_data_bindings", "visual_seed_sensitivity", "governance_locks", "evidence"}
    exact(report, fields, "runtime report")
    if report["schema"] != REPORT_ID or report["schema_version"] != "1.0" or report["selector_count_expected"] != 9 or len(report["selectors"]) != 9:
        raise ContractError("runtime report identity/denominator mismatch")
    if report["planner_invocations_expected"] != 45 or report["godot_runtime_processes_expected"] != 45:
        raise ContractError("runtime report expected denominators mismatch")
    if report["payload_materialized"] is not False or report["media_created"] is not False or report["approved_bindings"] != 0 or report["approved_custom_data_bindings"] != 0:
        raise ContractError("runtime report claims prohibited side effect/approval")
    if report["governance_locks"] != GOVERNANCE:
        raise ContractError("runtime report governance locks changed")
    statuses = [row.get("status") for row in report["selectors"]]
    if any(not isinstance(row, dict) for row in report["selectors"]):
        raise ContractError("runtime report selector row malformed")
    if report["status"] == "PASS_SAFE_PROJECTION_SEED_SENSITIVITY":
        if statuses != ["ACCEPTED_SAFE_PROJECTION_RUNTIME"] * 9 or report["planner_invocations"] != 45 or report["godot_runtime_process_invocations"] != 45 or report["visual_seed_sensitivity"] != "ACCEPTED_BY_SAFE_PROJECTION_HASH":
            raise ContractError("runtime report claims PASS with incomplete matrix")
    elif report["status"] == "BLOCKED":
        if report["visual_seed_sensitivity"] not in ("BLOCKED", "NOT_TESTED"):
            raise ContractError("blocked report sensitivity marker inconsistent")
    else:
        raise ContractError("unknown top-level runtime report status")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--evidence-dir", required=True)
    ap.add_argument("--implementation-test-receipt", required=True)
    ap.add_argument("--contract-sha256", required=True)
    ap.add_argument("--godot", default=None)
    args = ap.parse_args()
    root = Path(args.repo_root).resolve(); ev = Path(args.evidence_dir).resolve(); receipt_path = Path(args.implementation_test_receipt).resolve()
    if not root.is_dir() or not (root / "project.godot").is_file():
        print("C11D_V2B_RUNTIME_RESULT=BLOCKED reason=INVALID_REPO_ROOT", file=sys.stderr); return 2
    if ev.exists() and any(ev.iterdir()):
        print("C11D_V2B_RUNTIME_RESULT=BLOCKED reason=EVIDENCE_DIR_NOT_EMPTY", file=sys.stderr); return 2
    ev.mkdir(parents=True, exist_ok=True)
    report_path = ev / "report.json"
    failure: str | None = None; contract: dict[str, Any] | None = None; design: dict[str, Any] | None = None; matrix: dict[str, Any] | None = None
    contract_sha = args.contract_sha256; pin_errors_before: list[str] = []; pin_errors_after: list[str] = []
    exe = None; version = ""; version_code = -1; version_out_sha = sha_bytes(b""); version_err_sha = sha_bytes(b"")
    planner_calls = 0; process_calls = 0; version_probes = 0; rows: list[dict[str, Any]] = []
    try:
        contract_path = safe_child(root, RUNTIME_CONTRACT_REL.as_posix())
        contract = load_json(contract_path, "runtime contract")
        actual_contract_sha = sha_file(contract_path)
        if not is_sha(contract_sha) or actual_contract_sha != contract_sha:
            raise ContractError("runtime contract SHA does not match caller pin")
        contract["_actual_sha256"] = actual_contract_sha
        public_contract = {k: v for k, v in contract.items() if k != "_actual_sha256"}
        validate_runtime_contract(public_contract, actual_contract_sha)
        impl = public_contract["implementation"]
        for rel, expected_sha, label in (
            (impl["harness_path"], impl["harness_sha256"], "runtime harness"),
            (impl["receipt_schema_path"], impl["receipt_schema_sha256"], "receipt schema"),
            (impl["report_schema_path"], impl["report_schema_sha256"], "report schema"),
            (impl["contract_schema_path"], impl["contract_schema_sha256"], "runtime contract schema"),
        ):
            p = safe_child(root, rel)
            if not p.is_file() or sha_file(p) != expected_sha:
                raise ContractError(f"{label} implementation pin mismatch")
        test_receipt = validate_implementation_test_receipt(root, receipt_path, actual_contract_sha, public_contract)
        design, matrix, pin_errors_before = load_upstream(root, public_contract)
        if pin_errors_before:
            failure = "SOURCE_PIN_RECONCILIATION_FAILED:" + pin_errors_before[0]
        if design is not None and len(design.get("selectors", [])) != 9:
            failure = failure or "DESIGN_SELECTOR_DENOMINATOR_INVALID"
        if design is not None and matrix is not None:
            if matrix.get("per_selector_invocations") != {"canonical_planner_invocations": 5, "godot_runtime_processes": 5} or matrix.get("whole_increment_invocations") != {"selector_count": 9, "canonical_planner_invocations": 45, "godot_runtime_processes": 45}:
                failure = failure or "SEED_MATRIX_DENOMINATOR_CHANGED"
        exe = resolve_godot(args.godot) if not failure else None
        if not failure and not exe:
            failure = "GODOT_EXECUTABLE_NOT_RESOLVED"
        if exe and not failure:
            version_probes = 1
            version, version_code, version_out_sha, version_err_sha = version_probe(exe)
            if version_code != 0 or "4.7.1" not in version or "mono" not in version.lower():
                failure = f"GODOT_4_7_1_MONO_REQUIRED:exit={version_code}:version={version}"
        if design is None or matrix is None or contract is None:
            raise ContractError("runtime preflight did not load all authority inputs")
        for selector in design["selectors"]:
            row = blank_row(selector)
            row["block_reasons"] = []
            if failure:
                if not rows:
                    row["status"] = "BLOCKED"; row["block_reasons"] = [failure]
                else:
                    row["status"] = "NOT_RUN_AFTER_FIRST_FAILURE"; row["block_reasons"] = ["NOT_RUN_AFTER_FIRST_FAILURE"]
                rows.append(row)
                break
            planners: list[dict[str, Any]] = []; runs: list[dict[str, Any]] = []
            source_seed = read_source_seed(root, selector)
            for role in ROLES:
                try:
                    preg = make_planner(root, selector, role, source_seed)
                    planner_calls += 1
                    planners.append(preg)
                    run, run_error = run_godot(exe, version, root, ev, actual_contract_sha, contract, selector, preg, role)
                    process_calls += 1
                    runs.append(run)
                    if run_error:
                        row["status"] = "BLOCKED"; row["block_reasons"] = [run_error]; failure = run_error
                        break
                except PlannerInvocationFailed as exc:
                    planner_calls += 1
                    row["status"] = "BLOCKED"; row["block_reasons"] = [f"CANONICAL_PLANNER_OR_ROUTE_BLOCKED:{exc}"]; failure = row["block_reasons"][0]
                    break
                except Exception as exc:
                    row["status"] = "BLOCKED"; row["block_reasons"] = [f"CANONICAL_SELECTION_OR_SETUP_BLOCKED:{type(exc).__name__}:{exc}"]; failure = row["block_reasons"][0]
                    break
            row["planner_variants"] = planners
            row["runtime_runs"] = runs
            if not failure:
                comparison, reasons = compare_selector_runs(selector, planners, runs)
                row["comparison"] = comparison
                if reasons:
                    row["status"] = "BLOCKED"; row["block_reasons"] = reasons; failure = reasons[0]
                else:
                    row["status"] = "ACCEPTED_SAFE_PROJECTION_RUNTIME"; row["block_reasons"] = []
            rows.append(row)
            if failure:
                break
        # Keep the strict 9-selector report denominator after any first failure.
        existing = {r["selector"]["challenge_id"] for r in rows}
        for selector in design["selectors"]:
            if selector["challenge_id"] not in existing:
                rows.append(blank_row(selector))
        rows.sort(key=lambda r: IDS.index(r["selector"]["challenge_id"]) if r["selector"]["challenge_id"] in IDS else 999)
        pin_errors_after = load_upstream(root, public_contract)[2]
        if pin_errors_after and not failure:
            failure = "SOURCE_PIN_DRIFT_AFTER_RUNTIME:" + pin_errors_after[0]
            for row in rows:
                if row["status"] == "ACCEPTED_SAFE_PROJECTION_RUNTIME":
                    row["status"] = "BLOCKED"; row["block_reasons"] = [failure]; row["comparison"] = row.get("comparison")
        all_accepted = len(rows) == 9 and all(r["status"] == "ACCEPTED_SAFE_PROJECTION_RUNTIME" for r in rows) and not failure and not pin_errors_after
        status = "PASS_SAFE_PROJECTION_SEED_SENSITIVITY" if all_accepted else "BLOCKED"
        report = {
            "schema": REPORT_ID, "schema_version": "1.0", "status": status,
            "runtime_contract_sha256": actual_contract_sha, "design_contract_sha256": DESIGN_SHA,
            "frozen_manifest_sha256": FROZEN_SHA, "selector_count_expected": 9, "selectors": rows,
            "planner_invocations": planner_calls, "planner_invocations_expected": 45,
            "godot_version_probe_invocations": version_probes, "godot_runtime_process_invocations": process_calls,
            "godot_runtime_processes_expected": 45, "payload_materialized": False, "media_created": False,
            "approved_bindings": 0, "approved_custom_data_bindings": 0,
            "visual_seed_sensitivity": "ACCEPTED_BY_SAFE_PROJECTION_HASH" if all_accepted else ("NOT_TESTED" if process_calls == 0 else "BLOCKED"),
            "governance_locks": GOVERNANCE,
            "evidence": {
                "directory": str(ev), "godot_executable": exe, "godot_version": version,
                "godot_version_probe_exit_code": version_code, "godot_version_stdout_sha256": version_out_sha,
                "godot_version_stderr_sha256": version_err_sha, "implementation_test_receipt": str(receipt_path),
                "implementation_test_receipt_sha256": sha_file(receipt_path), "source_pin_errors_before_runtime": pin_errors_before,
                "source_pin_errors_after_runtime": pin_errors_after, "failure": failure,
                "evidence_file_sha256": evidence_hashes(ev),
                "scope_note": "In-memory source-state observation only; no payload/media/renderer input; candidate probes are hash-only and unapproved."
            }
        }
        validate_report(report)
    except Exception as exc:
        message = f"{type(exc).__name__}:{exc}"
        print("C11D_V2B_DIAGNOSTIC=" + message, file=sys.stderr)
        for selector in ((design or {}).get("selectors", [])):
            if selector.get("challenge_id") not in {r.get("selector", {}).get("challenge_id") for r in rows}:
                rows.append(blank_row(selector, "BLOCKED", "PREFLIGHT_OR_REPORT_FAILED:" + message))
        if len(rows) != 9:
            rows = [blank_row({"challenge_id": cid, "mechanic": "unknown"}, "BLOCKED", "PREFLIGHT_OR_REPORT_FAILED:" + message) for cid in IDS]
        rows.sort(key=lambda r: IDS.index(r["selector"]["challenge_id"]) if r["selector"]["challenge_id"] in IDS else 999)
        report = {
            "schema": REPORT_ID, "schema_version": "1.0", "status": "BLOCKED",
            "runtime_contract_sha256": contract_sha if is_sha(contract_sha) else "0"*64,
            "design_contract_sha256": DESIGN_SHA, "frozen_manifest_sha256": FROZEN_SHA,
            "selector_count_expected": 9, "selectors": rows, "planner_invocations": planner_calls,
            "planner_invocations_expected": 45, "godot_version_probe_invocations": version_probes,
            "godot_runtime_process_invocations": process_calls, "godot_runtime_processes_expected": 45,
            "payload_materialized": False, "media_created": False, "approved_bindings": 0,
            "approved_custom_data_bindings": 0, "visual_seed_sensitivity": "NOT_TESTED" if process_calls == 0 else "BLOCKED",
            "governance_locks": GOVERNANCE,
            "evidence": {"directory": str(ev), "godot_executable": exe, "godot_version": version,
                         "source_pin_errors_before_runtime": pin_errors_before, "source_pin_errors_after_runtime": pin_errors_after,
                         "failure": message, "evidence_file_sha256": evidence_hashes(ev),
                         "scope_note": "Blocked; no acceptance inferred."}
        }
    report_sha = dump_json(report_path, report)
    accepted = sum(r["status"] == "ACCEPTED_SAFE_PROJECTION_RUNTIME" for r in report["selectors"])
    print("C11D_V2B_RUNTIME_RESULT=" + report["status"])
    print("C11D_V2B_RUNTIME_REPORT=" + str(report_path))
    print("C11D_V2B_RUNTIME_REPORT_SHA256=" + report_sha)
    print(f"C11D_V2B_PLANNER_INVOCATIONS={planner_calls}/45")
    print(f"C11D_V2B_GODOT_RUNTIME_PROCESSES={process_calls}/45")
    print(f"C11D_V2B_SELECTORS={accepted}/9")
    print("C11D_V2B_GODOT_VERSION=" + version)
    print("C11D_V2B_GOVERNANCE=renderer=OFF;media_created=false;payload_materialized=false;approved_bindings=0;candidate_input_admissible=false;D4.8=BLOCKED;D9.10=PREPARE_ONLY;D10=BLOCKED_FOR_PROMOTION;release_authority=NONE")
    return 0 if report["status"] == "PASS_SAFE_PROJECTION_SEED_SENSITIVITY" else 1

if __name__ == "__main__":
    raise SystemExit(main())
