from __future__ import annotations

"""C11-E E6 Challenge six-selector E1/D-envelope plan-only builder.

This tool prepares E1 TEST intents and D-only envelopes for six Challenge
selectors. It does NOT invoke Godot, renderers, FFmpeg/FFprobe, D3 audio,
media, dispatch, or reserve an E6 BatchId. It writes evidence only.

The proposed A/B/C music fixtures are metadata in this plan. E1 intents retain
its unresolved tempo/duration values and remain non-dispatchable.
"""

import argparse
import hashlib
import importlib.util
import json
import sys
import uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]

C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D4_8_POLICY_SHA256 = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
E6_AUDIT_RECEIPT_REL = Path(
    "artifacts/tests/c11e/e6_smoke18_audit/E6AUDITV2_20261116T235057Z_B7FA0492/"
    "E6_SMOKE18_READONLY_AUDIT_RECEIPT_V2.json"
)
E6_AUDIT_RECEIPT_SHA256 = "054ed52aefe45cc4d986c4621adbbdb6ca7cf36dc1c4a12cbd76238de86e21fd"
D4_8_POLICY_REL = Path("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
PRODUCER_SCHEMA_REL = Path("c11c-suite/c11c-producer/producer_schema.json")
PRODUCER_SCHEMA_SHA256 = "564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0"
E1_SERVICE_REL = Path("c11c-suite/c11c-producer/c11e_production_service.py")
E1_SERVICE_SHA256 = "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87"
CHALLENGE_IDS = tuple(f"CHALLENGE_{n:03d}" for n in range(1, 8))
SELECTED_IDS = (
    "CHALLENGE_001",
    "CHALLENGE_002",
    "CHALLENGE_004",
    "CHALLENGE_005",
    "CHALLENGE_006",
    "CHALLENGE_007",
)
EXCLUDED_PILOT_ID = "CHALLENGE_003"

EXPECTED_CHALLENGE_PINS = {
    "challenges/CHALLENGE_001.json": "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea",
    "challenges/CHALLENGE_002.json": "db5d70a28c460e986e785c6787447529372ac5ea3b5a7ff0507667decbe2a160",
    "challenges/CHALLENGE_003.json": "38cb0166482c5ba4862deef8ab75dad4a6e1524590b6850312bab5238f078419",
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "challenges/CHALLENGE_005.json": "e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30",
    "challenges/CHALLENGE_006.json": "2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694",
    "challenges/CHALLENGE_007.json": "269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61",
}

E4A_POLICY_REL = Path("definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json")
LAYOUT_REL = Path("docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md")
E4A_POLICY_SHA256 = "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
LAYOUT_SHA256 = "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
ENVELOPE_CONSUMER_REL = Path("tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd")
ENVELOPE_CONSUMER_SHA256 = "eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203"
E4A6_BUILDER_REL = Path("tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py")
E4A6_BUILDER_SHA256 = "9ea0219f681a912760de3bcdf2469f8a3812a7afe7fb3f5ac569664f354ac18e"
E4A7_RUNNER_REL = Path("tools/c11d/d9/c11e_e4a_challenge_av_review.py")
E4A7_RUNNER_SHA256 = "a31083dcad457b2621610ae68d180a9797cdeb12537a300150e53ec880ee06de"
E3_AUDIO_PIPELINE_REL = Path("c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py")
E3_AUDIO_PIPELINE_SHA256 = "46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d"
E4A7_RECEIPT_REL = Path("artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json")
E4A7_RECEIPT_SHA256 = "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0"
GENERATOR_REL = Path("GeneradorMaestro.gd")
GENERATOR_D_ONLY_POSTIMAGE_SHA256 = "d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82"

# This six-row set is a working design decision from the delegated continuation.
# It is not the E6 media-execution authorization.
MUSIC_FIXTURES = {
    "A": 840001,
    "B_REPEAT": 840001,
    "C_CHANGED_MUSIC_SEED": 840002,
}
MUSIC_PROFILE_ID = "challenge_8bit_v1"
MUSIC_PROFILE_VERSION = "1.0"
MUSIC_TEMPO_BPM = 104
MUSIC_VARIATION_INDEX = 0
SOURCE_FPS_REQUIRED = 60
REVIEW_FPS_PROPOSAL = 30
REVIEW_PROFILE_ID = "REVIEW_720"
PRESENTATION_PROFILE_ID = "social_default_v1"

ENVELOPE_SCHEMA = "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1"
EXPECTED_FIELDS = ("title", "subtitle", "player_name", "challenge_label", "call_to_action", "language")
EXPECTED_POLICY = {
    "title": ("visual_text", "HEADER", ["HOOK"]),
    "subtitle": ("visual_text", "HEADER", ["HOOK"]),
    "player_name": ("visual_text", "CHALLENGE_OVERLAY", ["HOOK", "GAME"]),
    "challenge_label": ("visual_text", "CHALLENGE_OVERLAY", ["HOOK", "GAME"]),
    "call_to_action": ("visual_text", "FOOTER", ["CTA"]),
    "language": ("metadata_only", None, []),
}
PHASE_CONFIG = (
    ("HOOK", "hook_duration"),
    ("GAME", "game_duration"),
    ("REVEAL", "reveal_duration"),
    ("CTA", "cta_duration"),
)


class PlanAuditError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def write_json(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    path.write_text(payload, encoding="utf-8")
    digest = sha256_file(path)
    path.with_suffix(path.suffix + ".sha256").write_text(f"{digest}  {path.name}\n", encoding="ascii")
    return digest


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise PlanAuditError(f"Invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PlanAuditError(f"Expected JSON object: {path}")
    return value


def frames(duration: Any, fps: int, label: str) -> int:
    try:
        value = Decimal(str(duration)) * Decimal(fps)
    except Exception as exc:
        raise PlanAuditError(f"Invalid {label} duration") from exc
    if value < 0:
        raise PlanAuditError(f"Negative {label} duration")
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _load_e1_service(root: Path):
    service_path = root / E1_SERVICE_REL
    spec = importlib.util.spec_from_file_location("c11e_e6_plan_only_e1_service", service_path)
    if spec is None or spec.loader is None:
        raise PlanAuditError(f"Cannot load E1 service: {service_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def verify_pins(root: Path) -> list[dict[str, Any]]:
    expected: dict[str, str] = {
        MANIFEST_REL.as_posix(): C11C_MANIFEST_SHA256,
        D4_8_POLICY_REL.as_posix(): D4_8_POLICY_SHA256,
        E6_AUDIT_RECEIPT_REL.as_posix(): E6_AUDIT_RECEIPT_SHA256,
        E4A_POLICY_REL.as_posix(): E4A_POLICY_SHA256,
        LAYOUT_REL.as_posix(): LAYOUT_SHA256,
        ENVELOPE_CONSUMER_REL.as_posix(): ENVELOPE_CONSUMER_SHA256,
        E4A6_BUILDER_REL.as_posix(): E4A6_BUILDER_SHA256,
        E4A7_RUNNER_REL.as_posix(): E4A7_RUNNER_SHA256,
        E3_AUDIO_PIPELINE_REL.as_posix(): E3_AUDIO_PIPELINE_SHA256,
        PRODUCER_SCHEMA_REL.as_posix(): PRODUCER_SCHEMA_SHA256,
        E1_SERVICE_REL.as_posix(): E1_SERVICE_SHA256,
        E4A7_RECEIPT_REL.as_posix(): E4A7_RECEIPT_SHA256,
        GENERATOR_REL.as_posix(): GENERATOR_D_ONLY_POSTIMAGE_SHA256,
    }
    expected.update(EXPECTED_CHALLENGE_PINS)
    rows: list[dict[str, Any]] = []
    for rel, expected_sha in expected.items():
        path = root / Path(*Path(rel).parts)
        if not path.is_file():
            rows.append({"path": rel, "status": "MISSING", "expected_sha256": expected_sha, "actual_sha256": None})
            continue
        actual = sha256_file(path)
        rows.append({"path": rel, "status": "PASS" if actual == expected_sha else "MISMATCH", "expected_sha256": expected_sha, "actual_sha256": actual, "bytes": path.stat().st_size})
    return rows


def load_candidate_documents(root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for challenge_id in CHALLENGE_IDS:
        path = root / "challenges" / f"{challenge_id}.json"
        result[challenge_id] = load_json(path)
    return result


def analyze_matrix(root: Path) -> dict[str, Any]:
    docs = load_candidate_documents(root)
    schema = load_json(root / PRODUCER_SCHEMA_REL)
    if schema.get("challenge_timing_policy") != "phase_sum_only; legacy total_duration is ignored":
        raise PlanAuditError("Producer schema challenge_timing_policy differs from pinned phase-sum authority")

    schema_rows = {str(row.get("id")): row for row in schema.get("challenges", []) if isinstance(row, Mapping)}
    candidate_rows: list[dict[str, Any]] = []
    for challenge_id in CHALLENGE_IDS:
        doc = docs[challenge_id]
        generation = doc.get("generation", {})
        video = doc.get("video", {})
        mechanic = str(doc.get("mechanic", ""))
        gameplay_seed = generation.get("seed")
        fps_raw = video.get("fps")
        if isinstance(gameplay_seed, bool) or not isinstance(gameplay_seed, int):
            raise PlanAuditError(f"Canonical gameplay seed invalid: {challenge_id}")
        if isinstance(fps_raw, bool) or not isinstance(fps_raw, int) or fps_raw != SOURCE_FPS_REQUIRED:
            raise PlanAuditError(f"Canonical FPS must be {SOURCE_FPS_REQUIRED}: {challenge_id}")
        phase_rows = []
        total_frames = 0
        total_seconds = Decimal("0")
        for phase, field in PHASE_CONFIG:
            duration = video.get(field, 0.0)
            count = frames(duration, SOURCE_FPS_REQUIRED, f"{challenge_id}.{field}")
            phase_rows.append({"phase": phase, "duration_seconds": float(duration), "start_frame": total_frames, "end_frame": total_frames + count})
            total_frames += count
            total_seconds += Decimal(str(duration))
        if total_frames <= 0:
            raise PlanAuditError(f"No positive frame total: {challenge_id}")
        schema_row = schema_rows.get(challenge_id)
        if not isinstance(schema_row, Mapping):
            raise PlanAuditError(f"Producer schema lacks Challenge row: {challenge_id}")
        if schema_row.get("mechanic") != mechanic or schema_row.get("default_seed") != gameplay_seed or schema_row.get("fps") != SOURCE_FPS_REQUIRED:
            raise PlanAuditError(f"Canonical definition / producer schema identity mismatch: {challenge_id}")
        if Decimal(str(schema_row.get("duration_seconds"))) != total_seconds:
            raise PlanAuditError(f"Producer schema duration is not the canonical phase sum: {challenge_id}")
        candidate_rows.append({
            "challenge_id": challenge_id,
            "mechanic": mechanic,
            "family_id": mechanic,
            "gameplay_seed": gameplay_seed,
            "source_fps": SOURCE_FPS_REQUIRED,
            "phase_sum_seconds": float(total_seconds),
            "source_frames": total_frames,
            "proposed_review_fps": REVIEW_FPS_PROPOSAL,
            "proposed_review_frames": frames(total_seconds, REVIEW_FPS_PROPOSAL, f"{challenge_id}.review"),
            "canonical_source": f"challenges/{challenge_id}.json",
            "canonical_source_sha256": EXPECTED_CHALLENGE_PINS[f"challenges/{challenge_id}.json"],
            "phase_ranges": phase_rows,
            "video_profile_label": doc.get("video_profile"),
            "selection_disposition": "SELECTED" if challenge_id in SELECTED_IDS else ("EXCLUDED_PILOT_DUPLICATE_GAMEPLAY_SEED" if challenge_id == EXCLUDED_PILOT_ID else "NOT_SELECTED"),
        })

    selected = [row for row in candidate_rows if row["challenge_id"] in SELECTED_IDS]
    excluded = next(row for row in candidate_rows if row["challenge_id"] == EXCLUDED_PILOT_ID)
    selected_seeds = [row["gameplay_seed"] for row in selected]
    selected_mechanics = [row["mechanic"] for row in selected]
    if len(selected) != 6 or len(set(selected_seeds)) != 6 or len(set(selected_mechanics)) != 6:
        raise PlanAuditError("Selected six must have six unique gameplay seeds and mechanics")
    if "RNG ISOLATION TEST" not in str(docs[EXCLUDED_PILOT_ID].get("content", {}).get("cta", "")):
        raise PlanAuditError("CHALLENGE_003 is no longer identified as the RNG isolation pilot")
    if excluded["gameplay_seed"] != next(row["gameplay_seed"] for row in selected if row["challenge_id"] == "CHALLENGE_004"):
        raise PlanAuditError("CHALLENGE_003 no longer duplicates CHALLENGE_004 gameplay seed")
    if docs["CHALLENGE_004"].get("challenge_id") != "CHALLENGE_004":
        raise PlanAuditError("Accepted CHALLENGE_004 identity missing")

    return {
        "candidate_pool_count": 7,
        "candidate_pool": candidate_rows,
        "selected_ids": list(SELECTED_IDS),
        "selected_rows": selected,
        "excluded_id": EXCLUDED_PILOT_ID,
        "excluded_reason": "Canonical pilot/RNG-isolation case; duplicates gameplay_seed 314159 with accepted CHALLENGE_004, so it adds no new gameplay-seed domain in the six-row smoke sample.",
        "selection_rule": [
            "Retain CHALLENGE_004 because it is the sole accepted E4A.7 A/V anchor.",
            "Choose six distinct canonical mechanics and six distinct gameplay seeds.",
            "Exclude the explicit CHALLENGE_003 RNG-isolation pilot because it duplicates CHALLENGE_004 gameplay seed 314159.",
            "Keep CHALLENGE_008/009 outside the candidate pool because their 11s declaration / 12s phase-sum issue remains held.",
        ],
        "timing_policy": schema["challenge_timing_policy"],
        "producer_schema_sha256_observed": sha256_file(root / PRODUCER_SCHEMA_REL),
    }


def validate_e1_intent(intent: Mapping[str, Any], challenge_id: str, gameplay_seed: int, music_seed: int, service_validation: Mapping[str, Any]) -> None:
    if service_validation.get("status") != "PASS_E1_PREPARATION_ONLY" or service_validation.get("valid") is not True:
        raise PlanAuditError(f"E1 validation failed: {challenge_id} music_seed={music_seed}")
    if intent.get("schema") != "C11-E-PRODUCTION-INTENT-V1" or intent.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise PlanAuditError(f"E1 intent state invalid: {challenge_id}")
    request = intent.get("request", {})
    selection = request.get("selection", {})
    if request.get("content_type") != "challenges" or selection.get("variant_id") != challenge_id:
        raise PlanAuditError(f"E1 Challenge identity mismatch: {challenge_id}")
    domains = intent.get("seed_domains", {})
    if domains.get("gameplay", {}).get("value") != gameplay_seed or domains.get("music", {}).get("value") != music_seed or domains.get("independent_domains") is not True:
        raise PlanAuditError(f"E1 seed domain mapping mismatch: {challenge_id}")
    music = intent.get("music_contract", {})
    if music.get("status") != "PLANNED_NOT_RENDERED" or music.get("dispatchable") is not False or music.get("engine_invoked") is not False or music.get("audio_created") is not False:
        raise PlanAuditError(f"E1 D3 contract crossed planning boundary: {challenge_id}")
    if music.get("unresolved_engine_parameters") != ["tempo_bpm", "duration_seconds"]:
        raise PlanAuditError(f"E1 unresolved music parameters unexpectedly changed: {challenge_id}")
    engine_request = music.get("engine_request")
    if not isinstance(engine_request, Mapping) or engine_request.get("music_seed") != music_seed or engine_request.get("tempo_bpm") is not None or engine_request.get("duration_seconds") is not None:
        raise PlanAuditError(f"E1 music request does not preserve unresolved parameter boundary: {challenge_id}")
    boundary = intent.get("execution_boundary", {})
    for key in ("dispatch_authorized", "renderer_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created"):
        if boundary.get(key) is not False:
            raise PlanAuditError(f"E1 execution boundary crossed: {challenge_id}:{key}")
    if boundary.get("release_authority") != "NONE" or boundary.get("d4_8") != "BLOCKED":
        raise PlanAuditError(f"E1 governance boundary changed: {challenge_id}")
    output = intent.get("output", {})
    if output.get("created") is not False:
        raise PlanAuditError(f"E1 intent reports output creation: {challenge_id}")


def build_envelope(root: Path, intent: Mapping[str, Any], challenge: Mapping[str, Any]) -> dict[str, Any]:
    policy = load_json(root / E4A_POLICY_REL)
    policy_sha = sha256_file(root / E4A_POLICY_REL)
    layout_sha = sha256_file(root / LAYOUT_REL)
    if policy_sha != E4A_POLICY_SHA256 or layout_sha != LAYOUT_SHA256:
        raise PlanAuditError("E4A editorial policy or D1.5 layout contract pin mismatch")
    if policy.get("schema") != "C11E-E4A-CHALLENGE-EDITORIAL-PRESENTATION-POLICY-APPROVAL-V1" or policy.get("status") != "APPROVED_BY_OPERATOR_FOR_CHALLENGE_SEMANTIC_MAPPING":
        raise PlanAuditError("E4A Challenge editorial policy identity/status mismatch")

    challenge_id = str(challenge.get("challenge_id", challenge.get("id", "")))
    request = intent.get("request", {})
    selection = request.get("selection", {})
    if challenge_id != str(selection.get("variant_id", "")):
        raise PlanAuditError("Canonical Challenge and E1 intent identity differ")
    video = challenge.get("video", {})
    fps = video.get("fps")
    if isinstance(fps, bool) or not isinstance(fps, int) or fps != SOURCE_FPS_REQUIRED:
        raise PlanAuditError(f"Invalid source FPS in {challenge_id}")

    phase_ranges: list[dict[str, Any]] = []
    cursor = 0
    for phase, key in PHASE_CONFIG:
        count = frames(video.get(key, 0.0), fps, f"{challenge_id}.{key}")
        phase_ranges.append({
            "phase": phase,
            "start_frame": cursor,
            "end_frame": cursor + count,
            "timebase": "SOURCE_FPS_HALF_OPEN",
        })
        cursor += count
    if cursor <= 0:
        raise PlanAuditError(f"No frames in canonical timeline: {challenge_id}")

    policy_rows = {str(row.get("field")): row for row in policy.get("fields", []) if isinstance(row, Mapping)}
    if set(policy_rows) != set(EXPECTED_FIELDS) or len(policy.get("fields", [])) != 6:
        raise PlanAuditError("E4A editorial policy field allowlist differs")

    editorial = intent.get("editorial", {})
    fields: list[dict[str, Any]] = []
    phase_by_name = {row["phase"]: row for row in phase_ranges}
    for field in EXPECTED_FIELDS:
        policy_row = policy_rows[field]
        expected_kind, expected_region, expected_windows = EXPECTED_POLICY[field]
        if policy_row.get("kind") != expected_kind or policy_row.get("region") != expected_region or policy_row.get("source_phase_windows") != expected_windows:
            raise PlanAuditError(f"Approved E4A field mapping changed: {field}")
        source_value = editorial.get(field, "UNKNOWN")
        if not isinstance(source_value, str):
            raise PlanAuditError(f"E1 editorial value is not text: {field}")
        cleaned = source_value.strip()
        if not cleaned or cleaned == "UNKNOWN":
            disposition = "OMITTED_EMPTY"
            effective_value = ""
        elif expected_kind == "metadata_only":
            disposition = "METADATA_ONLY"
            effective_value = cleaned
        elif expected_region == "CHALLENGE_OVERLAY":
            disposition = "BLOCKED_GEOMETRY_UNRESOLVED"
            effective_value = cleaned
        else:
            disposition = "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
            effective_value = cleaned
        frame_ranges = []
        for phase in expected_windows:
            segment = phase_by_name[phase]
            frame_ranges.append({
                "phase": phase,
                "start_frame": segment["start_frame"],
                "end_frame": segment["end_frame"],
                "timebase": "SOURCE_FPS_HALF_OPEN",
            })
        fields.append({
            "field": field,
            "kind": expected_kind,
            "region": expected_region if expected_region is not None else "METADATA",
            "effective_value": effective_value,
            "source_value_sha256": sha256_bytes(source_value.encode("utf-8")),
            "value_sha256": sha256_bytes(effective_value.encode("utf-8")),
            "source_phase_windows": list(expected_windows),
            "source_frame_ranges": frame_ranges,
            "disposition": disposition,
            "policy_sha256": policy_sha,
            "layout_contract_sha256": layout_sha,
        })

    option = request.get("presentation_options", {"show_hook_countdown": True})
    if not isinstance(option, Mapping) or set(option) != {"show_hook_countdown"} or type(option.get("show_hook_countdown")) is not bool:
        raise PlanAuditError(f"E1 presentation option malformed: {challenge_id}")

    return {
        "schema": ENVELOPE_SCHEMA,
        "schema_version": "1.0",
        "status": "PREPARED_E1_NOT_DISPATCHED",
        "content_type": "challenges",
        "challenge_id": challenge_id,
        "e1_intent": dict(intent),
        "intent_hash": str(intent.get("identity", {}).get("intent_hash", "")),
        "request_id": str(request.get("request_id", "")),
        "presentation_options": {"show_hook_countdown": bool(option["show_hook_countdown"])},
        "source_timebase": {"fps": fps, "total_frames": cursor, "kind": "SOURCE_FRAME_INDEX"},
        "source_phase_ranges": phase_ranges,
        "fields": fields,
        "policy_sha256": policy_sha,
        "layout_contract_sha256": layout_sha,
        "governance": {
            "renderer_input_emitted": False,
            "production_dispatch": False,
            "media_created": False,
            "release_authority": "NONE",
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
        },
    }


def validate_envelope_static(envelope: Mapping[str, Any], challenge_id: str, expected_frames: int, expected_fps: int = 60) -> None:
    if envelope.get("schema") != ENVELOPE_SCHEMA or envelope.get("schema_version") != "1.0":
        raise PlanAuditError("Envelope schema mismatch")
    if envelope.get("status") != "PREPARED_E1_NOT_DISPATCHED" or envelope.get("content_type") != "challenges":
        raise PlanAuditError("Envelope crossed preparation boundary")
    if envelope.get("challenge_id") != challenge_id:
        raise PlanAuditError("Envelope Challenge id mismatch")
    if envelope.get("intent_hash") != envelope.get("e1_intent", {}).get("identity", {}).get("intent_hash"):
        raise PlanAuditError("Envelope E1 intent hash mismatch")
    if envelope.get("source_timebase") != {"fps": expected_fps, "total_frames": expected_frames, "kind": "SOURCE_FRAME_INDEX"}:
        raise PlanAuditError("Envelope source timebase mismatch")
    if len(envelope.get("source_phase_ranges", [])) != 4 or len(envelope.get("fields", [])) != 6:
        raise PlanAuditError("Envelope phase/field inventory incomplete")
    gov = envelope.get("governance", {})
    if gov.get("renderer_input_emitted") is not False or gov.get("production_dispatch") is not False or gov.get("media_created") is not False or gov.get("release_authority") != "NONE" or gov.get("d4_8") != "BLOCKED":
        raise PlanAuditError("Envelope governance boundary changed")


def _challenge_request(resolver: Any, challenge: Mapping[str, Any], music_seed: int, request_id: str) -> dict[str, Any]:
    challenge_id = str(challenge.get("challenge_id", challenge.get("id", "")))
    return {
        "schema": resolver.REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "REVIEW",
        "selection": {
            "content_type": "challenges",
            "family_id": str(challenge.get("mechanic", "")),
            "variant_id": challenge_id,
        },
        "seed": int(challenge["generation"]["seed"]),
        "music_seed": int(music_seed),
        "delivery_profile_id": REVIEW_PROFILE_ID,
        "presentation_profile_id": PRESENTATION_PROFILE_ID,
        "variation_index": MUSIC_VARIATION_INDEX,
        "audio_enabled": True,
        "personalization_enabled": False,
        "editorial_profile": {},
        "production_override": {},
        "provenance": {
            "source_revision": "C11E-E6-CHALLENGE-PLAN-ONLY-V1",
            "request_origin": "TEST",
        },
    }


def run_plan(root: Path, output_root: Path) -> dict[str, Any]:
    root = root.resolve()
    output_root = output_root.resolve()
    run_id = "E6CHPLAN_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper()
    run_dir = output_root / run_id
    if run_dir.exists():
        raise PlanAuditError(f"Run directory already exists: {run_dir}")

    pin_rows = verify_pins(root)
    pin_failures = [row for row in pin_rows if row["status"] != "PASS"]
    if pin_failures:
        raise PlanAuditError(f"Source pin verification failed: {len(pin_failures)} paths")

    manifest_sha = sha256_file(root / MANIFEST_REL)
    policy_sha = sha256_file(root / D4_8_POLICY_REL)
    audit_receipt = load_json(root / E6_AUDIT_RECEIPT_REL)
    if audit_receipt.get("schema") != "C11E-E6-SMOKE18-READONLY-AUDIT-RECEIPT-V2" or audit_receipt.get("status") != "PASS_AUDIT_READ_ONLY_EVIDENCE_RECONCILED_EXECUTION_HELD":
        raise PlanAuditError("Predecessor E6 V2 audit receipt is not an accepted PASS")
    if audit_receipt.get("diagnostics", {}).get("evidence_evaluator_errors") != []:
        raise PlanAuditError("Predecessor E6 V2 audit still has evidence evaluator errors")
    if audit_receipt.get("source_pins", {}).get("passed") != 50 or audit_receipt.get("baseline_document_pins", {}).get("passed") != 11:
        raise PlanAuditError("Predecessor E6 source/document pins are not 50/50 and 11/11")
    if audit_receipt.get("execution", {}).get("media_invoked") is not False or audit_receipt.get("execution", {}).get("new_batch_id_consumed") is not False:
        raise PlanAuditError("Predecessor E6 audit receipt crossed the media/BatchId boundary")

    d4_8 = load_json(root / D4_8_POLICY_REL)
    if sha256_file(root / D4_8_POLICY_REL) != D4_8_POLICY_SHA256:
        raise PlanAuditError("D4.8 R1V V2 policy hash mismatch")
    if not any("smoke18" in str(value).lower() for value in json.dumps(d4_8, ensure_ascii=False).splitlines()):
        raise PlanAuditError("D4.8 policy no longer contains explicit Smoke18 restriction")

    matrix = analyze_matrix(root)
    run_dir.mkdir(parents=True, exist_ok=False)
    service = _load_e1_service(root)
    resolver = service._load_d9_resolver(root)

    intent_rows: list[dict[str, Any]] = []
    envelope_rows: list[dict[str, Any]] = []
    selected_docs = load_candidate_documents(root)
    by_id = {row["challenge_id"]: row for row in matrix["selected_rows"]}

    for challenge_id in SELECTED_IDS:
        challenge = selected_docs[challenge_id]
        matrix_row = by_id[challenge_id]
        for label, music_seed in MUSIC_FIXTURES.items():
            request_id = f"{run_id}-{challenge_id}-{label}"
            raw_request = _challenge_request(resolver, challenge, music_seed, request_id)
            prepared = service.prepare_c11e_production_intent(raw_request, root, request_origin="TEST", resolver_module=resolver)
            intent = prepared.get("intent")
            if not isinstance(intent, Mapping):
                raise PlanAuditError(f"E1 did not return an intent: {challenge_id}/{label}")
            validation = service.validate_c11e_production_intent(intent, root)
            validate_e1_intent(intent, challenge_id, matrix_row["gameplay_seed"], music_seed, validation)
            envelope = build_envelope(root, intent, challenge)
            validate_envelope_static(envelope, challenge_id, matrix_row["source_frames"])

            stem = f"{challenge_id}_{label}"
            intent_path = run_dir / "intents" / f"{stem}_E1_INTENT.json"
            envelope_path = run_dir / "envelopes" / f"{stem}_D_ENVELOPE.json"
            intent_sha = write_json(intent_path, dict(intent))
            envelope_sha = write_json(envelope_path, envelope)
            intent_rows.append({
                "challenge_id": challenge_id,
                "label": label,
                "gameplay_seed": matrix_row["gameplay_seed"],
                "music_seed": music_seed,
                "request_id": request_id,
                "validation_status": validation.get("status"),
                "intent_sha256": intent_sha,
                "intent_path": str(intent_path.relative_to(root)).replace("\\", "/") if intent_path.is_relative_to(root) else str(intent_path),
                "unresolved_music_parameters": intent.get("music_contract", {}).get("unresolved_engine_parameters", []),
            })
            envelope_rows.append({
                "challenge_id": challenge_id,
                "label": label,
                "intent_hash": envelope["intent_hash"],
                "envelope_sha256": envelope_sha,
                "envelope_path": str(envelope_path.relative_to(root)).replace("\\", "/") if envelope_path.is_relative_to(root) else str(envelope_path),
                "source_fps": envelope["source_timebase"]["fps"],
                "source_frames": envelope["source_timebase"]["total_frames"],
            })

    if len(intent_rows) != 18 or len(envelope_rows) != 18:
        raise PlanAuditError("Expected exactly 18 E1 intents and 18 D envelopes")

    receipt = {
        "schema": "C11E-E6-CHALLENGE-PLAN-ONLY-RECEIPT-V1",
        "status": "PASS_E1_AND_D_ENVELOPE_PLANS_18_OF_18_EXECUTION_HELD",
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "scope": "E6_CHALLENGE_SIX_SELECTOR_E1_AND_D_ENVELOPE_PLAN_ONLY",
        "source_pins": {"expected": len(pin_rows), "passed": len(pin_rows), "failed": 0, "rows": pin_rows},
        "predecessor_e6_audit": {
            "run_id": audit_receipt.get("run_id"),
            "receipt_sha256": E6_AUDIT_RECEIPT_SHA256,
            "status": audit_receipt.get("status"),
        },
        "c11c_frozen_manifest_sha256": manifest_sha,
        "d4_8_policy_sha256": policy_sha,
        "challenge_matrix": matrix,
        "music_test_fixture_proposal": {
            "status": "PROPOSED_E6_TEST_ONLY_NOT_PRODUCT_DEFAULT",
            "family_profile_id": MUSIC_PROFILE_ID,
            "family_profile_version": MUSIC_PROFILE_VERSION,
            "tempo_bpm": MUSIC_TEMPO_BPM,
            "tempo_source": "D9.2 historical fixed pilot fixture, reused by E4A.7 CHALLENGE_004; not a product default",
            "variation_index": MUSIC_VARIATION_INDEX,
            "music_seed_A_B": MUSIC_FIXTURES["A"],
            "music_seed_C": MUSIC_FIXTURES["C_CHANGED_MUSIC_SEED"],
            "duration_source": "canonical Challenge phase sum under producer_schema.challenge_timing_policy; not an E1 default",
            "audio_duration_per_scenario": {row["challenge_id"]: row["phase_sum_seconds"] for row in matrix["selected_rows"]},
            "e1_contract_remains_unresolved": ["tempo_bpm", "duration_seconds"],
        },
        "e1_intents": {"expected": 18, "passed": 18, "rows": intent_rows},
        "d_envelopes": {"expected": 18, "passed": 18, "validation": "STATIC_SCHEMA_AND_TIMEBASE_ONLY_NO_GODOT_RUNTIME", "rows": envelope_rows},
        "executor_audit": {
            "generic_d_consumer_source_pinned": True,
            "generic_d_consumer_dynamic_challenge_identity_check": True,
            "e4a6_envelope_builder_scope": "CHALLENGE_004_ONLY",
            "e4a7_av_runner_scope": "CHALLENGE_004_ONLY",
            "e3_audio_pipeline_scope": "CHALLENGE_001_ONLY",
            "generador_maestro_status": "KNOWN_E4A6_D_ONLY_POSTIMAGE_POLICY_CONFLICT_UNCHANGED",
            "multi_selector_godot_runtime": "NOT_RUN_NOT_PROVEN",
            "family_owned_av_executor": "NOT_PROVEN",
        },
        "execution": {
            "e6_test_only_authorized": False,
            "godot_invoked": False,
            "renderer_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "audio_generated": False,
            "mux_invoked": False,
            "media_created": False,
            "production_dispatch": False,
            "new_batch_id_consumed": False,
            "release_authority": "NONE",
        },
        "remaining_blockers": [
            "MULTI_SELECTOR_GODOT_RUNTIME_NOT_PROVEN_FOR_SIX_CHALLENGE_TIMELINES",
            "FAMILY_OWNED_CHALLENGE_AV_EXECUTOR_NOT_PROVEN",
            "MUSIC_FIXTURE_PROPOSAL_REQUIRES_SEPARATE_E6_TEST_ONLY_GOVERNANCE_AUTHORIZATION",
            "D4_8_R1V_V2_PROHIBITS_SMOKE18_D3_AUDIO_AND_FFMPEG_MUX",
        ],
    }
    receipt_sha = write_json(run_dir / "E6_CHALLENGE_PLAN_ONLY_RECEIPT_V1.json", receipt)
    plan = {
        "schema": "C11E-E6-CHALLENGE-SIX-SELECTOR-PLAN-V1",
        "status": "PREPARED_PLAN_ONLY_NOT_FROZEN_FOR_MEDIA",
        "run_id": run_id,
        "receipt_sha256": receipt_sha,
        "selected_ids": list(SELECTED_IDS),
        "selected_rows": matrix["selected_rows"],
        "music_test_fixture_proposal": receipt["music_test_fixture_proposal"],
        "execution": receipt["execution"],
        "remaining_blockers": receipt["remaining_blockers"],
    }
    write_json(run_dir / "E6_CHALLENGE_SIX_SELECTOR_PLAN_V1.json", plan)

    print("E6_CHALLENGE_PLAN_ONLY_STATUS=PASS_E1_AND_D_ENVELOPE_PLANS_18_OF_18_EXECUTION_HELD")
    print(f"E6_CHALLENGE_PLAN_ONLY_RUN_ID={run_id}")
    print(f"E6_CHALLENGE_SOURCE_PINS={len(pin_rows)}/{len(pin_rows)} PASS")
    print("E6_CHALLENGE_SELECTOR_SET=" + ",".join(SELECTED_IDS))
    print("E6_CHALLENGE_E1_INTENTS=18/18 PASS_E1_PREPARATION_ONLY")
    print("E6_CHALLENGE_D_ENVELOPES=18/18 PASS_STATIC_SCHEMA_TIMEBASE")
    print("E6_CHALLENGE_GODOT_RUNTIME=NOT_RUN")
    print("E6_CHALLENGE_MUSIC_FIXTURE=PROPOSAL_ONLY_840001_840002_104BPM_PHASE_SUM")
    print("E6_MEDIA_INVOKED=FALSE")
    print("NEW_BATCH_ID_CONSUMED=FALSE")
    print("PRODUCTION_DISPATCH=FALSE")
    print("RELEASE_AUTHORITY=NONE")
    print(f"E6_CHALLENGE_PLAN_ONLY_RECEIPT={run_dir / 'E6_CHALLENGE_PLAN_ONLY_RECEIPT_V1.json'}")
    print(f"E6_CHALLENGE_PLAN_ONLY_RECEIPT_SHA256={receipt_sha}")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args()
    root = args.project_root.resolve()
    output_root = args.output_root or (root / "artifacts/tests/c11e/e6_challenge_plan_only")
    run_plan(root, output_root)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PlanAuditError as exc:
        print(f"E6_CHALLENGE_PLAN_ONLY_ERROR={exc}", file=sys.stderr)
        raise SystemExit(2)
