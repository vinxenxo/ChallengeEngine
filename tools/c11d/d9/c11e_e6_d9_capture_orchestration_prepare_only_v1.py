#!/usr/bin/env python3
"""C11-E E6 D9 multi-selector capture orchestration PREPARE_ONLY V1.

Builds a six-group logical capture plan from the accepted D9 V2 linkage manifest.
Each selector has one immutable visual-source capture shared by A/B/C probe rows.
This tool does not build runtime commands, start processes, reserve BatchIds, invoke
Godot/FFmpeg/FFprobe, generate audio, mux, render, dispatch, or create media.
Only a new JSON manifest and receipt (plus SHA-256 sidecars) are written beneath
artifacts/tests/c11e/e6_d9_capture_orchestration_prepare_only/.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA_MANIFEST = "C11E-E6-D9-CAPTURE-ORCHESTRATION-PREPARE-ONLY-MANIFEST-V1"
SCHEMA_RECEIPT = "C11E-E6-D9-CAPTURE-ORCHESTRATION-PREPARE-ONLY-RECEIPT-V1"
PROJECT_ROOT_DEFAULT = Path(__file__).resolve().parents[3]

ORCHESTRATOR_REL = Path("tools/c11d/d9/c11e_e6_d9_capture_orchestration_prepare_only_v1.py")
ROUTE_AUDIT_SCRIPT_NAME = "c11e_e6_challenge_capture_route_audit_v1.py"
ROUTE_AUDIT_SCRIPT_REL = Path("tools/c11d/d9") / ROUTE_AUDIT_SCRIPT_NAME
ROUTE_AUDIT_SCRIPT_SHA256 = "288fdf5b9bc579e766d6a57e07ee2199c6eaea9054ab8b355f9a38db3fab978d"

D9_RUN_ID = "E6D9PREP_20261117T202442Z_BCCD3C39"
D9_ROOT_REL = Path("artifacts/tests/c11e/e6_d9_prepare_only") / D9_RUN_ID
D9_MANIFEST_REL = D9_ROOT_REL / "E6_D9_CHALLENGE_PREPARE_ONLY_MANIFEST_V2.json"
D9_MANIFEST_SHA256 = "11cbf8fd1c2862d0004dbfd28bd27c78cf882a7db725d571484617862af35c18"
D9_RECEIPT_REL = D9_ROOT_REL / "E6_D9_CHALLENGE_PREPARE_ONLY_RECEIPT_V2.json"
D9_RECEIPT_SHA256 = "53f01752de6928044707cb08dda04e3f2ab5f87f9f177daac70737ea039b4f88"

HYDRATION_RUN_ID = "E6HYDRATE_20261118T073344Z_1A9D7C52"
HYDRATION_REPORT_REL = (
    Path("artifacts/tests/c11e/e6_reuse_evidence_hydration_v2")
    / HYDRATION_RUN_ID
    / f"{HYDRATION_RUN_ID}_REPORT_V2.json"
)
HYDRATION_REPORT_SHA256 = "11f0eeba941f4740759132b3ba984eecf80c68a69aad27fe605a81a4ff8f5a77"

FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D4_8_SHA256 = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
PIN_ACCEPTANCE_REL = Path(
    "artifacts/tests/c11e/e6_runtime_dependency_pin_acceptance/"
    "E6DEPPINACCEPT_20261117T141326Z_C980FF81/"
    "E6_RUNTIME_DEPENDENCY_PIN_ACCEPTANCE_RECEIPT_V1.json"
)
PIN_ACCEPTANCE_SHA256 = "41c62276465803dfb289a91b8a7f74c9b57c213dbad64c1323d6f626e3b2edd0"
PLAN_RUN_ID = "E6CHPLAN_20261117T001949Z_D87FADA4"
PLAN_ROOT_REL = Path("artifacts/tests/c11e/e6_challenge_plan_only") / PLAN_RUN_ID
PLAN_RECEIPT_REL = PLAN_ROOT_REL / "E6_CHALLENGE_PLAN_ONLY_RECEIPT_V1.json"
PLAN_RECEIPT_SHA256 = "8fcd63fcfd04df9446f20c5ea8dd1646f169051403f2ee04a356997cd3dd257e"
PLAN_JSON_REL = PLAN_ROOT_REL / "E6_CHALLENGE_SIX_SELECTOR_PLAN_V1.json"
PLAN_JSON_SHA256 = "ef86fe532cd6c92c3c2dc9937a65d149dc699fcd6c0295382a135413f04af6ae"
CONTRACT_RECEIPT_REL = Path(
    "artifacts/tests/c11e/e6_challenge_consumer_contract/"
    "E6CHCONTRACT_20261117T005638Z_B3412977/"
    "E6_CHALLENGE_CONSUMER_CONTRACT_PREFLIGHT_RECEIPT_V1.json"
)
CONTRACT_RECEIPT_SHA256 = "e22abc1fc1779f60dd48abf4cdbf7960b7a3a02b2ef9bc0a7e975053f5effce8"

SELECTED_IDS = (
    "CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004",
    "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007",
)
LABELS = ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED")
EXPECTED_GAMEPLAY_SEEDS = {
    "CHALLENGE_001": 193847,
    "CHALLENGE_002": 987654,
    "CHALLENGE_004": 314159,
    "CHALLENGE_005": 998877,
    "CHALLENGE_006": 884422,
    "CHALLENGE_007": 7770001,
}
EXPECTED_SOURCE_FRAMES = {
    "CHALLENGE_001": 540, "CHALLENGE_002": 600, "CHALLENGE_004": 900,
    "CHALLENGE_005": 420, "CHALLENGE_006": 540, "CHALLENGE_007": 600,
}
EXPECTED_DEFINITION_SHA256 = {
    "CHALLENGE_001": "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea",
    "CHALLENGE_002": "db5d70a28c460e986e785c6787447529372ac5ea3b5a7ff0507667decbe2a160",
    "CHALLENGE_004": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "CHALLENGE_005": "e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30",
    "CHALLENGE_006": "2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694",
    "CHALLENGE_007": "269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61",
}
EXPECTED_HISTORICAL_FAILURES = {
    (
        "tools/c11d/d9/universal_editorial_model.py",
        "5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5",
        "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd",
    ),
    (
        "c11c-suite/c11c-producer/c11e_production_service.py",
        "348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951",
        "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87",
    ),
}

OUTPUT_REL = Path("artifacts/tests/c11e/e6_d9_capture_orchestration_prepare_only")


class PlanError(RuntimeError):
    """Raised when any source, evidence, or governance predicate is not met."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise PlanError(f"INVALID_JSON:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise PlanError(f"EXPECTED_JSON_OBJECT:{path}")
    return value


def contained_path(root: Path, relative: str | Path) -> Path:
    raw = str(relative).replace("\\", "/")
    rel = Path(raw)
    if rel.is_absolute() or ".." in rel.parts or not raw.strip():
        raise PlanError(f"UNSAFE_RELATIVE_PATH:{relative}")
    target = (root / Path(*rel.parts)).resolve()
    base = root.resolve()
    if target != base and base not in target.parents:
        raise PlanError(f"PATH_ESCAPES_PROJECT_ROOT:{relative}")
    return target


def verify_file(root: Path, relative: str | Path, expected_sha: str, label: str, sidecar: bool = True) -> dict[str, Any]:
    path = contained_path(root, relative)
    if not path.is_file():
        raise PlanError(f"{label}_MISSING:{relative}")
    actual = sha256_file(path)
    if actual != expected_sha:
        raise PlanError(f"{label}_SHA256_MISMATCH:{relative}:{actual}")
    if sidecar:
        side = Path(str(path) + ".sha256")
        if not side.is_file():
            raise PlanError(f"{label}_SIDECAR_MISSING:{relative}")
        token = side.read_text(encoding="ascii").strip().split()
        if not token or token[0].lower() != expected_sha:
            raise PlanError(f"{label}_SIDECAR_MISMATCH:{relative}")
    return {"path": str(relative).replace("\\", "/"), "sha256": actual, "bytes": path.stat().st_size, "status": "PASS"}


def phase_signature(rows: Any, expected_frames: int) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or len(rows) != 4:
        raise PlanError("EXPECTED_FOUR_CANONICAL_PHASE_RANGES")
    result = []
    cursor = 0
    expected_names = ["HOOK", "GAME", "REVEAL", "CTA"]
    for row, expected_name in zip(rows, expected_names):
        if not isinstance(row, Mapping):
            raise PlanError("MALFORMED_PHASE_RANGE")
        start, end = row.get("start_frame"), row.get("end_frame")
        if isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int) or not isinstance(end, int):
            raise PlanError("PHASE_INDICES_NOT_INTEGERS")
        if row.get("phase") != expected_name or start != cursor or end < start:
            raise PlanError("PHASE_RANGES_NOT_CONTIGUOUS_HALF_OPEN")
        result.append({"phase": expected_name, "start_frame": start, "end_frame": end})
        cursor = end
    if cursor != expected_frames:
        raise PlanError(f"PHASE_SUM_MISMATCH:{cursor}:{expected_frames}")
    return result


def load_route_audit_module(script_path: Path):
    if not script_path.is_file():
        raise PlanError(f"ROUTE_AUDIT_SCRIPT_MISSING:{script_path}")
    expected = ROUTE_AUDIT_SCRIPT_SHA256
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise PlanError("ROUTE_AUDIT_SCRIPT_PIN_NOT_CONFIGURED")
    actual = sha256_file(script_path)
    if actual != expected:
        raise PlanError(f"ROUTE_AUDIT_SCRIPT_PIN_MISMATCH:{actual}")
    spec = importlib.util.spec_from_file_location("c11e_e6_route_audit_pinned", script_path)
    if spec is None or spec.loader is None:
        raise PlanError("ROUTE_AUDIT_IMPORT_SPEC_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, "audit_route", None)):
        raise PlanError("ROUTE_AUDIT_API_MISSING")
    return module


def validate_hydration_report_content(report: Mapping[str, Any]) -> dict[str, Any]:
    if report.get("run_id") != HYDRATION_RUN_ID or report.get("status") != "BLOCKED_E6_REUSE_EVIDENCE_INCOMPLETE":
        raise PlanError("HYDRATION_REPORT_RUN_OR_STATUS_MISMATCH")
    if report.get("check_count") != 1803 or report.get("passed_checks") != 1801 or report.get("failed_checks") != 2:
        raise PlanError("HYDRATION_REPORT_COUNTS_MISMATCH")
    if report.get("failure_categories") != {"historical_source_pin_divergence": 2, "other_failures": 0}:
        raise PlanError("HYDRATION_REPORT_FAILURE_CATEGORIES_MISMATCH")
    failures = {
        (str(x.get("path")), str(x.get("expected_sha256")), str(x.get("actual_sha256")))
        for x in report.get("checks", []) if isinstance(x, dict) and x.get("status") != "PASS"
    }
    if failures != EXPECTED_HISTORICAL_FAILURES:
        raise PlanError("HYDRATION_REPORT_FAILURE_SET_MISMATCH_NO_AUTO_WAIVER")
    counts = report.get("counts", {})
    expected_counts = {
        "challenge004_nested_files": 34,
        "drill_nested_files": 1680,
        "drill_receipts": 6,
        "loop22_nested_files": 8,
        "r1v_loop_slots": 5,
        "source_pins": 33,
    }
    if counts != expected_counts:
        raise PlanError("HYDRATION_REPORT_EVIDENCE_COUNTS_MISMATCH")
    gov = report.get("governance", {})
    if (
        gov.get("source_checkout_mutated") is not False
        or gov.get("godot_invoked") is not False
        or gov.get("ffmpeg_invoked") is not False
        or gov.get("ffprobe_invoked") is not False
        or gov.get("media_created") is not False
        or gov.get("batch_id_consumed") is not False
        or gov.get("release_authority") != "NONE"
    ):
        raise PlanError("HYDRATION_REPORT_CROSSED_EXECUTION_BOUNDARY")
    return {
        "run_id": HYDRATION_RUN_ID,
        "sha256": HYDRATION_REPORT_SHA256,
        "checks": "1801/1803",
        "failures": 2,
        "failure_disposition": "CH004_REUSE_DISALLOWED_PENDING_HISTORICAL_SOURCE_PIN_ADJUDICATION",
        "drill_receipts": "6/6",
        "drill_nested_hashes": 1680,
        "r1v_loop_slots": "5/5",
        "loop22_nested_hashes": 8,
    }


def verify_hydration_report(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    report_row = verify_file(root, HYDRATION_REPORT_REL, HYDRATION_REPORT_SHA256, "E6_REUSE_HYDRATION_REPORT")
    report = load_json(contained_path(root, HYDRATION_REPORT_REL))
    summary = validate_hydration_report_content(report)
    return report_row, summary


def verify_d9_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    d9_manifest_row = verify_file(root, D9_MANIFEST_REL, D9_MANIFEST_SHA256, "D9_PREPARE_ONLY_MANIFEST")
    d9_receipt_row = verify_file(root, D9_RECEIPT_REL, D9_RECEIPT_SHA256, "D9_PREPARE_ONLY_RECEIPT")
    manifest = load_json(contained_path(root, D9_MANIFEST_REL))
    receipt = load_json(contained_path(root, D9_RECEIPT_REL))
    if manifest.get("run_id") != D9_RUN_ID or manifest.get("status") != "PREPARED_ONLY_LINKAGE_COMPLETE_NOT_FROZEN_FOR_MEDIA":
        raise PlanError("D9_MANIFEST_STATUS_OR_IDENTITY_MISMATCH")
    if receipt.get("run_id") != D9_RUN_ID or receipt.get("status") != "PASS_D9_PREPARE_ONLY_18_INTENTS_18_ENVELOPES_LINKED_EXECUTION_HELD":
        raise PlanError("D9_RECEIPT_STATUS_OR_IDENTITY_MISMATCH")
    if receipt.get("manifest_sha256") != D9_MANIFEST_SHA256:
        raise PlanError("D9_RECEIPT_MANIFEST_HASH_LINK_MISMATCH")
    if receipt.get("source_pin_count") != 33 or receipt.get("linked_e1_intents") != 18 or receipt.get("linked_d_envelopes") != 18:
        raise PlanError("D9_RECEIPT_CARDINALITY_MISMATCH")

    lineage = manifest.get("lineage", {})
    if lineage.get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA256 or lineage.get("d4_8_policy_sha256") != D4_8_SHA256:
        raise PlanError("D9_LINEAGE_GOVERNANCE_HASH_MISMATCH")
    if manifest.get("selected_ids") != list(SELECTED_IDS):
        raise PlanError("D9_SELECTOR_SET_MISMATCH")
    if manifest.get("smoke18_counting", {}).get("smoke18_total") != 18:
        raise PlanError("SMOKE18_TOP_LEVEL_DENOMINATOR_MISMATCH")

    pins = manifest.get("source_authority", {}).get("accepted_source_pins", [])
    if len(pins) != 33:
        raise PlanError("EXPECTED_33_ACCEPTED_SOURCE_PINS")
    pin_paths = set()
    for pin in pins:
        if not isinstance(pin, dict):
            raise PlanError("MALFORMED_SOURCE_PIN_ROW")
        rel = str(pin.get("path", ""))
        if not rel or rel in pin_paths:
            raise PlanError(f"EMPTY_OR_DUPLICATE_SOURCE_PIN:{rel}")
        pin_paths.add(rel)
        if pin.get("status") != "PASS":
            raise PlanError(f"SOURCE_PIN_RECEIPT_ROW_NOT_PASS:{rel}")
        actual = verify_file(root, rel, str(pin.get("sha256", "")), "ACCEPTED_SOURCE_PIN", sidecar=False)
        if pin.get("bytes") is not None and actual["bytes"] != int(pin["bytes"]):
            raise PlanError(f"SOURCE_PIN_BYTE_COUNT_MISMATCH:{rel}")
    dep = manifest.get("source_authority", {}).get("dependency_pin_acceptance_receipt", {})
    verify_file(root, dep.get("path", ""), PIN_ACCEPTANCE_SHA256, "DEPENDENCY_PIN_ACCEPTANCE_RECEIPT")

    plan_receipt = verify_file(root, PLAN_RECEIPT_REL, PLAN_RECEIPT_SHA256, "PREDECESSOR_PLAN_RECEIPT")
    plan_json = verify_file(root, PLAN_JSON_REL, PLAN_JSON_SHA256, "PREDECESSOR_PLAN_JSON")
    contract_receipt = verify_file(root, CONTRACT_RECEIPT_REL, CONTRACT_RECEIPT_SHA256, "PREDECESSOR_CONSUMER_CONTRACT_RECEIPT")
    predecessor_rows = manifest.get("predecessors", {})
    for key, expected in (("plan_only_receipt", plan_receipt), ("plan_json", plan_json), ("consumer_contract_receipt", contract_receipt)):
        row = predecessor_rows.get(key, {})
        if row.get("sha256") != expected["sha256"] or row.get("path") != expected["path"]:
            raise PlanError(f"D9_PREDECESSOR_LINEAGE_MISMATCH:{key}")

    receipt_execution = receipt.get("execution", {})
    receipt_false_flags = ("e6_test_only_authorized", "godot_invoked", "renderer_invoked", "ffmpeg_invoked", "ffprobe_invoked", "audio_generated", "mux_invoked", "media_created", "production_dispatch", "new_batch_id_consumed")
    if any(receipt_execution.get(k) is not False for k in receipt_false_flags) or receipt_execution.get("release_authority") != "NONE":
        raise PlanError("D9_RECEIPT_EXECUTION_BOUNDARY_MISMATCH")

    governance = manifest.get("governance", {})
    expected_false = ["dispatch", "media_created", "godot_invoked", "ffmpeg_invoked", "ffprobe_invoked", "audio_generated", "mux_invoked", "new_batch_id_consumed", "e6_test_only_authorized"]
    if any(governance.get(k) is not False for k in expected_false):
        raise PlanError("D9_MANIFEST_GOVERNANCE_FLAGS_NOT_HELD")
    if governance.get("e1") != "PREPARE_ONLY" or governance.get("d9") != "PREPARE_ONLY" or governance.get("d4_8") != "BLOCKED" or governance.get("renderer") != "OFF" or governance.get("release_authority") != "NONE":
        raise PlanError("D9_MANIFEST_GOVERNANCE_STATE_MISMATCH")
    return d9_manifest_row, d9_receipt_row, manifest.get("linked_probes", [])


def verify_probes(root: Path, probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(probes) != 18:
        raise PlanError(f"EXPECTED_18_LINKED_PROBES:{len(probes)}")
    grouped: dict[str, dict[str, dict[str, Any]]] = {key: {} for key in SELECTED_IDS}
    checked = []
    for row in probes:
        challenge_id = row.get("challenge_id")
        label = row.get("label")
        if challenge_id not in grouped or label not in LABELS or label in grouped[challenge_id]:
            raise PlanError(f"UNKNOWN_OR_DUPLICATE_PROBE:{challenge_id}:{label}")
        intent_path = str(row.get("intent_path", ""))
        envelope_path = str(row.get("envelope_path", ""))
        intent_file = verify_file(root, intent_path, str(row.get("intent_sha256", "")), "E1_INTENT", sidecar=False)
        envelope_file = verify_file(root, envelope_path, str(row.get("envelope_sha256", "")), "D_ENVELOPE", sidecar=False)
        intent = load_json(contained_path(root, intent_path))
        envelope = load_json(contained_path(root, envelope_path))
        expected_seed = EXPECTED_GAMEPLAY_SEEDS[challenge_id]
        expected_frames = EXPECTED_SOURCE_FRAMES[challenge_id]
        music_seed = row.get("music_seed")
        expected_music_seed = 840001 if label in ("A", "B_REPEAT") else 840002
        if row.get("gameplay_seed") != expected_seed or intent.get("seed_domains", {}).get("gameplay", {}).get("value") != expected_seed:
            raise PlanError(f"GAMEPLAY_SEED_MISMATCH:{challenge_id}:{label}")
        if music_seed != expected_music_seed or intent.get("seed_domains", {}).get("music", {}).get("value") != expected_music_seed:
            raise PlanError(f"MUSIC_SEED_PROPOSAL_MISMATCH:{challenge_id}:{label}")
        if intent.get("request_origin") != "TEST" or intent.get("request", {}).get("selection", {}).get("variant_id") != challenge_id:
            raise PlanError(f"E1_INTENT_IDENTITY_MISMATCH:{challenge_id}:{label}")
        if intent.get("request", {}).get("request_id") != row.get("request_id"):
            raise PlanError(f"E1_REQUEST_ID_MISMATCH:{challenge_id}:{label}")
        if intent.get("identity", {}).get("intent_hash") != row.get("intent_hash"):
            raise PlanError(f"E1_INTENT_HASH_MISMATCH:{challenge_id}:{label}")
        music = intent.get("music_contract", {})
        engine_request = music.get("engine_request", {})
        if (
            engine_request.get("music_seed") != expected_music_seed
            or engine_request.get("tempo_bpm") is not None
            or engine_request.get("duration_seconds") is not None
            or music.get("engine_invoked") is not False
            or music.get("audio_created") is not False
        ):
            raise PlanError(f"E1_MUSIC_CONTRACT_BOUNDARY_MISMATCH:{challenge_id}:{label}")
        boundary = intent.get("execution_boundary", {})
        if any(boundary.get(k) is not False for k in ("dispatch_authorized", "renderer_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created")) or boundary.get("release_authority") != "NONE" or boundary.get("d4_8") != "BLOCKED":
            raise PlanError(f"E1_EXECUTION_BOUNDARY_MISMATCH:{challenge_id}:{label}")
        if envelope.get("challenge_id") != challenge_id or envelope.get("request_id") != row.get("request_id"):
            raise PlanError(f"D_ENVELOPE_IDENTITY_MISMATCH:{challenge_id}:{label}")
        if envelope.get("intent_hash") != row.get("intent_hash") or envelope.get("e1_intent", {}).get("identity", {}).get("intent_hash") != row.get("intent_hash"):
            raise PlanError(f"D_ENVELOPE_INTENT_LINK_MISMATCH:{challenge_id}:{label}")
        timebase = envelope.get("source_timebase", {})
        if timebase != {"fps": 60, "total_frames": expected_frames, "kind": "SOURCE_FRAME_INDEX"} or row.get("source_fps") != 60 or row.get("source_frames") != expected_frames:
            raise PlanError(f"SOURCE_TIMEBASE_MISMATCH:{challenge_id}:{label}")
        phases = phase_signature(envelope.get("source_phase_ranges"), expected_frames)
        row_phases = phase_signature(row.get("phase_ranges"), expected_frames)
        if phases != row_phases:
            raise PlanError(f"PHASE_RANGE_LINK_MISMATCH:{challenge_id}:{label}")
        if envelope.get("status") != "PREPARED_E1_NOT_DISPATCHED" or envelope.get("governance", {}).get("media_created") is not False:
            raise PlanError(f"D_ENVELOPE_GOVERNANCE_MISMATCH:{challenge_id}:{label}")

        normalized = {
            "challenge_id": challenge_id,
            "label": label,
            "gameplay_seed": expected_seed,
            "music_seed_proposal": expected_music_seed,
            "request_id": row["request_id"],
            "intent_hash": row["intent_hash"],
            "intent_sha256": intent_file["sha256"],
            "intent_path": intent_path,
            "envelope_sha256": envelope_file["sha256"],
            "envelope_path": envelope_path,
            "source_fps": 60,
            "source_frames": expected_frames,
            "phase_ranges": phases,
        }
        grouped[challenge_id][label] = normalized
        checked.append(normalized)

    for challenge_id, group in grouped.items():
        if set(group) != set(LABELS):
            raise PlanError(f"PROBE_LABEL_CARDINALITY_MISMATCH:{challenge_id}")
        a, b, c = group["A"], group["B_REPEAT"], group["C_CHANGED_MUSIC_SEED"]
        if a["gameplay_seed"] != b["gameplay_seed"] or a["music_seed_proposal"] != b["music_seed_proposal"]:
            raise PlanError(f"A_B_REPEATABILITY_MISMATCH:{challenge_id}")
        if c["gameplay_seed"] != a["gameplay_seed"] or c["music_seed_proposal"] == a["music_seed_proposal"]:
            raise PlanError(f"C_MUST_CHANGE_MUSIC_ONLY:{challenge_id}")
        if not (a["phase_ranges"] == b["phase_ranges"] == c["phase_ranges"]):
            raise PlanError(f"A_B_C_PHASE_RANGES_DIFFER:{challenge_id}")
    return checked


def build_capture_groups(root: Path, probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = []
    for challenge_id in SELECTED_IDS:
        rows = {r["label"]: r for r in probes if r["challenge_id"] == challenge_id}
        frames = EXPECTED_SOURCE_FRAMES[challenge_id]
        definition_rel = f"challenges/{challenge_id}.json"
        definition = verify_file(root, definition_rel, EXPECTED_DEFINITION_SHA256[challenge_id], "CHALLENGE_CANONICAL_DEFINITION", sidecar=False)
        if challenge_id == "CHALLENGE_004":
            reuse_disposition = "FRESH_SOURCE_CAPTURE_REQUIRED_HISTORICAL_SOURCE_PIN_DIVERGENCE_NO_WAIVER"
        else:
            reuse_disposition = "FRESH_SOURCE_CAPTURE_REQUIRED_NO_ACCEPTED_E6_CHALLENGE_AV_REUSE"
        groups.append({
            "scenario_id": "E6-CH-" + challenge_id[-3:],
            "challenge_id": challenge_id,
            "canonical_definition": definition,
            "gameplay_seed": EXPECTED_GAMEPLAY_SEEDS[challenge_id],
            "source_timebase": {"fps": 60, "frames": frames, "duration_seconds": frames / 60},
            "review_timebase_proposal": {"fps": 30, "frames": frames // 2, "duration_seconds": frames / 60, "status": "PROPOSAL_REQUIRES_FFPROBE_NOT_AUTHORIZED"},
            "visual_source": {
                "logical_capture_id": f"{challenge_id}_D_COMPOSITED_SOURCE",
                "logical_capture_count": 1,
                "shared_by_probe_labels": list(LABELS),
                "planned_evidence_path": f"artifacts/tests/c11e/e6_challenge_capture/{challenge_id}/D_COMPOSITED_SOURCE",
                "path_status": "PROPOSED_NOT_CREATED",
                "capture_authorized": False,
            },
            "audio_probe_variants": [
                {
                    "label": label,
                    "request_id": rows[label]["request_id"],
                    "intent_hash": rows[label]["intent_hash"],
                    "intent_sha256": rows[label]["intent_sha256"],
                    "envelope_sha256": rows[label]["envelope_sha256"],
                    "gameplay_seed": rows[label]["gameplay_seed"],
                    "music_seed_proposal": rows[label]["music_seed_proposal"],
                    "music_seed_status": "HISTORICAL_TEST_FIXTURE_PROPOSAL_ONLY_NOT_AUTHORIZED",
                    "shares_visual_source": True,
                    "audio_authorized": False,
                }
                for label in LABELS
            ],
            "reuse_disposition": reuse_disposition,
        })
    return groups


def build_plan(root: Path) -> dict[str, Any]:
    root = root.resolve()
    self_path = Path(__file__).resolve()
    try:
        self_rel = self_path.relative_to(root).as_posix()
    except ValueError as exc:
        raise PlanError("ORCHESTRATOR_MUST_RUN_FROM_ACTIVE_CHECKOUT") from exc
    if self_rel != ORCHESTRATOR_REL.as_posix():
        raise PlanError(f"ORCHESTRATOR_PATH_MISMATCH:{self_rel}")
    self_source = {"path": self_rel, "sha256": sha256_file(self_path), "bytes": self_path.stat().st_size, "status": "OBSERVED_NEW_TOOLING_NOT_YET_IN_ACCEPTED_33_PINS"}
    route_audit_script = contained_path(root, ROUTE_AUDIT_SCRIPT_REL)
    route_module = load_route_audit_module(route_audit_script)
    route_source = {"path": ROUTE_AUDIT_SCRIPT_REL.as_posix(), "sha256": sha256_file(route_audit_script), "bytes": route_audit_script.stat().st_size, "status": "OBSERVED_NEW_TOOLING_NOT_YET_IN_ACCEPTED_33_PINS"}
    route_report = route_module.audit_route(root)
    route_counts = route_report.get("counts", {})
    if route_report.get("status") != "PASS_STATIC_ROUTE_AUDIT_EXECUTION_HELD":
        raise PlanError("STATIC_CHALLENGE_ROUTE_AUDIT_NOT_PASS")
    if route_counts.get("contract_source_pins_passed") != 24 or route_counts.get("selected_challenge_definitions_passed") != 6 or route_counts.get("static_route_checks_passed") != 18:
        raise PlanError("STATIC_CHALLENGE_ROUTE_AUDIT_COUNTS_MISMATCH")
    if route_report.get("execution", {}).get("godot_invoked") is not False or route_report.get("execution", {}).get("media_created") is not False:
        raise PlanError("ROUTE_AUDIT_CROSSED_EXECUTION_BOUNDARY")

    frozen = verify_file(root, "release/C11C_FREEZE_PACKAGE_MANIFEST.json", FROZEN_MANIFEST_SHA256, "FROZEN_C11C_MANIFEST", sidecar=False)
    d48 = verify_file(root, "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json", D4_8_SHA256, "D4_8_V2_POLICY", sidecar=False)
    pin_receipt = verify_file(root, PIN_ACCEPTANCE_REL, PIN_ACCEPTANCE_SHA256, "E6_DEPENDENCY_PIN_ACCEPTANCE_RECEIPT")
    d9_manifest_row, d9_receipt_row, raw_probes = verify_d9_inputs(root)
    hydration_row, hydration_summary = verify_hydration_report(root)
    probes = verify_probes(root, raw_probes)
    groups = build_capture_groups(root, probes)

    blockers = list(route_report.get("blockers", []))
    blockers.extend([
        "NINE_ADDITIONAL_ROUTE_DEPENDENCIES_OBSERVED_BUT_NOT_ACCEPTED_SOURCE_PINS",
        "CH004_HISTORICAL_SOURCE_PIN_DIVERGENCE_REQUIRES_EXPLICIT_ADJUDICATION_OR_FRESH_CAPTURE",
    ])
    blockers = list(dict.fromkeys(blockers))

    return {
        "schema": SCHEMA_MANIFEST,
        "schema_version": "1.0",
        "status": "PASS_D9_MULTISELECTOR_CAPTURE_GROUP_PLAN_READY_EXECUTION_HELD",
        "run_id": "E6CAPPLAN_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper(),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "STATIC_PREPARE_ONLY_CAPTURE_GROUPING_NO_RUNTIME_COMMANDS_NO_MEDIA",
        "baseline": {"active_checkout_is_authority": True, "nightly_is_reference_baseline_only": True, "frozen_c11c_manifest": frozen, "d4_8_policy": d48},
        "predecessors": {
            "d9_prepare_only_manifest": d9_manifest_row,
            "d9_prepare_only_receipt": d9_receipt_row,
            "dependency_pin_acceptance_receipt": pin_receipt,
            "reuse_hydration_report": hydration_row,
            "implementation_sources": [self_source, route_source],
            "route_audit_source_sha256": ROUTE_AUDIT_SCRIPT_SHA256,
            "route_audit_status": route_report["status"],
            "route_audit_counts": route_counts,
        },
        "counting_contract": {
            "smoke18_top_level_scenarios": 18,
            "family_counts": {"challenge": 6, "visual_loop": 6, "visual_drill": 6},
            "challenge_selector_groups": 6,
            "challenge_e1_d_probe_rows": 18,
            "visual_source_captures_logical_count": 6,
            "one_visual_source_per_selector_shared_by_abc": True,
            "abc_rows_are_audio_seed_subprobes_not_extra_top_level_scenarios": True,
        },
        "capture_groups": groups,
        "reuse_ledger_disposition": {
            "challenge_004": {
                "status": "NOT_REUSABLE_E6_HISTORICAL_SOURCE_PIN_DIVERGENCE",
                "historical_failures": 2,
                "treatment": "FRESH_CHALLENGE_SOURCE_CAPTURE_REQUIRED_UNLESS_SEPARATELY_ADJUDICATED",
            },
            "visual_loop": {
                "status": "CANDIDATE_NOT_E6_ACCEPTED_ROW_LEVEL_OUTPUT_LINKAGE_INCOMPLETE",
                "r1v_slots_verified": hydration_summary["r1v_loop_slots"],
                "loop22_nested_hashes_verified": hydration_summary["loop22_nested_hashes"],
                "top_level_scenarios": 6,
                "treatment": "KEEP_CANDIDATE_ONLY_NO_RERUN_NO_IMPLICIT_ACCEPTANCE",
            },
            "visual_drill": {
                "status": "CANDIDATE_NESTED_EVIDENCE_HASHES_VERIFIED_AWAITING_E6_LEDGER_FREEZE",
                "receipts_verified": hydration_summary["drill_receipts"],
                "nested_hashes_verified": hydration_summary["drill_nested_hashes"],
                "top_level_scenarios": 6,
                "treatment": "KEEP_CANDIDATE_ONLY_NO_RERUN_NO_IMPLICIT_ACCEPTANCE",
            },
            "hydration_summary": hydration_summary,
        },
        "runtime_boundary": {
            "status": "NOT_AUTHORIZED_D4_8_BLOCKED",
            "runtime_commands_emitted": False,
            "processes_started": False,
            "godot_invoked": False,
            "movie_maker_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "d3_audio_generated": False,
            "mux_invoked": False,
            "media_created": False,
            "batch_id_consumed": False,
            "production_dispatch": False,
            "renderer": "OFF",
            "e1": "PREPARE_ONLY",
            "d9": "PREPARE_ONLY",
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "unresolved_e1_parameters": ["tempo_bpm", "duration_seconds"],
            "music_seed_fixture_status": "PROPOSAL_ONLY_NOT_PRODUCT_DEFAULT_NOT_AUTHORIZED",
        },
        "blockers": blockers,
        "next_increment": "Review this six-group plan, then implement one D9-owned orchestration adapter that consumes these groups without modifying any existing C11-C generator, binder, renderer, Producer, or suite module; runtime remains held until separate governance resolution.",
    }


def atomic_write(path: Path, data: bytes) -> None:
    if path.exists():
        raise PlanError(f"OUTPUT_COLLISION:{path}")
    temp = path.with_name(path.name + ".tmp")
    if temp.exists():
        raise PlanError(f"OUTPUT_TEMP_COLLISION:{temp}")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def write_plan(root: Path, plan: dict[str, Any]) -> tuple[Path, str, str]:
    base = contained_path(root, OUTPUT_REL)
    base.mkdir(parents=True, exist_ok=True)
    final_id = plan["run_id"]
    stage = base / ("." + final_id + ".staging")
    final = base / final_id
    if stage.exists() or final.exists():
        raise PlanError("UNIQUE_RUN_OUTPUT_COLLISION")
    stage.mkdir()
    try:
        manifest_raw = (json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
        manifest_sha = sha256_bytes(manifest_raw)
        receipt = {
            "schema": SCHEMA_RECEIPT,
            "schema_version": "1.0",
            "status": "PASS_D9_MULTISELECTOR_CAPTURE_GROUP_PLAN_READY_EXECUTION_HELD",
            "run_id": final_id,
            "created_utc": plan["created_utc"],
            "manifest_name": "E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_MANIFEST_V1.json",
            "manifest_sha256": manifest_sha,
            "selected_challenge_groups": 6,
            "linked_e1_intents": 18,
            "linked_d_envelopes": 18,
            "logical_visual_source_captures": 6,
            "shared_abc_video_source_policy": True,
            "historical_ch004_reuse": "DISALLOWED_PENDING_ADJUDICATION",
            "execution": {
                "runtime_commands_emitted": False,
                "processes_started": False,
                "godot_invoked": False,
                "ffmpeg_invoked": False,
                "ffprobe_invoked": False,
                "audio_generated": False,
                "mux_invoked": False,
                "media_created": False,
                "batch_id_consumed": False,
                "production_dispatch": False,
                "release_authority": "NONE",
            },
        }
        receipt_raw = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
        receipt_sha = sha256_bytes(receipt_raw)
        payloads = [
            ("E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_MANIFEST_V1.json", manifest_raw),
            ("E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_MANIFEST_V1.json.sha256", f"{manifest_sha}  E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_MANIFEST_V1.json\n".encode("ascii")),
            ("E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_RECEIPT_V1.json", receipt_raw),
            ("E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_RECEIPT_V1.json.sha256", f"{receipt_sha}  E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_RECEIPT_V1.json\n".encode("ascii")),
        ]
        for name, content in payloads:
            atomic_write(stage / name, content)
        os.replace(stage, final)
        return final, manifest_sha, receipt_sha
    except Exception:
        if stage.exists():
            for child in stage.iterdir():
                if child.is_file():
                    child.unlink()
            stage.rmdir()
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT_DEFAULT)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not root.is_dir():
        print("E6_D9_CAPTURE_PLAN_ERROR=PROJECT_ROOT_NOT_FOUND", file=sys.stderr)
        return 2
    try:
        plan = build_plan(root)
        out, manifest_sha, receipt_sha = write_plan(root, plan)
    except PlanError as exc:
        print(f"E6_D9_CAPTURE_PLAN_ERROR={exc}", file=sys.stderr)
        return 3
    print("E6_D9_CAPTURE_PLAN_STATUS=" + plan["status"])
    print("E6_D9_ROUTE_AUDIT=24/24 PINS; 6/6 DEFINITIONS; 18/18 ROUTE CHECKS")
    print("E6_D9_LINKED_PROBES=18/18")
    print("E6_D9_CAPTURE_GROUPS=6/6")
    print("E6_D9_LOGICAL_VISUAL_SOURCE_CAPTURES=6 (ONE PER SELECTOR; SHARED A/B/C)")
    print("E6_D9_CH004_REUSE=DISALLOWED_HISTORICAL_SOURCE_PIN_DIVERGENCE")
    print("E6_D9_D4_8=BLOCKED; RUNTIME=HELD")
    print("E6_D9_GODOT=FALSE; FFMPEG=FALSE; FFPROBE=FALSE; AUDIO=FALSE; MUX=FALSE")
    print("E6_D9_MEDIA_CREATED=FALSE; BATCH_ID_CONSUMED=FALSE; RELEASE_AUTHORITY=NONE")
    print("E6_D9_CAPTURE_PLAN_RUN_ID=" + plan["run_id"])
    print("E6_D9_CAPTURE_PLAN_MANIFEST_SHA256=" + manifest_sha)
    print("E6_D9_CAPTURE_PLAN_RECEIPT_SHA256=" + receipt_sha)
    print("E6_D9_CAPTURE_PLAN_OUTPUT=" + str(out))
    print("E6_D9_BLOCKERS=" + str(len(plan["blockers"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
