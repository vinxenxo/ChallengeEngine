#!/usr/bin/env python3
"""E4A.3: exercise the existing D-owned Godot materializer over real C11-C frames.

Reuses the accepted E4A.2 silent Challenge 004 test MP4 and its normalized
REVIEW_720 derivative. FFmpeg extracts six unmodified background frames only.
The existing D materializer's off-screen Godot SubViewport creates a transparent
editorial layer and alpha-composites it over those frames. No C11-C render,
production renderer, D9.10 dispatch, FFmpeg drawtext, audio, or production media.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
MATERIALIZER = Path("tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd")
MATERIALIZER_SHA256 = "3d1c8288ffbea3ff328d785def5fabba250b042c0d2d1b1f94215b1c62cde29b"
PREVIOUS_RUNNER = Path("tools/c11d/d9/c11e_e4a_challenge_real_body_pixel_review.py")
PREVIOUS_RUNNER_SHA256 = "5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b"
PREVIOUS_TEST = Path("tools/c11d/d9/test_c11e_e4a_challenge_real_body_pixel_review.py")
PREVIOUS_TEST_SHA256 = "657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b"
E1_INTENT_HELPER = Path("tools/c11d/d9/c11e_e4a_challenge_pixel_review.py")
E1_INTENT_HELPER_SHA256 = "939a12f369df9eaa0dbaf5b06b0635a0d4dc906e14fd7d5bdf9c12b3ec2b97a0"
E1_SERVICE = Path("c11c-suite/c11c-producer/c11e_production_service.py")
E1_SERVICE_SHA256 = "f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0"
D99_RESOLVER = Path("tools/c11d/d9/universal_producer.py")
D99_RESOLVER_SHA256 = "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1"
C11C_RENDERER = Path("tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1")
C11C_RENDERER_SHA256 = "c3fed414912f50efed1687e258c48c5e85c08989a473ed12c38dc9784db171d5"
MAIN_SOURCE = Path("c11c-suite/c11c-producer/main.py")
MAIN_SOURCE_SHA256 = "f0adc54de884d6d812396707cd6ced49038df0f52e4a9bc516a9ca5e6a0ddcd3"
CHALLENGE_SOURCE = Path("challenges/CHALLENGE_004.json")
CHALLENGE_SHA256 = "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
APPROVAL_SOURCE = Path("definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json")
APPROVAL_SHA256 = "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
LAYOUT_SOURCE = Path("docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md")
LAYOUT_SHA256 = "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
MANIFEST_SOURCE = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
PREVIOUS_REPORT_SHA256 = "e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159"
BASE_MP4_SHA256 = "fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de"
NORMALIZED_MP4_SHA256 = "edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e"
PREVIOUS_RECEIPT_SCHEMA = "C11E-E4A-REAL-BODY-PIXEL-RUNNER-RECEIPT-V1"
PREVIOUS_REPORT_SCHEMA = "C11E-E4A-REAL-BODY-PIXEL-REPORT-V1"
CONFIG_SCHEMA = "C11E-E4A-D-GODOT-COMPOSITOR-PIXEL-TEST-CONFIG-V1"
REPORT_SCHEMA = "C11E-E4A-D-GODOT-COMPOSITOR-REAL-BODY-PIXEL-REPORT-V1"
RECEIPT_SCHEMA = "C11E-E4A-D-GODOT-COMPOSITOR-REAL-BODY-PIXEL-RECEIPT-V1"
DELIVERY_FPS = 30
SOURCE_FPS = 60
WIDTH = 720
HEIGHT = 1280
EXPECTED_SAMPLES = [
    {"label": "hook_first", "phase": "HOOK", "delivery_frame": 0},
    {"label": "hook_last", "phase": "HOOK", "delivery_frame": 89},
    {"label": "game_first", "phase": "GAME", "delivery_frame": 90},
    {"label": "reveal_first", "phase": "REVEAL", "delivery_frame": 300},
    {"label": "cta_first", "phase": "CTA", "delivery_frame": 390},
    {"label": "cta_last", "phase": "CTA", "delivery_frame": 449},
]
REGIONS = {
    "HEADER": (0, 0, 720, 192),
    "BODY": (0, 192, 720, 1088),
    "FOOTER": (0, 1088, 720, 1280),
}


class CompositorReviewError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise CompositorReviewError(f"Cannot parse JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CompositorReviewError(f"Expected JSON object in {path}")
    return value


def import_previous_runner(root: Path):
    path = root / PREVIOUS_RUNNER
    spec = importlib.util.spec_from_file_location("c11e_e4a_previous_real_body_runner", path)
    if spec is None or spec.loader is None:
        raise CompositorReviewError("Cannot load the accepted E4A.2 evidence validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_source_pins(root: Path) -> dict[str, str]:
    pins = {
        "d_owned_materializer_v3": (MATERIALIZER, MATERIALIZER_SHA256),
        "e4a2_runner": (PREVIOUS_RUNNER, PREVIOUS_RUNNER_SHA256),
        "e4a2_test": (PREVIOUS_TEST, PREVIOUS_TEST_SHA256),
        "e1_intent_helper": (E1_INTENT_HELPER, E1_INTENT_HELPER_SHA256),
        "e1_service": (E1_SERVICE, E1_SERVICE_SHA256),
        "d99_resolver": (D99_RESOLVER, D99_RESOLVER_SHA256),
        "c11c_renderer_read_only": (C11C_RENDERER, C11C_RENDERER_SHA256),
        "producer_main_read_only": (MAIN_SOURCE, MAIN_SOURCE_SHA256),
        "challenge_004": (CHALLENGE_SOURCE, CHALLENGE_SHA256),
        "approved_policy": (APPROVAL_SOURCE, APPROVAL_SHA256),
        "d1_5_layout": (LAYOUT_SOURCE, LAYOUT_SHA256),
        "frozen_manifest": (MANIFEST_SOURCE, MANIFEST_SHA256),
    }
    observed: dict[str, str] = {}
    for name, (relative, expected) in pins.items():
        path = root / relative
        if not path.is_file():
            raise CompositorReviewError(f"Pinned source is missing: {relative.as_posix()}")
        actual = sha256_file(path)
        if actual != expected:
            raise CompositorReviewError(f"Source pin mismatch {relative.as_posix()}: {actual}")
        observed[name] = actual
    # Reuse the accepted E4A.2 authority resolver as an independent cross-check.
    prior = import_previous_runner(root)
    prior.validate_authorities(root)
    return observed


def validate_previous_evidence(base_run: Path, root: Path) -> dict[str, Any]:
    allowed_parent = (root / "artifacts/tests/c11e/e4a_real_body_pixel_review").resolve()
    source_run = base_run.resolve()
    if source_run.parent != allowed_parent or not source_run.name.startswith("RUN_") or not source_run.is_dir():
        raise CompositorReviewError("--base-run must name an existing E4A.2 RUN_* directly under artifacts/tests/c11e/e4a_real_body_pixel_review")
    receipt_path = source_run / "C11E_E4A_REAL_BODY_PIXEL_RUNNER_RECEIPT.json"
    report_path = source_run / "C11E_E4A_REAL_BODY_PIXEL_REPORT.json"
    if not receipt_path.is_file() or not report_path.is_file():
        raise CompositorReviewError("Prior E4A.2 run is missing its immutable receipt or report")
    receipt = load_json(receipt_path)
    report = load_json(report_path)
    if receipt.get("schema") != PREVIOUS_RECEIPT_SCHEMA or receipt.get("status") != "PASS_ISOLATED_REAL_C11C_BODY_PIXEL_PROOF_TEST_ONLY":
        raise CompositorReviewError("Prior E4A.2 receipt schema/status is not accepted")
    if report.get("schema") != PREVIOUS_REPORT_SCHEMA or report.get("status") != "PASS_ISOLATED_REAL_C11C_BODY_PIXEL_PROOF_TEST_ONLY":
        raise CompositorReviewError("Prior E4A.2 report schema/status is not accepted")
    if sha256_file(report_path) != PREVIOUS_REPORT_SHA256 or receipt.get("report_sha256") != PREVIOUS_REPORT_SHA256:
        raise CompositorReviewError("Prior E4A.2 report SHA-256 does not match the operator-accepted evidence")
    if receipt.get("base_video_sha256") != BASE_MP4_SHA256 or receipt.get("normalized_review_video_sha256") != NORMALIZED_MP4_SHA256:
        raise CompositorReviewError("Prior E4A.2 receipt has unexpected C11-C/normalized MP4 identities")
    if receipt.get("pixel_png_count") != 18 or receipt.get("pixel_comparison_count") != 12 or receipt.get("body_crop_hash_count") != 18:
        raise CompositorReviewError("Prior E4A.2 receipt is incomplete")
    if report.get("invariants", {}).get("body_pixels_A_B_identical_at_all_six_samples") is not True:
        raise CompositorReviewError("Prior real gameplay BODY identity evidence is absent")
    if report.get("test_only_visual_layout_disposition", {}).get("visual_placement_approved") is not False:
        raise CompositorReviewError("Prior visual placement must remain explicitly unapproved")
    base_mp4 = source_run / "c11c_base_render/CHALLENGE_004/CHALLENGE_004_seed_314159.mp4"
    normalized_mp4 = source_run / "review_delivery/CHALLENGE_004_REVIEW_720_30FPS_TEST_ONLY.mp4"
    manifest = source_run / "c11c_base_render/CHALLENGE_004/production_manifest.json"
    for path, expected, label in (
        (base_mp4, BASE_MP4_SHA256, "C11-C source MP4"),
        (normalized_mp4, NORMALIZED_MP4_SHA256, "normalized REVIEW_720 MP4"),
    ):
        if not path.is_file() or sha256_file(path) != expected:
            raise CompositorReviewError(f"Prior {label} is missing or hash-mismatched")
    if not manifest.is_file():
        raise CompositorReviewError("Prior C11-C production manifest is missing")
    c_manifest = load_json(manifest)
    if c_manifest.get("challenge_id") != "CHALLENGE_004" or c_manifest.get("seed") != 314159 or c_manifest.get("audio_present") is not False:
        raise CompositorReviewError("Prior C11-C production manifest does not identify the silent CHALLENGE_004 test render")
    if c_manifest.get("delivery_profile") not in ("REVIEW_720", "review_720"):
        raise CompositorReviewError("Prior C11-C manifest delivery profile is not REVIEW_720")
    # Ensure the preserved A/B/C intents are from the prior approved E1 service run.
    intents = {}
    for variant in ("A", "B", "C"):
        path = source_run / f"e1_intent_{variant}.json"
        if not path.is_file():
            raise CompositorReviewError(f"Prior run is missing e1_intent_{variant}.json")
        intents[variant] = load_json(path)
        if intents[variant].get("schema") != "C11-E-PRODUCTION-INTENT-V1" or intents[variant].get("status") != "PREPARED_E1_NOT_DISPATCHED":
            raise CompositorReviewError(f"E1 {variant} intent is not PREPARED_E1_NOT_DISPATCHED")
        boundary = intents[variant].get("execution_boundary", {})
        if boundary.get("renderer_dispatch_invoked") is not False or boundary.get("renderer_input_emitted") is not False or boundary.get("media_created") is not False:
            raise CompositorReviewError(f"E1 {variant} intent crossed the dispatch boundary")
        request = intents[variant].get("request", {})
        selection = request.get("selection", {})
        if selection.get("variant_id") != "CHALLENGE_004" or intents[variant].get("delivery", {}).get("audio_enabled") is not False:
            raise CompositorReviewError(f"E1 {variant} intent does not target the approved silent Challenge fixture")
    a, b, c = (intents[k]["editorial"] for k in ("A", "B", "C"))
    for field in ("title", "subtitle", "call_to_action"):
        if b.get(field) != c.get(field) or a.get(field) != "UNKNOWN":
            raise CompositorReviewError(f"E1 A/B/C visual field control mismatch: {field}")
    if b.get("language") != "es" or c.get("language") != "en" or b.get("player_name") == "UNKNOWN" or b.get("challenge_label") == "UNKNOWN":
        raise CompositorReviewError("E1 B/C language or blocked Challenge field negative-control mismatch")
    return {"run": source_run, "receipt": receipt, "report": report, "base_mp4": base_mp4,
            "normalized_mp4": normalized_mp4, "manifest": manifest, "c_manifest": c_manifest, "intents": intents}


def run_command(command: list[str], cwd: Path, stdout_path: Path, stderr_path: Path,
                timeout_seconds: int = 60, progress_label: str = "COMMAND") -> int:
    """Run with durable live logs, heartbeat, and a hard timeout (never block forever)."""
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    next_heartbeat = 5.0
    timed_out = False
    return_code: int | None = None
    with stdout_path.open("wb") as stdout_handle, stderr_path.open("wb") as stderr_handle:
        proc = subprocess.Popen(command, cwd=str(cwd), stdout=stdout_handle, stderr=stderr_handle)
        while True:
            return_code = proc.poll()
            if return_code is not None:
                break
            elapsed = time.monotonic() - started
            if elapsed >= timeout_seconds:
                timed_out = True
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
                break
            if elapsed >= next_heartbeat:
                print(f"{progress_label}_RUNNING elapsed_seconds={int(elapsed)} timeout_seconds={timeout_seconds}", flush=True)
                next_heartbeat += 5.0
            time.sleep(0.25)
        stdout_handle.flush()
        stderr_handle.flush()
    if timed_out:
        raise CompositorReviewError(
            f"{progress_label}_TIMEOUT after {timeout_seconds}s; logs preserved: "
            f"stdout={stdout_path} stderr={stderr_path}"
        )
    return int(return_code if return_code is not None else 1)


def resolve_executable(explicit: str | None, env_name: str, candidates: tuple[str, ...]) -> str:
    if explicit:
        path = Path(explicit)
        if path.is_file():
            return str(path)
        found = shutil.which(explicit)
        if found:
            return found
        raise CompositorReviewError(f"Executable not found: {explicit}")
    env_value = os.environ.get(env_name)
    if env_value and Path(env_value).is_file():
        return env_value
    for candidate in candidates:
        found = shutil.which(candidate)
        if found:
            return found
    raise CompositorReviewError(f"Cannot resolve {env_name}; set it or add the executable to PATH")


def parse_rate(value: str) -> float:
    if "/" not in value:
        return float(value)
    a, b = value.split("/", 1)
    return float(a) / float(b) if float(b) else 0.0


def extract_base_frame(ffmpeg: str, video: Path, delivery_frame: int, output: Path,
                       evidence_dir: Path, label: str, root: Path) -> dict[str, Any]:
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(video),
               "-vf", f"select=eq(n\\,{delivery_frame})", "-frames:v", "1",
               "-fps_mode", "passthrough", "-y", str(output)]
    log_base = evidence_dir / "commands" / f"extract_{label}"
    exit_code = run_command(command, root, log_base.with_suffix(".stdout.txt"), log_base.with_suffix(".stderr.txt"))
    if exit_code != 0 or not output.is_file():
        tail = log_base.with_suffix(".stderr.txt").read_text(encoding="utf-8", errors="replace")[-3000:]
        raise CompositorReviewError(f"FFmpeg failed extracting {label} (exit={exit_code}): {tail}")
    previous = import_previous_runner(root)
    decoded = previous.decode_png(output)
    if (decoded.width, decoded.height) != (WIDTH, HEIGHT):
        raise CompositorReviewError(f"Extracted base frame is not 720x1280: {label}")
    return {"command": command, "exit_code": exit_code, "path": str(output), "sha256": sha256_file(output),
            "width": decoded.width, "height": decoded.height}


def source_frame_for_delivery(delivery_frame: int) -> int:
    if delivery_frame < 0:
        raise CompositorReviewError("Delivery frame index cannot be negative")
    return int(round(float(delivery_frame) * SOURCE_FPS / DELIVERY_FPS))


def build_godot_command(godot: str, root: Path, config_path: Path) -> list[str]:
    # This test reads SubViewport textures. Godot --headless disables rendering
    # and RenderingServer signals, so it must run with the real renderer enabled.
    return [godot, "--path", str(root), "--script", "res://" + MATERIALIZER.as_posix(),
            "--", "--e4a-config", str(config_path)]


def build_config(output_dir: Path, base_frames: list[dict[str, Any]], intents: Mapping[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": CONFIG_SCHEMA,
        "mode": "D_OWNED_GODOT_SUBVIEWPORT_ALPHA_COMPOSITE_OVER_REAL_C11C_REVIEW_FRAME_TEST_ONLY",
        "output_dir": output_dir.as_posix(),
        "base_frames": base_frames,
        "variants": [{"id": key, "intent": intents[key]} for key in ("A", "B", "C")],
        "authorization": {
            "isolated_e4a_test_rendering": True,
            "production_renderer": False,
            "production_dispatch": False,
            "production_media": False,
        },
    }


def run(root: Path, base_run_arg: str, ffmpeg_arg: str | None, ffprobe_arg: str | None,
        godot_arg: str | None) -> int:
    authorities = validate_source_pins(root)
    base = validate_previous_evidence(Path(base_run_arg), root)
    ffmpeg = resolve_executable(ffmpeg_arg, "C11E_FFMPEG_EXECUTABLE", ("ffmpeg.exe", "ffmpeg"))
    ffprobe = resolve_executable(ffprobe_arg, "C11E_FFPROBE_EXECUTABLE", ("ffprobe.exe", "ffprobe"))
    if godot_arg:
        godot = resolve_executable(godot_arg, "C11D_GODOT_EXECUTABLE", ())
    else:
        env_godot = os.environ.get("C11D_GODOT_EXECUTABLE")
        fallback = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local"))) / "Microsoft/WinGet/Packages/GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe/Godot_v4.7.1-stable_mono_win64/godot.exe"
        if env_godot and Path(env_godot).is_file():
            godot = env_godot
        elif fallback.is_file():
            godot = str(fallback)
        else:
            found = shutil.which("godot.exe") or shutil.which("godot")
            if not found:
                raise CompositorReviewError("Godot 4.7.1 executable not found; set C11D_GODOT_EXECUTABLE")
            godot = found

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    evidence_dir = root / "artifacts/tests/c11e/e4a_d_compositor_pixel_review" / f"RUN_{stamp}"
    evidence_dir.mkdir(parents=True, exist_ok=False)
    print(f"EVIDENCE_DIR={evidence_dir}", flush=True)
    print("E4A3_STAGE=VALIDATING_ACCEPTED_E4A2_INPUT", flush=True)
    # Reconfirm the normalized MP4 contract; keep all new logs in this RUN and
    # never write into the accepted E4A.2 evidence directory.
    prior = import_previous_runner(root)
    normalized_video_sha_before = sha256_file(base["normalized_mp4"])
    source_video_sha_before = sha256_file(base["base_mp4"])
    if normalized_video_sha_before != NORMALIZED_MP4_SHA256 or source_video_sha_before != BASE_MP4_SHA256:
        raise CompositorReviewError("Accepted E4A.2 source video identity changed before E4A.3")
    normalized_video = prior.probe_video(ffprobe, base["normalized_mp4"], evidence_dir, root)
    if normalized_video.get("pix_fmt") != "yuv420p" or normalized_video.get("color_range") != "tv":
        raise CompositorReviewError("Normalized REVIEW_720 input is not yuv420p/tv")

    base_frames_dir = evidence_dir / "base_frames"
    base_frames_dir.mkdir()
    image_dir = evidence_dir / "godot_composited_png"
    image_dir.mkdir()

    # Derive time windows from the pinned canonical Challenge definition; do not hand-author phase intervals.
    challenge = load_json(root / CHALLENGE_SOURCE)
    timeline, source_fps, duration = prior.source_timeline(challenge)
    if source_fps != SOURCE_FPS or abs(duration - 15.0) > 1e-9:
        raise CompositorReviewError(f"Pinned CHALLENGE_004 timeline drift: source_fps={source_fps}, duration={duration}")
    source_samples = prior.sample_frames(timeline, DELIVERY_FPS)
    expected_samples = [{"label": s["sample"], "phase": s["phase"], "delivery_frame": s["delivery_frame"]} for s in source_samples]
    if expected_samples != EXPECTED_SAMPLES:
        raise CompositorReviewError(f"Canonical source/delivery sample map changed: {expected_samples}")

    base_frame_records: list[dict[str, Any]] = []
    extraction_commands = []
    for sample in source_samples:
        label = str(sample["sample"])
        delivery_frame = int(sample["delivery_frame"])
        source_frame = source_frame_for_delivery(delivery_frame)
        phase = str(sample["phase"])
        output = base_frames_dir / f"{label}.png"
        print(f"E4A3_STAGE=EXTRACT_BASE_FRAME sample={label} delivery_frame={delivery_frame}", flush=True)
        record = extract_base_frame(ffmpeg, base["normalized_mp4"], delivery_frame, output, evidence_dir, label, root)
        base_frame_records.append({"label": label, "phase": phase, "delivery_frame": delivery_frame,
                                   "source_frame": source_frame, "path": str(output.resolve()),
                                   "sha256": record["sha256"], "width": WIDTH, "height": HEIGHT})
        extraction_commands.append(record)

    intents = base["intents"]
    for variant in ("A", "B", "C"):
        write_json(evidence_dir / f"e1_intent_{variant}.json", intents[variant])
    config_path = evidence_dir / "e4a_d_compositor_pixel_test_config.json"
    config = build_config(evidence_dir, base_frame_records, intents)
    write_json(config_path, config)

    godot_version_command = [godot, "--version"]
    version_exit = run_command(godot_version_command, root, evidence_dir / "godot_version.stdout.txt", evidence_dir / "godot_version.stderr.txt", timeout_seconds=15, progress_label="GODOT_VERSION")
    if version_exit != 0:
        raise CompositorReviewError(f"Godot --version failed: {version_exit}")
    godot_version = (evidence_dir / "godot_version.stdout.txt").read_text(encoding="utf-8", errors="replace").strip()
    if "4.7.1" not in godot_version:
        raise CompositorReviewError(f"Expected Godot 4.7.1, got {godot_version!r}")

    materializer_sha_before = sha256_file(root / MATERIALIZER)
    manifest_sha_before = sha256_file(root / MANIFEST_SOURCE)
    c11c_script_sha_before = sha256_file(root / C11C_RENDERER)
    producer_sha_before = sha256_file(root / MAIN_SOURCE)
    command = build_godot_command(godot, root, config_path)
    print("E4A3_STAGE=GODOT_COMPOSITOR_START renderer=ENABLED headless=false timeout_seconds=90", flush=True)
    godot_exit = run_command(command, root, evidence_dir / "godot_compositor.stdout.txt", evidence_dir / "godot_compositor.stderr.txt", timeout_seconds=90, progress_label="GODOT_COMPOSITOR")
    print(f"E4A3_STAGE=GODOT_COMPOSITOR_EXIT exit_code={godot_exit}", flush=True)
    stdout = (evidence_dir / "godot_compositor.stdout.txt").read_text(encoding="utf-8", errors="replace")
    stderr = (evidence_dir / "godot_compositor.stderr.txt").read_text(encoding="utf-8", errors="replace")
    materializer_sha_after = sha256_file(root / MATERIALIZER)
    manifest_sha_after = sha256_file(root / MANIFEST_SOURCE)
    c11c_script_sha_after = sha256_file(root / C11C_RENDERER)
    producer_sha_after = sha256_file(root / MAIN_SOURCE)
    if materializer_sha_before != materializer_sha_after or manifest_sha_before != manifest_sha_after:
        raise CompositorReviewError("Source materializer or frozen C11-C manifest changed during test execution")
    if c11c_script_sha_before != c11c_script_sha_after or producer_sha_before != producer_sha_after:
        raise CompositorReviewError("Read-only C11-C source changed during D compositor test")
    if sha256_file(base["base_mp4"]) != source_video_sha_before or sha256_file(base["normalized_mp4"]) != normalized_video_sha_before:
        raise CompositorReviewError("Accepted E4A.2 source media changed during D compositor test")
    for frame_record in base_frame_records:
        if sha256_file(Path(frame_record["path"])) != frame_record["sha256"]:
            raise CompositorReviewError(f"Extracted immutable base frame changed during Godot composition: {frame_record['label']}")
    if godot_exit != 0:
        raise CompositorReviewError(f"Godot D materializer exited {godot_exit}: {stderr[-4000:]} {stdout[-1000:]}")
    if "C11E E4A D-OWNED GODOT REAL-BODY COMPOSITOR PASS" not in stdout:
        raise CompositorReviewError("Godot exited 0 without the D-owned real-body compositor PASS marker")

    report_path = evidence_dir / "C11E_E4A_D_COMPOSITOR_PIXEL_REPORT.json"
    if not report_path.is_file():
        raise CompositorReviewError("Godot PASS marker exists but compositor report is missing")
    report = load_json(report_path)
    if report.get("schema") != REPORT_SCHEMA or report.get("status") != "PASS_ISOLATED_D_OWNED_GODOT_LAYER_REAL_BODY_PIXEL_PROOF_TEST_ONLY":
        raise CompositorReviewError("Godot compositor report schema/status mismatch")
    if report.get("base_payload_sha256") == "" or report.get("game_frame_record_count") != 420:
        raise CompositorReviewError("D materializer payload/frame lineage is incomplete")
    if report.get("execution_boundary", {}).get("production_dispatch_invoked") is not False or report.get("execution_boundary", {}).get("production_media_created") is not False:
        raise CompositorReviewError("Test compositor crossed the production execution boundary")
    if report.get("test_only_visual_layout_disposition", {}).get("visual_placement_approved") is not False:
        raise CompositorReviewError("Test-only placeholder visual placement was incorrectly approved")

    artifact_rows = report.get("pixel_artifacts", [])
    if len(artifact_rows) != 18 or report.get("pixel_comparisons") is None or len(report["pixel_comparisons"]) != 12:
        raise CompositorReviewError("Godot report must contain 18 real-body PNGs and 12 comparisons")
    artifacts: list[dict[str, Any]] = []
    artifact_map: dict[tuple[str, str], Path] = {}
    previous = import_previous_runner(root)
    for row in artifact_rows:
        variant, sample = str(row.get("variant", "")), str(row.get("sample", ""))
        path = root / str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        if variant not in ("A", "B", "C") or sample not in {x["label"] for x in EXPECTED_SAMPLES} or (variant, sample) in artifact_map:
            raise CompositorReviewError("Godot report has an invalid/duplicate artifact identity")
        if not path.is_file() or sha256_file(path) != expected:
            raise CompositorReviewError(f"Godot output PNG missing/hash mismatch: {variant}/{sample}")
        decoded = previous.decode_png(path)
        if (decoded.width, decoded.height) != (WIDTH, HEIGHT):
            raise CompositorReviewError(f"Godot output PNG dimensions are not 720x1280: {path.name}")
        artifact_map[(variant, sample)] = path
        artifacts.append({"variant": variant, "sample": sample, "phase": row.get("phase"),
                          "delivery_frame": row.get("delivery_frame"), "source_frame": row.get("source_frame"),
                          "width": decoded.width, "height": decoded.height, "sha256": expected,
                          "path": path.relative_to(root).as_posix(), "base_frame_sha256": row.get("base_frame_sha256")})
    if set(artifact_map) != {(v, s["label"]) for v in ("A", "B", "C") for s in EXPECTED_SAMPLES}:
        raise CompositorReviewError("Godot output PNG matrix is incomplete")

    comparisons: list[dict[str, Any]] = []
    body_hashes: list[dict[str, str]] = []
    for sample in EXPECTED_SAMPLES:
        name, phase = sample["label"], sample["phase"]
        source_background = next(x for x in base_frame_records if x["label"] == name)
        base_png = previous.decode_png(Path(source_background["path"]))
        a = previous.decode_png(artifact_map[("A", name)])
        b = previous.decode_png(artifact_map[("B", name)])
        c = previous.decode_png(artifact_map[("C", name)])
        # A must be the exact unmodified base frame, ignoring the added opaque alpha channel.
        if not rgb_pixels_equal(base_png, a):
            raise CompositorReviewError(f"A control did not preserve the extracted C11-C frame exactly: {name}")
        allowed = REGIONS["HEADER"] if phase == "HOOK" else REGIONS["FOOTER"] if phase == "CTA" else None
        ab = previous.pixel_compare(a, b, allowed)
        bc = previous.pixel_compare(b, c, None)
        positive = phase in ("HOOK", "CTA")
        ab_ok = (ab["changed_pixels"] > 0 and ab["changed_outside_allowed_region"] == 0 and ab["changed_body_pixels"] == 0) if positive else ab["changed_pixels"] == 0
        bc_ok = bc["changed_pixels"] == 0
        comparisons.extend([
            {"comparison": f"A_TO_B_{name.upper()}", "allowed_region": phase if positive else "NONE", **ab, "success": ab_ok},
            {"comparison": f"B_TO_C_{name.upper()}_METADATA_AND_BLOCKED_FIELDS_NO_PIXELS", "allowed_region": "NONE", **bc, "success": bc_ok},
        ])
        if not ab_ok or not bc_ok:
            raise CompositorReviewError(f"Godot D compositor pixel invariant failed at {name}: A/B={ab}; B/C={bc}")
        for variant, png in (("A", a), ("B", b), ("C", c)):
            body = crop_hash(png, REGIONS["BODY"])
            body_hashes.append({"variant": variant, "sample": name, "body_crop_sha256": body})
    # All three variants must have identical BODY hashes at every sampled timepoint.
    for sample in EXPECTED_SAMPLES:
        values = {x["body_crop_sha256"] for x in body_hashes if x["sample"] == sample["label"]}
        if len(values) != 1:
            raise CompositorReviewError(f"Real gameplay BODY crop hash diverged across A/B/C: {sample['label']}")

    report["python_independent_validation"] = {
        "a_control_matches_extracted_base_exactly_rgb": True,
        "real_gameplay_body_crop_identity_all_variants": True,
        "python_comparisons": comparisons,
        "body_crop_hashes": body_hashes,
        "previous_e4a2_report_sha256": PREVIOUS_REPORT_SHA256,
        "previous_e4a2_normalized_mp4_sha256": NORMALIZED_MP4_SHA256,
    }
    # Update and re-hash the final report after independent Python validation is attached.
    write_json(report_path, report)
    report_sha = sha256_file(report_path)
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "status": report["status"],
        "scope": report["scope"],
        "godot_executable": godot,
        "godot_version": godot_version,
        "godot_exit_code": godot_exit,
        "godot_command": command,
        "godot_stdout_sha256": sha256_file(evidence_dir / "godot_compositor.stdout.txt"),
        "godot_stderr_sha256": sha256_file(evidence_dir / "godot_compositor.stderr.txt"),
        "ffmpeg_executable": ffmpeg,
        "ffprobe_executable": ffprobe,
        "normalized_review_mp4_sha256_before_after": normalized_video_sha_before,
        "original_c11c_base_mp4_sha256_before_after": source_video_sha_before,
        "base_frame_inputs_sha256_before_after": {row["label"]: row["sha256"] for row in base_frame_records},
        "base_run_receipt_sha256": sha256_file(base["run"] / "C11E_E4A_REAL_BODY_PIXEL_RUNNER_RECEIPT.json"),
        "base_run_report_sha256": PREVIOUS_REPORT_SHA256,
        "base_frames": base_frame_records,
        "pixel_png_count": len(artifacts),
        "pixel_comparison_count": len(comparisons),
        "body_crop_hash_count": len(body_hashes),
        "report_sha256": report_sha,
        "source_pins": authorities,
        "materializer_sha256_before_after": materializer_sha_before,
        "c11c_renderer_sha256_before_after": c11c_script_sha_before,
        "producer_main_sha256_before_after": producer_sha_before,
        "frozen_c11c_manifest_sha256_before_after": manifest_sha_before,
        "governance": {
            "production_renderer": False, "production_dispatch": False, "production_media_created": False,
            "test_media_created": False, "test_png_artifacts_created": True,
            "d4_8": "BLOCKED", "d9_10": "PREPARE_ONLY", "d9_14": "BLOCKED", "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO", "d10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE"
        },
    }
    receipt_path = evidence_dir / "C11E_E4A_D_COMPOSITOR_PIXEL_RECEIPT.json"
    write_json(receipt_path, receipt)
    sums = []
    for path in sorted(evidence_dir.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            sums.append(f"{sha256_file(path)}  {path.relative_to(root).as_posix()}")
    (evidence_dir / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")

    print("C11E_E4A_D_COMPOSITOR_REAL_BODY_PIXEL_REVIEW=PASS_ISOLATED_TEST_ONLY")
    print("MATERIALIZER=EXISTING_D_OWNED_GODOT_SUBVIEWPORT_LAYER")
    print("BASE=REUSED_E4A2_REVIEW_720_H264_720x1280_30FPS_450_FRAMES_NO_C11C_RERUN")
    print("REAL_C11C_FRAMES_EXTRACTED=6/6; GODOT_COMPOSITED_PNG=18/18; PIXEL_COMPARISONS=12/12")
    print("BODY_PIXEL_IDENTITY=PASS_AT_6_REAL_DELIVERY_SAMPLES")
    print("D_FIELDS=title/subtitle=HEADER/HOOK; call_to_action=FOOTER/CTA; REGION_ONLY")
    print("VISUAL_PLACEMENT=UNAPPROVED_D1_5_SAFE_AREA_TYPOGRAPHY_UNKNOWN")
    print("CHALLENGE_OVERLAY=BLOCKED_GEOMETRY_UNRESOLVED; LANGUAGE=METADATA_ONLY")
    print("PRODUCTION_RENDERER=false; PRODUCTION_DISPATCH=false; D4.8=BLOCKED; D9.10=PREPARE_ONLY; RELEASE_AUTHORITY=NONE")
    print(f"EVIDENCE_DIR={evidence_dir}")
    print(f"RECEIPT_SHA256={sha256_file(receipt_path)}")
    return 0


def rgb_pixels_equal(a: Any, b: Any) -> bool:
    if (a.width, a.height) != (b.width, b.height):
        return False
    for idx in range(a.width * a.height):
        ai, bi = idx * a.channels, idx * b.channels
        if a.pixels[ai:ai + 3] != b.pixels[bi:bi + 3]:
            return False
    return True


def crop_hash(image: Any, rect: tuple[int, int, int, int]) -> str:
    x0, y0, x1, y1 = rect
    rows = []
    stride = image.width * image.channels
    for y in range(y0, y1):
        rows.append(image.pixels[y * stride + x0 * image.channels:y * stride + x1 * image.channels])
    return sha256_bytes(b"".join(rows))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-run", required=True, help="Existing accepted E4A.2 RUN_* path under artifacts/tests/c11e/e4a_real_body_pixel_review")
    parser.add_argument("--ffmpeg", help="FFmpeg executable; otherwise C11E_FFMPEG_EXECUTABLE/PATH")
    parser.add_argument("--ffprobe", help="FFprobe executable; otherwise C11E_FFPROBE_EXECUTABLE/PATH")
    parser.add_argument("--godot", help="Godot 4.7.1 executable; otherwise C11D_GODOT_EXECUTABLE/WinGet/PATH")
    args = parser.parse_args()
    try:
        return run(ROOT, args.base_run, args.ffmpeg, args.ffprobe, args.godot)
    except Exception as exc:
        print(f"C11E_E4A_D_COMPOSITOR_REAL_BODY_PIXEL_REVIEW=FAIL {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
