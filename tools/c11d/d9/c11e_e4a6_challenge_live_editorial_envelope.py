#!/usr/bin/env python3
"""Prepare a non-dispatched E1 intent and E4A.6 Challenge editorial envelope.

This creates a sidecar consumed by the optional D-only live Challenge consumer.
It does not alter the canonical Challenge JSON, call Godot/FFmpeg, emit renderer
input, create media, or dispatch production.
"""
from __future__ import annotations

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
SCHEMA = "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1"
POLICY_REL = Path("definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json")
LAYOUT_REL = Path("docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md")
CHALLENGE_REL = Path("challenges/CHALLENGE_004.json")
POLICY_SHA256 = "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
LAYOUT_SHA256 = "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
EXPECTED_FIELDS = ("title", "subtitle", "player_name", "challenge_label", "call_to_action", "language")
EXPECTED_POLICY = {
    "title": ("visual_text", "HEADER", ["HOOK"]),
    "subtitle": ("visual_text", "HEADER", ["HOOK"]),
    "player_name": ("visual_text", "CHALLENGE_OVERLAY", ["HOOK", "GAME"]),
    "challenge_label": ("visual_text", "CHALLENGE_OVERLAY", ["HOOK", "GAME"]),
    "call_to_action": ("visual_text", "FOOTER", ["CTA"]),
    "language": ("metadata_only", None, []),
}


class EnvelopeError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = sha256_file(path)
    path.with_suffix(path.suffix + ".sha256").write_text(f"{digest}  {path.name}\n", encoding="ascii")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise EnvelopeError(f"Invalid JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EnvelopeError(f"Expected JSON object: {path}")
    return value


def _load_service(root: Path):
    service_path = root / "c11c-suite/c11c-producer/c11e_production_service.py"
    spec = importlib.util.spec_from_file_location("c11e_e4a6_production_service", service_path)
    if spec is None or spec.loader is None:
        raise EnvelopeError(f"Cannot load E1 service: {service_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def prepare_test_intent(root: Path, show_hook_countdown: bool = True) -> dict[str, Any]:
    service = _load_service(root)
    resolver = service._load_d9_resolver(root)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8].upper()
    values = {
        "title": "E4A.6 LIVE TITLE",
        "subtitle": "D HEADER SUBTITLE",
        "player_name": "BLOCKED PLAYER TEST",
        "challenge_label": "BLOCKED CHALLENGE LABEL",
        "call_to_action": "FOLLOW FOR MORE",
        "language": "es",
    }
    raw_request = {
        "schema": resolver.REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": f"E4A6-CH004-LIVE-{stamp}",
        "mode": "REVIEW",
        "selection": {
            "content_type": "challenges",
            "family_id": "parking_v2",
            "variant_id": "CHALLENGE_004",
        },
        "seed": 314159,
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": False,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": values,
        "presentation_options": {"show_hook_countdown": bool(show_hook_countdown)},
        "provenance": {
            "source_revision": "C11E-E4A6-LIVE-CONSUMER-TEST-V1",
            "request_origin": "TEST",
        },
    }
    prepared = service.prepare_c11e_production_intent(
        raw_request, root, request_origin="TEST", resolver_module=resolver
    )
    intent = prepared.get("intent")
    if not isinstance(intent, Mapping):
        raise EnvelopeError("E1 service returned no sealed intent")
    intent_dict = dict(intent)
    _validate_intent(intent_dict)
    return intent_dict


def _validate_intent(intent: Mapping[str, Any]) -> None:
    if intent.get("schema") != "C11-E-PRODUCTION-INTENT-V1" or intent.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise EnvelopeError("E1 intent is not sealed and preparation-only")
    request = intent.get("request")
    if not isinstance(request, Mapping) or request.get("content_type") != "challenges":
        raise EnvelopeError("E1 request content type is not Challenge")
    selection = request.get("selection")
    if not isinstance(selection, Mapping) or selection.get("content_type") != "challenges" or selection.get("variant_id") != "CHALLENGE_004":
        raise EnvelopeError("E1 selector is not CHALLENGE_004")
    identity = intent.get("identity")
    if not isinstance(identity, Mapping):
        raise EnvelopeError("E1 identity is missing")
    for key in ("request_hash", "editorial_hash", "plan_hash", "intent_hash"):
        value = identity.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise EnvelopeError(f"E1 identity hash is invalid: {key}")
    editorial = intent.get("editorial")
    if not isinstance(editorial, Mapping) or set(editorial) != set(EXPECTED_FIELDS):
        raise EnvelopeError("E1 editorial field set differs from the six-field Challenge allowlist")
    boundary = intent.get("execution_boundary", {})
    if not isinstance(boundary, Mapping):
        raise EnvelopeError("E1 execution boundary is malformed")
    for key in ("dispatch_authorized", "renderer_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created"):
        if boundary.get(key) is not False:
            raise EnvelopeError(f"E1 execution boundary crossed: {key}")
    if boundary.get("release_authority") != "NONE" or boundary.get("d4_8") != "BLOCKED":
        raise EnvelopeError("E1 governance boundary is not fail-closed")
    seeds = intent.get("seed_domains", {})
    if not isinstance(seeds, Mapping) or seeds.get("independent_domains") is not True:
        raise EnvelopeError("E1 independent seed domains are not preserved")
    if intent.get("output", {}).get("created") is not False:
        raise EnvelopeError("E1 reports output creation")


def _frames(duration: Any, fps: int, label: str) -> int:
    try:
        value = Decimal(str(duration)) * Decimal(fps)
    except Exception as exc:
        raise EnvelopeError(f"Invalid {label} duration") from exc
    if value < 0:
        raise EnvelopeError(f"Negative {label} duration")
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def build_envelope(root: Path, intent: Mapping[str, Any]) -> dict[str, Any]:
    _validate_intent(intent)
    challenge = load_json(root / CHALLENGE_REL)
    policy = load_json(root / POLICY_REL)
    policy_sha = sha256_file(root / POLICY_REL)
    layout_sha = sha256_file(root / LAYOUT_REL)
    if policy_sha != POLICY_SHA256:
        raise EnvelopeError(f"Approved E4A policy hash drift: {policy_sha}")
    if layout_sha != LAYOUT_SHA256:
        raise EnvelopeError(f"D1.5 layout contract hash drift: {layout_sha}")
    if policy.get("schema") != "C11E-E4A-CHALLENGE-EDITORIAL-PRESENTATION-POLICY-APPROVAL-V1" or policy.get("status") != "APPROVED_BY_OPERATOR_FOR_CHALLENGE_SEMANTIC_MAPPING":
        raise EnvelopeError("E4A approval policy schema/status mismatch")
    challenge_id = str(challenge.get("challenge_id", challenge.get("id", "")))
    selection = intent["request"]["selection"]
    if challenge_id != str(selection.get("variant_id", "")):
        raise EnvelopeError("Challenge source and E1 selector identities differ")
    video = challenge.get("video")
    if not isinstance(video, Mapping):
        raise EnvelopeError("Challenge has no video timebase")
    fps_raw = video.get("fps")
    if isinstance(fps_raw, bool) or not isinstance(fps_raw, (int, float)) or fps_raw <= 0 or int(fps_raw) != fps_raw:
        raise EnvelopeError("Challenge FPS must be a positive integer")
    fps = int(fps_raw)
    phase_config = (
        ("HOOK", "hook_duration"),
        ("GAME", "game_duration"),
        ("REVEAL", "reveal_duration"),
        ("CTA", "cta_duration"),
    )
    phase_ranges: list[dict[str, Any]] = []
    cursor = 0
    for phase, key in phase_config:
        duration = video.get(key)
        if isinstance(duration, bool) or not isinstance(duration, (int, float)):
            raise EnvelopeError(f"Challenge phase duration is invalid: {key}")
        count = _frames(duration, fps, key)
        phase_ranges.append({
            "phase": phase,
            "start_frame": cursor,
            "end_frame": cursor + count,
            "timebase": "SOURCE_FPS_HALF_OPEN",
        })
        cursor += count
    total_frames = cursor
    if total_frames <= 0:
        raise EnvelopeError("Challenge source frame count must be positive")

    policy_rows = {str(row.get("field")): row for row in policy.get("fields", []) if isinstance(row, Mapping)}
    if set(policy_rows) != set(EXPECTED_FIELDS) or len(policy.get("fields", [])) != 6:
        raise EnvelopeError("Approved E4A policy is not the exact six-field allowlist")
    editorial = intent["editorial"]
    fields: list[dict[str, Any]] = []
    phase_by_name = {row["phase"]: row for row in phase_ranges}
    for field in EXPECTED_FIELDS:
        policy_row = policy_rows[field]
        expected_kind, expected_region, expected_windows = EXPECTED_POLICY[field]
        if policy_row.get("kind") != expected_kind or policy_row.get("region") != expected_region or policy_row.get("source_phase_windows") != expected_windows:
            raise EnvelopeError(f"Approved E4A field policy drift: {field}")
        source_value = editorial.get(field, "")
        if not isinstance(source_value, str):
            raise EnvelopeError(f"E1 effective editorial value must be text: {field}")
        clean_value = source_value.strip()
        if not clean_value or clean_value == "UNKNOWN":
            disposition = "OMITTED_EMPTY"
            effective_value = ""
        elif expected_kind == "metadata_only":
            disposition = "METADATA_ONLY"
            effective_value = clean_value
        elif expected_region == "CHALLENGE_OVERLAY":
            disposition = "BLOCKED_GEOMETRY_UNRESOLVED"
            effective_value = clean_value
        else:
            disposition = "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
            effective_value = clean_value
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

    request = intent["request"]
    option = request.get("presentation_options", {"show_hook_countdown": True})
    if not isinstance(option, Mapping) or set(option) != {"show_hook_countdown"} or type(option.get("show_hook_countdown")) is not bool:
        raise EnvelopeError("E1 Challenge presentation option is invalid")

    return {
        "schema": SCHEMA,
        "schema_version": "1.0",
        "status": "PREPARED_E1_NOT_DISPATCHED",
        "content_type": "challenges",
        "challenge_id": challenge_id,
        "e1_intent": dict(intent),
        "intent_hash": str(intent["identity"]["intent_hash"]),
        "request_id": str(request.get("request_id", "")),
        "presentation_options": {"show_hook_countdown": bool(option["show_hook_countdown"])},
        "source_timebase": {"fps": fps, "total_frames": total_frames, "kind": "SOURCE_FRAME_INDEX"},
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--show-hook-countdown", choices=("on", "off"), default="on")
    args = parser.parse_args()
    root = args.root.resolve()
    intent = prepare_test_intent(root, args.show_hook_countdown == "on")
    envelope = build_envelope(root, intent)
    write_json(args.output, envelope)
    print(f"E4A6_ENVELOPE={args.output.resolve()}")
    print(f"E4A6_ENVELOPE_SHA256={sha256_file(args.output)}")
    print(f"E4A6_INTENT_HASH={envelope['intent_hash']}")
    print(f"E4A6_SOURCE_TIMEBASE={envelope['source_timebase']['fps']}FPS/{envelope['source_timebase']['total_frames']}FRAMES")
    print("E4A6_PRODUCTION_DISPATCH=false; MEDIA_CREATED=false; RELEASE_AUTHORITY=NONE")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EnvelopeError as exc:
        print(f"E4A6_ENVELOPE_ERROR={exc}", file=sys.stderr)
        raise SystemExit(2)
