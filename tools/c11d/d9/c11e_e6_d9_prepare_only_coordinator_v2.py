from __future__ import annotations

"""C11-E E6 D9 PREPARE_ONLY coordinator V2.

Read-only coordinator over the already accepted E6 Challenge plan-only run.
It does not call the E1 service, regenerate intents/envelopes, invoke external
processes, reserve a BatchId, dispatch, or create media. It writes only a new
linkage manifest and receipt under the selected evidence root.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA_MANIFEST = "C11E-E6-D9-CHALLENGE-PREPARE-ONLY-MANIFEST-V2"
SCHEMA_RECEIPT = "C11E-E6-D9-CHALLENGE-PREPARE-ONLY-RECEIPT-V2"
PROJECT_ROOT_DEFAULT = Path(__file__).resolve().parents[3]

ACCEPTANCE_RECEIPT_REL = Path(
    "artifacts/tests/c11e/e6_runtime_dependency_pin_acceptance/"
    "E6DEPPINACCEPT_20261117T141326Z_C980FF81/"
    "E6_RUNTIME_DEPENDENCY_PIN_ACCEPTANCE_RECEIPT_V1.json"
)
ACCEPTANCE_RECEIPT_SHA256 = "41c62276465803dfb289a91b8a7f74c9b57c213dbad64c1323d6f626e3b2edd0"
PLAN_RUN_ID = "E6CHPLAN_20261117T001949Z_D87FADA4"
PLAN_ROOT_REL = Path("artifacts/tests/c11e/e6_challenge_plan_only") / PLAN_RUN_ID
PLAN_RECEIPT_NAME = "E6_CHALLENGE_PLAN_ONLY_RECEIPT_V1.json"
PLAN_JSON_NAME = "E6_CHALLENGE_SIX_SELECTOR_PLAN_V1.json"
PLAN_RECEIPT_SHA256 = "8fcd63fcfd04df9446f20c5ea8dd1646f169051403f2ee04a356997cd3dd257e"
PLAN_JSON_SHA256 = "ef86fe532cd6c92c3c2dc9937a65d149dc699fcd6c0295382a135413f04af6ae"
CONTRACT_RECEIPT_REL = Path(
    "artifacts/tests/c11e/e6_challenge_consumer_contract/"
    "E6CHCONTRACT_20261117T005638Z_B3412977/"
    "E6_CHALLENGE_CONSUMER_CONTRACT_PREFLIGHT_RECEIPT_V1.json"
)
CONTRACT_RECEIPT_SHA256 = "e22abc1fc1779f60dd48abf4cdbf7960b7a3a02b2ef9bc0a7e975053f5effce8"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D4_8_SHA256 = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
SELECTED_IDS = (
    "CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004",
    "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007",
)
LABELS = ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED")
MUSIC_SEEDS = {"A": 840001, "B_REPEAT": 840001, "C_CHANGED_MUSIC_SEED": 840002}
EXPECTED_FRAMES = {
    "CHALLENGE_001": 540, "CHALLENGE_002": 600, "CHALLENGE_004": 900,
    "CHALLENGE_005": 420, "CHALLENGE_006": 540, "CHALLENGE_007": 600,
}


class CoordinatorError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise CoordinatorError(f"Invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CoordinatorError(f"Expected JSON object: {path}")
    return value


def contained_path(root: Path, relative: str | Path) -> Path:
    raw = str(relative).replace("\\", "/")
    rel = Path(raw)
    if rel.is_absolute() or ".." in rel.parts or not raw.strip():
        raise CoordinatorError(f"Unsafe evidence path: {relative}")
    target = (root / Path(*rel.parts)).resolve()
    base = root.resolve()
    if target != base and base not in target.parents:
        raise CoordinatorError(f"Evidence path escapes project root: {relative}")
    return target


def verify_fixed_file(root: Path, relative: Path, expected_sha: str, label: str) -> dict[str, Any]:
    path = contained_path(root, relative)
    if not path.is_file():
        raise CoordinatorError(f"Required {label} missing: {relative.as_posix()}")
    actual = sha256_file(path)
    if actual != expected_sha:
        raise CoordinatorError(f"{label} SHA-256 mismatch: expected={expected_sha} actual={actual}")
    return {"path": relative.as_posix(), "sha256": actual, "bytes": path.stat().st_size, "status": "PASS"}


def verify_accepted_source_pins(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    receipt_row = verify_fixed_file(root, ACCEPTANCE_RECEIPT_REL, ACCEPTANCE_RECEIPT_SHA256, "E6 dependency-pin acceptance receipt")
    receipt = load_json(contained_path(root, ACCEPTANCE_RECEIPT_REL))
    if receipt.get("status") != "PASS_E6_STATIC_ROUTE_DEPENDENCY_PIN_BASELINE_ACCEPTED":
        raise CoordinatorError("E6 static dependency-pin acceptance status is not PASS")
    rows = receipt.get("source_pin_verification")
    if not isinstance(rows, list) or len(rows) != 33:
        raise CoordinatorError("Expected exactly 33 accepted E6 source pins")
    verified: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise CoordinatorError("Malformed source pin row")
        rel = str(row.get("path", ""))
        if rel in seen:
            raise CoordinatorError(f"Duplicate source pin path: {rel}")
        seen.add(rel)
        path = contained_path(root, rel)
        if not path.is_file():
            raise CoordinatorError(f"Accepted source pin missing: {rel}")
        expected = str(row.get("sha256", "")).lower()
        actual = sha256_file(path)
        if actual != expected or row.get("status") != "PASS":
            raise CoordinatorError(f"Accepted source pin mismatch: {rel}")
        if row.get("bytes") is not None and path.stat().st_size != int(row["bytes"]):
            raise CoordinatorError(f"Accepted source pin byte-count mismatch: {rel}")
        verified.append({"path": rel, "sha256": actual, "bytes": path.stat().st_size, "status": "PASS", "pin_scope": row.get("pin_scope")})
    governance = receipt.get("governance", {})
    if governance.get("runtime_authorized") is not False or governance.get("godot_invoked") is not False or governance.get("media_created") is not False or governance.get("release_authority") != "NONE":
        raise CoordinatorError("E6 pin acceptance receipt crossed its static-only authority boundary")
    if governance.get("d4_8") != "BLOCKED_UNCHANGED" or governance.get("e1") != "PREPARE_ONLY":
        raise CoordinatorError("E6 pin acceptance governance state changed")
    return receipt_row, verified


def _validate_sidecar(path: Path, expected: str) -> None:
    sidecar = path.with_suffix(path.suffix + ".sha256")
    if not sidecar.is_file():
        raise CoordinatorError(f"Required SHA sidecar missing: {sidecar}")
    token = sidecar.read_text(encoding="ascii").strip().split()[0].lower()
    if token != expected:
        raise CoordinatorError(f"SHA sidecar mismatch: {sidecar}")


def _phase_signature(ranges: Any) -> list[tuple[str, int, int]]:
    if not isinstance(ranges, list) or len(ranges) != 4:
        raise CoordinatorError("Expected exactly four half-open phase ranges")
    result: list[tuple[str, int, int]] = []
    cursor = 0
    for row in ranges:
        if not isinstance(row, Mapping):
            raise CoordinatorError("Malformed phase range")
        phase = str(row.get("phase", ""))
        start, end = row.get("start_frame"), row.get("end_frame")
        if isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int) or not isinstance(end, int):
            raise CoordinatorError("Phase frame indices must be integers")
        if start != cursor or end < start:
            raise CoordinatorError("Phase ranges are not contiguous nonnegative half-open intervals")
        if row.get("timebase") not in (None, "SOURCE_FPS_HALF_OPEN"):
            raise CoordinatorError("Unexpected phase timebase")
        result.append((phase, start, end))
        cursor = end
    if [x[0] for x in result] != ["HOOK", "GAME", "REVEAL", "CTA"]:
        raise CoordinatorError("Canonical phase order mismatch")
    return result


def validate_plan_artifacts(root: Path, receipt: Mapping[str, Any], plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    if receipt.get("schema") != "C11E-E6-CHALLENGE-PLAN-ONLY-RECEIPT-V1" or receipt.get("status") != "PASS_E1_AND_D_ENVELOPE_PLANS_18_OF_18_EXECUTION_HELD":
        raise CoordinatorError("Predecessor plan-only receipt schema/status mismatch")
    if receipt.get("run_id") != PLAN_RUN_ID or plan.get("run_id") != PLAN_RUN_ID:
        raise CoordinatorError("Predecessor plan-only run identity mismatch")
    if plan.get("schema") != "C11E-E6-CHALLENGE-SIX-SELECTOR-PLAN-V1" or plan.get("status") != "PREPARED_PLAN_ONLY_NOT_FROZEN_FOR_MEDIA":
        raise CoordinatorError("Predecessor Challenge plan schema/status mismatch")
    if plan.get("receipt_sha256") != PLAN_RECEIPT_SHA256:
        raise CoordinatorError("Plan JSON does not bind the accepted receipt SHA")
    if plan.get("selected_ids") != list(SELECTED_IDS):
        raise CoordinatorError("Selected Challenge selector set/order mismatch")
    if receipt.get("c11c_frozen_manifest_sha256") != FROZEN_MANIFEST_SHA256 or receipt.get("d4_8_policy_sha256") != D4_8_SHA256:
        raise CoordinatorError("Plan receipt frozen baseline or D4.8 identity mismatch")
    if receipt.get("source_pins", {}).get("expected") != 20 or receipt.get("source_pins", {}).get("passed") != 20 or receipt.get("source_pins", {}).get("failed") != 0:
        raise CoordinatorError("Accepted plan-only source-pin result is not 20/20")
    execution = receipt.get("execution", {})
    forbidden = ("e6_test_only_authorized", "godot_invoked", "renderer_invoked", "ffmpeg_invoked", "ffprobe_invoked", "audio_generated", "mux_invoked", "media_created", "production_dispatch", "new_batch_id_consumed")
    if any(execution.get(key) is not False for key in forbidden) or execution.get("release_authority") != "NONE":
        raise CoordinatorError("Predecessor plan-only execution boundary changed")
    if plan.get("execution") != execution:
        raise CoordinatorError("Plan/receipt execution boundary mismatch")
    if receipt.get("e1_intents", {}).get("expected") != 18 or receipt.get("e1_intents", {}).get("passed") != 18:
        raise CoordinatorError("Predecessor E1 intent count is not 18/18")
    if receipt.get("d_envelopes", {}).get("expected") != 18 or receipt.get("d_envelopes", {}).get("passed") != 18:
        raise CoordinatorError("Predecessor D envelope count is not 18/18")

    matrix_rows = plan.get("selected_rows")
    if not isinstance(matrix_rows, list) or len(matrix_rows) != 6:
        raise CoordinatorError("Plan must contain exactly six selected Challenge rows")
    matrix = {str(row.get("challenge_id")): row for row in matrix_rows if isinstance(row, Mapping)}
    if set(matrix) != set(SELECTED_IDS):
        raise CoordinatorError("Plan matrix Challenge identity set mismatch")

    intent_rows = receipt.get("e1_intents", {}).get("rows", [])
    envelope_rows = receipt.get("d_envelopes", {}).get("rows", [])
    if not isinstance(intent_rows, list) or not isinstance(envelope_rows, list) or len(intent_rows) != 18 or len(envelope_rows) != 18:
        raise CoordinatorError("Plan receipt must enumerate 18 E1 intents and 18 D envelopes")
    indexed_intents: dict[tuple[str, str], Mapping[str, Any]] = {}
    indexed_envelopes: dict[tuple[str, str], Mapping[str, Any]] = {}
    for row, index, kind in ((r, indexed_intents, "intent") for r in intent_rows):
        key = (str(row.get("challenge_id", "")), str(row.get("label", "")))
        if key in index:
            raise CoordinatorError(f"Duplicate E1 intent row: {key}")
        index[key] = row
    for row in envelope_rows:
        key = (str(row.get("challenge_id", "")), str(row.get("label", "")))
        if key in indexed_envelopes:
            raise CoordinatorError(f"Duplicate D envelope row: {key}")
        indexed_envelopes[key] = row
    expected_keys = {(challenge_id, label) for challenge_id in SELECTED_IDS for label in LABELS}
    if set(indexed_intents) != expected_keys or set(indexed_envelopes) != expected_keys:
        raise CoordinatorError("E1/D references do not form the exact six-selector A/B/C matrix")

    linked: list[dict[str, Any]] = []
    for challenge_id in SELECTED_IDS:
        matrix_row = matrix[challenge_id]
        expected_frames = EXPECTED_FRAMES[challenge_id]
        if matrix_row.get("source_fps") != 60 or matrix_row.get("source_frames") != expected_frames:
            raise CoordinatorError(f"Canonical native timebase mismatch: {challenge_id}")
        for label in LABELS:
            key = (challenge_id, label)
            ir = indexed_intents[key]
            er = indexed_envelopes[key]
            if ir.get("validation_status") != "PASS_E1_PREPARATION_ONLY":
                raise CoordinatorError(f"E1 validation status mismatch: {key}")
            if ir.get("gameplay_seed") != matrix_row.get("gameplay_seed") or ir.get("music_seed") != MUSIC_SEEDS[label]:
                raise CoordinatorError(f"Receipt seed relation mismatch: {key}")
            ipath = contained_path(root, str(ir.get("intent_path", "")))
            epath = contained_path(root, str(er.get("envelope_path", "")))
            if not ipath.is_file() or not epath.is_file():
                raise CoordinatorError(f"Referenced E1 intent or D envelope missing: {key}")
            ihash, ehash = sha256_file(ipath), sha256_file(epath)
            if ihash != str(ir.get("intent_sha256", "")).lower() or ehash != str(er.get("envelope_sha256", "")).lower():
                raise CoordinatorError(f"Referenced artifact hash mismatch: {key}")
            intent, envelope = load_json(ipath), load_json(epath)
            request = intent.get("request", {})
            selection = request.get("selection", {})
            domains = intent.get("seed_domains", {})
            identity = intent.get("identity", {})
            if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED" or request.get("request_id") != ir.get("request_id"):
                raise CoordinatorError(f"E1 intent status/request identity mismatch: {key}")
            if request.get("content_type") != "challenges" or selection.get("variant_id") != challenge_id:
                raise CoordinatorError(f"E1 nested selector mismatch: {key}")
            gameplay_seed = domains.get("gameplay", {}).get("value")
            music_seed = domains.get("music", {}).get("value")
            if gameplay_seed != matrix_row.get("gameplay_seed") or music_seed != MUSIC_SEEDS[label] or domains.get("independent_domains") is not True:
                raise CoordinatorError(f"E1 seed-domain provenance mismatch: {key}")
            if intent.get("music_contract", {}).get("unresolved_engine_parameters") != ["tempo_bpm", "duration_seconds"]:
                raise CoordinatorError(f"E1 tempo/duration unexpectedly resolved: {key}")
            music_contract = intent.get("music_contract", {})
            engine_request = music_contract.get("engine_request", {})
            if engine_request.get("music_seed") != music_seed or engine_request.get("tempo_bpm") is not None or engine_request.get("duration_seconds") is not None:
                raise CoordinatorError(f"E1 engine request seed/parameter boundary mismatch: {key}")
            if music_contract.get("dispatchable") is not False or music_contract.get("engine_invoked") is not False or music_contract.get("audio_created") is not False:
                raise CoordinatorError(f"E1 music contract crossed preparation boundary: {key}")
            boundary = intent.get("execution_boundary", {})
            for flag in ("dispatch_authorized", "renderer_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created"):
                if boundary.get(flag) is not False:
                    raise CoordinatorError(f"E1 execution boundary changed: {key}:{flag}")
            if boundary.get("release_authority") != "NONE" or boundary.get("d4_8") != "BLOCKED":
                raise CoordinatorError(f"E1 governance boundary changed: {key}")
            if intent.get("output", {}).get("created") is not False:
                raise CoordinatorError(f"E1 intent reports output creation: {key}")
            if envelope.get("schema") != "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1" or envelope.get("schema_version") != "1.0":
                raise CoordinatorError(f"D envelope schema mismatch: {key}")
            if envelope.get("status") != "PREPARED_E1_NOT_DISPATCHED" or envelope.get("content_type") != "challenges" or envelope.get("challenge_id") != challenge_id:
                raise CoordinatorError(f"D envelope status/selector mismatch: {key}")
            if envelope.get("request_id") != request.get("request_id") or envelope.get("e1_intent") != intent:
                raise CoordinatorError(f"D envelope nested E1 identity mismatch: {key}")
            if envelope.get("intent_hash") != identity.get("intent_hash") or er.get("intent_hash") != identity.get("intent_hash"):
                raise CoordinatorError(f"D envelope intent hash mismatch: {key}")
            if envelope.get("source_timebase") != {"fps": 60, "total_frames": expected_frames, "kind": "SOURCE_FRAME_INDEX"}:
                raise CoordinatorError(f"D envelope native timebase mismatch: {key}")
            phases = _phase_signature(envelope.get("source_phase_ranges"))
            if phases[-1][2] != expected_frames:
                raise CoordinatorError(f"D envelope phase sum mismatch: {key}")
            matrix_phases = _phase_signature(matrix_row.get("phase_ranges"))
            if phases != matrix_phases:
                raise CoordinatorError(f"D envelope phases differ from canonical plan timeline: {key}")
            if not isinstance(envelope.get("fields"), list) or len(envelope["fields"]) != 6:
                raise CoordinatorError(f"D envelope six-field consumer contract mismatch: {key}")
            gov = envelope.get("governance", {})
            if gov.get("renderer_input_emitted") is not False or gov.get("production_dispatch") is not False or gov.get("media_created") is not False or gov.get("release_authority") != "NONE" or gov.get("d4_8") != "BLOCKED":
                raise CoordinatorError(f"D envelope governance boundary changed: {key}")
            linked.append({
                "challenge_id": challenge_id, "label": label,
                "gameplay_seed": gameplay_seed, "music_seed": music_seed,
                "request_id": request["request_id"],
                "intent_hash": identity.get("intent_hash"),
                "intent_sha256": ihash, "intent_path": str(ir["intent_path"]).replace("\\", "/"),
                "envelope_sha256": ehash, "envelope_path": str(er["envelope_path"]).replace("\\", "/"),
                "source_fps": 60, "source_frames": expected_frames,
                "phase_ranges": [{"phase": p, "start_frame": s, "end_frame": e} for p, s, e in phases],
            })

    # Cross-row A/B/C invariants: A and B repeat both domains; C changes music only.
    for challenge_id in SELECTED_IDS:
        group = {row["label"]: row for row in linked if row["challenge_id"] == challenge_id}
        if group["A"]["gameplay_seed"] != group["B_REPEAT"]["gameplay_seed"] or group["A"]["music_seed"] != group["B_REPEAT"]["music_seed"]:
            raise CoordinatorError(f"A/B repeatability identity mismatch: {challenge_id}")
        if group["C_CHANGED_MUSIC_SEED"]["gameplay_seed"] != group["A"]["gameplay_seed"] or group["C_CHANGED_MUSIC_SEED"]["music_seed"] == group["A"]["music_seed"]:
            raise CoordinatorError(f"C changed more than the music seed or failed to change it: {challenge_id}")
        if group["A"]["phase_ranges"] != group["B_REPEAT"]["phase_ranges"] or group["A"]["phase_ranges"] != group["C_CHANGED_MUSIC_SEED"]["phase_ranges"]:
            raise CoordinatorError(f"A/B/C timeline identity mismatch: {challenge_id}")
    return linked


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    if path.exists() or temp.exists():
        raise CoordinatorError(f"ADD_ONLY output collision: {path}")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def write_new_run(output_root: Path, run_id: str, manifest: dict[str, Any], receipt_base: dict[str, Any]) -> tuple[Path, str, str]:
    output_root.mkdir(parents=True, exist_ok=True)
    final_dir = output_root / run_id
    stage_dir = output_root / ("." + run_id + ".staging")
    if final_dir.exists() or stage_dir.exists():
        raise CoordinatorError("Unique run output collision; refusing reuse")
    stage_dir.mkdir()
    try:
        manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
        manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
        receipt = dict(receipt_base)
        receipt["manifest_sha256"] = manifest_sha
        receipt["linked_artifacts"] = {"e1_intents": 18, "d_envelopes": 18, "total": 36}
        receipt_bytes = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
        receipt_sha = hashlib.sha256(receipt_bytes).hexdigest()
        files = (
            ("E6_D9_CHALLENGE_PREPARE_ONLY_MANIFEST_V2.json", manifest_bytes),
            ("E6_D9_CHALLENGE_PREPARE_ONLY_MANIFEST_V2.json.sha256", f"{manifest_sha}  E6_D9_CHALLENGE_PREPARE_ONLY_MANIFEST_V2.json\n".encode("ascii")),
            ("E6_D9_CHALLENGE_PREPARE_ONLY_RECEIPT_V2.json", receipt_bytes),
            ("E6_D9_CHALLENGE_PREPARE_ONLY_RECEIPT_V2.json.sha256", f"{receipt_sha}  E6_D9_CHALLENGE_PREPARE_ONLY_RECEIPT_V2.json\n".encode("ascii")),
        )
        for name, payload in files:
            atomic_write(stage_dir / name, payload)
        os.replace(stage_dir, final_dir)
        return final_dir, manifest_sha, receipt_sha
    except Exception:
        # Roll back only this run's private staging directory.
        if stage_dir.exists():
            for child in stage_dir.iterdir():
                if child.is_file():
                    child.unlink()
            stage_dir.rmdir()
        raise


def run(root: Path, output_root: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    acceptance_row, pins = verify_accepted_source_pins(root)
    plan_receipt_path = contained_path(root, PLAN_ROOT_REL / PLAN_RECEIPT_NAME)
    plan_json_path = contained_path(root, PLAN_ROOT_REL / PLAN_JSON_NAME)
    plan_receipt_row = verify_fixed_file(root, PLAN_ROOT_REL / PLAN_RECEIPT_NAME, PLAN_RECEIPT_SHA256, "accepted E6 plan-only receipt")
    plan_json_row = verify_fixed_file(root, PLAN_ROOT_REL / PLAN_JSON_NAME, PLAN_JSON_SHA256, "accepted E6 six-selector plan")
    _validate_sidecar(plan_receipt_path, PLAN_RECEIPT_SHA256)
    _validate_sidecar(plan_json_path, PLAN_JSON_SHA256)
    contract_row = verify_fixed_file(root, CONTRACT_RECEIPT_REL, CONTRACT_RECEIPT_SHA256, "E6 consumer-contract preflight receipt")
    contract = load_json(contained_path(root, CONTRACT_RECEIPT_REL))
    if contract.get("status") != "PASS_STATIC_CONSUMER_CONTRACT_18_OF_18_EXECUTION_HELD":
        raise CoordinatorError("E6 consumer-contract predecessor is not accepted")
    if contract.get("e1_intents", {}).get("passed") != 18 or contract.get("d_envelopes", {}).get("passed") != 18:
        raise CoordinatorError("E6 consumer-contract predecessor does not confirm 18/18")
    contract_execution = contract.get("execution", {})
    for flag in ("godot_invoked", "ffmpeg_invoked", "ffprobe_invoked", "audio_generated", "media_created", "production_dispatch"):
        if contract_execution.get(flag) is not False:
            raise CoordinatorError(f"E6 consumer-contract predecessor crossed execution boundary: {flag}")
    if contract_execution.get("release_authority") != "NONE":
        raise CoordinatorError("E6 consumer-contract predecessor release authority is not NONE")
    receipt = load_json(plan_receipt_path)
    plan = load_json(plan_json_path)
    linked = validate_plan_artifacts(root, receipt, plan)

    run_id = "E6D9PREP_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper()
    manifest = {
        "schema": SCHEMA_MANIFEST,
        "status": "PREPARED_ONLY_LINKAGE_COMPLETE_NOT_FROZEN_FOR_MEDIA",
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "E6_D9_CHALLENGE_SIX_SELECTOR_PLAN_LINKAGE_PREPARE_ONLY",
        "coordinator_version": "V2_ZERO_LENGTH_PHASE_COMPATIBILITY",
        "smoke18_counting": {"top_level_challenge_scenarios": 6, "challenge_abc_subprobes": 18, "smoke18_total": 18, "families": {"challenge": 6, "loop": 6, "drill": 6}},
        "selected_ids": list(SELECTED_IDS),
        "source_authority": {"dependency_pin_acceptance_receipt": acceptance_row, "accepted_source_pins": pins},
        "predecessors": {"plan_only_receipt": plan_receipt_row, "plan_json": plan_json_row, "consumer_contract_receipt": contract_row},
        "lineage": {"plan_only_run_id": PLAN_RUN_ID, "plan_only_receipt_sha256": PLAN_RECEIPT_SHA256, "plan_json_sha256": PLAN_JSON_SHA256, "consumer_contract_receipt_sha256": CONTRACT_RECEIPT_SHA256, "frozen_c11c_manifest_sha256": FROZEN_MANIFEST_SHA256, "d4_8_policy_sha256": D4_8_SHA256},
        "linked_probes": linked,
        "music_fixture_disposition": "HISTORICAL_PROPOSAL_METADATA_ONLY_NOT_PRODUCT_DEFAULT_NOT_EXECUTION_AUTHORIZATION",
        "unresolved_e1_parameters": ["tempo_bpm", "duration_seconds"],
        "governance": {"e1": "PREPARE_ONLY", "d9": "PREPARE_ONLY", "d4_8": "BLOCKED", "renderer": "OFF", "dispatch": False, "media_created": False, "godot_invoked": False, "ffmpeg_invoked": False, "ffprobe_invoked": False, "audio_generated": False, "mux_invoked": False, "new_batch_id_consumed": False, "e6_test_only_authorized": False, "release_authority": "NONE"},
    }
    receipt_base = {
        "schema": SCHEMA_RECEIPT,
        "status": "PASS_D9_PREPARE_ONLY_18_INTENTS_18_ENVELOPES_LINKED_EXECUTION_HELD",
        "run_id": run_id,
        "created_utc": manifest["created_utc"],
        "manifest_name": "E6_D9_CHALLENGE_PREPARE_ONLY_MANIFEST_V2.json",
        "source_pin_count": 33,
        "linked_probe_count": 18,
        "linked_e1_intents": 18,
        "linked_d_envelopes": 18,
        "plan_only_run_id": PLAN_RUN_ID,
        "plan_only_receipt_sha256": PLAN_RECEIPT_SHA256,
        "plan_json_sha256": PLAN_JSON_SHA256,
        "consumer_contract_receipt_sha256": CONTRACT_RECEIPT_SHA256,
        "execution": {"e6_test_only_authorized": False, "godot_invoked": False, "renderer_invoked": False, "ffmpeg_invoked": False, "ffprobe_invoked": False, "audio_generated": False, "mux_invoked": False, "media_created": False, "production_dispatch": False, "new_batch_id_consumed": False, "release_authority": "NONE"},
    }
    out = output_root or (root / "artifacts/tests/c11e/e6_d9_prepare_only")
    final_dir, manifest_sha, receipt_sha = write_new_run(out.resolve(), run_id, manifest, receipt_base)
    result = {**receipt_base, "manifest_sha256": manifest_sha, "receipt_sha256": receipt_sha, "output_dir": str(final_dir)}
    print("E6_D9_PREPARE_ONLY_STATUS=" + result["status"])
    print("E6_D9_SOURCE_PINS=33/33 PASS")
    print("E6_D9_LINKED_E1_INTENTS=18/18 PASS")
    print("E6_D9_LINKED_D_ENVELOPES=18/18 PASS")
    print("E6_D9_GODOT_INVOKED=FALSE")
    print("E6_D9_MEDIA_CREATED=FALSE")
    print("E6_D9_BATCH_ID_CONSUMED=FALSE")
    print("E6_D9_RELEASE_AUTHORITY=NONE")
    print("E6_D9_RUN_ID=" + run_id)
    print("E6_D9_MANIFEST_SHA256=" + manifest_sha)
    print("E6_D9_RECEIPT_SHA256=" + receipt_sha)
    print("E6_D9_OUTPUT_DIR=" + str(final_dir))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT_DEFAULT)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)
    run(args.project_root, args.output_root)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CoordinatorError as exc:
        print(f"E6_D9_PREPARE_ONLY_ERROR={exc}", file=sys.stderr)
        raise SystemExit(2)
