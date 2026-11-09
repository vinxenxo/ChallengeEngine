#!/usr/bin/env python3
"""Read-only projection of accepted R1P receipts and current Loop policy fingerprints.

This tool does not run Godot, C11-C launchers, music generation, FFmpeg/FFprobe,
production tests, renderer dispatch, or media work. It writes only new audit
artifacts below artifacts/tests/c11e/e4b_loop22_r1p_policy_refresh/.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "C11E-E4B-LOOP22-R1P-PROJECTION-POLICY-REFRESH-V1"
EXPECTED_ROOT_WIN = r"C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
FROZEN_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_MANIFEST_BYTES = 796318
R1P_RUN_ID = "E4B_R1P_20261107_032743_5F75045C"
R1P_ARCHIVE_SHA = "d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52"
R1P_ARCHIVE_BYTES = 210961
AUDIT_REPORT_REL = Path("artifacts/tests/c11e/e4b_loop22_source_reconciliation/LOOP22_READ_ONLY_AUDIT_20261108T232702Z.json")
R1V_CLOSEOUT_REL = Path("artifacts/tests/c11e/r1v_operator_human_review_closeout/R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json")
R1V_INSTALL_RECEIPT_REL = Path("artifacts/tests/c11e/r1v_human_acceptance_loop22_handoff_v7/INSTALL_RECEIPT.json")
R1V_INSTALL_RECEIPT_SHA = "917ea340f345956c40e0fa9e60ba9be2721ca920b8cee867ceffe4bdbca3e15b"
PILOT = {
    ("c11c_geometric_waves_v1", "harmonic_membrane"),
    ("c11c_fractal_bloom_v1", "radial_bloom"),
    ("c11c_sacred_symmetry_v1", "astrolabe"),
    ("c11c_living_particles_v1", "swarm"),
    ("c11c_invisible_forces_v1", "dipole_field"),
}
FAMILY_PROFILES = {
    "c11c_geometric_waves_v1": "CIRCUIT_PULSE",
    "c11c_fractal_bloom_v1": "ORGANIC_BLOOM",
    "c11c_sacred_symmetry_v1": "ORBITAL_RITUAL",
    "c11c_living_particles_v1": "ORGANIC_BLOOM",
    "c11c_invisible_forces_v1": "FLOWING_VECTOR",
}
CYCLE_SECONDS = {1: 20, 2: 22, 3: 23}
POLICIES = {
    "A.1": {
        "label": "Shared presentation semantic regions",
        "path": "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json",
        "decision_gate": "D-only Loop visual consumer",
    },
    "A.3": {
        "label": "Loop/Drill editorial field windows",
        "path": "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json",
        "decision_gate": "D-only Loop visual consumer",
    },
    "E4B_LOOP": {
        "label": "E4B Loop outer editorial composition",
        "path": "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json",
        "decision_gate": "D-only Loop visual consumer",
    },
    "B.1": {
        "label": "Unified delivery timebase",
        "path": "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json",
        "decision_gate": "A/V timebase, mux and delivery",
    },
    "D.1": {
        "label": "Unified audio/music delivery",
        "path": "definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json",
        "decision_gate": "Family-native music, AAC mux and A/V delivery",
    },
}
REQUIRED_REQUEST_IDENTITY = (
    "request_id", "request_hash", "plan_hash", "editorial_hash",
    "bridge_record_hash", "adapter_envelope_hash", "family_stage_contract_sha256",
)
FORBIDDEN_TRUE_FLAGS = (
    "launcher_invoked", "prototype_node_instantiated", "renderer_instantiated",
    "renderer_native_input_emitted", "frame_buffers_materialized",
    "frame_inventory_materialized", "pixel_payload_materialized", "media_created",
    "ffmpeg_invoked", "audio_or_d3_invoked",
)


class AuditError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def canonical_digest(value: Any, field: str) -> str:
    if not isinstance(value, dict) or field not in value:
        raise AuditError(f"CANONICAL_DIGEST_FIELD_MISSING:{field}")
    material = dict(value)
    declared = material.pop(field)
    actual = sha256_bytes(canonical_json_bytes(material))
    if declared != actual:
        raise AuditError(f"CANONICAL_DIGEST_MISMATCH:{field}:{declared}:{actual}")
    return actual


def parse_sidecar_bytes(raw: bytes) -> str:
    try:
        token = raw.decode("ascii").strip().split()[0].lower()
    except Exception as exc:
        raise AuditError("SIDECAR_PARSE_FAILED") from exc
    if len(token) != 64 or any(c not in "0123456789abcdef" for c in token):
        raise AuditError("SIDECAR_SHA256_INVALID")
    return token


def check_raw_sidecar(zip_file: zipfile.ZipFile, data_name: str) -> str:
    data = zip_file.read(data_name)
    side = parse_sidecar_bytes(zip_file.read(data_name + ".sha256"))
    actual = sha256_bytes(data)
    if actual != side:
        raise AuditError(f"RAW_SIDECAR_MISMATCH:{data_name}")
    return actual


def load_json_path(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise AuditError(f"MISSING_FILE:{label}:{path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise AuditError(f"INVALID_JSON:{label}:{path}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"JSON_ROOT_NOT_OBJECT:{label}")
    return value


def normalize_rel(value: str) -> Path:
    return Path(value.replace("\\", "/"))


def validate_closeout(root: Path) -> dict[str, Any]:
    install_receipt = root / R1V_INSTALL_RECEIPT_REL
    if not install_receipt.is_file():
        raise AuditError(f"MISSING_R1V_V7_INSTALL_RECEIPT:{install_receipt}")
    install_sha = sha256_file(install_receipt)
    if install_sha != R1V_INSTALL_RECEIPT_SHA:
        raise AuditError(f"R1V_V7_INSTALL_RECEIPT_SHA_MISMATCH:{install_sha}")
    closeout_path = root / R1V_CLOSEOUT_REL
    closeout = load_json_path(closeout_path, "R1V_HUMAN_CLOSEOUT")
    if closeout.get("schema") != "C11E-R1V-HUMAN-REVIEW-CLOSEOUT-RECEIPT-V1":
        raise AuditError("R1V_CLOSEOUT_SCHEMA_MISMATCH")
    if closeout.get("status") != "PASS_TEST_ONLY_OPERATOR_ACCEPTED" or closeout.get("phase_closed") is not True:
        raise AuditError("R1V_CLOSEOUT_NOT_ACCEPTED")
    acceptance = closeout.get("acceptance", {})
    expected = {
        "visual_layer_editorial_layout": "10/10_PASS",
        "audio_music_listening": "10/10_PASS",
        "combined_slots": "10/10_PASS",
    }
    if any(acceptance.get(k) != v for k, v in expected.items()):
        raise AuditError("R1V_CLOSEOUT_ACCEPTANCE_INCOMPLETE")
    slots = closeout.get("slots", [])
    if len(slots) != 10 or any(s.get("visual_status") not in ("OPERATOR_CONFIRMED_PASS", "OPERATOR_CONFIRMED_AV_PASS") or s.get("audio_status") not in ("OPERATOR_CONFIRMED_PASS", "OPERATOR_CONFIRMED_AV_PASS") for s in slots):
        raise AuditError("R1V_CLOSEOUT_SLOT_STATUS_INCOMPLETE")
    gov = closeout.get("governance", {})
    if gov.get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA or gov.get("production_release_authority") != "NONE":
        raise AuditError("R1V_CLOSEOUT_GOVERNANCE_MISMATCH")
    return {
        "install_receipt_path": R1V_INSTALL_RECEIPT_REL.as_posix(),
        "install_receipt_sha256": install_sha,
        "closeout_path": R1V_CLOSEOUT_REL.as_posix(),
        "closeout_sha256": sha256_file(closeout_path),
        "status": closeout["status"],
        "phase_closed": True,
        "acceptance": acceptance,
        "operator_review_date": closeout.get("reviewed_local_date"),
    }


def load_source_audit(root: Path, audit_path: Path) -> tuple[dict[str, Any], str]:
    if not audit_path.is_file():
        raise AuditError(f"MISSING_SOURCE_AUDIT:{audit_path}")
    side_path = audit_path.with_suffix(audit_path.suffix + ".sha256")
    if not side_path.is_file():
        raise AuditError(f"MISSING_SOURCE_AUDIT_SIDECAR:{side_path}")
    actual = sha256_file(audit_path)
    side = parse_sidecar_bytes(side_path.read_bytes())
    if actual != side:
        raise AuditError("SOURCE_AUDIT_SIDECAR_MISMATCH")
    audit = load_json_path(audit_path, "LOOP22_SOURCE_AUDIT")
    if audit.get("schema") != "C11E-E4B-LOOP22-ACTIVE-SOURCE-READ-ONLY-AUDIT-V1":
        raise AuditError("SOURCE_AUDIT_SCHEMA_MISMATCH")
    if audit.get("status") != "PASS_STATIC_SOURCE_MAPPING_R1P_ARCHIVE_HASH_AND_CRC_PRESENT":
        raise AuditError("SOURCE_AUDIT_NOT_PASS")
    if audit.get("frozen_c11c_manifest", {}).get("sha256") != FROZEN_MANIFEST_SHA:
        raise AuditError("SOURCE_AUDIT_FROZEN_MANIFEST_MISMATCH")
    return audit, actual


def read_r1p_archive(root: Path, audit: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    discovery = audit.get("r1p_archive_discovery", {})
    matches = discovery.get("matches", [])
    if discovery.get("status") != "FOUND_EXACT_HASH_AND_CRC_PASS" or len(matches) != 1:
        raise AuditError("R1P_ARCHIVE_DISCOVERY_NOT_EXACT_SINGLE_MATCH")
    match = matches[0]
    rel = normalize_rel(match.get("path", ""))
    archive_path = root / rel
    if not archive_path.is_file():
        raise AuditError(f"R1P_ARCHIVE_MISSING:{archive_path}")
    archive_sha = sha256_file(archive_path)
    if archive_sha != R1P_ARCHIVE_SHA or archive_sha != match.get("sha256"):
        raise AuditError(f"R1P_ARCHIVE_SHA_MISMATCH:{archive_sha}")
    if archive_path.stat().st_size != R1P_ARCHIVE_BYTES:
        raise AuditError("R1P_ARCHIVE_BYTE_COUNT_MISMATCH")
    with zipfile.ZipFile(archive_path, "r") as zf:
        corrupt = zf.testzip()
        if corrupt is not None:
            raise AuditError(f"R1P_ARCHIVE_CRC_FAILURE:{corrupt}")
        report_bytes = zf.read("r1p_report.json")
        report = json.loads(report_bytes.decode("utf-8-sig"))
        report_digest = canonical_digest(report, "report_sha256")
        report_sidecar = parse_sidecar_bytes(zf.read("r1p_report.sha256"))
        if report_sidecar != report_digest:
            raise AuditError("R1P_REPORT_SIDECAR_CANONICAL_MISMATCH")
        manifest_bytes = zf.read("source_manifest.json")
        manifest_sha = sha256_bytes(manifest_bytes)
        if manifest_sha != report.get("source_manifest_sha256"):
            raise AuditError("R1P_SOURCE_MANIFEST_RAW_SHA_MISMATCH")
        manifest = json.loads(manifest_bytes.decode("utf-8-sig"))
        if manifest.get("schema") != "C11E-E4B-R1P-SOURCE-MANIFEST-V1" or manifest.get("run_id") != R1P_RUN_ID:
            raise AuditError("R1P_SOURCE_MANIFEST_IDENTITY_MISMATCH")
        if manifest.get("source_pins") != report.get("source_pins"):
            raise AuditError("R1P_SOURCE_PIN_MANIFEST_REPORT_DIVERGENCE")
        runner_bytes = zf.read("runner_process_receipt.json")
        runner_sidecar = parse_sidecar_bytes(zf.read("runner_process_receipt.sha256"))
        if sha256_bytes(runner_bytes) != runner_sidecar:
            raise AuditError("R1P_RUNNER_RECEIPT_SIDECAR_MISMATCH")
        runner = json.loads(runner_bytes.decode("utf-8-sig"))
        if runner.get("run_id") != R1P_RUN_ID or runner.get("process_success") is not True:
            raise AuditError("R1P_RUNNER_RECEIPT_NOT_PASS")
        if runner.get("checkout_source_files_written") is not False or runner.get("renderer_or_media_invoked") is not False:
            raise AuditError("R1P_RUNNER_GOVERNANCE_MISMATCH")
        receipt_hashes: list[str] = []
        receipts: list[dict[str, Any]] = []
        for i in range(1, 28):
            basename = f"{i:02d}_{R1P_RUN_ID}_{i:02d}.json"
            name = f"receipts/{basename}"
            side_name = name + ".sha256"
            raw = zf.read(name)
            receipt = json.loads(raw.decode("utf-8-sig"))
            digest = canonical_digest(receipt, "receipt_sha256")
            if parse_sidecar_bytes(zf.read(side_name)) != digest:
                raise AuditError(f"R1P_RECEIPT_SIDECAR_MISMATCH:{basename}")
            if receipt.get("receipt_index") != i or receipt.get("case_id") != f"{R1P_RUN_ID}_{i:02d}":
                raise AuditError(f"R1P_RECEIPT_SEQUENCE_MISMATCH:{basename}")
            receipts.append(receipt)
            receipt_hashes.append(digest)
        expected_hash_set = sha256_bytes(json.dumps(receipt_hashes, separators=(",", ":")).encode("utf-8"))
        if expected_hash_set != report.get("receipt_hash_set_sha256"):
            raise AuditError("R1P_RECEIPT_HASH_SET_MISMATCH")
        if report.get("case_count") != 27 or report.get("grammar_count") != 27 or report.get("family_count") != 5 or report.get("receipt_count") != 27:
            raise AuditError("R1P_REPORT_CARDINALITY_MISMATCH")
        if report.get("schema") != "C11E-E4B-R1P-LOOP-PARAMETER-PAYLOAD-RUN-V1" or report.get("run_id") != R1P_RUN_ID:
            raise AuditError("R1P_REPORT_IDENTITY_MISMATCH")
        if report.get("status") != "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27":
            raise AuditError("R1P_REPORT_STATUS_NOT_PASS")
        if report.get("scope") != "REQUEST_SCOPED_C11C_FAMILY_PARAMETER_PAYLOADS_ONLY":
            raise AuditError("R1P_REPORT_SCOPE_MISMATCH")
        gov = report.get("governance", {})
        if gov.get("renderer") != "OFF" or gov.get("D4.8") != "BLOCKED" or gov.get("D9.10") != "PREPARE_ONLY" or gov.get("release_authority") != "NONE":
            raise AuditError("R1P_REPORT_GOVERNANCE_MISMATCH")
        if report.get("scope_limits", {}).get("parameter_payload_materialized_in_memory") is not True or report.get("scope_limits", {}).get("renderer_native_input_emitted") is not False:
            raise AuditError("R1P_REPORT_MATERIALIZATION_BOUNDARY_MISMATCH")
        archive_meta = {
            "path": rel.as_posix(),
            "sha256": archive_sha,
            "bytes": archive_path.stat().st_size,
            "zip_crc": "PASS",
            "run_id": R1P_RUN_ID,
            "report_sha256": report_digest,
            "source_manifest_sha256": manifest_sha,
            "source_pin_count": len(manifest.get("source_pins", {})),
            "receipt_count": len(receipts),
            "receipt_hash_set_sha256": expected_hash_set,
        }
    return report, manifest, receipts, archive_meta


def validate_receipt(receipt: dict[str, Any], source_pins: dict[str, Any]) -> dict[str, Any]:
    if receipt.get("schema") != "C11E-E4B-R1P-LOOP-FAMILY-PARAMETER-RECEIPT-V1":
        raise AuditError("R1P_RECEIPT_SCHEMA_MISMATCH")
    if receipt.get("status") != "PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT":
        raise AuditError("R1P_RECEIPT_STATUS_NOT_PASS")
    if receipt.get("payload_sha256") != receipt.get("repeat_payload_sha256"):
        raise AuditError("R1P_REPEAT_PAYLOAD_MISMATCH")
    for field in ("payload_sha256", "repeat_payload_sha256"):
        value = receipt.get(field)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise AuditError(f"R1P_PAYLOAD_HASH_INVALID:{field}")
    mat = receipt.get("materialization", {})
    if mat.get("parameter_payload_materialized_in_memory") is not True:
        raise AuditError("R1P_PARAMETER_PAYLOAD_NOT_MATERIALIZED")
    if any(mat.get(flag) is not False for flag in FORBIDDEN_TRUE_FLAGS):
        raise AuditError("R1P_RECEIPT_EXCEEDS_PLAN_ONLY_BOUNDARY")
    seed = receipt.get("seed_domains", {})
    if seed.get("automatic_seed_generation") is not False or seed.get("runtime_seed_derivation") is not False:
        raise AuditError("R1P_SEED_AUTOGENERATION_ENABLED")
    if seed.get("music_seed_consumed_by_visual_parameters") is not False or seed.get("visual_parameters_use") != "request.seed":
        raise AuditError("R1P_SEED_DOMAIN_LEAKAGE")
    if not isinstance(seed.get("gameplay_seed"), int) or not isinstance(seed.get("music_seed"), int) or seed["gameplay_seed"] == seed["music_seed"]:
        raise AuditError("R1P_SEED_DOMAINS_INVALID")
    selection = receipt.get("selection", {})
    family_id = selection.get("family_id")
    grammar_id = selection.get("grammar_id")
    if selection.get("content_type") != "visual_loops" or family_id not in FAMILY_PROFILES or not grammar_id:
        raise AuditError("R1P_SELECTOR_IDENTITY_INVALID")
    if receipt.get("family_music_profile_id") != FAMILY_PROFILES[family_id]:
        raise AuditError(f"R1P_FAMILY_MUSIC_PROFILE_MISMATCH:{family_id}:{grammar_id}")
    timing = receipt.get("timing", {})
    try:
        cycles = int(timing["loop_cycles"])
        duration = int(timing["duration_seconds"])
        fps = int(timing["fps"])
        frames = int(timing["frame_count"])
    except Exception as exc:
        raise AuditError("R1P_TIMING_FIELDS_INVALID") from exc
    if cycles not in CYCLE_SECONDS or duration != CYCLE_SECONDS[cycles] or fps != 30 or frames != duration * fps:
        raise AuditError(f"R1P_DURATION_CONTRACT_MISMATCH:{family_id}:{grammar_id}")
    visual = receipt.get("visual_parameters", {})
    recipe = visual.get("variation_recipe", {})
    if visual.get("family_id") != family_id or recipe.get("grammar_name") != grammar_id or int(recipe.get("loop_cycles", -1)) != cycles:
        raise AuditError(f"R1P_VISUAL_RECIPE_IDENTITY_MISMATCH:{family_id}:{grammar_id}")
    identity = receipt.get("request_identity", {})
    missing = [key for key in REQUIRED_REQUEST_IDENTITY if not identity.get(key)]
    if missing:
        raise AuditError(f"R1P_REQUEST_BOUND_IDENTITY_INCOMPLETE:{family_id}:{grammar_id}:{','.join(missing)}")
    hash_identity_fields = REQUIRED_REQUEST_IDENTITY[1:]
    invalid_hashes = [key for key in hash_identity_fields if not isinstance(identity.get(key), str) or len(identity[key]) != 64 or any(c not in "0123456789abcdef" for c in identity[key])]
    if invalid_hashes:
        raise AuditError(f"R1P_REQUEST_BOUND_HASH_INVALID:{family_id}:{grammar_id}:{','.join(invalid_hashes)}")
    source = receipt.get("case_source_pins", {})
    proto = source.get("prototype", {})
    launcher = source.get("launcher", {})
    if not proto.get("path") or not launcher.get("path"):
        raise AuditError(f"R1P_FAMILY_SOURCE_BINDING_MISSING:{family_id}:{grammar_id}")
    for item in (proto, launcher):
        pin = source_pins.get(item["path"])
        digest = item.get("prototype_sha256") if "prototype_sha256" in item else item.get("sha256")
        if not pin or pin.get("sha256") != digest:
            raise AuditError(f"R1P_FAMILY_SOURCE_BINDING_PIN_MISMATCH:{family_id}:{grammar_id}")
    if receipt.get("source_pins") != source_pins:
        raise AuditError(f"R1P_RECEIPT_SOURCE_MANIFEST_DIVERGENCE:{family_id}:{grammar_id}")
    return {
        "family_id": family_id,
        "grammar_id": grammar_id,
        "music_profile": receipt["family_music_profile_id"],
        "gameplay_seed": seed["gameplay_seed"],
        "music_seed": seed["music_seed"],
        "loop_cycles": cycles,
        "duration_seconds": duration,
        "fps": fps,
        "frame_count": frames,
        "receipt_index": receipt["receipt_index"],
        "receipt_sha256": receipt["receipt_sha256"],
        "payload_sha256": receipt["payload_sha256"],
        "request_id": identity["request_id"],
        "request_hash": identity["request_hash"],
        "plan_hash": identity["plan_hash"],
        "editorial_hash": identity["editorial_hash"],
        "bridge_record_hash": identity["bridge_record_hash"],
        "adapter_envelope_hash": identity["adapter_envelope_hash"],
        "family_stage_contract_sha256": identity["family_stage_contract_sha256"],
        "family_prototype_path": proto["path"],
        "family_prototype_sha256": proto.get("prototype_sha256"),
        "family_launcher_path": launcher["path"],
        "family_launcher_sha256": launcher.get("sha256"),
        "r1p_status": receipt["status"],
        "request_compatibility": "PLAN_ONLY_NOT_D4_EXECUTABLE_COMPATIBILITY",
    }


def compare_projection(audit: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected_rows = audit.get("remaining_selector_rows", [])
    if len(expected_rows) != 22:
        raise AuditError("SOURCE_AUDIT_REMAINING_SELECTOR_COUNT_NOT_22")
    expected_by_key = {(r.get("family_id"), r.get("grammar_id")): r for r in expected_rows}
    row_by_key = {(r["family_id"], r["grammar_id"]): r for r in rows}
    if len(expected_by_key) != 22 or len(row_by_key) != 27:
        raise AuditError("R1P_SELECTOR_UNIQUENESS_OR_CARDINALITY_FAILURE")
    non_pilot = [r for r in rows if (r["family_id"], r["grammar_id"]) not in PILOT]
    pilot_rows = [r for r in rows if (r["family_id"], r["grammar_id"]) in PILOT]
    if len(pilot_rows) != 5 or len(non_pilot) != 22:
        raise AuditError("R1V_PILOT_COMPLEMENT_CARDINALITY_FAILURE")
    if set(expected_by_key) != {(r["family_id"], r["grammar_id"]) for r in non_pilot}:
        raise AuditError("R1P_22_COMPLEMENT_DIFFERS_FROM_ACTIVE_SOURCE_AUDIT")
    compare_fields = ("music_profile", "gameplay_seed", "music_seed", "loop_cycles", "duration_seconds", "fps", "frame_count")
    for key, expected in expected_by_key.items():
        actual = row_by_key[key]
        for field in compare_fields:
            if actual[field] != expected[field]:
                raise AuditError(f"R1P_AUDIT_MATRIX_FIELD_MISMATCH:{key[0]}:{key[1]}:{field}:{actual[field]}!={expected[field]}")
    counts = Counter(r["family_id"] for r in non_pilot)
    expected_counts = {
        "c11c_geometric_waves_v1": 4,
        "c11c_fractal_bloom_v1": 4,
        "c11c_sacred_symmetry_v1": 4,
        "c11c_living_particles_v1": 4,
        "c11c_invisible_forces_v1": 6,
    }
    if dict(counts) != expected_counts:
        raise AuditError("R1P_22_FAMILY_DISTRIBUTION_MISMATCH")
    return sorted(non_pilot, key=lambda r: (list(expected_counts).index(r["family_id"]), r["receipt_index"]))


def verify_checkout_source_pins(root: Path, audit: dict[str, Any], source_manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    pins = source_manifest.get("source_pins", {})
    if len(pins) != 30:
        raise AuditError(f"R1P_SOURCE_PIN_COUNT_NOT_30:{len(pins)}")
    results: list[dict[str, Any]] = []
    drift: list[dict[str, Any]] = []
    for rel, pin in sorted(pins.items()):
        path = root / normalize_rel(rel)
        if not path.is_file():
            row = {"path": rel, "status": "MISSING", "expected_sha256": pin.get("sha256"), "actual_sha256": None}
            drift.append(row)
        else:
            actual = sha256_file(path)
            ok = actual == pin.get("sha256") and path.stat().st_size == pin.get("bytes")
            row = {
                "path": rel,
                "status": "PASS" if ok else "PIN_DRIFT",
                "expected_sha256": pin.get("sha256"),
                "actual_sha256": actual,
                "expected_bytes": pin.get("bytes"),
                "actual_bytes": path.stat().st_size,
            }
            if not ok:
                drift.append(row)
        results.append(row)

    # The earlier 17-pin read-only audit covers a broader but not identical set:
    # two rows (the current FAMILY_MUSIC_V4 generator and the V7 plan) are not
    # part of the original 30-file R1P source manifest. Recheck all 17 independently.
    source_report_rows = audit.get("source_pins_before_after", {}).get("rows", [])
    if len(source_report_rows) != 17 or audit.get("source_pins_before_after", {}).get("stable") is not True:
        raise AuditError("PRIOR_17_SOURCE_PIN_AUDIT_INCOMPLETE")
    prior_results: list[dict[str, Any]] = []
    for prior in source_report_rows:
        rel = prior.get("path")
        if not rel:
            raise AuditError("PRIOR_SOURCE_AUDIT_PIN_PATH_MISSING")
        path = root / normalize_rel(rel)
        if not path.is_file():
            row = {"path": rel, "status": "MISSING", "expected_sha256": prior.get("sha256"), "actual_sha256": None}
            drift.append(row)
        else:
            actual = sha256_file(path)
            ok = prior.get("stable") is True and actual == prior.get("sha256")
            row = {
                "path": rel,
                "status": "PASS" if ok else "PIN_DRIFT",
                "expected_sha256": prior.get("sha256"),
                "actual_sha256": actual,
                "stable_in_prior_audit": prior.get("stable"),
                "bytes": path.stat().st_size,
            }
            if not ok:
                drift.append(row)
        prior_results.append(row)
    if len(prior_results) != 17:
        raise AuditError("PRIOR_SOURCE_AUDIT_PIN_COUNT_INVALID")
    return results, drift, prior_results


def fingerprint_policies(root: Path, source_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    pins = source_manifest.get("source_pins", {})
    result = []
    for key, spec in POLICIES.items():
        path = root / normalize_rel(spec["path"])
        if not path.is_file():
            raise AuditError(f"MISSING_POLICY_PROPOSAL:{key}:{path}")
        raw = path.read_bytes()
        try:
            value = json.loads(raw.decode("utf-8-sig"))
        except Exception as exc:
            raise AuditError(f"POLICY_PROPOSAL_INVALID_JSON:{key}") from exc
        if not isinstance(value, dict):
            raise AuditError(f"POLICY_PROPOSAL_JSON_ROOT_INVALID:{key}")
        actual = sha256_bytes(raw)
        old_pin = pins.get(spec["path"], {})
        result.append({
            "group": key,
            "label": spec["label"],
            "path": spec["path"],
            "sha256": actual,
            "bytes": len(raw),
            "schema": value.get("schema"),
            "status": value.get("status"),
            "r1p_archive_sha256": old_pin.get("sha256"),
            "r1p_archive_bytes": old_pin.get("bytes"),
            "matches_r1p_archive_pin": actual == old_pin.get("sha256") and len(raw) == old_pin.get("bytes"),
            "decision_gate": spec["decision_gate"],
            "decision": "PENDING_OPERATOR_DECISION",
            "sha_confirmed": "PENDING_OPERATOR_HASH_CONFIRMATION",
        })
    return result


def build_docket(policies: list[dict[str, Any]], run_id: str, closeout: dict[str, Any]) -> str:
    lines = [
        "# C11-E E4B Loop Current-Hash Policy Decision Docket — V2",
        "",
        f"**Fingerprint capture:** `{run_id}` (active-checkout read-only run)",
        "**Current project continuation:** operator approved continuation on 2026-11-09. This is not interpreted as a hash-specific policy decision.",
        "**R1V prerequisite:** `PASS_TEST_ONLY_OPERATOR_ACCEPTED`; ten combined slots, ten visual/editorial/layout passes and ten audio/music listening passes.",
        "",
        "## Decision protocol",
        "",
        "For each row, explicitly select `APPROVE AS PROPOSED`, `REQUEST CHANGES`, or `DEFER`, and confirm the complete SHA-256 shown. A general instruction to continue the project does not substitute for confirming the exact proposal fingerprint. A decision is binding only after it is recorded in a versioned D-owned record with the exact hash, rationale, operator/date and focused positive/negative tests.",
        "",
        "## Current-hash decisions",
        "",
        "| Group | Proposal | Active-checkout SHA-256 | Bytes | Match to R1P archived pin | Gate | Decision | SHA confirmed | Rationale / change | Operator + date |",
        "|---|---|---|---:|---|---|---|---|---|---|",
    ]
    for p in policies:
        lines.append(f"| {p['group']} — {p['label']} | `{p['path']}` | `{p['sha256']}` | {p['bytes']} | {'YES' if p['matches_r1p_archive_pin'] else 'NO — refreshed hash differs'} | {p['decision_gate']} | **PENDING** | **PENDING** | PENDING | PENDING |")
    lines += [
        "",
        "## Dependency interpretation",
        "",
        "- A.1, A.3 and E4B_LOOP: required before implementing the D-only Loop visual consumer. These decisions do not authorize renderer-native input by themselves.",
        "- B.1 and D.1: required before family-native audio generation, AAC mux and A/V delivery for the expanded 22-selector scope. The five-selector R1V AV approval is not silently extended.",
        "- No decision in this docket activates D4.8, D9.10 dispatch, renderer input or production authority. D9.9/R1P request-bound materialization remains plan-only.",
        "",
        "## R1P projection boundary",
        "",
        "The paired projection report verifies 27/27 request-scoped parameter receipts and isolates the 22 non-pilot selectors. Their payloads were materialized in memory; no prototype Node, C11-C launcher, renderer-native input, audio generator, FFmpeg, FFprobe or media was invoked by this audit.",
        "",
        "## Governance",
        "",
        f"- R1V closeout receipt SHA-256: `{closeout['closeout_sha256']}`.",
        f"- Frozen C11-C manifest SHA-256: `{FROZEN_MANIFEST_SHA}` (796,318 bytes); immutable.",
        "- Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.",
        "- No Git checks; operator-managed commits; no C11-C source writes.",
        "",
    ]
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def run_audit(root: Path, audit_path: Path, output_root: Path) -> tuple[dict[str, Any], Path]:
    root = root.resolve()
    if os.name == "nt" and str(root).lower() != EXPECTED_ROOT_WIN.lower():
        raise AuditError("ACTIVE_CHECKOUT_PATH_MISMATCH")
    manifest_path = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    if not manifest_path.is_file() or manifest_path.stat().st_size != FROZEN_MANIFEST_BYTES or sha256_file(manifest_path) != FROZEN_MANIFEST_SHA:
        raise AuditError("FROZEN_C11C_MANIFEST_MISMATCH")
    closeout = validate_closeout(root)
    audit, audit_sha = load_source_audit(root, audit_path)
    r1p_report, source_manifest, receipts, archive_meta = read_r1p_archive(root, audit)
    all_rows = [validate_receipt(r, source_manifest["source_pins"]) for r in receipts]
    if len({(r["family_id"], r["grammar_id"]) for r in all_rows}) != 27:
        raise AuditError("R1P_SELECTOR_SET_DUPLICATED")
    loop22_rows = compare_projection(audit, all_rows)
    source_pin_results, source_pin_drift, prior_pin_results = verify_checkout_source_pins(root, audit, source_manifest)
    policy_rows = fingerprint_policies(root, source_manifest)
    policy_pin_drift = [p for p in policy_rows if not p["matches_r1p_archive_pin"]]
    run_id = "LOOP22_R1P_POLICY_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = output_root / run_id
    output.mkdir(parents=True, exist_ok=False)
    blocking = []
    if source_pin_drift:
        blocking.append("R1P_ACTIVE_SOURCE_PIN_DRIFT")
    status = "PASS_R1P_RECEIPTS_PROJECTED_27_OF_27_POLICY_FINGERPRINTS_REFRESHED_5_OF_5" if not blocking else "BLOCKED_R1P_SOURCE_PIN_DRIFT"
    report: dict[str, Any] = {
        "schema": SCHEMA,
        "run_id": run_id,
        "status": status,
        "run_mode": "READ_ONLY_R1P_RECEIPT_PROJECTION_AND_POLICY_FINGERPRINT_REFRESH",
        "active_checkout": str(root),
        "source_audit": {"path": str(audit_path.relative_to(root)), "sha256": audit_sha, "status": audit["status"]},
        "r1v_closeout": closeout,
        "r1p_archive": archive_meta,
        "r1p_projection": {
            "receipt_count_verified": len(all_rows),
            "pilot_selectors_excluded": len(PILOT),
            "remaining_selectors_projected": len(loop22_rows),
            "planned_ab_output_slots": len(loop22_rows) * 2,
            "family_distribution": dict(Counter(r["family_id"] for r in loop22_rows)),
            "family_music_profile_distribution": dict(Counter(r["music_profile"] for r in loop22_rows)),
            "plan_only_request_bound_identities": sum(1 for r in loop22_rows if r["request_id"] and r["request_hash"] and r["plan_hash"] and r["adapter_envelope_hash"] and r["bridge_record_hash"] and r["family_stage_contract_sha256"]),
            "seed_domains_separate": all(r["gameplay_seed"] != r["music_seed"] for r in loop22_rows),
            "status": "PASS_27_R1P_RECEIPTS_PROJECTED_22_NON_PILOT_SELECTORS_PLAN_ONLY",
            "rows": loop22_rows,
            "all_27_receipt_hashes": [{"receipt_index": r["receipt_index"], "family_id": r["family_id"], "grammar_id": r["grammar_id"], "receipt_sha256": r["receipt_sha256"]} for r in all_rows],
        },
        "active_source_pins": {
            "verified": sum(1 for row in source_pin_results if row["status"] == "PASS"),
            "total": len(source_pin_results),
            "prior_17_audit_pins_rechecked": sum(1 for row in prior_pin_results if row["status"] == "PASS"),
            "prior_17_audit_pins_total": len(prior_pin_results),
            "drift_count": len(source_pin_drift),
            "rows": source_pin_results,
            "prior_audit_rows": prior_pin_results,
            "drift": source_pin_drift,
        },
        "policy_fingerprints": {
            "captured": len(policy_rows),
            "total": len(POLICIES),
            "r1p_pin_mismatch_count": len(policy_pin_drift),
            "rows": policy_rows,
            "old_archive_pin_mismatches": policy_pin_drift,
            "operator_decisions": "REQUIRED_FOR_EACH_CURRENT_HASH",
        },
        "execution_authority": {
            "operator_project_continuation_approval": "RECORDED_2026_11_09",
            "hash_specific_policy_decisions": "PENDING",
            "loop22_execution_amendment": "NOT_ISSUED",
            "loop22_media_authorization": "NOT_GRANTED_BY_THIS_READ_ONLY_AUDIT",
            "renderer": "OFF",
            "release_authority": "NONE",
        },
        "processes_invoked": {
            "git": False, "tests": False, "godot": False, "c11c_launchers": False,
            "music_generation": False, "ffmpeg": False, "ffprobe": False,
            "renderer": False, "dispatch": False, "media_created": False, "media_modified": False,
        },
        "blocking_conditions": blocking,
        "next_gate": "Record explicit current-hash decisions in the V2 docket; then prepare a separate 22-selector / 44-output execution amendment. Do not launch media from this audit.",
    }
    # Output a canonical report digest and a raw file checksum sidecar.
    report["report_sha256"] = sha256_bytes(canonical_json_bytes(report))
    report_path = output / "LOOP22_R1P_POLICY_REFRESH_REPORT_V1.json"
    report_raw = (json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    report_path.write_bytes(report_raw)
    (output / "LOOP22_R1P_POLICY_REFRESH_REPORT_V1.json.sha256").write_text(f"{sha256_bytes(report_raw)}  {report_path.name}\n", encoding="ascii")
    projection_fields = [
        "family_id", "grammar_id", "music_profile", "gameplay_seed", "music_seed", "loop_cycles",
        "duration_seconds", "fps", "frame_count", "receipt_index", "receipt_sha256", "payload_sha256",
        "request_id", "request_hash", "plan_hash", "editorial_hash", "bridge_record_hash",
        "adapter_envelope_hash", "family_stage_contract_sha256", "family_prototype_path", "family_prototype_sha256",
        "family_launcher_path", "family_launcher_sha256", "r1p_status", "request_compatibility",
    ]
    write_csv(output / "LOOP22_R1P_22_SELECTOR_PROJECTION.csv", loop22_rows, projection_fields)
    policy_fields = ["group", "label", "path", "sha256", "bytes", "schema", "status", "r1p_archive_sha256", "r1p_archive_bytes", "matches_r1p_archive_pin", "decision_gate", "decision", "sha_confirmed"]
    write_csv(output / "CURRENT_POLICY_FINGERPRINTS_AND_DECISIONS.csv", policy_rows, policy_fields)
    docket = build_docket(policy_rows, run_id, closeout)
    (output / "C11E_E4B_LOOP_POLICY_DECISION_DOCKET_V2.md").write_text(docket, encoding="utf-8")
    runner_receipt = {
        "schema": "C11E-E4B-LOOP22-R1P-POLICY-REFRESH-RUNNER-RECEIPT-V1",
        "run_id": run_id,
        "status": status,
        "report_sha256": report["report_sha256"],
        "r1p_receipts_verified": len(all_rows),
        "loop22_selectors_projected": len(loop22_rows),
        "policy_fingerprints_captured": len(policy_rows),
        "active_r1p_source_pins_verified": sum(1 for row in source_pin_results if row["status"] == "PASS"),
        "active_r1p_source_pins_total": len(source_pin_results),
        "prior_source_audit_pins_rechecked": sum(1 for row in prior_pin_results if row["status"] == "PASS"),
        "prior_source_audit_pins_total": len(prior_pin_results),
        "tests_invoked": False, "git_invoked": False, "godot_invoked": False,
        "launchers_invoked": False, "music_invoked": False, "ffmpeg_invoked": False,
        "ffprobe_invoked": False, "renderer_invoked": False, "media_created": False,
        "media_modified": False, "c11c_source_modified": False,
        "loop22_media_authorization": "NOT_GRANTED",
        "release_authority": "NONE",
    }
    runner_path = output / "PROJECTOR_RECEIPT.json"
    runner_path.write_text(json.dumps(runner_receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Evidence ZIP is additive and contains only projection/report/docket artifacts.
    evidence_zip = output / f"{run_id}_EVIDENCE.zip"
    with zipfile.ZipFile(evidence_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(output.iterdir()):
            if path.is_file() and path != evidence_zip:
                zf.write(path, path.name)
    if zipfile.ZipFile(evidence_zip).testzip() is not None:
        raise AuditError("OUTPUT_EVIDENCE_ZIP_CRC_FAILURE")
    evidence_sha = sha256_file(evidence_zip)
    evidence_zip.with_suffix(evidence_zip.suffix + ".sha256").write_text(f"{evidence_sha}  {evidence_zip.name}\n", encoding="ascii")
    # The report inside the evidence ZIP is byte-identical to the report on disk.
    # ZIP identity is emitted on stdout and in a separate SHA sidecar; it is not
    # inserted into its own archived report, avoiding a circular hash dependency.
    print("========== C11-E E4B LOOP22 R1P PROJECTION / POLICY REFRESH V1 ==========")
    print(f"STATUS={status}")
    print(f"R1P_RECEIPTS_VERIFIED={len(all_rows)}/27")
    print(f"LOOP22_PROJECTED={len(loop22_rows)}/22")
    print(f"PLANNED_AB_OUTPUT_SLOTS={len(loop22_rows)*2}")
    print(f"R1P_SOURCE_PINS_VERIFIED={sum(1 for row in source_pin_results if row['status'] == 'PASS')}/{len(source_pin_results)}")
    print(f"PRIOR_SOURCE_AUDIT_PINS_RECHECKED={sum(1 for row in prior_pin_results if row['status'] == 'PASS')}/{len(prior_pin_results)}")
    print(f"CURRENT_POLICY_FINGERPRINTS={len(policy_rows)}/5")
    print(f"POLICY_ARCHIVE_PIN_MISMATCHES={len(policy_pin_drift)}; OPERATOR_HASH_DECISIONS=REQUIRED")
    print("REQUEST_BOUND_IDENTITY=PLAN_ONLY; D4_EXECUTABLE_COMPATIBILITY=NOT_CLAIMED")
    print("GIT=False; GODOT=False; LAUNCHERS=False; MUSIC=False; FFMPEG=False; FFPROBE=False; RENDERER=False; DISPATCH=False; MEDIA=False")
    print("LOOP22_MEDIA_AUTHORIZATION=NOT_GRANTED; RELEASE_AUTHORITY=NONE")
    print(f"REPORT={report_path}")
    print(f"REPORT_CANONICAL_SHA256={report['report_sha256']}")
    print(f"REPORT_FILE_SHA256={sha256_file(report_path)}")
    print(f"EVIDENCE_ZIP={evidence_zip}")
    print(f"EVIDENCE_ZIP_SHA256={evidence_sha}")
    return report, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--source-audit", default=str(AUDIT_REPORT_REL))
    parser.add_argument("--output-root", default="artifacts/tests/c11e/e4b_loop22_r1p_policy_refresh")
    args = parser.parse_args()
    root = Path(args.project_root)
    audit_path = (root / normalize_rel(args.source_audit)).resolve()
    output_root = root / normalize_rel(args.output_root)
    try:
        report, output = run_audit(root, audit_path, output_root)
    except (AuditError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"STATUS=BLOCKED_FAIL_CLOSED; ERROR={exc}", file=sys.stderr)
        return 2
    return 0 if report["status"].startswith("PASS_") else 3


if __name__ == "__main__":
    raise SystemExit(main())
