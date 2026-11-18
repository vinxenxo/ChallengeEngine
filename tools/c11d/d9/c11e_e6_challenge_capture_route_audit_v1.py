#!/usr/bin/env python3
"""C11-E E6 Challenge capture-route audit V1.

Read-only source/evidence audit. It does not import the project, invoke Godot,
FFmpeg, FFprobe, the Producer, E1 dispatch, or any media generator. It writes
only a JSON audit receipt and SHA-256 sidecar beneath the selected evidence root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "C11E-E6-CHALLENGE-CAPTURE-ROUTE-AUDIT-RECEIPT-V1"
CONTRACT_RECEIPT_REL = Path(
    "artifacts/tests/c11e/e6_challenge_consumer_contract/"
    "E6CHCONTRACT_20261117T005638Z_B3412977/"
    "E6_CHALLENGE_CONSUMER_CONTRACT_PREFLIGHT_RECEIPT_V1.json"
)
CONTRACT_RECEIPT_SHA = "e22abc1fc1779f60dd48abf4cdbf7960b7a3a02b2ef9bc0a7e975053f5effce8"
PLAN_RUN = "E6CHPLAN_20261117T001949Z_D87FADA4"
PLAN_ROOT_REL = Path("artifacts/tests/c11e/e6_challenge_plan_only") / PLAN_RUN
PLAN_RECEIPT_REL = PLAN_ROOT_REL / "E6_CHALLENGE_PLAN_ONLY_RECEIPT_V1.json"
PLAN_RECEIPT_SHA = "8fcd63fcfd04df9446f20c5ea8dd1646f169051403f2ee04a356997cd3dd257e"
PLAN_JSON_REL = PLAN_ROOT_REL / "E6_CHALLENGE_SIX_SELECTOR_PLAN_V1.json"
PLAN_JSON_SHA = "ef86fe532cd6c92c3c2dc9937a65d149dc699fcd6c0295382a135413f04af6ae"
RECOVERY_REL = Path(
    "artifacts/tests/c11e/e6_challenge_plan_only_install/"
    "E6CHREC2_20261117T001937Z_659245DC/"
    "E6_CHALLENGE_PLAN_ONLY_RECOVERY_RECEIPT_V2.json"
)
RECOVERY_SHA = "bee886f606a57c3e5f7fce5cd9b3a7f289f868338830f32b930d5f0bd28ddf62"
PREDECESSOR_AUDIT_SHA = "054ed52aefe45cc4d986c4621adbbdb6ca7cf36dc1c4a12cbd76238de86e21fd"
CONSUMER_REL = Path("tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd")
ENVELOPE_BUILDER_REL = Path("tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py")
FROZEN_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D48_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"

EXPECTED_SELECTED = [
    "CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004",
    "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007",
]
SELECTED_DEFINITION_SHA = {
    "CHALLENGE_001": "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea",
    "CHALLENGE_002": "db5d70a28c460e986e785c6787447529372ac5ea3b5a7ff0507667decbe2a160",
    "CHALLENGE_004": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "CHALLENGE_005": "e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30",
    "CHALLENGE_006": "2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694",
    "CHALLENGE_007": "269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61",
}
EXPECTED_GAMEPLAY_SEEDS = {
    "CHALLENGE_001": 193847,
    "CHALLENGE_002": 987654,
    "CHALLENGE_004": 314159,
    "CHALLENGE_005": 998877,
    "CHALLENGE_006": 884422,
    "CHALLENGE_007": 7770001,
}
EXPECTED_TIMEBASE = {
    "CHALLENGE_001": {"source_fps": 60, "source_frames": 540, "review_fps": 30, "review_frames": 270, "duration_seconds": 9},
    "CHALLENGE_002": {"source_fps": 60, "source_frames": 600, "review_fps": 30, "review_frames": 300, "duration_seconds": 10},
    "CHALLENGE_004": {"source_fps": 60, "source_frames": 900, "review_fps": 30, "review_frames": 450, "duration_seconds": 15},
    "CHALLENGE_005": {"source_fps": 60, "source_frames": 420, "review_fps": 30, "review_frames": 210, "duration_seconds": 7},
    "CHALLENGE_006": {"source_fps": 60, "source_frames": 540, "review_fps": 30, "review_frames": 270, "duration_seconds": 9},
    "CHALLENGE_007": {"source_fps": 60, "source_frames": 600, "review_fps": 30, "review_frames": 300, "duration_seconds": 10},
}

# 24 pins are sourced from the SHA-pinned, operator-executed E6 consumer-contract
# receipt. The script verifies that receipt itself before trusting the rows.
REQUIRED_SOURCE_PINS = 24
REQUIRED_UNPINNED_ROUTE_FILES = [
    "project.godot",
    "Main.tscn",
    "core/authoring/ChallengeMigrationAdapter.gd",
    "core/execution/ChallengeTimelineBuilder.gd",
    "core/authoring/ChallengeTimeLiine.gd",
    "core/authoring/TemporalCore.gd",
    "core/validation/ChallengeDefinitionValidator.gd",
    "core/presentation/PresentationProfile.gd",
    "core/validation/PresentationProfileValidator.gd",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(read_text(path))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def contained_path(root: Path, relative: str | Path) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"Unsafe relative path: {relative}")
    resolved = (root / rel).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"Path escaped project root: {relative}")
    return resolved


def verify_known_file(root: Path, rel: Path, expected_sha: str) -> dict[str, Any]:
    path = contained_path(root, rel)
    row: dict[str, Any] = {"path": rel.as_posix(), "expected_sha256": expected_sha}
    if not path.is_file():
        row.update({"actual_sha256": None, "status": "MISSING"})
        return row
    actual = sha256_file(path)
    row.update({"actual_sha256": actual, "status": "PASS" if actual == expected_sha else "MISMATCH", "bytes": path.stat().st_size})
    return row


def frame_count(seconds: Any, fps: int) -> int:
    value = Decimal(str(seconds)) * Decimal(fps)
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def timeline_from_definition(challenge: dict[str, Any]) -> dict[str, Any]:
    video = challenge.get("video")
    if not isinstance(video, dict):
        raise ValueError("video must be an object")
    fps_raw = video.get("fps")
    if isinstance(fps_raw, bool) or not isinstance(fps_raw, (int, float)) or int(fps_raw) != fps_raw or fps_raw <= 0:
        raise ValueError("video.fps must be a positive integer")
    fps = int(fps_raw)
    phases = []
    cursor = 0
    for name, key in (("HOOK", "hook_duration"), ("GAME", "game_duration"), ("REVEAL", "reveal_duration"), ("CTA", "cta_duration")):
        duration = video.get(key, 0.0 if name == "REVEAL" else None)
        if duration is None or isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError(f"invalid video.{key}")
        count = frame_count(duration, fps)
        phases.append({"phase": name, "duration_seconds": float(duration), "frames": count, "start_frame": cursor, "end_frame": cursor + count})
        cursor += count
    if phases[1]["frames"] <= 0:
        raise ValueError("GAME must be positive")
    return {"fps": fps, "phases": phases, "source_frames": cursor, "duration_seconds": float(cursor / fps)}


def verify_sidecar(path: Path, expected_sha: str | None = None) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    if not path.is_file():
        return {"path": path.as_posix(), "status": "MISSING"}
    actual = sha256_file(path)
    result = {"path": path.as_posix(), "actual_sha256": actual, "status": "PASS" if expected_sha is None or actual == expected_sha else "MISMATCH"}
    if sidecar.is_file():
        text = read_text(sidecar).strip()
        result["sidecar_status"] = "PASS" if text.split()[0].lower() == actual else "MISMATCH"
    else:
        result["sidecar_status"] = "MISSING"
    return result


def scan_movie_maker_scripts(root: Path) -> list[dict[str, Any]]:
    """Inventory active (non-history/non-artifact) source scripts with Movie Maker flags."""
    roots = [root / "tools", root / "c11c-suite"]
    excluded = {"history", "artifacts", ".git", ".godot", "node_modules", "__pycache__"}
    suffixes = {".ps1", ".py", ".cmd", ".bat"}
    found: list[dict[str, Any]] = []
    for base in roots:
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            if any(part.lower() in excluded for part in path.relative_to(root).parts):
                continue
            try:
                text = path.read_text(encoding="utf-8-sig", errors="replace")
            except OSError:
                continue
            if "--write-movie" not in text:
                continue
            rel = path.relative_to(root).as_posix()
            lower = rel.lower()
            if lower.startswith("tools/c11e/e2/"):
                classification = "C11E_E2_CH001_BOUNDED_NOT_E6"
            elif lower.startswith("tools/prototypes/c11c_bulk/") and "challenge" in lower:
                classification = "C11C_EXISTING_CHALLENGE_LAUNCHER_REFERENCE_ONLY"
            elif "visual_drill" in lower or "drill" in lower:
                classification = "C11C_DRILL_ROUTE_NOT_CHALLENGE"
            elif lower.startswith("tools/c11d/d9/"):
                classification = "D9_CANDIDATE_REQUIRES_SCOPE_REVIEW"
            else:
                classification = "OTHER_EXISTING_MOVIE_MAKER_SCRIPT"
            scene = None
            scene_match = re.search(r"--scene['\"]?\s*,?\s*['\"]([^'\"]+\.tscn)", text, re.IGNORECASE)
            if scene_match:
                scene = scene_match.group(1)
            found.append({
                "path": rel,
                "classification": classification,
                "observed_sha256": sha256_file(path),
                "scene_argument_observed": scene,
                "contains_c11e_envelope_argument": "--c11e-editorial-envelope" in text,
                "contains_config_argument": "--config=" in text,
            })
    return sorted(found, key=lambda x: x["path"])


def _all_patterns(text: str, patterns: Iterable[str]) -> bool:
    return all(pattern in text for pattern in patterns)


def audit_route(root: Path) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, Any]] = []
    blockers: list[str] = []
    warnings: list[str] = []

    # Pin and evidence chain.
    contract_path = contained_path(root, CONTRACT_RECEIPT_REL)
    contract_hash = sha256_file(contract_path) if contract_path.is_file() else None
    contract: dict[str, Any] = read_json(contract_path) if contract_path.is_file() else {}
    contract_pin_rows = contract.get("source_pins", {}).get("rows", [])
    contract_pin_paths = [str(x.get("path", "")) for x in contract_pin_rows if isinstance(x, dict)]
    contract_execution = contract.get("execution", {})
    contract_valid = bool(
        contract_hash == CONTRACT_RECEIPT_SHA
        and contract.get("status") == "PASS_STATIC_CONSUMER_CONTRACT_18_OF_18_EXECUTION_HELD"
        and contract.get("source_pins", {}).get("expected") == REQUIRED_SOURCE_PINS
        and contract.get("source_pins", {}).get("passed") == REQUIRED_SOURCE_PINS
        and len(contract_pin_rows) == REQUIRED_SOURCE_PINS
        and len(set(contract_pin_paths)) == REQUIRED_SOURCE_PINS
        and all(x.get("status") == "PASS" and re.fullmatch(r"[0-9a-f]{64}", str(x.get("expected_sha256", ""))) for x in contract_pin_rows if isinstance(x, dict))
        and contract_execution.get("godot_invoked") is False
        and contract_execution.get("ffmpeg_invoked") is False
        and contract_execution.get("ffprobe_invoked") is False
        and contract_execution.get("audio_generated") is False
        and contract_execution.get("media_created") is False
        and contract_execution.get("production_dispatch") is False
        and contract_execution.get("release_authority") == "NONE"
    )
    findings.append({"id": "CONSUMER_CONTRACT_RECEIPT", "status": "PASS" if contract_valid else "BLOCKED", "path": CONTRACT_RECEIPT_REL.as_posix(), "sha256": contract_hash, "expected_sha256": CONTRACT_RECEIPT_SHA})
    if not contract_valid:
        blockers.append("PINNED_E6_CHALLENGE_CONSUMER_CONTRACT_RECEIPT_MISSING_OR_MISMATCH")

    pin_rows: list[dict[str, Any]] = []
    if contract_valid:
        for source_row in contract.get("source_pins", {}).get("rows", []):
            rel = Path(str(source_row.get("path", "")))
            expected = str(source_row.get("expected_sha256", ""))
            row = verify_known_file(root, rel, expected)
            row["receipt_status"] = source_row.get("status")
            pin_rows.append(row)
    pin_passed = sum(1 for r in pin_rows if r.get("status") == "PASS")
    findings.append({"id": "CONSUMER_CONTRACT_SOURCE_PINS", "expected": REQUIRED_SOURCE_PINS, "passed": pin_passed, "status": "PASS" if pin_passed == REQUIRED_SOURCE_PINS else "BLOCKED", "rows": pin_rows})
    if pin_passed != REQUIRED_SOURCE_PINS:
        blockers.append("E6_CONSUMER_SOURCE_PIN_DRIFT_OR_MISSING_FILES")

    # Plan-only and recovery receipts.
    plan_rec = verify_known_file(root, PLAN_RECEIPT_REL, PLAN_RECEIPT_SHA)
    plan_json_rec = verify_known_file(root, PLAN_JSON_REL, PLAN_JSON_SHA)
    recovery_rec = verify_known_file(root, RECOVERY_REL, RECOVERY_SHA)
    findings.extend([
        {"id": "CHALLENGE_PLAN_RECEIPT", **plan_rec},
        {"id": "CHALLENGE_PLAN_JSON", **plan_json_rec},
        {"id": "CHALLENGE_PLAN_RECOVERY_RECEIPT", **recovery_rec},
    ])
    plan_ok = all(x.get("status") == "PASS" for x in (plan_rec, plan_json_rec, recovery_rec))
    if not plan_ok:
        blockers.append("PINNED_CHALLENGE_PLAN_OR_RECOVERY_EVIDENCE_MISSING_OR_MISMATCH")

    plan: dict[str, Any] = read_json(contained_path(root, PLAN_JSON_REL)) if plan_json_rec.get("status") == "PASS" else {}
    selected_ids = plan.get("selected_ids", [])
    selected_rows = plan.get("selected_rows", [])
    if selected_ids != EXPECTED_SELECTED or len(selected_rows) != 6:
        blockers.append("CHALLENGE_SELECTOR_PLAN_NOT_EXACT_SIX")

    plan_matrix_rows = {str(row.get("challenge_id")): row for row in selected_rows if isinstance(row, dict)}
    challenge_rows: list[dict[str, Any]] = []
    for challenge_id in EXPECTED_SELECTED:
        rel = Path(f"challenges/{challenge_id}.json")
        path = contained_path(root, rel)
        row: dict[str, Any] = {"challenge_id": challenge_id, "path": rel.as_posix()}
        expected_sha = SELECTED_DEFINITION_SHA[challenge_id]
        if not path.is_file():
            row.update({"status": "MISSING", "expected_sha256": expected_sha})
            challenge_rows.append(row)
            continue
        actual_sha = sha256_file(path)
        source = read_json(path)
        row.update({"sha256": actual_sha, "expected_sha256": expected_sha, "source_pin_status": "PASS" if actual_sha == expected_sha else "MISMATCH"})
        seed = source.get("generation", {}).get("seed")
        challenge_id_value = str(source.get("challenge_id", source.get("id", "")))
        matrix_row = plan_matrix_rows.get(challenge_id, {})
        try:
            timeline = timeline_from_definition(source)
            expected_timebase = EXPECTED_TIMEBASE[challenge_id]
            phase_match = (
                timeline["fps"] == expected_timebase["source_fps"]
                and timeline["source_frames"] == expected_timebase["source_frames"]
                and timeline["duration_seconds"] == expected_timebase["duration_seconds"]
                and timeline["source_frames"] * expected_timebase["review_fps"] % expected_timebase["source_fps"] == 0
                and timeline["source_frames"] * expected_timebase["review_fps"] // expected_timebase["source_fps"] == expected_timebase["review_frames"]
            )
        except Exception as exc:
            timeline = {"error": str(exc)}
            phase_match = False
        asset_rows = []
        for key, asset in source.get("assets", {}).items():
            asset_rel = str(asset).removeprefix("res://")
            asset_path = contained_path(root, asset_rel)
            asset_rows.append({"key": key, "res_path": str(asset), "exists": asset_path.is_file()})
        required_asset_paths = {"background_path", "target_path", "object_path"}
        asset_contract_ok = required_asset_paths.issubset(set(source.get("assets", {}).keys())) and all(a["exists"] for a in asset_rows)
        row.update({
            "challenge_id_matches_filename": challenge_id_value == challenge_id,
            "gameplay_seed": seed,
            "expected_gameplay_seed": EXPECTED_GAMEPLAY_SEEDS[challenge_id],
            "gameplay_seed_status": "PASS" if seed == EXPECTED_GAMEPLAY_SEEDS[challenge_id] else "MISMATCH",
            "timeline": timeline,
            "timeline_status": "PASS" if phase_match else "MISMATCH",
            "plan_source_hash_matches": matrix_row.get("canonical_source_sha256") == actual_sha,
            "plan_timebase_matches": matrix_row.get("source_frames") == timeline.get("source_frames") and matrix_row.get("source_fps") == timeline.get("fps"),
            "assets_status": "PASS" if asset_contract_ok else "MISMATCH",
            "assets": asset_rows,
        })
        source_ok = (actual_sha == expected_sha and challenge_id_value == challenge_id and seed == EXPECTED_GAMEPLAY_SEEDS[challenge_id] and phase_match and asset_contract_ok and matrix_row.get("canonical_source_sha256") == actual_sha and matrix_row.get("source_frames") == timeline.get("source_frames"))
        row["status"] = "PASS" if source_ok else "BLOCKED"
        challenge_rows.append(row)
    challenge_passed = sum(1 for r in challenge_rows if r.get("status") == "PASS")
    findings.append({"id": "SIX_CANONICAL_CHALLENGE_DEFINITIONS", "expected": 6, "passed": challenge_passed, "status": "PASS" if challenge_passed == 6 else "BLOCKED", "rows": challenge_rows})
    if challenge_passed != 6:
        blockers.append("SELECTED_CHALLENGE_DEFINITION_SEED_TIMELINE_OR_ASSET_DRIFT")

    # Project root / scene and CLI route.
    project_path = root / "project.godot"
    main_scene_path = root / "Main.tscn"
    generator_path = root / "GeneradorMaestro.gd"
    consumer_path = contained_path(root, CONSUMER_REL)
    adapter_path = root / "tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd"
    migration_path = root / "core/authoring/ChallengeMigrationAdapter.gd"
    timeline_builder_path = root / "core/execution/ChallengeTimelineBuilder.gd"
    timeline_path = root / "core/authoring/ChallengeTimeLiine.gd"
    temporal_path = root / "core/authoring/TemporalCore.gd"
    definition_validator_path = root / "core/validation/ChallengeDefinitionValidator.gd"

    route_sources = [project_path, main_scene_path, generator_path, consumer_path, adapter_path, migration_path, timeline_builder_path, timeline_path, temporal_path, definition_validator_path]
    route_text = {p.name: read_text(p) if p.is_file() else "" for p in route_sources}
    project_text = route_text["project.godot"]
    scene_text = route_text["Main.tscn"]
    generator_text = route_text["GeneradorMaestro.gd"]
    consumer_text = route_text["C11EChallengeLiveEditorialConsumer.gd"]
    adapter_text = route_text["c11e_challenge_editorial_presentation_adapter.gd"]
    migration_text = route_text["ChallengeMigrationAdapter.gd"]
    timeline_builder_text = route_text["ChallengeTimelineBuilder.gd"]
    timeline_text = route_text["ChallengeTimeLiine.gd"]
    temporal_text = route_text["TemporalCore.gd"]
    validator_text = route_text["ChallengeDefinitionValidator.gd"]

    route_checks = {
        "project_main_scene_is_main_tscn": 'run/main_scene="res://Main.tscn"' in project_text,
        "project_native_viewport_540x960": 'window/size/viewport_width=540' in project_text and 'window/size/viewport_height=960' in project_text,
        "main_scene_uses_generador_maestro": 'res://GeneradorMaestro.gd' in scene_text,
        "main_scene_uses_unified_social_frame": 'res://core/presentation/UnifiedSocialFrame.tscn' in scene_text,
        "generator_reads_config_argument": '"--config="' in generator_text,
        "generator_reads_optional_d_envelope_argument": 'get_cli_arg_value("--c11e-editorial-envelope")' in generator_text,
        "generator_configures_existing_generic_consumer": '_configure_c11e_live_editorial_consumer()' in generator_text and 'configure_from_file(' in generator_text,
        "generator_applies_d_after_native_bind_in_four_phases": generator_text.count('_apply_c11e_live_editorial_after_native_bind(rm)') == 4,
        "migration_copies_inline_video_timebase": 'for key in ["fps", "hook_duration", "game_duration", "reveal_duration", "cta_duration"]' in migration_text,
        "timeline_builder_consumes_canonical_inline_video": 'canonical_v2.get("video", "")' in timeline_builder_text and 'VideoTimeline.new(timeline_config)' in timeline_builder_text,
        "timeline_sums_four_phases": all(x in timeline_text for x in ['hook_frames =', 'game_frames =', 'reveal_frames =', 'cta_frames =', 'total_frames = hook_frames + game_frames + reveal_frames + cta_frames']),
        "temporal_core_rounds_duration_to_frames": 'round(duration_seconds * float(fps))' in temporal_text,
        "validator_requires_challenge_id_mechanic_generation_video_assets": all(x in validator_text for x in ['challenge_id', 'mechanic', 'generation', 'video', 'assets']),
        "consumer_checks_dynamic_challenge_identity": 'challenge_config.get("challenge_id", challenge_config.get("id", ""))' in consumer_text and 'envelope.get("challenge_id", "")' in consumer_text,
        "consumer_checks_timeline_timebase_and_phase_ranges": all(x in consumer_text for x in ['timeline.total_frames', 'timeline.fps', 'source_phase_ranges', 'SOURCE_FPS_HALF_OPEN']),
        "consumer_applies_after_native_bind": 'func apply_after_native_bind(' in consumer_text,
        "consumer_does_not_hardcode_challenge_004": 'CHALLENGE_004' not in consumer_text,
        "adapter_is_challenge_scoped_not_selector_locked": 'Challenge-only' in adapter_text and 'CHALLENGE_004' not in adapter_text,
    }
    route_passed = sum(1 for v in route_checks.values() if v)
    route_rows = [{"check": k, "status": "PASS" if v else "BLOCKED"} for k, v in route_checks.items()]
    findings.append({"id": "STATIC_EXISTING_CHALLENGE_CAPTURE_ROUTE", "expected": len(route_checks), "passed": route_passed, "status": "PASS" if route_passed == len(route_checks) else "BLOCKED", "checks": route_rows})
    if route_passed != len(route_checks):
        blockers.append("EXISTING_CHALLENGE_SCENE_CONFIG_OR_D_CONSUMER_ROUTE_DRIFT")

    # Record hashes for additional timeline/scene dependencies not included in
    # the 24-row E6 consumer receipt. These are observed, not silently promoted
    # to accepted source pins.
    unpinned_rows = []
    for rel in REQUIRED_UNPINNED_ROUTE_FILES:
        path = contained_path(root, rel)
        unpinned_rows.append({
            "path": rel,
            "status": "OBSERVED_UNPINNED" if path.is_file() else "MISSING",
            "observed_sha256": sha256_file(path) if path.is_file() else None,
            "bytes": path.stat().st_size if path.is_file() else None,
        })
    findings.append({"id": "ADDITIONAL_RUNTIME_ROUTE_DEPENDENCY_FINGERPRINTS", "status": "RECORDED_NOT_ACCEPTED_SOURCE_PINS", "rows": unpinned_rows})
    warnings.append("Main scene, project settings, migration, timeline builder and timeline arithmetic dependencies are fingerprinted here but are not part of the prior 24 accepted E6 source pins; pin them before authorizing runtime.")

    # Current envelope/audio executors remain selector-scoped.
    envelope_builder_path = contained_path(root, ENVELOPE_BUILDER_REL)
    av_review_path = root / "tools/c11d/d9/c11e_e4a_challenge_av_review.py"
    e3_audio_path = root / "c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py"
    envelope_builder_text = read_text(envelope_builder_path) if envelope_builder_path.is_file() else ""
    av_review_text = read_text(av_review_path) if av_review_path.is_file() else ""
    e3_audio_text = read_text(e3_audio_path) if e3_audio_path.is_file() else ""
    scoped_checks = {
        "e4a6_builder_pins_challenge_004_definition": 'CHALLENGE_REL = Path("challenges/CHALLENGE_004.json")' in envelope_builder_text,
        "e4a6_builder_uses_challenge_004_intent_identity": '"variant_id": "CHALLENGE_004"' in envelope_builder_text and '!= "CHALLENGE_004"' in envelope_builder_text,
        "e4a6_builder_pins_legacy_challenge_004_seeds": '"seed": 314159' in envelope_builder_text and '"music_seed": 840001' in envelope_builder_text,
        "e4a7_av_worker_isolated_challenge_004": 'CHALLENGE_004' in av_review_text and 'ISOLATED_CHALLENGE_004_D3_V5_AUDIO_MUX_REVIEW_TEST_ONLY' in av_review_text,
        "e3_audio_pipeline_is_challenge_001_only": 'selection.get("variant_id") != "CHALLENGE_001"' in e3_audio_text,
    }
    scoped_passed = sum(1 for v in scoped_checks.values() if v)
    findings.append({"id": "EXISTING_ENVELOPE_AND_AUDIO_EXECUTOR_SCOPE", "expected": len(scoped_checks), "passed": scoped_passed, "status": "PASS" if scoped_passed == len(scoped_checks) else "REVIEW", "checks": [{"check": k, "status": "PASS" if v else "REVIEW"} for k, v in scoped_checks.items()]})
    if scoped_passed != len(scoped_checks):
        warnings.append("One or more expected selector-specific scope markers could not be confirmed in current source; inspect before designing the next executor.")
    else:
        blockers.extend([
            "E4A6_ENVELOPE_BUILDER_IS_CHALLENGE_004_ONLY",
            "E4A7_AUDIO_MUX_REVIEW_WORKER_IS_CHALLENGE_004_ONLY",
            "E3_D3_V5_PIPELINE_IS_CHALLENGE_001_ONLY",
        ])

    # Inventory Movie Maker launchers without running them.
    movie_scripts = scan_movie_maker_scripts(root)
    d9_movie_runners = [x for x in movie_scripts if x["path"].lower().startswith("tools/c11d/d9/")]
    e2_movie_runners = [x for x in movie_scripts if x["classification"] == "C11E_E2_CH001_BOUNDED_NOT_E6"]
    c11c_challenge_runners = [x for x in movie_scripts if x["classification"] == "C11C_EXISTING_CHALLENGE_LAUNCHER_REFERENCE_ONLY"]
    findings.append({
        "id": "MOVIE_MAKER_LAUNCHER_INVENTORY",
        "d9_movie_maker_candidates": d9_movie_runners,
        "e2_bounded_runners": e2_movie_runners,
        "c11c_challenge_reference_runners": c11c_challenge_runners,
        "all_active_script_hits": len(movie_scripts),
        "challenge_e6_d9_runner_status": "FOUND" if d9_movie_runners else "NOT_FOUND",
    })
    if not d9_movie_runners:
        blockers.append("CHALLENGE_E6_D9_MOVIE_MAKER_ORCHESTRATOR_NOT_FOUND")
    if e2_movie_runners:
        warnings.append("The E2 Movie Maker runner is CHALLENGE_001/E2-specific (different scene and title sidecar); it is not a multi-selector E6 runner.")
    if c11c_challenge_runners:
        warnings.append("The existing C11-C bulk Challenge Movie Maker launcher is recorded as a reference only; do not modify or treat it as D9 E6 authorization.")

    # Verify governance remains held in the pinned receipts/plan.
    plan_execution = plan.get("execution", {})
    music_fixture = plan.get("music_test_fixture_proposal", {})
    governance_ok = (
        plan_execution.get("godot_invoked") is False
        and plan_execution.get("ffmpeg_invoked") is False
        and plan_execution.get("ffprobe_invoked") is False
        and plan_execution.get("audio_generated") is False
        and plan_execution.get("media_created") is False
        and plan_execution.get("production_dispatch") is False
        and plan_execution.get("release_authority") == "NONE"
        and music_fixture.get("status") == "PROPOSED_E6_TEST_ONLY_NOT_PRODUCT_DEFAULT"
        and set(music_fixture.get("e1_contract_remains_unresolved", [])) == {"tempo_bpm", "duration_seconds"}
    )
    findings.append({"id": "PLAN_GOVERNANCE_AND_MUSIC_FIXTURE_BOUNDARY", "status": "PASS" if governance_ok else "BLOCKED", "d4_8_policy_sha256": D48_SHA, "media_authorized": False, "music_fixture_status": music_fixture.get("status"), "unresolved_engine_parameters": music_fixture.get("e1_contract_remains_unresolved", [])})
    if not governance_ok:
        blockers.append("PLAN_OR_GOVERNANCE_BOUNDARY_NOT_FAIL_CLOSED")
    else:
        blockers.extend([
            "D4_8_R1V_V2_STILL_FORBIDS_SMOKE18_D3_AUDIO_PCM_AND_FFMPEG_MUX",
            "E6_TEST_ONLY_GOVERNANCE_AUTHORIZATION_NOT_PRESENT",
            "E1_TEMPO_BPM_AND_DURATION_SECONDS_REMAIN_UNRESOLVED",
        ])

    # Determine what is reusable versus new capture work, without authorizing it.
    e4a7_receipt_path = contained_path(root, "artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json")
    e4a7_receipt_status = "MISSING"
    e4a7_receipt_actual = None
    if e4a7_receipt_path.is_file():
        e4a7_receipt_actual = sha256_file(e4a7_receipt_path)
        e4a7_receipt_status = "PASS_PINNED" if e4a7_receipt_actual == "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0" else "MISMATCH"
    findings.append({
        "id": "CHALLENGE_004_REUSE_CANDIDATE",
        "receipt_path": "artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json",
        "receipt_sha256": e4a7_receipt_actual,
        "status": e4a7_receipt_status,
        "reuse_disposition": "CANDIDATE_REQUIRES_E6_LEDGER_ACCEPTANCE" if e4a7_receipt_status == "PASS_PINNED" else "NOT_REUSABLE_UNTIL_RECONCILED",
        "new_challenge_source_captures_if_reuse_accepted": 5 if e4a7_receipt_status == "PASS_PINNED" else 6,
    })

    status = "PASS_STATIC_ROUTE_AUDIT_EXECUTION_HELD" if contract_valid and plan_ok and challenge_passed == 6 and route_passed == len(route_checks) else "BLOCKED_STATIC_ROUTE_AUDIT"
    unique_blockers = list(dict.fromkeys(blockers))
    return {
        "schema": SCHEMA,
        "schema_version": "1.0",
        "status": status,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": "E6ROUTEAUDIT_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper(),
        "project_root": str(root),
        "scope": "READ_ONLY_SOURCE_AND_EVIDENCE_AUDIT_NO_GODOT_NO_FFMPEG_NO_AUDIO_NO_MEDIA",
        "execution": {
            "source_files_written": False,
            "git_checks": "SKIPPED",
            "commits": "OPERATOR_MANAGED",
            "source_file_pins_enforced": True,
            "godot_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "audio_generated": False,
            "mux_invoked": False,
            "media_created": False,
            "new_batch_id_consumed": False,
            "production_dispatch": False,
            "renderer": "OFF",
            "release_authority": "NONE",
        },
        "counts": {
            "contract_source_pins_expected": REQUIRED_SOURCE_PINS,
            "contract_source_pins_passed": pin_passed,
            "selected_challenge_definitions_expected": 6,
            "selected_challenge_definitions_passed": challenge_passed,
            "static_route_checks_expected": len(route_checks),
            "static_route_checks_passed": route_passed,
        },
        "findings": findings,
        "blockers": unique_blockers,
        "warnings": warnings,
        "next_design_boundary": {
            "existing_single_renderer": "GeneradorMaestro.gd + Main.tscn; keep unchanged",
            "existing_consumer": "C11EChallengeLiveEditorialConsumer.gd; selector-generic Challenge identity and timeline validation",
            "missing_increment": "One D9-owned PREPARE_ONLY multi-selector orchestration seam; no new Producer/binder/renderer/module",
            "per_selector_capture_inputs": ["canonical challenge JSON path", "exact per-selector E1/D envelope", "native source FPS", "native source frame count", "unique evidence path"],
            "per_selector_a_b_c_video_policy": "One immutable D-composited video source per selected Challenge, shared across A/B/C audio seed comparisons; no duplicate gameplay captures for music-only seed changes",
            "authorization": "No Movie Maker, D3 V5, FFmpeg or FFprobe invocation until separate governance approval explicitly resolves D4.8 conflict",
        },
    }


def write_receipt(report: dict[str, Any], output_root: Path) -> tuple[Path, Path]:
    output_root.mkdir(parents=True, exist_ok=False)
    receipt = output_root / "E6_CHALLENGE_CAPTURE_ROUTE_AUDIT_RECEIPT_V1.json"
    raw = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    receipt.write_bytes(raw)
    digest = sha256_bytes(raw)
    sidecar = Path(str(receipt) + ".sha256")
    sidecar.write_text(f"{digest}  {receipt.name}\n", encoding="ascii")
    return receipt, sidecar


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not root.is_dir():
        print("E6_ROUTE_AUDIT_ERROR=PROJECT_ROOT_NOT_FOUND", file=sys.stderr)
        return 2
    report = audit_route(root)
    if args.output_root is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper()
        output_root = root / "artifacts/tests/c11e/e6_challenge_capture_route_audit" / ("E6ROUTEAUDIT_" + stamp)
    else:
        output_root = args.output_root.resolve()
    receipt, sidecar = write_receipt(report, output_root)
    print(f"E6_CHALLENGE_CAPTURE_ROUTE_AUDIT_STATUS={report['status']}")
    print(f"E6_ROUTE_SOURCE_PINS={report['counts']['contract_source_pins_passed']}/{report['counts']['contract_source_pins_expected']}")
    print(f"E6_ROUTE_CHALLENGE_DEFINITIONS={report['counts']['selected_challenge_definitions_passed']}/6")
    print(f"E6_ROUTE_STATIC_ROUTE_CHECKS={report['counts']['static_route_checks_passed']}/{report['counts']['static_route_checks_expected']}")
    print(f"E6_ROUTE_BLOCKERS={len(report['blockers'])}")
    print(f"E6_GODOT_INVOKED={str(report['execution']['godot_invoked']).upper()}")
    print(f"E6_MEDIA_CREATED={str(report['execution']['media_created']).upper()}")
    print(f"E6_NEW_BATCH_ID_CONSUMED={str(report['execution']['new_batch_id_consumed']).upper()}")
    print(f"E6_PRODUCTION_DISPATCH={str(report['execution']['production_dispatch']).upper()}")
    print(f"E6_RELEASE_AUTHORITY={report['execution']['release_authority']}")
    print(f"E6_ROUTE_AUDIT_RECEIPT={receipt}")
    print(f"E6_ROUTE_AUDIT_RECEIPT_SHA256={sha256_file(receipt)}")
    print(f"E6_ROUTE_AUDIT_SIDECAR={sidecar}")
    # A source-route audit can pass while execution remains held. A BLOCKED result
    # means there is source/evidence drift, not that any runtime/media was attempted.
    return 0 if report["status"] == "PASS_STATIC_ROUTE_AUDIT_EXECUTION_HELD" else 3


if __name__ == "__main__":
    raise SystemExit(main())
