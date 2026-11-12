#!/usr/bin/env python3
"""Recompose one accepted E4C Drill A/V evidence set with the V2 social-body consumer.

This tool does NOT invoke Godot, C11-C, a native capture, or FAMILY_MUSIC_V4.
It reuses the already-created native MP4 and A/B/C WAV files, produces isolated
V2 composition outputs, and writes a technical receipt pending human review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PureWindowsPath
from typing import Any

EXPECTED_REQUEST_ID = "E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8"
EXPECTED_RECEIPT_SHA256 = "57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903"
EXPECTED_NATIVE_SHA256 = "d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338"
EXPECTED_WAV_SHA256 = {
    "A": "e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277",
    "B": "e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277",
    "C": "5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40",
}
EXPECTED_E1_INTENT_SHA256 = "9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e"
FROZEN_C11C_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
PRESENTATION_PROFILE_SHA256 = "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24"
WIDTH, HEIGHT, FPS, CHANNELS = 720, 1280, 30, 3
FRAME_BYTES = WIDTH * HEIGHT * CHANNELS
PRE_ROLL_FRAMES, GAME_FRAMES, END_CTA_FRAMES = 90, 630, 90
TOTAL_FRAMES = PRE_ROLL_FRAMES + GAME_FRAMES + END_CTA_FRAMES


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def normalized_pins(rows: Any) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError("source pin list is malformed")
    normalized = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("source pin row is malformed")
        normalized.append({"path": str(row["path"]), "bytes": int(row["bytes"]), "sha256": str(row["sha256"])})
    return sorted(normalized, key=lambda row: row["path"])


def resolve_media(evidence_root: Path, absolute_recorded_path: str, subdir: str) -> Path:
    # The original receipt records Windows absolute paths; resolve by basename
    # under the preserved evidence root to avoid trusting stale drive prefixes.
    basename = PureWindowsPath(absolute_recorded_path).name or Path(absolute_recorded_path).name
    path = evidence_root / subdir / basename
    if not path.is_file():
        raise FileNotFoundError(f"preserved evidence media missing: {path}")
    return path


def read_exact(stream: Any, count: int) -> bytes:
    data = bytearray()
    while len(data) < count:
        part = stream.read(count - len(data))
        if not part:
            break
        data.extend(part)
    if len(data) != count:
        raise RuntimeError(f"FFmpeg raw frame short read: expected={count}; actual={len(data)}")
    return bytes(data)


def compose_all_frames_v2(
    source_mp4: Path,
    target_mp4: Path,
    plan: dict[str, Any],
    project_root: Path,
    ffmpeg: Path,
    evidence_dir: Path,
    consumer: Any,
    executor: Any,
) -> dict[str, Any]:
    """Run the unchanged E4C FFmpeg frame pipeline with stronger V2 pixel oracles."""
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    consumer._ensure_qt_app()
    consumer.validate_plan(plan)
    decode_log = evidence_dir / "v2_ffmpeg_decode_stderr.log"
    encode_log = evidence_dir / "v2_ffmpeg_encode_stderr.log"
    decode_command = [
        str(ffmpeg), "-hide_banner", "-loglevel", "error", "-i", str(source_mp4),
        "-map", "0:v:0", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1",
    ]
    encode_command = [
        str(ffmpeg), "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}",
        "-framerate", str(FPS), "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", "fast",
        "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-color_range", "tv",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-r", str(FPS), "-g", "90", "-keyint_min", "90", "-sc_threshold", "0",
        "-x264-params", "open_gop=0:keyint=90:min-keyint=90:scenecut=0", "-movflags", "+faststart", str(target_mp4),
    ]
    counts = {"PRE_ROLL": 0, "GAME": 0, "END_CTA": 0}
    sample_rows: list[dict[str, Any]] = []
    game_identity_checked = 0
    passthrough_identity_checked = 0
    with decode_log.open("w", encoding="utf-8") as dec_log, encode_log.open("w", encoding="utf-8") as enc_log:
        decoder = subprocess.Popen(decode_command, stdout=subprocess.PIPE, stderr=dec_log, cwd=str(project_root))
        encoder = subprocess.Popen(encode_command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=enc_log, cwd=str(project_root))
        try:
            if decoder.stdout is None or encoder.stdin is None:
                raise RuntimeError("FFmpeg raw-frame pipes could not be opened")
            for frame_index in range(TOTAL_FRAMES):
                raw = read_exact(decoder.stdout, FRAME_BYTES)
                phase, phase_index = executor.phase_for_final_frame(frame_index, GAME_FRAMES)
                source = consumer.QImage(raw, WIDTH, HEIGHT, WIDTH * CHANNELS, consumer.QImage.Format.Format_RGB888).copy()
                if source.isNull() or (source.width(), source.height()) != (WIDTH, HEIGHT):
                    raise RuntimeError(f"Qt source frame invalid at index {frame_index}")
                source_hash = consumer._image_rgb_sha256(source)
                result = consumer.compose_frame(source, plan, phase, phase_index, GAME_FRAMES, FPS, 1, project_root)
                composed = result.get("image")
                if composed is None or composed.isNull() or (composed.width(), composed.height()) != (WIDTH, HEIGHT):
                    raise RuntimeError(f"V2 consumer returned invalid frame at {frame_index}")
                if result.get("source_unchanged") is not True or consumer._image_rgb_sha256(source) != source_hash:
                    raise RuntimeError(f"V2 consumer mutated input at frame {frame_index}")
                mapping = result.get("mapping", {})
                if mapping.get("phase") != phase or mapping.get("d_editorial_visible") is not (phase == "GAME"):
                    raise RuntimeError(f"V2 phase/editorial visibility mismatch at frame {frame_index}")
                if phase == "GAME":
                    source_body = source.copy(0, 192, 720, 896)
                    output_body = composed.copy(0, 192, 720, 896)
                    if consumer._image_rgb_bytes(source_body) != consumer._image_rgb_bytes(output_body):
                        raise RuntimeError(f"V2 GAME native body is not pixel-identical at frame {frame_index}")
                    if result.get("native_body_pixel_identity") is not True:
                        raise RuntimeError(f"V2 consumer did not attest body pixel identity at frame {frame_index}")
                    game_identity_checked += 1
                else:
                    if consumer._image_rgb_bytes(composed) != consumer._image_rgb_bytes(source):
                        raise RuntimeError(f"V2 {phase} did not pass through complete native frame at frame {frame_index}")
                    if result.get("native_full_frame_identity") is not True:
                        raise RuntimeError(f"V2 {phase} passthrough attestation missing at frame {frame_index}")
                    passthrough_identity_checked += 1
                expected_final = frame_index if phase != "GAME" else PRE_ROLL_FRAMES + phase_index
                if mapping.get("final_presentation_frame_index") != expected_final:
                    raise RuntimeError(f"V2 timebase mapping changed at frame {frame_index}")
                encoder.stdin.write(consumer._image_rgb_bytes(composed))
                counts[phase] += 1
                if frame_index in (0, 89, 90, 405, 719, 720, 809):
                    sample_rows.append({
                        "frame_index": frame_index, "phase": phase, "phase_index": phase_index,
                        "mode": result.get("mode"), "source_rgb_sha256": source_hash,
                        "output_rgb_sha256": consumer._image_rgb_sha256(composed),
                        "native_body_pixel_identity": result.get("native_body_pixel_identity", False),
                        "native_full_frame_identity": result.get("native_full_frame_identity", False),
                    })
            if decoder.stdout.read(1):
                raise RuntimeError("native source contains extra frames beyond the preserved 810-frame timebase")
            encoder.stdin.close()
            decoder.stdout.close()
            dec_exit = decoder.wait(timeout=180)
            enc_exit = encoder.wait(timeout=360)
            if dec_exit != 0:
                raise RuntimeError(f"FFmpeg source decode failed with exit {dec_exit}; inspect {decode_log}")
            if enc_exit != 0:
                raise RuntimeError(f"FFmpeg V2 encode failed with exit {enc_exit}; inspect {encode_log}")
        except Exception:
            for process in (decoder, encoder):
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=30)
            raise
    if counts != {"PRE_ROLL": 90, "GAME": 630, "END_CTA": 90}:
        raise RuntimeError(f"V2 phase-count mismatch: {counts}")
    if game_identity_checked != 630 or passthrough_identity_checked != 180:
        raise RuntimeError("V2 pixel identity sample cardinality mismatch")
    if not target_mp4.is_file() or target_mp4.stat().st_size <= 0:
        raise RuntimeError("V2 silent composed MP4 missing")
    return {
        "frames_expected": TOTAL_FRAMES, "frames_composed": sum(counts.values()),
        "phase_counts": counts, "game_native_body_pixel_identity_frames": game_identity_checked,
        "native_full_frame_passthrough_frames": passthrough_identity_checked,
        "sampled_frames": sample_rows, "silent_video_path": str(target_mp4),
        "silent_video_sha256": sha256_file(target_mp4), "silent_video_bytes": target_mp4.stat().st_size,
        "decode_log": str(decode_log), "encode_log": str(encode_log),
    }


def extract_review_frames(ffmpeg: Path, final_a: Path, review_dir: Path, executor: Any) -> list[dict[str, Any]]:
    samples = [
        (0, "PRE_ROLL_FIRST"), (89, "PRE_ROLL_LAST"), (90, "GAME_FIRST"),
        (405, "GAME_MID"), (719, "GAME_LAST"), (720, "END_CTA_FIRST"), (809, "END_CTA_LAST"),
    ]
    output = []
    for index, label in samples:
        target = review_dir / f"frame_{index:03d}_{label}.png"
        # Commas in select are escaped for FFmpeg's filter parser; process args
        # are passed directly, not through PowerShell/string-shell interpolation.
        expression = f"select=eq(n\\,{index})"
        command = [str(ffmpeg), "-y", "-hide_banner", "-loglevel", "error", "-i", str(final_a), "-vf", expression, "-vsync", "0", "-frames:v", "1", str(target)]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        if result.returncode != 0 or not target.is_file() or target.stat().st_size <= 0:
            raise RuntimeError(f"review frame extraction failed for {index}: {result.stderr[-2000:]}")
        output.append({"frame_index": index, "phase_label": label, "path": str(target), "sha256": sha256_file(target), "bytes": target.stat().st_size})
    return output


def run(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.project_root).resolve()
    evidence_root = Path(args.evidence_root).resolve()
    if not root.is_dir() or not evidence_root.is_dir():
        raise FileNotFoundError("ProjectRoot and preserved EvidenceRoot must already exist")
    if root == evidence_root or root not in evidence_root.parents:
        raise ValueError("EvidenceRoot must be an existing child of ProjectRoot")
    run_id = args.output_id
    if not re.fullmatch(r"E4C-CLI-COMPOSITION-V2-[A-Za-z0-9-]{12,80}", run_id):
        raise ValueError("output_id must be a fresh E4C-CLI-COMPOSITION-V2-* identifier")
    output_root = root / "artifacts" / "production" / "c11e" / run_id
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite V2 requalification output: {output_root}")
    output_root.mkdir(parents=True, exist_ok=False)
    qual_dir = output_root / "qualification"
    review_dir = output_root / "operator_review"
    qual_dir.mkdir(); review_dir.mkdir()
    receipt_path = evidence_root / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"
    receipt = read_json(receipt_path)
    request = read_json(evidence_root / "request.json")
    intent = read_json(evidence_root / "e1_intent.json")
    if sha256_file(receipt_path) != EXPECTED_RECEIPT_SHA256:
        raise ValueError("preserved CLI qualification receipt SHA-256 mismatch")
    if receipt.get("status") != "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION" or receipt.get("request_id") != EXPECTED_REQUEST_ID or receipt.get("request_origin") != "CLI":
        raise ValueError("source CLI receipt identity/status/origin mismatch")
    if request.get("request_id") != EXPECTED_REQUEST_ID or request.get("selection", {}).get("content_type") != "visual_drills" or request.get("selection", {}).get("family_id") != "tracking" or request.get("selection", {}).get("variant_id") != "tier-1":
        raise ValueError("preserved request does not match visual_drills/tracking/tier-1")
    editorial = request.get("production_override", {})
    if any(not isinstance(editorial.get(key), str) or not editorial.get(key).strip() for key in ("title", "subtitle", "call_to_action")):
        raise ValueError("preserved CLI request does not contain the accepted non-empty D editorial values")
    if (request.get("seed"), request.get("music_seed"), request.get("delivery_profile_id")) != (12345, 840001, "REVIEW_720"):
        raise ValueError("preserved request seed/profile mismatch")
    if request.get("mode") != "PRODUCTION" or request.get("audio_enabled") is not True or request.get("personalization_enabled") is not True:
        raise ValueError("preserved request production/audio/personalization controls mismatch")
    if intent.get("intent_sha256") != EXPECTED_E1_INTENT_SHA256 or receipt.get("e1_validation", {}).get("intent_sha256") != EXPECTED_E1_INTENT_SHA256:
        raise ValueError("preserved E1 intent hash mismatch")
    if receipt.get("e1_validation", {}).get("source_pin_count") != 91 or receipt.get("e1_validation", {}).get("status") != "PASS_E1_PREPARATION_ONLY":
        raise ValueError("preserved E1 preparation receipt is not accepted")
    if receipt.get("family_adapter_preparation_status") != "NOT_CONNECTED_E1" or receipt.get("production_dispatch") is not False or receipt.get("release_authority") != "NONE":
        raise ValueError("preserved receipt violates E1/release boundary")
    native_timeline = receipt.get("native_timeline", {})
    expected_timeline = {"duration_seconds": 27.0, "fps": 30, "pre_roll_frames": 90, "gameplay_frames": 630, "end_cta_frames": 90, "total_frames": 810}
    for key, value in expected_timeline.items():
        if native_timeline.get(key) != value:
            raise ValueError(f"preserved native timebase mismatch: {key}={native_timeline.get(key)!r}; expected={value!r}")
    old_plan = read_json(evidence_root / "d_composition_plan.json")
    old_viewport = old_plan.get("geometry", {}).get("source_frame_viewport", {})
    if old_plan.get("schema") != "C11E-E4C-DRILL-VISUAL-COMPOSITION-PLAN-V1" or old_viewport != {"x": 108, "y": 192, "width": 504, "height": 896}:
        raise ValueError("preserved CLI source plan is not the expected V1 centered-contain composition")
    native_info = receipt.get("native_source", {})
    native_name = PureWindowsPath(str(native_info.get("mp4", ""))).name
    native_dir = evidence_root / "native_source" / "tracking"
    native_matches = [candidate for candidate in native_dir.rglob(native_name) if candidate.is_file()] if native_name else []
    if len(native_matches) != 1:
        raise ValueError(f"expected exactly one preserved native C11-C MP4 named {native_name}; found={len(native_matches)}")
    native_source = native_matches[0]
    if sha256_file(native_source) != EXPECTED_NATIVE_SHA256 or native_info.get("mp4_sha256") != EXPECTED_NATIVE_SHA256:
        raise ValueError("preserved native C11-C source MP4 does not match accepted evidence hash")
    fm = receipt.get("family_music", {})
    if fm.get("route") != "C11_C_FAMILY_MUSIC_V4" or fm.get("profile_id") != "FLOWING_VECTOR" or fm.get("same_seed_ab_identical") is not True or fm.get("changed_seed_c_distinct") is not True:
        raise ValueError("preserved family music receipt is not the accepted FAMILY_MUSIC_V4 A/B/C run")
    wavs = {}
    expected_seeds = {"A": 840001, "B": 840001, "C": 840002}
    for key, subkey in (("A", "A"), ("B", "B"), ("C", "C")):
        row = fm.get(key, {})
        if row.get("seed") != expected_seeds[key] or row.get("family") != "tracking" or row.get("sample_rate_hz") != 44100 or row.get("channels") != 2 or float(row.get("duration_seconds", 0)) != 27.0:
            raise ValueError(f"preserved family music {key} metadata mismatch")
        expected = EXPECTED_WAV_SHA256[key]
        wav = resolve_media(evidence_root, str(row.get("path", "")), "qualification")
        if row.get("sha256") != expected or sha256_file(wav) != expected:
            raise ValueError(f"preserved FAMILY_MUSIC_V4 {key} WAV hash mismatch")
        wavs[key] = wav
    if sha256_file(wavs["A"]) != sha256_file(wavs["B"]) or sha256_file(wavs["A"]) == sha256_file(wavs["C"]):
        raise ValueError("preserved music A/B/C seed isolation does not match the accepted receipt")
    old_pins = normalized_pins(receipt.get("source_pins_pre_execution"))
    if old_pins != normalized_pins(receipt.get("source_pins_immediately_pre_renderer")) or old_pins != normalized_pins(receipt.get("source_pins_post_execution")) or len(old_pins) != 91:
        raise ValueError("preserved 91-pin pre/pre-render/post inventories were not identical")

    # Import the unchanged installed D execution helpers; the V2 consumer is
    # loaded by compose_all_frames_v2 from this checkout's existing D tools path.
    tools_dir = root / "tools" / "c11d" / "d9"
    sys.path.insert(0, str(tools_dir))
    import c11e_e4c_drill_execution as executor  # type: ignore
    import c11e_e4c_drill_visual_composition_consumer as consumer  # type: ignore
    current_pins = normalized_pins(executor._source_pins(intent, root))
    if current_pins != old_pins:
        raise ValueError("current E1 source pins differ from the preserved accepted 91-pin inventory")
    profile_pin = next((row for row in current_pins if row["path"] == "core/presentation/PresentationProfile.gd"), None)
    if profile_pin is None or profile_pin["sha256"] != PRESENTATION_PROFILE_SHA256:
        raise ValueError("PresentationProfile.gd does not match the exact social geometry source pin")
    plan = consumer.build_composition_plan(intent, root)
    consumer.validate_plan(plan)
    write_json(output_root / "d_composition_plan_v2.json", plan)
    ffprobe = executor.discover_binary("ffprobe.exe", args.ffprobe)
    ffmpeg = executor.discover_binary("ffmpeg.exe", args.ffmpeg, sibling_of=ffprobe)
    ffmpeg_version = executor.verify_executable(ffmpeg, "FFmpeg", ["-version"]).splitlines()[0]
    ffprobe_version = executor.verify_executable(ffprobe, "FFprobe", ["-version"]).splitlines()[0]
    native_probe = executor.ffprobe_json(ffprobe, native_source)
    native_streams = native_probe.get("streams", [])
    native_videos = [row for row in native_streams if row.get("codec_type") == "video"]
    native_audios = [row for row in native_streams if row.get("codec_type") == "audio"]
    if len(native_videos) != 1 or native_audios or int(native_videos[0].get("nb_read_frames", -1)) != TOTAL_FRAMES:
        raise RuntimeError("reused native C11-C source must be one silent 810-frame video stream")
    if (int(native_videos[0].get("width", 0)), int(native_videos[0].get("height", 0)), str(native_videos[0].get("avg_frame_rate"))) != (WIDTH, HEIGHT, "30/1"):
        raise RuntimeError("reused native source dimensions/FPS differ from REVIEW_720 30fps contract")

    silent = qual_dir / "d_composed_silent_v2.mp4"
    composition = compose_all_frames_v2(native_source, silent, plan, root, ffmpeg, qual_dir, consumer, executor)
    probe_silent = executor.ffprobe_json(ffprobe, silent)
    video_streams = [s for s in probe_silent.get("streams", []) if s.get("codec_type") == "video"]
    audio_streams = [s for s in probe_silent.get("streams", []) if s.get("codec_type") == "audio"]
    if len(video_streams) != 1 or audio_streams or int(video_streams[0].get("nb_read_frames", -1)) != TOTAL_FRAMES:
        raise RuntimeError("V2 silent composed intermediate FFprobe contract failed")

    duration = float(native_timeline["duration_seconds"])
    finals = {}
    for key in ("A", "B", "C"):
        seed = int(fm[key].get("seed", 0))
        suffix = "changed_music_840002" if key == "C" else f"music_840001_{key}"
        target = output_root / f"{run_id}_{key}_{suffix}.mp4"
        finals[key] = executor.mux_audio(ffmpeg, ffprobe, silent, wavs[key], target, duration, TOTAL_FRAMES, qual_dir)
    video_hashes, audio_hashes = {}, {}
    for key in ("A", "B", "C"):
        video_hashes[key] = executor.stream_hash(ffmpeg, Path(finals[key]["path"]), "v", qual_dir / f"v2_video_stream_hash_{key}.log")
        audio_hashes[key] = executor.stream_hash(ffmpeg, Path(finals[key]["path"]), "a", qual_dir / f"v2_audio_stream_hash_{key}.log")
    if len(set(video_hashes.values())) != 1:
        raise RuntimeError("V2 music-only seed change altered video bitstream across A/B/C")
    if audio_hashes["A"] != audio_hashes["B"] or audio_hashes["A"] == audio_hashes["C"]:
        raise RuntimeError("V2 final audio elementary streams do not preserve A/B repeat and C change")
    review_frames = extract_review_frames(ffmpeg, Path(finals["A"]["path"]), review_dir, executor)
    post_pins = normalized_pins(executor._source_pins(intent, root))
    if post_pins != old_pins:
        raise RuntimeError("E1 source pins changed during V2 requalification")

    result = {
        "schema": "C11E-E4C-DRILL-V2-EXISTING-MEDIA-REQUALIFICATION-RECEIPT-V1",
        "status": "PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE",
        "request_id": run_id,
        "source_request_id": EXPECTED_REQUEST_ID,
        "source_receipt_sha256": EXPECTED_RECEIPT_SHA256,
        "source_native_mp4_sha256": EXPECTED_NATIVE_SHA256,
        "source_music_wav_sha256": EXPECTED_WAV_SHA256,
        "native_capture_reused": True,
        "godot_invoked": False,
        "c11c_launcher_invoked": False,
        "new_native_capture": False,
        "family_music_generation_invoked": False,
        "family_music_wavs_reused": True,
        "d_executor_replaced": False,
        "d_consumer_contract": "V2_SOCIAL_BODY_PIXEL_EXACT",
        "geometry": {"header": [0,0,720,192], "body": [0,192,720,896], "footer": [0,1088,720,192]},
        "presentation_profile_sha256": PRESENTATION_PROFILE_SHA256,
        "e1_source_pins": {"count": len(old_pins), "pre": old_pins, "post": post_pins, "unchanged": True},
        "d_composition": composition,
        "native_source_ffprobe": native_probe,
        "silent_video_ffprobe": probe_silent,
        "final_A": finals["A"], "final_B": finals["B"], "final_C": finals["C"],
        "stream_hashes": {"video": video_hashes, "audio": audio_hashes,
                              "video_A_B_C_identical": True, "audio_A_B_identical": True, "audio_C_distinct": True},
        "operator_review_frames": review_frames,
        "ffmpeg_version": ffmpeg_version, "ffprobe_version": ffprobe_version,
        "e1_status": "PREPARE_ONLY", "family_adapter_status": "NOT_CONNECTED_E1",
        "production_dispatch": False, "release_authority": "NONE",
        "visual_acceptance": "PENDING_OPERATOR_REVIEW",
        "audio_acceptance": "PENDING_OPERATOR_LISTENING_REVIEW",
        "evidence_root": str(output_root),
    }
    write_json(output_root / "E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json", result)
    (output_root / "OPERATOR_REVIEW_CHECKLIST.md").write_text(
        "# E4C Drill V2 operator review\n\n"
        "Review the A/B/C outputs and the seven extracted frames. Confirm: (1) PRE_ROLL is the complete native frame; "
        "(2) GAME shows the native visual effect only in the full-width body rectangle; (3) native tracking header and telemetry footer "
        "are absent from GAME; (4) D title/subtitle occupy the top band and D CTA the bottom band; (5) END_CTA is the complete native frame "
        "with native C11-C ownership; (6) A and B audio are identical in content, C differs; (7) no A/V sync or clipping artefacts.\n\n"
        "This review is required before the selector is counted as V2-accepted. This receipt grants no production dispatch or release authority.\n",
        encoding="utf-8", newline="\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--evidence-root", required=True, help="Preserved E4C-CLI-SMOKE evidence root; read-only")
    parser.add_argument("--output-id", required=True, help="Fresh E4C-CLI-COMPOSITION-V2-* output ID")
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    args = parser.parse_args()
    try:
        result = run(args)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {"schema": "C11E-E4C-DRILL-V2-EXISTING-MEDIA-REQUALIFICATION-FAILURE-V1", "status": "FAIL_CLOSED_V2_REQUALIFICATION", "request_id": getattr(args, "output_id", None), "error_type": type(exc).__name__, "error": str(exc), "native_capture_reused": True, "godot_invoked": False, "c11c_launcher_invoked": False, "new_native_capture": False, "family_music_generation_invoked": False, "production_dispatch": False, "release_authority": "NONE"}
        try:
            root = Path(args.project_root).resolve()
            output_root = root / "artifacts" / "production" / "c11e" / str(args.output_id)
            if output_root.is_dir() and not (output_root / "E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json").exists():
                write_json(output_root / "E4C_DRILL_V2_REQUALIFICATION_FAILURE.json", failure)
        except Exception:
            pass
        print(json.dumps(failure, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
