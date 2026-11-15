#!/usr/bin/env python3
"""Fail-closed, sequential E4C tracking tier-2..tier-5 qualification coordinator.

This module only coordinates the existing E1 CLI facade and D-owned executor.
It does not implement a Producer, binder, renderer, compositor, or music engine.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid
from typing import Any, Mapping

FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
STYLE_GUIDE_PATH = "docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261114_V23.md"
STYLE_GUIDE_SHA256 = "1900b8a06f52156ff18790adb44ef82268c386e2633d2b31237ebc705208c3a5"
STYLE_GUIDE_V27_PATH = "docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V27.md"
STYLE_GUIDE_V27_SHA256 = "93b83ec7c5a640235edc3d70e877088896babe9d6d3b1fc3ed224fe0b6b07f43"
BASE_REQUEST_REL = "artifacts/production/c11e/E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8/request.json"
BASE_RECEIPT_REL = "artifacts/production/c11e/E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8/E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"
BASE_REQUEST_SHA256 = "886c21782ded4759585352f01615aecc0d6639628285c0293e53a59dc953000e"
BASE_RECEIPT_SHA256 = "57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903"
CLI_REL = "c11c-suite/c11c-producer/c11e_production_cli.py"
EXECUTOR_REL = "tools/c11d/d9/c11e_e4c_drill_execution.py"
CONSUMER_REL = "tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py"
CONSUMER_TEST_REL = "tests/test_c11e_e4c_drill_visual_composition_consumer.py"

# Exact post-R6.3A source identity. Includes the amended D consumer and its test;
# the other rows come from the accepted R6.3A package's 25-source-pin manifest.
SOURCE_PINS: dict[str, str] = {
    "assets/fonts/Inter-Bold.otf": "9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d",
    "assets/fonts/NotoSansMono-Regular.ttf": "6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f",
    "c11c-suite/c11c-producer/C11CVisualDrillProducerEnvelopeGenerator.gd": "9e2a2f394db7efce6f646600d0bb8f4ee8488c87a184df1a0fb7f7cdcb9066e9",
    "c11c-suite/c11c-producer/c11e_production_cli.py": "3e530e535accc31455207d1e8e3253140c95b390348b4ee252ec8b5ee140869a",
    "c11c-suite/c11c-producer/c11e_production_service.py": "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87",
    "c11c-suite/c11c-producer/main.py": "86eeca0c3fc37105c1202295db3f27e6dc249f4eafdcb48c5709cd2d76164393",
    "c11c-suite/c11c-producer/run_visual_drill_production.ps1": "ad6a7f0a6ce87804363810123f76ff0765b1582426cb2c8f69f6864ec3a0c808",
    "core/presentation/PresentationProfile.gd": "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24",
    "core/presentation/rendering/VisualContentPlayer.gd": "58d86d56ebd7507c9e800c83010103b9be12f1b5dca9356da61ca623e4cf0145",
    "core/presentation/rendering/VisualContentPlayer.tscn": "8c3005a68aa0e818b078b06ae31054524d523b95e396dc1676dce28374ff8b27",
    "definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_SCHEMA_V1.json": "c5cedcd749a6702dc47b1de0bd67c57721bb9a06cee5cb3709cdc1b17d8a6806",
    "definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_V1.json": "44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8",
    "profiles/difficulty/visual_drill_peripheral_scan.json": "7c52112bf9c106152d7fe03b646bde0f415881a04efb75560d731fa3f18fa73e",
    "profiles/difficulty/visual_drill_pursuit.json": "ab6a29af53bdb45fb6976bfdd558e3275c477eb7ad9afd61b9d01e36d43afb05",
    "profiles/difficulty/visual_drill_saccade.json": "6be50f582ef5ce11d36b72943750b88e72da67d858d67c3ac3d38d33c11ccf38",
    "profiles/difficulty/visual_drill_tracking.json": "6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e",
    "profiles/presentation/c11c_visual_music_profiles.json": "b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58",
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": FROZEN_MANIFEST_SHA256,
    EXECUTOR_REL: "b7cbf7bd97f76f4c2e339840fc694d3f5b0e50186ba2456e45ff00e585751abe",
    "tools/prototypes/c11c_common/C11CSafeAmbient.py": "c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c",
    "tools/prototypes/c11c_common/generate_c11c_family_music.py": "41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d",
    "core/presentation/C11CVisualEditorialLayer.gd": "f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d",
    "core/presentation/C11CVisualTypography.gd": "9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633",
    "tools/prototypes/c11c_common/C11CDrillPaletteBank.gd": "757786a6bcc4e819fd43c1c41ea29e8b00dbe3b3f2f5c72fa19776a368b3c8ec",
    "definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_FAMILY_TITLE_AMENDMENT_R1_20261114.json": "1d0d5393368ca1e1ecb867059314e28463205fffc81e8af902909896e0ac7331",
    CONSUMER_REL: "d5cd8e24c0cfdd83ec035b006c76468ed637d6babf5f0a9fcca8a93817ba1aa8",
    CONSUMER_TEST_REL: "5da9ec59d0f6d716861e9a4cbcfc36db5e61f992c966a2294bb23ef2c344bafb",
    STYLE_GUIDE_PATH: STYLE_GUIDE_SHA256,
    BASE_REQUEST_REL: BASE_REQUEST_SHA256,
    BASE_RECEIPT_REL: BASE_RECEIPT_SHA256,
}

EXPECTED_PROFILE = "FLOWING_VECTOR"
TIERS = (2, 3, 4, 5)


class BatchError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise BatchError(f"expected JSON object: {path}")
    return value


def write_json_exclusive(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def write_json_replace(path: Path, value: Mapping[str, Any]) -> None:
    """Atomically refresh a coordinator-owned progress file inside its new batch root."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verify_pins(root: Path) -> dict[str, str]:
    actual: dict[str, str] = {}
    failures: list[str] = []
    for relative, expected in SOURCE_PINS.items():
        path = root / Path(*relative.split("/"))
        if not path.is_file():
            failures.append(f"MISSING:{relative}")
            continue
        digest = sha256_file(path)
        actual[relative] = digest
        if digest != expected:
            failures.append(f"SHA_MISMATCH:{relative}:{expected}:{digest}")
    if failures:
        raise BatchError("SOURCE_PIN_PREFLIGHT_FAILED: " + " | ".join(failures))
    return actual


def verify_postinstall_style_guide(root: Path) -> str:
    path = root / Path(*STYLE_GUIDE_V27_PATH.split("/"))
    if not path.is_file():
        raise BatchError(f"POSTINSTALL_STYLE_GUIDE_V27_MISSING: {path}")
    digest = sha256_file(path)
    if digest != STYLE_GUIDE_V27_SHA256:
        raise BatchError(f"POSTINSTALL_STYLE_GUIDE_V27_SHA_MISMATCH: {digest}")
    return digest


def verify_environment(root: Path) -> dict[str, str]:
    if sys.version_info[:2] != (3, 13):
        raise BatchError(f"PYTHON_3_13_REQUIRED: found={sys.version.split()[0]}")
    try:
        import PySide6  # noqa: F401
    except Exception as exc:  # pragma: no cover - Windows environment guard
        raise BatchError(f"PYSIDE6_IMPORT_FAILED: {exc}") from exc
    if not (root / CLI_REL).is_file():
        raise BatchError(f"CLI_FACADE_MISSING: {CLI_REL}")
    return {"python": sys.version.split()[0], "pyside6": PySide6.__version__}


def create_request(base: Mapping[str, Any], tier: int, request_id: str) -> dict[str, Any]:
    request = json.loads(json.dumps(base))
    request["request_id"] = request_id
    request["selection"]["content_type"] = "visual_drills"
    request["selection"]["family_id"] = "tracking"
    request["selection"]["variant_id"] = f"tier-{tier}"
    request["seed"] = 12345
    request["music_seed"] = 840001
    request["variation_index"] = 0
    request["audio_enabled"] = True
    request["personalization_enabled"] = True
    request["mode"] = "PRODUCTION"
    request["delivery_profile_id"] = "REVIEW_720"
    request["production_override"]["title"] = f"SEGUIMIENTO VISUAL · NIVEL {tier}"
    request["production_override"]["subtitle"] = "Sigue el objetivo con precisión"
    request["production_override"]["call_to_action"] = "Mantén la mirada en el objetivo"
    request.setdefault("provenance", {})["request_origin"] = "CLI"
    return request


def validate_base(root: Path) -> dict[str, Any]:
    base_path = root / Path(*BASE_REQUEST_REL.split("/"))
    receipt_path = root / Path(*BASE_RECEIPT_REL.split("/"))
    if sha256_file(base_path) != BASE_REQUEST_SHA256:
        raise BatchError("BASE_REQUEST_HASH_MISMATCH")
    if sha256_file(receipt_path) != BASE_RECEIPT_SHA256:
        raise BatchError("BASE_ACCEPTED_CLI_RECEIPT_HASH_MISMATCH")
    request = read_json(base_path)
    receipt = read_json(receipt_path)
    if request.get("request_id") != "E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8":
        raise BatchError("BASE_REQUEST_ID_MISMATCH")
    if request.get("selection") != {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"}:
        raise BatchError("BASE_SELECTOR_MISMATCH")
    if receipt.get("status") != "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION":
        raise BatchError("BASE_TECHNICAL_RECEIPT_NOT_PASS")
    if receipt.get("request_id") != request["request_id"] or receipt.get("request_origin") != "CLI":
        raise BatchError("BASE_RECEIPT_REQUEST_BINDING_MISMATCH")
    if receipt.get("family_music_profile") != EXPECTED_PROFILE:
        raise BatchError("BASE_MUSIC_PROFILE_MISMATCH")
    if receipt.get("production_dispatch") is not False or receipt.get("release_authority") != "NONE":
        raise BatchError("BASE_GOVERNANCE_MISMATCH")
    return request


def verify_ffprobe_contract(final: Mapping[str, Any], label: str) -> None:
    if abs(float(final.get("duration_seconds", -1)) - 27.0) > 0.001:
        raise BatchError(f"{label}_DURATION_MISMATCH")
    if abs(float(final.get("av_start_delta_seconds", 999)) - 0.0) > 0.001:
        raise BatchError(f"{label}_AV_START_DRIFT")
    probe = final.get("ffprobe", {})
    streams = probe.get("streams", []) if isinstance(probe, Mapping) else []
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not video or not audio or len(streams) != 2:
        raise BatchError(f"{label}_FFPROBE_STREAM_CARDINALITY")
    expected_video = {
        "codec_name": "h264", "profile": "High", "width": 720, "height": 1280,
        "pix_fmt": "yuv420p", "color_range": "tv", "avg_frame_rate": "30/1",
    }
    for field, expected in expected_video.items():
        if video.get(field) != expected:
            raise BatchError(f"{label}_VIDEO_{field}_MISMATCH: {video.get(field)!r}")
    if str(video.get("nb_read_frames")) != "810":
        raise BatchError(f"{label}_VIDEO_FRAME_COUNT_MISMATCH")
    expected_audio = {"codec_name": "aac", "profile": "LC", "sample_rate": "48000", "channels": 2, "channel_layout": "stereo"}
    for field, expected in expected_audio.items():
        if audio.get(field) != expected:
            raise BatchError(f"{label}_AUDIO_{field}_MISMATCH: {audio.get(field)!r}")


def validate_qualification(root: Path, request: Mapping[str, Any], summary_path: Path, tier: int) -> dict[str, Any]:
    summary = read_json(summary_path)
    request_id = str(request["request_id"])
    selector = f"tracking/tier-{tier}"
    if summary.get("status") != "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION":
        raise BatchError(f"{selector}_SUMMARY_STATUS={summary.get('status')}")
    if summary.get("request_id") != request_id or summary.get("selector") != selector:
        raise BatchError(f"{selector}_SUMMARY_IDENTITY_MISMATCH")
    if summary.get("family_music_profile") != EXPECTED_PROFILE:
        raise BatchError(f"{selector}_SUMMARY_MUSIC_PROFILE_MISMATCH")
    receipt_path = Path(str(summary.get("receipt", ""))).resolve()
    if not receipt_path.is_file():
        raise BatchError(f"{selector}_FULL_RECEIPT_MISSING: {receipt_path}")
    expected_root = (root / "artifacts" / "production" / "c11e" / request_id).resolve()
    if receipt_path.parent != expected_root:
        raise BatchError(f"{selector}_RECEIPT_OUTSIDE_EXPECTED_ROOT")
    receipt = read_json(receipt_path)
    checks = {
        "status": "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION",
        "request_id": request_id,
        "request_origin": "CLI",
        "family": "tracking",
        "tier": tier,
        "gameplay_seed": 12345,
        "music_seed_a": 840001,
        "music_seed_b": 840001,
        "family_music_profile": EXPECTED_PROFILE,
        "family_adapter_preparation_status": "NOT_CONNECTED_E1",
        "release_authority": "NONE",
        "production_dispatch": False,
        "production_release": False,
        "c11c_frozen_manifest_unchanged": True,
        "c11c_manifest_sha256": FROZEN_MANIFEST_SHA256,
        "c11c_source_mutation": False,
        "renderer_invoked": True,
        "d_postcomposition": True,
        "ffmpeg_decode_encode_mux": True,
        "audio_generated": True,
        "source_pins_pre_post_equal": True,
        "source_pin_count": 91,
    }
    for field, expected in checks.items():
        if receipt.get(field) != expected:
            raise BatchError(f"{selector}_RECEIPT_{field}_MISMATCH: {receipt.get(field)!r}")
    if receipt.get("family_adapter_execution", {}).get("shared_entrypoint") != "c11e_e4c_drill_execution.py":
        raise BatchError(f"{selector}_SHARED_EXECUTOR_MISMATCH")
    parity = receipt.get("e1_gui_cli_parity", {})
    if parity.get("status") != "PASS_E1_SHARED_GUI_CLI_INTENT_PARITY" or parity.get("semantic_identity_equal") is not True:
        raise BatchError(f"{selector}_GUI_CLI_PARITY_FAIL")
    if receipt.get("e1_validation", {}).get("status") != "PASS_E1_PREPARATION_ONLY":
        raise BatchError(f"{selector}_E1_BOUNDARY_FAIL")
    timeline = receipt.get("native_timeline", {})
    if timeline.get("fps") != 30 or timeline.get("total_frames") != 810 or abs(float(timeline.get("duration_seconds", -1)) - 27.0) > 0.001:
        raise BatchError(f"{selector}_NATIVE_TIMELINE_MISMATCH")
    composition = receipt.get("d_composition", {})
    if composition.get("frames_composed") != 810 or composition.get("frames_expected") != 810:
        raise BatchError(f"{selector}_D_COMPOSITION_FRAME_COUNT_MISMATCH")
    if composition.get("phase_counts") != {"PRE_ROLL": 90, "GAME": 630, "END_CTA": 90}:
        raise BatchError(f"{selector}_D_PHASE_CARDINALITY_MISMATCH")
    visible = set(receipt.get("d_editorial_visible_fields", []))
    if not {"title", "subtitle", "call_to_action"}.issubset(visible):
        raise BatchError(f"{selector}_D_EDITORIAL_VISIBILITY_FAIL")
    music = receipt.get("family_music", {})
    if music.get("route") != "C11_C_FAMILY_MUSIC_V4" or music.get("profile_id") != EXPECTED_PROFILE:
        raise BatchError(f"{selector}_FAMILY_MUSIC_ROUTE_OR_PROFILE_FAIL")
    if music.get("same_seed_ab_identical") is not True or music.get("changed_seed_c_distinct") is not True:
        raise BatchError(f"{selector}_FAMILY_MUSIC_SEED_ISOLATION_FAIL")
    music_hashes = [music.get(k, {}).get("sha256") for k in ("A", "B", "C")]
    music_paths = [Path(str(music.get(k, {}).get("path", ""))) for k in ("A", "B", "C")]
    if not all(isinstance(h, str) and re.fullmatch(r"[a-f0-9]{64}", h) for h in music_hashes):
        raise BatchError(f"{selector}_MUSIC_HASHES_MISSING")
    if music_hashes[0] != music_hashes[1] or music_hashes[0] == music_hashes[2]:
        raise BatchError(f"{selector}_MUSIC_HASH_RELATION_FAIL")
    for label, path, digest in zip(("A", "B", "C"), music_paths, music_hashes):
        if not path.is_file() or sha256_file(path) != digest:
            raise BatchError(f"{selector}_MUSIC_{label}_WAV_FILE_HASH_FAIL")
    isolation = receipt.get("bitstream_isolation", {})
    if isolation.get("video_stream_identical") is not True or isolation.get("audio_stream_changed") is not True:
        raise BatchError(f"{selector}_FINAL_STREAM_ISOLATION_FAIL")
    if isolation.get("video_stream_sha256_A") != isolation.get("video_stream_sha256_C"):
        raise BatchError(f"{selector}_VIDEO_STREAM_SHA_RELATION_FAIL")
    if isolation.get("audio_stream_sha256_A") == isolation.get("audio_stream_sha256_C"):
        raise BatchError(f"{selector}_AUDIO_STREAM_SHA_RELATION_FAIL")
    verify_ffprobe_contract(receipt.get("final_A", {}), f"{selector}_A")
    verify_ffprobe_contract(receipt.get("final_C_changed_music", {}), f"{selector}_C")
    for label, media in (("A", receipt.get("final_A", {})), ("C", receipt.get("final_C_changed_music", {}))):
        media_path = Path(str(media.get("path", "")))
        if not media_path.is_file() or sha256_file(media_path) != media.get("sha256"):
            raise BatchError(f"{selector}_FINAL_{label}_MEDIA_HASH_FAIL")
    return {
        "selector": selector,
        "request_id": request_id,
        "technical_status": receipt["status"],
        "qualification_receipt": str(receipt_path),
        "qualification_receipt_sha256": sha256_file(receipt_path),
        "final_A": receipt["final_A"]["path"],
        "final_A_sha256": receipt["final_A"]["sha256"],
        "final_C": receipt["final_C_changed_music"]["path"],
        "final_C_sha256": receipt["final_C_changed_music"]["sha256"],
        "music_A_B_sha256": music_hashes[0],
        "music_C_sha256": music_hashes[2],
        "review_status": "PENDING_OPERATOR_VISUAL_AUDIO_REVIEW",
    }


def batch_plan(batch_id: str) -> list[dict[str, Any]]:
    if not re.fullmatch(r"E4C-TRACKING-T2-5-[A-Za-z0-9._-]{8,64}", batch_id):
        raise BatchError("BATCH_ID_INVALID")
    short = batch_id.rsplit("-", 1)[-1]
    return [
        {"tier": tier, "selector": f"tracking/tier-{tier}", "request_id": f"E4C-TRK-T{tier}-{short}",
         "gameplay_seed": 12345, "music_seed_a_b": 840001, "music_seed_c": "DERIVED_BY_EXISTING_EXECUTOR",
         "family_music_profile": EXPECTED_PROFILE, "expected_frames": 810}
        for tier in TIERS
    ]


def execute_batch(root: Path, python: Path, batch_id: str, timeout_seconds: int) -> dict[str, Any]:
    plan = batch_plan(batch_id)
    actual_pins = verify_pins(root)
    environment = verify_environment(root)
    base = validate_base(root)
    cli_path = root / Path(*CLI_REL.split("/"))

    for row in plan:
        product_root = root / "artifacts" / "production" / "c11e" / row["request_id"]
        if product_root.exists():
            raise BatchError(f"OUTPUT_COLLISION: {product_root}")

    evidence_root = root / "artifacts" / "tests" / "c11e" / "e4c_tracking_tier_batch" / batch_id
    if evidence_root.exists():
        raise BatchError(f"BATCH_EVIDENCE_COLLISION: {evidence_root}")
    evidence_root.mkdir(parents=True, exist_ok=False)
    lock_path = evidence_root / "ATTEMPT_RESERVED.lock.json"
    lock = {"schema": "C11E-E4C-TRACKING-TIER-BATCH-LOCK-V1", "status": "ATTEMPT_RESERVED",
            "batch_id": batch_id, "request_ids": [r["request_id"] for r in plan],
            "source_pin_set_sha256": hashlib.sha256(json.dumps(actual_pins, sort_keys=True).encode()).hexdigest(),
            "git_checks": "SKIPPED", "commits": "OPERATOR_MANAGED"}
    write_json_exclusive(lock_path, lock)
    authorization_path = evidence_root / "EXECUTION_AUTHORIZED_ONCE.json"
    write_json_exclusive(authorization_path, {"schema": "C11E-E4C-TRACKING-TIER-BATCH-EXECUTION-AUTH-V1",
        "status": "AUTHORIZED_ONCE_BEFORE_FIRST_CHILD", "batch_id": batch_id,
        "request_ids": [r["request_id"] for r in plan],
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "policy": "Any failure after this marker forbids retry with this batch ID; preserve outputs and use a newly reviewed continuation."})

    batch_rows: list[dict[str, Any]] = []
    progress_path = evidence_root / "BATCH_PROGRESS.json"
    progress: dict[str, Any] = {"schema": "C11E-E4C-TRACKING-TIER-BATCH-PROGRESS-V1",
        "status": "RUNNING", "batch_id": batch_id, "expected": [r["selector"] for r in plan],
        "completed_rows": [], "current_selector": None, "failed_selector": None,
        "operator_review": "PENDING", "release_authority": "NONE"}
    write_json_exclusive(progress_path, progress)
    for row in plan:
        tier = row["tier"]
        request_id = row["request_id"]
        request = create_request(base, tier, request_id)
        request_path = evidence_root / f"{request_id}.request.json"
        summary_path = evidence_root / f"{request_id}.CLI_EXECUTION_RESULT.json"
        stdout_path = evidence_root / f"{request_id}.CLI_STDOUT.log"
        stderr_path = evidence_root / f"{request_id}.CLI_STDERR.log"
        write_json_exclusive(request_path, request)
        command = [str(python), str(cli_path), "--request", str(request_path), "--origin", "CLI",
                   "--execute-drill-av", "--output", str(summary_path)]
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        try:
            process = subprocess.run(command, cwd=str(root), capture_output=True, text=True,
                                     encoding="utf-8", errors="replace", timeout=timeout_seconds, check=False)
            exit_code = int(process.returncode)
            stdout = process.stdout or ""
            stderr = process.stderr or ""
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            stdout_path.write_text(stdout, encoding="utf-8")
            stderr_path.write_text(stderr, encoding="utf-8")
            failure = {"selector": row["selector"], "request_id": request_id, "status": "TIMEOUT_FAIL_CLOSED",
                       "timeout_seconds": timeout_seconds, "started_utc": started,
                       "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                       "stdout_log": str(stdout_path), "stderr_log": str(stderr_path),
                       "production_dispatch": False, "release_authority": "NONE"}
            write_json_exclusive(evidence_root / f"{request_id}.BATCH_ROW_FAILURE.json", failure)
            progress.update({"status": "STOPPED_FAIL_CLOSED", "current_selector": row["selector"],
                             "failed_selector": row["selector"], "failure_receipt": str(evidence_root / f"{request_id}.BATCH_ROW_FAILURE.json")})
            write_json_replace(progress_path, progress)
            raise BatchError(f"{row['selector']} timed out; preserved logs and partial outputs") from exc
        stdout_path.write_text(stdout, encoding="utf-8")
        stderr_path.write_text(stderr, encoding="utf-8")
        if exit_code != 0:
            failure = {"selector": row["selector"], "request_id": request_id, "status": "CHILD_EXIT_FAIL_CLOSED",
                       "process_exit_code": exit_code, "started_utc": started,
                       "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                       "stdout_log": str(stdout_path), "stderr_log": str(stderr_path),
                       "cli_summary_exists": summary_path.is_file(), "production_dispatch": False, "release_authority": "NONE"}
            write_json_exclusive(evidence_root / f"{request_id}.BATCH_ROW_FAILURE.json", failure)
            progress.update({"status": "STOPPED_FAIL_CLOSED", "current_selector": row["selector"],
                             "failed_selector": row["selector"], "failure_receipt": str(evidence_root / f"{request_id}.BATCH_ROW_FAILURE.json")})
            write_json_replace(progress_path, progress)
            raise BatchError(f"{row['selector']} child exit code={exit_code}; preserved evidence")
        if not summary_path.is_file():
            failure = {"selector": row["selector"], "request_id": request_id,
                       "status": "CLI_SUMMARY_MISSING_FAIL_CLOSED", "process_exit_code": exit_code,
                       "stdout_log": str(stdout_path), "stderr_log": str(stderr_path),
                       "production_dispatch": False, "release_authority": "NONE"}
            failure_path = evidence_root / f"{request_id}.BATCH_ROW_FAILURE.json"
            write_json_exclusive(failure_path, failure)
            progress.update({"status": "STOPPED_FAIL_CLOSED", "current_selector": row["selector"],
                             "failed_selector": row["selector"], "failure_receipt": str(failure_path)})
            write_json_replace(progress_path, progress)
            raise BatchError(f"{row['selector']} CLI summary missing after child exit 0")
        try:
            row_result = validate_qualification(root, request, summary_path, tier)
            row_result.update({"request_path": str(request_path), "request_sha256": sha256_file(request_path),
                               "cli_summary_path": str(summary_path), "cli_summary_sha256": sha256_file(summary_path),
                               "process_exit_code": exit_code, "stdout_log": str(stdout_path), "stderr_log": str(stderr_path)})
            # Re-check before recording this selector as completed.
            if verify_pins(root) != actual_pins:
                raise BatchError(f"SOURCE_PIN_DRIFT_AFTER_{row['selector']}")
            batch_rows.append(row_result)
        except Exception as exc:
            failure = {"selector": row["selector"], "request_id": request_id,
                       "status": "POST_CHILD_AUDIT_FAIL_CLOSED", "error": f"{type(exc).__name__}: {exc}",
                       "process_exit_code": exit_code, "started_utc": started,
                       "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                       "request_path": str(request_path), "cli_summary_path": str(summary_path),
                       "stdout_log": str(stdout_path), "stderr_log": str(stderr_path),
                       "production_dispatch": False, "release_authority": "NONE"}
            failure_path = evidence_root / f"{request_id}.BATCH_ROW_FAILURE.json"
            if not failure_path.exists():
                write_json_exclusive(failure_path, failure)
            progress.update({"status": "STOPPED_FAIL_CLOSED", "current_selector": row["selector"],
                             "failed_selector": row["selector"], "failure_receipt": str(failure_path),
                             "completed_rows": batch_rows})
            write_json_replace(progress_path, progress)
            raise
        progress.update({"status": "RUNNING", "current_selector": None,
                         "completed_rows": batch_rows, "last_completed_selector": row["selector"]})
        write_json_replace(progress_path, progress)

    result = {
        "schema": "C11E-E4C-TRACKING-TIER-BATCH-RESULT-V1",
        "status": "PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW",
        "batch_id": batch_id,
        "selectors_expected": [r["selector"] for r in plan],
        "selectors_technical_pass": [r["selector"] for r in batch_rows],
        "coverage": "4/4 tracking tiers 2-5",
        "rows": batch_rows,
        "environment": environment,
        "source_pin_count": len(actual_pins),
        "source_pins_pre_post_equal": True,
        "base_accepted_cli_smoke": {"request_sha256": BASE_REQUEST_SHA256, "qualification_receipt_sha256": BASE_RECEIPT_SHA256,
                                     "selector": "tracking/tier-1", "rerun": False},
        "operator_review": {"status": "PENDING", "required_media": "For every row, review final_A and final_C video plus A/B/C family music evidence; confirm layout, typography, title role, editorial, visual identity and audio."},
        "governance": {"c11c_frozen_manifest_sha256": FROZEN_MANIFEST_SHA256, "c11c_source_mutation": False,
                       "production_dispatch": False, "release_authority": "NONE", "e1": "PREPARE_ONLY",
                       "family_adapter": "NOT_CONNECTED_E1", "git_checks": "SKIPPED", "commits": "OPERATOR_MANAGED"},
        "evidence_root": str(evidence_root),
        "lock": str(lock_path),
        "execution_authorization": str(authorization_path),
        "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    write_json_exclusive(evidence_root / "BATCH_RESULT.json", result)
    progress.update({"status": "PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW", "current_selector": None,
                     "completed_rows": batch_rows, "failed_selector": None,
                     "batch_result": str(evidence_root / "BATCH_RESULT.json")})
    write_json_replace(progress_path, progress)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="E4C tracking tier-2..tier-5 sequential qualification batch")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--python-exe", default=sys.executable)
    parser.add_argument("--batch-id", default=None)
    parser.add_argument("--execute", action="store_true", help="Authorize and execute the four isolated A/V qualifications")
    parser.add_argument("--timeout-seconds", type=int, default=7200)
    parser.add_argument("--require-v27-guide", action="store_true",
                        help="Require the installed V27 PowerShell style guide before batch execution")
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    python = Path(args.python_exe).resolve()
    if not root.is_dir():
        raise BatchError(f"PROJECT_ROOT_MISSING: {root}")
    if not python.is_file():
        raise BatchError(f"PYTHON_EXE_MISSING: {python}")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8]
    batch_id = args.batch_id or f"E4C-TRACKING-T2-5-{stamp}-{suffix}"
    plan = batch_plan(batch_id)
    if args.require_v27_guide:
        guide_sha = verify_postinstall_style_guide(root)
        print(f"POWERSHELL_STYLE_GUIDE_V27=PASS/{guide_sha}", file=sys.stderr)
    if not args.execute:
        pins = verify_pins(root)
        environment = verify_environment(root)
        validate_base(root)
        for row in plan:
            output = root / "artifacts" / "production" / "c11e" / row["request_id"]
            if output.exists():
                raise BatchError(f"OUTPUT_COLLISION: {output}")
        preview = {"status": "PASS_PREPARE_ONLY_NO_RENDER", "batch_id": batch_id,
                   "selectors": plan, "source_pin_count": len(pins), "environment": environment,
                   "base_cli_smoke": "PASS_REUSED_NO_RERUN", "renderer_invoked": False,
                   "godot_invoked": False, "ffmpeg_invoked": False, "production_media_created": False,
                   "production_dispatch": False, "release_authority": "NONE"}
        print(json.dumps(preview, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    result = execute_batch(root, python, batch_id, args.timeout_seconds)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BatchError as exc:
        print(json.dumps({"status": "FAIL_CLOSED_E4C_TRACKING_TIER_BATCH", "error": str(exc),
                          "production_dispatch": False, "release_authority": "NONE"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
