#!/usr/bin/env python3
"""C11-E Option C: D-owned post-composition handoff contract (prepare-only).

This module validates the accepted R1P archive and its embedded D9.9/D9.10
parent records, then creates a non-dispatchable 27-selector handoff manifest.
It does not launch C11-C, Godot, FFmpeg/FFprobe, a compositor, D3, audio or mux.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

MODULE_SCHEMA = "C11E-E-OPTION-C-POSTCOMPOSITION-HANDOFF-V1"
REPORT_SCHEMA = "C11E-E-OPTION-C-POSTCOMPOSITION-CONTRACT-REPORT-V1"
R1P_RUN_ID = "E4B_R1P_20261107_032743_5F75045C"
R1P_ZIP_SHA256 = "d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52"
FROZEN_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
R1P_REPORT_SHA256 = "9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41"
R1P_PARENT_BINDINGS_SHA256 = "460165c92f3afaebc023a49ab5e0fdb86f7fe4c8133032bb54f6bef67ef0911a"
R1P_RECEIPT_HASH_SET_SHA256 = "523add74c2607d6b5c85fb5f9b270fa5fbca800d3dd05d05131482b044e1a42d"
COMPOSITION_PROPOSAL_SHA256 = "9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da"
OPTION_C_DECISION_REL = Path("definitions/c11d/production/C11E_OPTION_C_D_POSTCOMPOSITION_DECISION_V1.json")
OPTION_C_BOUNDARY_REL = Path("definitions/c11d/production/C11E_OPTION_C_D_POSTCOMPOSITION_BOUNDARY_V1.json")
R1V_POLICY_REL = Path("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V1.json")
COMPOSITION_PROPOSAL_REL = Path("definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
EXPECTED_PINS = {
    "option_c_decision": (OPTION_C_DECISION_REL, "22cec26baecfb6018a814750cc781143f5fa13f897d3dce708f6e9e074f669ac"),
    "option_c_boundary": (OPTION_C_BOUNDARY_REL, "795be1da157dd07fd4992d3ec6d7cf091a015eed72d16d86df13085db296098b"),
    "r1v_qualification_policy": (R1V_POLICY_REL, "e0f9693584e5b7d42c6d67cf2c806ff691dec4644738458bd405cdcbd5d9c4db"),
}
EXPECTED_PILOTS = [
    {"receipt_index": 6, "family_id": "c11c_fractal_bloom_v1", "grammar_id": "radial_bloom", "grammar_index": 0, "gameplay_seed": 100006, "duration_seconds": 22.0, "fps": 30, "frame_count": 660},
    {"receipt_index": 1, "family_id": "c11c_geometric_waves_v1", "grammar_id": "harmonic_membrane", "grammar_index": 0, "gameplay_seed": 100001, "duration_seconds": 23.0, "fps": 30, "frame_count": 690},
    {"receipt_index": 21, "family_id": "c11c_invisible_forces_v1", "grammar_id": "dipole_field", "grammar_index": 0, "gameplay_seed": 100021, "duration_seconds": 22.0, "fps": 30, "frame_count": 660},
    {"receipt_index": 16, "family_id": "c11c_living_particles_v1", "grammar_id": "swarm", "grammar_index": 0, "gameplay_seed": 100016, "duration_seconds": 20.0, "fps": 30, "frame_count": 600},
    {"receipt_index": 11, "family_id": "c11c_sacred_symmetry_v1", "grammar_id": "astrolabe", "grammar_index": 0, "gameplay_seed": 100011, "duration_seconds": 23.0, "fps": 30, "frame_count": 690},
]
EXPECTED_FAMILY_COUNTS = {
    "c11c_fractal_bloom_v1": 5,
    "c11c_geometric_waves_v1": 5,
    "c11c_invisible_forces_v1": 7,
    "c11c_living_particles_v1": 5,
    "c11c_sacred_symmetry_v1": 5,
}
FORBIDDEN_TRUE_FLAGS = (
    "source_launcher_invoked", "renderer_dispatch_invoked", "compositor_invoked",
    "ffmpeg_invoked", "ffprobe_invoked", "godot_invoked", "d3_audio_invoked",
    "mux_invoked", "media_created", "c11c_source_mutation",
)


class OptionCContractError(ValueError):
    """Raised when Option C lineage or a non-dispatch boundary is violated."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha256_bytes(raw)


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise OptionCContractError(message)


def _load_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8-sig"))
    except Exception as exc:
        raise OptionCContractError(f"Cannot parse {label}: {exc}") from exc
    _expect(isinstance(value, dict), f"{label} must be a JSON object")
    return value


def _load_project_json(root: Path, relative: Path) -> dict[str, Any]:
    path = root / relative
    _expect(path.is_file(), f"Required project file missing: {relative.as_posix()}")
    return _load_json_bytes(path.read_bytes(), relative.as_posix())


def validate_project_pins(root: Path, report_source_pins: Mapping[str, Any]) -> dict[str, str]:
    """Revalidate the 30 R1P pins against the active checkout and this overlay."""
    _expect(isinstance(report_source_pins, Mapping) and len(report_source_pins) == 30,
            "R1P report must contain exactly 30 source pins")
    observed: dict[str, str] = {}
    for raw_rel, record in sorted(report_source_pins.items()):
        rel = PurePosixPath(str(raw_rel))
        _expect(not rel.is_absolute() and ".." not in rel.parts, f"Unsafe source pin path: {raw_rel}")
        _expect(isinstance(record, Mapping), f"Malformed source pin: {raw_rel}")
        expected_bytes = record.get("bytes")
        _expect(isinstance(expected_bytes, int) and expected_bytes >= 0, f"Invalid source pin byte length: {raw_rel}")
        expected = str(record.get("sha256", ""))
        _expect(bool(re.fullmatch(r"[0-9a-f]{64}", expected)), f"Invalid source pin SHA-256: {raw_rel}")
        path = root.joinpath(*rel.parts)
        _expect(path.is_file(), f"Pinned active-checkout source missing: {raw_rel}")
        actual_bytes = path.stat().st_size
        _expect(actual_bytes == expected_bytes, f"Active-checkout source byte-length mismatch: {raw_rel}: {actual_bytes}")
        actual = sha256_file(path)
        _expect(actual == expected, f"Active-checkout source pin mismatch: {raw_rel}: {actual}")
        observed[str(raw_rel)] = actual

    for label, (relative, expected) in EXPECTED_PINS.items():
        path = root / relative
        _expect(path.is_file(), f"Option C policy file missing: {relative.as_posix()}")
        actual = sha256_file(path)
        _expect(actual == expected, f"Option C fixed pin mismatch ({label}): {actual}")
        observed[f"[option-c]{relative.as_posix()}"] = actual
    return observed


def _parse_sidecar(raw: bytes, expected_name: str) -> str:
    try:
        line = raw.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise OptionCContractError(f"Receipt sidecar is not ASCII: {expected_name}") from exc
    match = re.fullmatch(r"([0-9a-f]{64})\s+\*?" + re.escape(expected_name), line)
    _expect(match is not None, f"Malformed receipt SHA-256 sidecar: {expected_name}")
    return match.group(1)


def _validate_receipt_and_parent(receipt: Mapping[str, Any], parent: Mapping[str, Any], report: Mapping[str, Any]) -> dict[str, Any]:
    _expect(receipt.get("schema") == "C11E-E4B-R1P-LOOP-FAMILY-PARAMETER-RECEIPT-V1", "Unexpected R1P receipt schema")
    _expect(receipt.get("status") == "PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT", "R1P receipt is not a passing parameter-only receipt")
    _expect(receipt.get("run_id") == R1P_RUN_ID, "R1P run identity mismatch")
    _expect(receipt.get("source_pins") == report.get("source_pins"), "R1P receipt source pin set differs from run report")
    case_source_pins = receipt.get("case_source_pins", {})
    _expect(isinstance(case_source_pins, Mapping), "R1P per-case source pins missing")
    launcher_pin = case_source_pins.get("launcher", {})
    prototype_pin = case_source_pins.get("prototype", {})
    _expect(isinstance(launcher_pin, Mapping) and isinstance(prototype_pin, Mapping), "R1P per-case launcher/prototype pins malformed")
    launcher_path = launcher_pin.get("path")
    prototype_path = prototype_pin.get("path")
    source_pin_set = report.get("source_pins", {})
    _expect(source_pin_set.get(launcher_path, {}).get("sha256") == launcher_pin.get("sha256"), "R1P per-case launcher pin not bound to source manifest")
    _expect(source_pin_set.get(prototype_path, {}).get("sha256") == prototype_pin.get("prototype_sha256"), "R1P per-case prototype pin not bound to source manifest")
    _expect(receipt.get("governance", {}).get("renderer") == "OFF", "R1P receipt renderer lock mismatch")
    _expect(receipt.get("governance", {}).get("D4.8") == "BLOCKED", "R1P receipt D4.8 lock mismatch")
    _expect(receipt.get("governance", {}).get("D9.10") == "PREPARE_ONLY", "R1P receipt D9.10 lock mismatch")
    _expect(receipt.get("governance", {}).get("release_authority") == "NONE", "R1P receipt release authority mismatch")
    _expect(receipt.get("materialization", {}).get("parameter_payload_materialized_in_memory") is True, "R1P parameter payload missing")
    _expect(receipt.get("materialization", {}).get("deterministic_repeat_pass") is True, "R1P deterministic repeat did not pass")
    _expect(receipt.get("payload_sha256") == receipt.get("repeat_payload_sha256"), "R1P primary/repeat payload hashes differ")
    _expect(bool(re.fullmatch(r"[0-9a-f]{64}", str(receipt.get("payload_sha256", "")))), "R1P payload SHA-256 is malformed")
    visual_parameters = receipt.get("visual_parameters")
    visual_parameters_canonical_json = receipt.get("visual_parameters_canonical_json")
    _expect(isinstance(visual_parameters, Mapping) and isinstance(visual_parameters_canonical_json, str), "R1P visual parameter canonical payload missing")
    canonical_parameters = json.dumps(visual_parameters, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    _expect(visual_parameters_canonical_json == canonical_parameters, "R1P visual parameter canonical JSON differs from parsed payload")
    _expect(receipt.get("visual_parameters_sha256") == sha256_bytes(canonical_parameters.encode("utf-8")), "R1P visual parameter SHA-256 mismatch")
    for key in ("launcher_invoked", "renderer_instantiated", "frame_buffers_materialized", "frame_inventory_materialized", "pixel_payload_materialized", "audio_or_d3_invoked", "ffmpeg_invoked", "media_created", "renderer_native_input_emitted"):
        _expect(receipt.get("materialization", {}).get(key) is False, f"R1P must remain parameter-only: {key}")

    case_id = str(receipt.get("case_id", ""))
    _expect(parent.get("case_id") == case_id, "R1P receipt and parent-binding case IDs differ")
    identity = receipt.get("request_identity")
    _expect(isinstance(identity, Mapping), "R1P request_identity missing")
    _expect(parent.get("request_identity") == identity, "R1P receipt and parent request identities differ")

    d99 = parent.get("d9_9_result")
    bridge = parent.get("d9_10_bridge_record")
    stage = parent.get("d_only_family_stage_contract")
    _expect(isinstance(d99, Mapping) and isinstance(bridge, Mapping) and isinstance(stage, Mapping), "R1P D9.9/D9.10/family-stage parent records are incomplete")
    request = d99.get("canonical_request")
    plan = d99.get("plan")
    _expect(isinstance(request, Mapping) and isinstance(plan, Mapping), "D9.9 canonical request/plan missing")
    _expect(d99.get("status") == "PLANNED", "D9.9 parent is not PLANNED")
    _expect(d99.get("request_hash") == canonical_sha256(request), "D9.9 request hash mismatch")
    _expect(d99.get("plan_hash") == canonical_sha256(plan), "D9.9 plan hash mismatch")
    _expect(d99.get("editorial_hash") == canonical_sha256({"selection": plan.get("selection"), "editorial": plan.get("editorial")}), "D9.9 editorial hash mismatch")
    _expect(plan.get("plan_kind") == "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY", "D9.9 plan kind exceeds Loop planning scope")
    _expect(plan.get("renderer_activation") is False and plan.get("production_execution") is False, "D9.9 parent attempts renderer/production activation")
    _expect(plan.get("d4_8") == "BLOCKED" and plan.get("release_authority") == "NONE", "D9.9 governance boundary mismatch")

    _expect(bridge.get("schema") == "C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-PLAN-V1", "D9.10 bridge schema mismatch")
    _expect(bridge.get("status") == "PLANNING_ONLY_NOT_RENDERABLE", "D9.10 bridge must remain planning-only")
    _expect(bridge.get("record_hash") == canonical_sha256({k: v for k, v in bridge.items() if k != "record_hash"}), "D9.10 bridge record hash mismatch")
    for key in ("request_hash", "plan_hash", "editorial_hash"):
        _expect(bridge.get("identity", {}).get(key) == d99.get(key), f"D9.10 to D9.9 parent identity mismatch: {key}")
    _expect(bridge.get("selection") == plan.get("selection"), "D9.10 content selection does not match D9.9")
    _expect(bridge.get("renderer_input_emitted") is False and bridge.get("renderer_adapter_invoked") is False and bridge.get("media_output_created") is False, "D9.10 bridge crossed prepare-only boundary")
    _expect(bridge.get("governance", {}).get("d4_8") == "BLOCKED" and bridge.get("release_authority") == "NONE", "D9.10 governance boundary mismatch")

    _expect(stage.get("schema") == "C11E-E4B-LOOP-FAMILY-STAGE-CONTRACT-V1", "Family-stage contract schema mismatch")
    _expect(stage.get("status") == "FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE", "Family-stage contract is not non-dispatchable")
    _expect(stage.get("contract_sha256") == canonical_sha256({k: v for k, v in stage.items() if k != "contract_sha256"}), "Family-stage contract digest mismatch")
    stage_id = stage.get("request_identity", {})
    for key, identity_key in (("request_hash", "request_hash"), ("plan_hash", "plan_hash"), ("editorial_hash", "editorial_hash"), ("bridge_record_hash", "bridge_record_hash"), ("d_only_adapter_envelope_hash", "adapter_envelope_hash")):
        _expect(stage_id.get(key) == identity.get(identity_key), f"Family-stage parent identity mismatch: {key}")
    _expect(stage_id.get("request_id") == case_id, "Family-stage request ID mismatch")
    for key in ("launcher_execution", "music_seed_passed_to_visual_launcher"):
        _expect(stage.get("family_visual_stage", {}).get(key) is False, f"Family stage unexpectedly executed or shared a seed: {key}")
    for key in ("launcher_invoked", "godot_invoked", "ffmpeg_invoked", "renderer_dispatch_invoked", "renderer_native_input_emitted", "media_created", "c11c_source_mutation"):
        _expect(stage.get("governance", {}).get(key) is False, f"Family-stage governance lock mismatch: {key}")
    _expect(stage.get("governance", {}).get("d4_8") == "BLOCKED" and stage.get("governance", {}).get("d9_10") == "PREPARE_ONLY", "Family-stage D4.8/D9.10 gate mismatch")

    selection = receipt.get("selection", {})
    plan_selection = plan.get("selection", {})
    _expect(selection.get("content_type") == "visual_loops", "Option C handoff currently accepts Visual Loops only")
    _expect(selection.get("family_id") == plan_selection.get("family_id"), "Receipt/D9.9 family identity mismatch")
    _expect(selection.get("grammar_id") == plan_selection.get("subtype_id"), "Receipt/D9.9 grammar identity mismatch")
    _expect(isinstance(selection.get("grammar_index"), int) and selection.get("grammar_index") >= 0,
            "R1P grammar_index must be a non-negative integer")

    seed = receipt.get("seed_domains", {})
    _expect(seed.get("visual_parameters_use") == "request.seed" and seed.get("music_seed_consumed_by_visual_parameters") is False, "R1P seed-domain contract mismatch")
    gameplay_seed = seed.get("gameplay_seed")
    music_seed = seed.get("music_seed")
    _expect(isinstance(gameplay_seed, int) and isinstance(music_seed, int) and gameplay_seed != music_seed, "Gameplay/music seed separation is invalid")
    _expect(request.get("seed") == gameplay_seed and request.get("music_seed") == music_seed, "R1P/D9.9 seed identity mismatch")
    _expect(bridge.get("seed_contract", {}).get("gameplay_seed") == gameplay_seed and bridge.get("seed_contract", {}).get("music_seed") == music_seed, "D9.10 seed identity mismatch")

    timing = receipt.get("timing", {})
    _expect(isinstance(timing.get("duration_seconds"), (int, float)) and timing.get("fps") == 30, "R1P timing descriptor invalid")
    _expect(timing.get("frame_count") == int(float(timing["duration_seconds"]) * int(timing["fps"])), "R1P parameter timing descriptor internally inconsistent")
    _expect(stage.get("composition", {}).get("source_frame_count_source") == "REQUEST_SCOPED_MATERIALIZED_C11C_PAYLOAD_ONLY", "R1P family composition source-frame count provenance drift")
    _expect(stage.get("composition", {}).get("frame_order") == "IDENTITY_NO_RESAMPLING", "R1P proposed frame order contract drift")
    _expect(stage.get("composition", {}).get("source_frame_transform", {}).get("cropping") is False, "R1P composition proposal allows cropping")
    _expect(stage.get("composition", {}).get("source_frame_transform", {}).get("nonuniform_stretch") is False, "R1P composition proposal allows nonuniform stretch")
    _expect(stage.get("composition", {}).get("source_frame_transform", {}).get("temporal_resampling") is False, "R1P composition proposal allows temporal resampling")
    _expect(stage.get("composition", {}).get("source_frame_transform", {}).get("source_frame_count_mutation") is False, "R1P composition proposal permits frame count mutation")

    _expect(identity.get("request_hash") == d99.get("request_hash"), "R1P request_hash does not match D9.9")
    _expect(identity.get("plan_hash") == d99.get("plan_hash"), "R1P plan_hash does not match D9.9")
    _expect(identity.get("editorial_hash") == d99.get("editorial_hash"), "R1P editorial_hash does not match D9.9")
    _expect(identity.get("bridge_record_hash") == bridge.get("record_hash"), "R1P bridge hash does not match D9.10")
    _expect(identity.get("family_stage_contract_sha256") == stage.get("contract_sha256"), "R1P family-stage contract hash mismatch")

    return {
        "request_id": case_id,
        "receipt_index": int(receipt.get("receipt_index", -1)),
        "receipt_sha256": str(receipt.get("receipt_sha256", "")),
        "payload_sha256": str(receipt.get("payload_sha256", "")),
        "repeat_payload_sha256": str(receipt.get("repeat_payload_sha256", "")),
        "request_hash": str(identity.get("request_hash", "")),
        "editorial_hash": str(identity.get("editorial_hash", "")),
        "plan_hash": str(identity.get("plan_hash", "")),
        "d9_10_bridge_record_hash": str(bridge.get("record_hash", "")),
        "d_only_adapter_envelope_hash": str(identity.get("adapter_envelope_hash", "")),
        "family_stage_contract_sha256": str(stage.get("contract_sha256", "")),
        "content_type": "visual_loops",
        "family_id": str(selection.get("family_id", "")),
        "grammar_id": str(selection.get("grammar_id", "")),
        "grammar_index": int(selection.get("grammar_index", -1)),
        "gameplay_seed": gameplay_seed,
        "music_seed_lineage_only": music_seed,
        "duration_seconds_descriptor_only": float(timing["duration_seconds"]),
        "fps_descriptor_only": int(timing["fps"]),
        "expected_frame_count_consistency_only": int(timing["frame_count"]),
        "visual_parameters_sha256": str(receipt.get("visual_parameters_sha256", "")),
        "editorial_values": dict(plan.get("editorial", {})),
        "composition_policy_state": str(stage.get("composition", {}).get("layout_measurement", "UNKNOWN")),
    }


def validate_option_c_boundary(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    decision = _load_project_json(root, OPTION_C_DECISION_REL)
    boundary = _load_project_json(root, OPTION_C_BOUNDARY_REL)
    policy = _load_project_json(root, R1V_POLICY_REL)
    _expect(decision.get("decision_state") == "OPERATOR_APPROVED_OPTION_C", "Option C operator decision is not recorded as approved")
    _expect(decision.get("operator_decision", {}).get("selected_option") == "C", "Only Option C is accepted by this handoff contract")
    _expect(decision.get("approval_boundary", {}).get("architecture_choice_approved") is True, "Option C architecture decision approval missing")
    _expect(decision.get("approval_boundary", {}).get("r1v_physical_execution_authorized") is False, "Option C decision must not authorize physical R1V")
    _expect(boundary.get("schema") == "C11E-E-OPTION-C-D-POSTCOMPOSITION-BOUNDARY-V1", "Option C boundary schema mismatch")
    _expect(boundary.get("status") == "PREPARE_ONLY_NOT_DISPATCHABLE", "Option C boundary must be prepare-only")
    _expect(boundary.get("layout_policy", {}).get("proposal_status") == "PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT", "Loop layout proposal must remain unapproved")
    _expect(boundary.get("layout_policy", {}).get("executable_geometry_approved") is False, "Loop layout geometry must remain unapproved")
    _expect(boundary.get("hard_locks", {}).get("renderer_dispatch_invoked") is False, "Option C boundary renderer lock mismatch")
    _expect(boundary.get("hard_locks", {}).get("media_created") is False, "Option C boundary media lock mismatch")
    _expect(boundary.get("hard_locks", {}).get("d4_8") == "BLOCKED", "Option C boundary D4.8 lock mismatch")
    _expect(boundary.get("hard_locks", {}).get("release_authority") == "NONE", "Option C release authority mismatch")

    _expect(policy.get("schema") == "C11E-D4.8-R1V-QUALIFICATION-ONLY-POLICY-V1", "R1V qualification policy schema mismatch")
    _expect(policy.get("status") == "PROPOSED_NOT_APPROVED" and policy.get("execution_authorized") is False, "R1V qualification policy is not safely pending approval")
    _expect(policy.get("approval", {}).get("policy_author") == "PENDING_EXPLICIT_ASSIGNMENT", "R1V policy author must remain unassigned")
    _expect(policy.get("approval", {}).get("independent_reviewer") == "PENDING_EXPLICIT_ASSIGNMENT", "R1V independent reviewer must remain unassigned")
    _expect(policy.get("approval", {}).get("operator_approver") == "PENDING_EXPLICIT_APPROVAL", "R1V operator approval must remain pending")
    _expect(policy.get("approval", {}).get("approval_timestamp") is None and policy.get("approval", {}).get("approval_record_sha256") is None, "R1V policy cannot contain fabricated approval evidence")
    _expect(len(policy.get("selectors", [])) == 5 and policy.get("scope", {}).get("total_launcher_invocations") == 10, "R1V policy must be limited to five selectors and two repeats")
    _expect(policy.get("scope", {}).get("music_seed_passed_to_visual_launcher") is False, "R1V policy must not pass music seed to visual launcher")
    for key, value in policy.get("forbidden", {}).items():
        _expect(value is True, f"R1V forbidden operation is not fail-closed: {key}")
    _expect(policy.get("governance", {}).get("renderer") == "OFF" and policy.get("governance", {}).get("d4_8") == "BLOCKED", "R1V policy governance locks mismatch")
    return decision, boundary, policy


def validate_r1p_archive(root: Path, archive_path: Path, verify_live_pins: bool = True) -> dict[str, Any]:
    _expect(archive_path.is_file(), f"Recovered R1P archive missing: {archive_path}")
    archive_sha = sha256_file(archive_path)
    _expect(archive_sha == R1P_ZIP_SHA256, f"Recovered R1P ZIP SHA-256 mismatch: {archive_sha}")
    try:
        archive = zipfile.ZipFile(archive_path, "r")
    except Exception as exc:
        raise OptionCContractError(f"Cannot open recovered R1P ZIP: {exc}") from exc
    with archive:
        _expect(archive.testzip() is None, "Recovered R1P ZIP CRC failure")
        names = archive.namelist()
        _expect(len(names) == 72, f"Recovered R1P ZIP member count mismatch: {len(names)}")
        _expect(len(names) == len(set(names)), "Recovered R1P ZIP contains duplicate member names")
        _expect(all("\\" not in name for name in names), "Recovered R1P ZIP contains Windows backslash paths")
        _expect(all(not PurePosixPath(name).is_absolute() and ".." not in PurePosixPath(name).parts for name in names), "Recovered R1P ZIP contains an unsafe member path")
        receipt_names = sorted(name for name in names if re.fullmatch(r"receipts/\d{2}_E4B_R1P_20261107_032743_5F75045C_\d{2}\.json", name))
        sidecar_names = sorted(name for name in names if re.fullmatch(r"receipts/\d{2}_E4B_R1P_20261107_032743_5F75045C_\d{2}\.json\.sha256", name))
        receipt_entries = [name for name in names if name.startswith("receipts/")]
        _expect(len(receipt_names) == 27 and len(sidecar_names) == 27 and len(receipt_entries) == 54, "Recovered R1P archive must contain only 27 receipts and 27 sidecars")
        _expect("r1p_report.json" in names and "parent_bindings.json" in names, "Recovered R1P report/parent-bindings missing")
        report_raw = archive.read("r1p_report.json")
        report = _load_json_bytes(report_raw, "r1p_report.json")
        _expect(_parse_sidecar(archive.read("r1p_report.sha256"), "r1p_report.json") == R1P_REPORT_SHA256,
                "R1P report sidecar digest mismatch")
        _expect(report.get("report_sha256") == canonical_sha256({k: v for k, v in report.items() if k != "report_sha256"}),
                "R1P canonical report self-digest mismatch")
        parent_raw = archive.read("parent_bindings.json")
        parents = _load_json_bytes(parent_raw, "parent_bindings.json")
        _expect(report.get("schema") == "C11E-E4B-R1P-LOOP-PARAMETER-PAYLOAD-RUN-V1", "R1P report schema mismatch")
        _expect(report.get("status") == "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27", "R1P report status is not passing")
        _expect(report.get("run_id") == R1P_RUN_ID and report.get("case_count") == 27 and report.get("receipt_count") == 27, "R1P report identity/count mismatch")
        _expect(report.get("scope") == "REQUEST_SCOPED_C11C_FAMILY_PARAMETER_PAYLOADS_ONLY", "R1P report scope widened unexpectedly")
        _expect(report.get("report_sha256") == R1P_REPORT_SHA256, "R1P canonical report hash pin mismatch")
        _expect(parents.get("schema") == "C11E-E4B-R1P-PARENT-BINDINGS-V1" and parents.get("run_id") == R1P_RUN_ID, "R1P parent-bindings schema/run mismatch")
        _expect(sha256_bytes(parent_raw) == R1P_PARENT_BINDINGS_SHA256, "R1P parent-bindings file SHA-256 mismatch")
        _expect(report.get("parent_bindings_sha256") == R1P_PARENT_BINDINGS_SHA256, "R1P report parent-bindings hash mismatch")
        _expect(report.get("receipt_hash_set_sha256") == R1P_RECEIPT_HASH_SET_SHA256, "R1P receipt hash-set digest mismatch")
        _expect(report.get("source_manifest_sha256") == "bb5b101492d18ee6c27a649874ffac75aa5dcb2de44cbdc5718902b4cfc6e441", "R1P source manifest digest mismatch")
        _expect(report.get("governance", {}).get("renderer") == "OFF" and report.get("governance", {}).get("D4.8") == "BLOCKED", "R1P report governance lock mismatch")
        _expect(len(parents.get("cases", [])) == 27, "R1P parent-binding case count mismatch")

        prepare_report = _load_json_bytes(archive.read("prepare_report.json"), "prepare_report.json")
        _expect(prepare_report.get("status") == "PASS_D9_9_D9_10_PARENT_PREPARATION_27_OF_27", "R1P parent-preparation report status mismatch")
        _expect(prepare_report.get("case_count") == 27 and prepare_report.get("explicit_selector_count") == 27 and prepare_report.get("family_count") == 5, "R1P parent-preparation report counts mismatch")
        _expect(prepare_report.get("parent_bindings_sha256") == R1P_PARENT_BINDINGS_SHA256, "R1P prepare report parent-binding digest mismatch")
        godot_input_raw = archive.read("godot_input.json")
        _expect(sha256_bytes(godot_input_raw) == prepare_report.get("godot_input_sha256"), "R1P Godot input digest mismatch")
        godot_input = _load_json_bytes(godot_input_raw, "godot_input.json")
        godot_cases = godot_input.get("cases", [])
        _expect(len(godot_cases) == 27, "R1P Godot input must contain 27 parameter cases")
        godot_case_by_id = {str(item.get("case_id")): item for item in godot_cases}
        _expect(len(godot_case_by_id) == 27, "R1P Godot input case IDs are not unique")
        expected_request_ids = [f"{R1P_RUN_ID}_{index:02d}" for index in range(1, 28)]
        _expect(prepare_report.get("request_ids") == expected_request_ids, "R1P prepare report request identity order mismatch")
        _expect(prepare_report.get("governance", {}).get("launcher_invoked") is False and prepare_report.get("governance", {}).get("media_created") is False and prepare_report.get("governance", {}).get("renderer_dispatch_invoked") is False, "R1P prepare report crossed its no-launch boundary")

        process_evidence = report.get("process_evidence", {})
        process_log_map = {
            "python_prepare_stdout_sha256": "python_prepare_stdout.log",
            "python_prepare_stderr_sha256": "python_prepare_stderr.log",
            "godot_stdout_sha256": "godot_stdout.log",
            "godot_stderr_sha256": "godot_stderr.log",
        }
        process_log_validations = 0
        for hash_key, log_name in process_log_map.items():
            _expect(log_name in names, f"R1P process log missing: {log_name}")
            actual_log_sha = sha256_bytes(archive.read(log_name))
            _expect(process_evidence.get(hash_key) == actual_log_sha, f"R1P captured process log hash mismatch: {log_name}")
            process_log_validations += 1
        _expect(process_evidence.get("python_prepare_exit_code") == 0 and process_evidence.get("godot_exit_code") == 0, "R1P captured process exit code is not zero")
        _expect(process_evidence.get("godot_version") == "4.7.1.stable.mono.official.a13da4feb", "R1P Godot version mismatch")
        python_version_output = archive.read("python_version.stdout.log").decode("utf-8", "replace")
        godot_version_output = archive.read("godot_version.stdout.log").decode("utf-8", "replace")
        _expect("Python 3.13." in python_version_output, "R1P Python runtime version evidence mismatch")
        _expect(process_evidence.get("godot_version") in godot_version_output, "R1P Godot runtime version evidence mismatch")
        _expect(sha256_bytes(archive.read("python_prepare_stderr.log")) == sha256_bytes(b""), "R1P Python prepare stderr is not empty")
        _expect(sha256_bytes(archive.read("godot_stderr.log")) == sha256_bytes(b""), "R1P Godot stderr is not empty")
        finalize_stdout = archive.read("python_finalize.stdout.log").decode("utf-8", "replace").strip()
        finalize_result = _load_json_bytes(finalize_stdout.encode("utf-8"), "python_finalize.stdout.log")
        _expect(finalize_result.get("status") == "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27" and finalize_result.get("receipt_count") == 27, "R1P finalization stdout is not a passing 27/27 result")
        _expect(finalize_result.get("report_sha256") == R1P_REPORT_SHA256 and finalize_result.get("run_id") == R1P_RUN_ID, "R1P finalization stdout identity mismatch")
        _expect(archive.read("python_finalize.stderr.log") == b"", "R1P finalizer stderr is not empty")
        _expect(archive.read("python_version.stderr.log") == b"" and archive.read("godot_version.stderr.log") == b"", "R1P runtime version stderr is not empty")

        parent_by_id = {str(item.get("case_id")): item for item in parents["cases"]}
        _expect(len(parent_by_id) == 27, "R1P parent-binding case IDs are not unique")
        validated: list[dict[str, Any]] = []
        family_counts: Counter[str] = Counter()
        receipt_hashes: list[str] = []
        for index, name in enumerate(receipt_names, start=1):
            receipt_raw = archive.read(name)
            receipt = _load_json_bytes(receipt_raw, name)
            expected_sidecar = _parse_sidecar(archive.read(name + ".sha256"), PurePosixPath(name).name)
            canonical_receipt_sha = canonical_sha256({k: v for k, v in receipt.items() if k != "receipt_sha256"})
            _expect(receipt.get("receipt_sha256") == canonical_receipt_sha == expected_sidecar, f"Receipt canonical/sidecar hash mismatch: {name}")
            _expect(int(receipt.get("receipt_index", -1)) == index, f"Receipt index ordering mismatch: {name}")
            parent = parent_by_id.get(str(receipt.get("case_id")))
            _expect(parent is not None, f"Parent-binding case missing for {name}")
            summary = _validate_receipt_and_parent(receipt, parent, report)
            godot_case = godot_case_by_id.get(summary["request_id"])
            _expect(godot_case is not None, f"R1P Godot input case missing for receipt {summary['request_id']}")
            _expect(godot_case.get("family_id") == summary["family_id"] and godot_case.get("grammar_id") == summary["grammar_id"] and godot_case.get("grammar_index") == summary["grammar_index"],
                    f"R1P Godot input selector identity mismatch: {summary['request_id']}")
            _expect(godot_case.get("gameplay_seed") == summary["gameplay_seed"] and godot_case.get("music_seed") == summary["music_seed_lineage_only"],
                    f"R1P Godot input seed-domain identity mismatch: {summary['request_id']}")
            _expect(godot_case.get("request_identity") == receipt.get("request_identity"), f"R1P Godot input parent identity mismatch: {summary['request_id']}")
            family_counts[summary["family_id"]] += 1
            receipt_hashes.append(canonical_receipt_sha)
            validated.append(summary)

        selector_keys = {(item["family_id"], item["grammar_id"]) for item in validated}
        _expect(len(selector_keys) == 27, "R1P receipts do not represent 27 unique family/grammar selectors")
        _expect(dict(family_counts) == EXPECTED_FAMILY_COUNTS, f"R1P family count mismatch: {dict(family_counts)}")
        _expect(report.get("family_count") == 5 and report.get("grammar_count") == 27, "R1P report family/grammar count mismatch")
        _expect(canonical_sha256(receipt_hashes) == report.get("receipt_hash_set_sha256") == R1P_RECEIPT_HASH_SET_SHA256,
                "R1P receipt hash-set digest does not match the validated canonical receipt hashes")
        if verify_live_pins:
            pins = validate_project_pins(root, report.get("source_pins", {}))
        else:
            pins = {}

    return {
        "archive_sha256": archive_sha,
        "archive_members": len(names),
        "receipt_count": len(validated),
        "sidecar_count": len(sidecar_names),
        "family_counts": dict(sorted(family_counts.items())),
        "source_pin_count": len(report.get("source_pins", {})),
        "process_log_validation_count": process_log_validations,
        "live_source_pins": pins,
        "r1p_report": report,
        "validated_cases": validated,
    }


def _case_to_handoff(case: Mapping[str, Any], decision_sha: str, boundary_sha: str, proposal_sha: str) -> dict[str, Any]:
    return {
        "schema": MODULE_SCHEMA,
        "status": "PREPARED_WAITING_FOR_R1V_ACTUAL_SOURCE_EVIDENCE",
        "architecture": "OPTION_C_D_ONLY_POSTCOMPOSITION_OVER_IMMUTABLE_C_SOURCE",
        "decision_sha256": decision_sha,
        "boundary_contract_sha256": boundary_sha,
        "lineage": {
            "r1p_run_id": R1P_RUN_ID,
            "r1p_request_id": case["request_id"],
            "r1p_receipt_sha256": case["receipt_sha256"],
            "r1p_payload_sha256": case["payload_sha256"],
            "r1p_repeat_payload_sha256": case["repeat_payload_sha256"],
            "d9_9_request_hash": case["request_hash"],
            "d9_9_plan_hash": case["plan_hash"],
            "d9_9_editorial_hash": case["editorial_hash"],
            "d9_10_bridge_record_hash": case["d9_10_bridge_record_hash"],
            "d9_10_adapter_envelope_hash": case["d_only_adapter_envelope_hash"],
            "family_stage_contract_sha256": case["family_stage_contract_sha256"],
            "c11c_manifest_sha256": FROZEN_C11C_MANIFEST_SHA256,
        },
        "content_identity": {
            "content_type": case["content_type"],
            "family_id": case["family_id"],
            "grammar_id": case["grammar_id"],
            "grammar_index": case["grammar_index"],
        },
        "visual_seed_domain": {
            "gameplay_seed": case["gameplay_seed"],
            "source": "request.seed",
            "music_seed_consumed_by_visual_composition": False,
            "music_seed_lineage_only_for_future_d3": case["music_seed_lineage_only"],
        },
        "editorial": {
            "values": case["editorial_values"],
            "visual_parameters_sha256": case["visual_parameters_sha256"],
            "source": "D9_9_CANONICAL_EDITORIAL_ALLOWLIST",
        },
        "r1p_timing_descriptor_not_measured_frame_inventory": {
            "duration_seconds": case["duration_seconds_descriptor_only"],
            "fps": case["fps_descriptor_only"],
            "expected_frame_count_consistency_only": case["expected_frame_count_consistency_only"],
            "actual_frame_count": None,
        },
        "c_source_video": {
            "state": "NOT_YET_MATERIALIZED_R1V_REQUIRED",
            "sha256": None,
            "byte_length": None,
            "ffprobe_metadata_sha256": None,
            "frame_inventory_sha256": None,
            "decoded_pixel_manifest_sha256": None,
            "immutable_input_required": True,
            "source_path": None,
        },
        "d_output": {
            "state": "NOT_MATERIALIZED",
            "output_artifact_path": None,
            "separate_artifact_required": True,
            "may_overwrite_c_source": False,
        },
        "composition_policy": {
            "proposal_path": COMPOSITION_PROPOSAL_REL.as_posix(),
            "proposal_sha256": proposal_sha,
            "proposal_status": "PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT",
            "layout_measurement": case["composition_policy_state"],
            "dispatchable": False,
        },
        "execution_boundary": {
            "source_launcher_invoked": False,
            "renderer_dispatch_invoked": False,
            "compositor_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "godot_invoked": False,
            "d3_audio_invoked": False,
            "mux_invoked": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "release_authority": "NONE",
        },
    }


def validate_no_dispatch(handoff: Mapping[str, Any]) -> None:
    _expect(isinstance(handoff, Mapping), "Option C handoff must be an object")
    boundary = handoff.get("execution_boundary")
    _expect(isinstance(boundary, Mapping), "Option C execution boundary missing")
    for flag in FORBIDDEN_TRUE_FLAGS:
        _expect(boundary.get(flag) is False, f"Option C handoff crossed prohibited execution boundary: {flag}")
    _expect(boundary.get("d4_8") == "BLOCKED" and boundary.get("d9_10") == "PREPARE_ONLY", "Option C governance status must remain blocked/prepare-only")
    _expect(boundary.get("release_authority") == "NONE", "Option C handoff cannot acquire release authority")
    _expect(handoff.get("status") == "PREPARED_WAITING_FOR_R1V_ACTUAL_SOURCE_EVIDENCE", "Option C handoff cannot claim actual source readiness")
    _expect(handoff.get("c_source_video", {}).get("sha256") is None, "No source-video SHA may be claimed before R1V")
    _expect(handoff.get("c_source_video", {}).get("frame_inventory_sha256") is None, "No frame inventory may be claimed before R1V")
    _expect(handoff.get("d_output", {}).get("output_artifact_path") is None, "No D output path may exist in a prepare-only handoff")
    _expect(handoff.get("composition_policy", {}).get("dispatchable") is False, "Unapproved layout policy cannot be dispatched")


def validate_source_output_separation(source_path: str, output_path: str) -> None:
    """Reusable fail-closed check for the eventual compositor's two artifact paths."""
    _expect(bool(source_path.strip()) and bool(output_path.strip()), "Source and output paths must be explicit")
    source = Path(source_path).resolve(strict=False)
    output = Path(output_path).resolve(strict=False)
    _expect(source != output, "D output path must never equal the immutable C source path")


def build_report(root: Path, archive_path: Path) -> dict[str, Any]:
    decision, boundary, qualification_policy = validate_option_c_boundary(root)
    validated = validate_r1p_archive(root, archive_path, verify_live_pins=True)
    decision_sha = sha256_file(root / OPTION_C_DECISION_REL)
    boundary_sha = sha256_file(root / OPTION_C_BOUNDARY_REL)
    proposal_sha = sha256_file(root / COMPOSITION_PROPOSAL_REL)
    _expect(decision_sha == EXPECTED_PINS["option_c_decision"][1], "Option C decision pin mismatch")
    _expect(boundary_sha == EXPECTED_PINS["option_c_boundary"][1], "Option C boundary pin mismatch")
    report_pins = validated["r1p_report"].get("source_pins", {})
    _expect(report_pins.get(COMPOSITION_PROPOSAL_REL.as_posix(), {}).get("sha256") == COMPOSITION_PROPOSAL_SHA256,
            "Loop composition proposal must remain pinned by the accepted R1P source set")
    _expect(report_pins.get(MANIFEST_REL.as_posix(), {}).get("sha256") == FROZEN_C11C_MANIFEST_SHA256,
            "Frozen C11-C manifest must remain pinned by the accepted R1P source set")

    by_index = {case["receipt_index"]: case for case in validated["validated_cases"]}
    pilot_summaries = []
    policy_pilots = {int(item["receipt_index"]): item for item in qualification_policy["selectors"]}
    _expect(set(policy_pilots) == {item["receipt_index"] for item in EXPECTED_PILOTS}, "D4.8 pilot allowlist changed")
    for spec in EXPECTED_PILOTS:
        case = by_index.get(spec["receipt_index"])
        policy = policy_pilots.get(spec["receipt_index"])
        _expect(case is not None and policy is not None, f"D4.8 pilot R1P receipt missing: {spec['receipt_index']}")
        for key in ("family_id", "grammar_id", "grammar_index", "gameplay_seed", "duration_seconds", "fps", "expected_frame_count_consistency_only"):
            source_key = "duration_seconds_descriptor_only" if key == "duration_seconds" else ("fps_descriptor_only" if key == "fps" else ("expected_frame_count_consistency_only" if key == "expected_frame_count_consistency_only" else key))
            expected_value = spec["frame_count"] if key == "expected_frame_count_consistency_only" else spec[key]
            _expect(case[source_key] == expected_value, f"R1V pilot differs from R1P receipt: {spec['receipt_index']} {key}")
            _expect(policy.get(key) == expected_value, f"D4.8 policy pilot differs from R1P receipt: {spec['receipt_index']} {key}")
        pins = validated["r1p_report"]["source_pins"]
        _expect(pins.get(policy["launcher_path"], {}).get("sha256") == policy["launcher_sha256"], f"D4.8 launcher pin mismatch: {policy['launcher_path']}")
        _expect(pins.get(policy["prototype_path"], {}).get("sha256") == policy["prototype_sha256"], f"D4.8 prototype pin mismatch: {policy['prototype_path']}")
        with zipfile.ZipFile(archive_path, "r") as _archive:
            receipt_name = f"receipts/{spec['receipt_index']:02d}_E4B_R1P_20261107_032743_5F75045C_{spec['receipt_index']:02d}.json"
            _receipt = _load_json_bytes(_archive.read(receipt_name), receipt_name)
        case_source_pins = _receipt.get("case_source_pins", {})
        _expect(case_source_pins.get("launcher", {}).get("path") == policy["launcher_path"] and case_source_pins.get("launcher", {}).get("sha256") == policy["launcher_sha256"],
                f"D4.8 pilot receipt launcher pin mismatch: {spec['receipt_index']}")
        _expect(case_source_pins.get("prototype", {}).get("path") == policy["prototype_path"] and case_source_pins.get("prototype", {}).get("prototype_sha256") == policy["prototype_sha256"],
                f"D4.8 pilot receipt prototype pin mismatch: {spec['receipt_index']}")
        pilot_summaries.append({
            "receipt_index": spec["receipt_index"],
            "family_id": spec["family_id"],
            "grammar_id": spec["grammar_id"],
            "gameplay_seed": spec["gameplay_seed"],
            "duration_seconds_descriptor_only": spec["duration_seconds"],
            "fps_descriptor_only": spec["fps"],
            "expected_frame_count_consistency_only": spec["frame_count"],
            "source_launcher_authorized_now": False,
            "repeat_count_proposed": 2,
        })

    handoffs = [_case_to_handoff(case, decision_sha, boundary_sha, proposal_sha) for case in validated["validated_cases"]]
    for item in handoffs:
        validate_no_dispatch(item)

    report = {
        "schema": REPORT_SCHEMA,
        "status": "PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY",
        "run_scope": "STATIC_AND_NEGATIVE_CONTRACT_VALIDATION_ONLY_NO_RENDER_NO_MEDIA",
        "architecture_decision": {
            "selected_option": "C",
            "decision_state": decision["decision_state"],
            "decision_sha256": decision_sha,
            "boundary_sha256": boundary_sha,
        },
        "r1p": {
            "run_id": R1P_RUN_ID,
            "recovered_zip_sha256": validated["archive_sha256"],
            "report_sha256": R1P_REPORT_SHA256,
            "parent_bindings_sha256": R1P_PARENT_BINDINGS_SHA256,
            "receipt_hash_set_sha256": R1P_RECEIPT_HASH_SET_SHA256,
            "receipt_count": validated["receipt_count"],
            "family_counts": validated["family_counts"],
            "r1p_source_pin_count": validated["source_pin_count"],
            "r1p_process_log_validation_count": validated["process_log_validation_count"],
            "option_c_policy_pin_validation_count": 3,
            "total_live_pin_validations": len(validated["live_source_pins"]),
        },
        "option_c_handoff": {
            "handoff_count": len(handoffs),
            "all_cases_waiting_for_r1v_actual_source": all(item["status"] == "PREPARED_WAITING_FOR_R1V_ACTUAL_SOURCE_EVIDENCE" for item in handoffs),
            "source_media_sha256_claims": 0,
            "measured_frame_inventories": 0,
            "d_output_artifacts": 0,
            "layout_policy_state": boundary["layout_policy"]["proposal_status"],
            "layout_policy_sha256": proposal_sha,
        },
        "r1v_qualification_request": {
            "policy_id": qualification_policy["policy_id"],
            "policy_sha256": sha256_file(root / R1V_POLICY_REL),
            "status": qualification_policy["status"],
            "execution_authorized": qualification_policy["execution_authorized"],
            "pilot_count": len(pilot_summaries),
            "proposed_launcher_invocations": qualification_policy["scope"]["total_launcher_invocations"],
            "pilots": pilot_summaries,
        },
        "governance": {
            "renderer": "OFF",
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
            "release_authority": "NONE",
            "renderer_dispatch_invoked": False,
            "compositor_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "launcher_invoked": False,
            "godot_invoked": False,
            "audio_or_d3_invoked": False,
            "mux_invoked": False,
            "media_created": False,
            "c11c_source_mutation": False,
        },
        "handoffs": handoffs,
    }
    _expect(len(handoffs) == 27, "Option C handoff count must be 27")
    _expect(report["r1p"]["r1p_source_pin_count"] == 30, "R1P source pin count must remain 30")
    _expect(report["r1p"]["option_c_policy_pin_validation_count"] == 3, "Option C policy pin validation count must be 3")
    _expect(report["r1p"]["total_live_pin_validations"] == 33, "Expected 30 R1P source pin validations plus 3 Option C policy pins")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Option C D post-composition prepare-only handoff contract")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--r1p-zip", required=True, type=Path)
    parser.add_argument("--report-out", required=True, type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    archive = args.r1p_zip.resolve()
    try:
        report = build_report(root, archive)
        args.report_out.parent.mkdir(parents=True, exist_ok=True)
        args.report_out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"OPTION_C_STATUS={report['status']}")
        print(f"R1P_RECEIPTS={report['r1p']['receipt_count']}/27")
        print(f"OPTION_C_HANDOFFS={report['option_c_handoff']['handoff_count']}/27")
        print(f"R1P_SOURCE_PINS={report['r1p']['r1p_source_pin_count']}/30")
        print(f"R1P_PROCESS_LOGS={report['r1p']['r1p_process_log_validation_count']}/4")
        print(f"OPTION_C_POLICY_PINS={report['r1p']['option_c_policy_pin_validation_count']}/3")
        print(f"TOTAL_LIVE_PIN_VALIDATIONS={report['r1p']['total_live_pin_validations']}/33")
        print(f"R1V_QUALIFICATION_POLICY={report['r1v_qualification_request']['status']}")
        print(f"R1V_EXECUTION_AUTHORIZED={str(report['r1v_qualification_request']['execution_authorized']).upper()}")
        print("RENDERER=OFF")
        print("MEDIA_CREATED=false")
        print("RELEASE_AUTHORITY=NONE")
        print(f"REPORT_PATH={args.report_out}")
        print(f"REPORT_SHA256={sha256_file(args.report_out)}")
        return 0
    except Exception as exc:
        print(f"OPTION_C_STATUS=FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
