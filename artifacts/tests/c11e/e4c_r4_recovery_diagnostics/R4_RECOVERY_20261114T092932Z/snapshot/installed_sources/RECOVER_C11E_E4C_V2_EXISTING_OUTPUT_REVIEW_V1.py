#!/usr/bin/env python3
"""Complete the review/evidence stage for the already-composed R3 E4C V2 run.

This recovery is intentionally bound to one immutable output id and exact hashes.
It does not compose frames, mux audio, generate music, capture native media, or
invoke C11-C/Godot. It revalidates existing media, hashes elementary streams,
extracts seven review PNGs with modern FFmpeg -fps_mode, and writes the final
technical receipt pending human visual/audio review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
from typing import Any

RUN_ID = "E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9"
EXPECTED_RECEIPT_SHA256 = "57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903"
EXPECTED_INTENT_SHA256 = "9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e"
EXPECTED_NATIVE_SHA256 = "d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338"
EXPECTED_WAV_SHA256 = {
    "A": "e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277",
    "B": "e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277",
    "C": "5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40",
}
EXPECTED_PLAN_SHA256 = "3bbdabdb106461bafb699ae889205c9d53be41fe9e94f58c7254c925e8e628fe"
EXPECTED_SILENT = (785860, "d674aa7700414c49c5b5ca957c4390da6e0020cea2de9d84750f30c6f14e14a5")
EXPECTED_FINALS = {
    "A": (1455889, "8808b5244c118dc74d9a6fcf9d5e5b49b8ddae33f686794a170fe76cbc971bc1", "E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9_A_music_840001_A.mp4"),
    "B": (1455889, "8808b5244c118dc74d9a6fcf9d5e5b49b8ddae33f686794a170fe76cbc971bc1", "E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9_B_music_840001_B.mp4"),
    "C": (1454787, "677edb16b0b1fcf47962633624df53ec5c53201080c95d5f563f10b1957c1961", "E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9_C_changed_music_840002.mp4"),
}
EXPECTED_PRESENTATION_PROFILE_SHA256 = "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24"
EXPECTED_AAC_STREAM_SHA256 = {"A": "2fd32bfeb275c53ae4d754796793d6c7c8ece5144de4d5ae83c2132952dd4501", "B": "2fd32bfeb275c53ae4d754796793d6c7c8ece5144de4d5ae83c2132952dd4501", "C": "e018e6c81a88b8d9ab216267f042d2c5f18b0e477fa3e84951958fa8ac63d9ad"}
FROZEN_C11C_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
WIDTH, HEIGHT, FPS = 720, 1280, 30
TOTAL_FRAMES = 810
SAMPLES = [
    (0, "PRE_ROLL_FIRST"), (89, "PRE_ROLL_LAST"), (90, "GAME_FIRST"),
    (405, "GAME_MID"), (719, "GAME_LAST"), (720, "END_CTA_FIRST"), (809, "END_CTA_LAST"),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def resolve_media(evidence_root: Path, recorded_path: str, subdir: str) -> Path:
    basename = PureWindowsPath(recorded_path).name or Path(recorded_path).name
    matches = [p for p in (evidence_root / subdir).rglob(basename) if p.is_file()]
    if len(matches) != 1:
        raise FileNotFoundError(f"expected exactly one preserved evidence media {basename}; found={len(matches)}")
    return matches[0]


def _stream_counts(probe: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    streams = probe.get("streams", [])
    return ([s for s in streams if s.get("codec_type") == "video"],
            [s for s in streams if s.get("codec_type") == "audio"])


def validate_video_stream(video: dict[str, Any], label: str) -> None:
    actual = (video.get("codec_name"), int(video.get("width", 0)), int(video.get("height", 0)),
              str(video.get("avg_frame_rate")), str(video.get("pix_fmt")),
              str(video.get("profile", "")).casefold(), str(video.get("color_range", "")).casefold(),
              int(video.get("nb_read_frames", -1)))
    expected = ("h264", WIDTH, HEIGHT, "30/1", "yuv420p", "high", "tv", TOTAL_FRAMES)
    if actual[:6] != expected[:6] or actual[6] not in ("tv", "limited") or actual[7] != expected[7]:
        raise RuntimeError(f"{label} video stream contract mismatch: {actual!r} != {expected!r}")


def validate_final_probe(probe: dict[str, Any], label: str) -> dict[str, Any]:
    videos, audios = _stream_counts(probe)
    if len(videos) != 1 or len(audios) != 1 or len(probe.get("streams", [])) != 2:
        raise RuntimeError(f"{label} must contain exactly one video and one audio stream")
    validate_video_stream(videos[0], label)
    audio = audios[0]
    audio_actual = (audio.get("codec_name"), str(audio.get("profile", "")).casefold(),
                    str(audio.get("sample_rate")), int(audio.get("channels", 0)))
    if audio_actual != ("aac", "lc", "48000", 2):
        raise RuntimeError(f"{label} AAC-LC stream contract mismatch: {audio_actual!r}")
    duration = float((probe.get("format") or {}).get("duration", 0.0))
    if abs(duration - 27.0) > 0.15:
        raise RuntimeError(f"{label} duration mismatch: {duration}")
    video_start = float(videos[0].get("start_time", 0.0) or 0.0)
    audio_start = float(audio.get("start_time", 0.0) or 0.0)
    delta = abs(video_start - audio_start)
    if delta > 0.020:
        raise RuntimeError(f"{label} A/V start offset exceeds 20ms: {delta}")
    return {"duration_seconds": duration, "av_start_delta_seconds": delta,
            "video": videos[0], "audio": audio, "ffprobe": probe}


def extract_review_frames(ffmpeg: Path, final_a: Path, review_dir: Path, qual_dir: Path) -> list[dict[str, Any]]:
    """Extract one selected frame without the removed -vsync CLI option."""
    review_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for index, label in SAMPLES:
        target = review_dir / f"frame_{index:03d}_{label}.png"
        if target.exists():
            raise FileExistsError(f"refusing to overwrite existing review frame: {target}")
        expression = f"select=eq(n\\,{index})"
        command = [str(ffmpeg), "-y", "-hide_banner", "-loglevel", "error", "-i", str(final_a),
                   "-vf", expression, "-fps_mode", "passthrough", "-frames:v", "1", str(target)]
        proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        log = qual_dir / f"review_frame_{index:03d}_{label}_ffmpeg.json"
        write_json(log, {"command": command, "returncode": proc.returncode, "stderr": proc.stderr,
                         "stdout": proc.stdout, "fps_mode": "passthrough"})
        if proc.returncode != 0 or not target.is_file() or target.stat().st_size <= 0:
            raise RuntimeError(f"review frame extraction failed for {index}: {proc.stderr[-2000:]}")
        results.append({"frame_index": index, "phase_label": label, "path": str(target),
                        "sha256": sha256_file(target), "bytes": target.stat().st_size,
                        "width": WIDTH, "height": HEIGHT, "fps_mode": "passthrough"})
    return results


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.output_id != RUN_ID:
        raise ValueError(f"recovery is bound to the existing R3 output id {RUN_ID}")
    root = Path(args.project_root).resolve()
    evidence_root = Path(args.evidence_root).resolve()
    if not root.is_dir() or not evidence_root.is_dir() or root not in evidence_root.parents:
        raise ValueError("ProjectRoot/EvidenceRoot invalid; EvidenceRoot must remain inside the active checkout")
    output_root = (root / "artifacts" / "production" / "c11e" / RUN_ID).resolve()
    if not output_root.is_dir() or root not in output_root.parents:
        raise FileNotFoundError(f"existing R3 output directory missing or outside project: {output_root}")
    qual_dir = output_root / "qualification"
    review_dir = output_root / "operator_review"
    if not qual_dir.is_dir() or not review_dir.is_dir():
        raise FileNotFoundError("existing R3 qualification/operator_review directories missing")

    # Revalidate the original, accepted CLI source evidence without modifying it.
    receipt_path = evidence_root / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"
    request_path = evidence_root / "request.json"
    intent_path = evidence_root / "e1_intent.json"
    receipt, request, intent = read_json(receipt_path), read_json(request_path), read_json(intent_path)
    if sha256_file(receipt_path) != EXPECTED_RECEIPT_SHA256:
        raise ValueError("preserved source receipt SHA-256 mismatch")
    if sha256_file(intent_path) != EXPECTED_INTENT_SHA256 or intent.get("intent_sha256") != EXPECTED_INTENT_SHA256:
        raise ValueError("preserved E1 intent SHA-256 mismatch")
    if request.get("request_id") != "E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8":
        raise ValueError("preserved source request identity mismatch")
    if receipt.get("status") != "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION" or receipt.get("request_origin") != "CLI":
        raise ValueError("preserved source receipt not accepted CLI evidence")
    if receipt.get("release_authority") != "NONE" or receipt.get("production_dispatch") is not False:
        raise ValueError("source evidence violates release/dispatch boundary")
    if receipt.get("e1_validation", {}).get("status") != "PASS_E1_PREPARATION_ONLY" or receipt.get("e1_validation", {}).get("source_pin_count") != 91:
        raise ValueError("source E1 receipt is not accepted PREPARE_ONLY/91-pin evidence")

    # Verify exact R3 partial-run artifacts by their captured byte count and SHA.
    plan_path = output_root / "d_composition_plan_v2.json"
    if not plan_path.is_file() or plan_path.stat().st_size != 8077 or sha256_file(plan_path) != EXPECTED_PLAN_SHA256:
        raise ValueError("existing V2 composition plan does not match the captured R3 postimage")
    plan = read_json(plan_path)
    geometry = plan.get("geometry", {})
    if plan.get("schema") != "C11E-E4C-DRILL-VISUAL-COMPOSITION-PLAN-V1":
        raise ValueError("stored composition plan schema mismatch")
    if plan.get("approval", {}).get("decision_record_sha256") != "bceef9a22c27447ccbef5487339c25626e4cb4c5d32509809b832411655914e8":
        raise ValueError("stored plan immutable decision pin mismatch")
    if geometry.get("canvas") != {"x": 0, "y": 0, "width": 720, "height": 1280, "aspect_ratio": "9:16"}:
        raise ValueError("stored plan canvas geometry mismatch")
    if geometry.get("body_rect") != {"x": 0, "y": 192, "width": 720, "height": 896}:
        raise ValueError("stored plan body geometry mismatch")
    if geometry.get("source_frame_viewport") != {"x": 0, "y": 192, "width": 720, "height": 896}:
        raise ValueError("stored plan source viewport mismatch")

    # Current E1 source pins: exactly match the three preserved receipt inventories.
    tools_dir = root / "tools" / "c11d" / "d9"
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    import c11e_e4c_drill_execution as executor  # type: ignore
    old_pins = sorted(receipt.get("source_pins_pre_execution", []), key=lambda r: r.get("path", ""))
    if len(old_pins) != 91 or old_pins != sorted(receipt.get("source_pins_immediately_pre_renderer", []), key=lambda r: r.get("path", "")) or old_pins != sorted(receipt.get("source_pins_post_execution", []), key=lambda r: r.get("path", "")):
        raise ValueError("preserved 91-pin pre/pre-render/post inventories mismatch")
    current_pins = executor._source_pins(intent, root)
    if sorted(current_pins, key=lambda r: r.get("path", "")) != old_pins:
        raise ValueError("current E1 source pins no longer match accepted 91-pin inventory")
    import c11e_e4c_drill_visual_composition_consumer as consumer  # type: ignore
    consumer.validate_plan(plan)
    rebuilt_plan = consumer.build_composition_plan_for_existing_media(intent, root, receipt, evidence_root)
    if rebuilt_plan != plan:
        raise ValueError("current D V2 consumer rebuild differs from the exact stored R3 composition plan")
    profile = next((r for r in old_pins if r.get("path") == "core/presentation/PresentationProfile.gd"), None)
    if not profile or profile.get("sha256") != EXPECTED_PRESENTATION_PROFILE_SHA256:
        raise ValueError("PresentationProfile exact geometry pin mismatch")
    frozen = root / "release" / "C11C_FREEZE_PACKAGE_MANIFEST.json"
    if frozen.stat().st_size != 796318 or sha256_file(frozen) != FROZEN_C11C_SHA256:
        raise ValueError("frozen C11-C manifest changed")

    # Reuse native source and original WAV media only for hash/probe comparison.
    native_info = receipt.get("native_source", {})
    native_source = resolve_media(evidence_root, str(native_info.get("mp4", "")), "native_source")
    if sha256_file(native_source) != EXPECTED_NATIVE_SHA256 or native_info.get("mp4_sha256") != EXPECTED_NATIVE_SHA256:
        raise ValueError("preserved native silent MP4 hash mismatch")
    fm = receipt.get("family_music", {})
    if fm.get("route") != "C11_C_FAMILY_MUSIC_V4" or fm.get("profile_id") != "FLOWING_VECTOR":
        raise ValueError("preserved music route/profile mismatch")
    wav_paths = {}
    for key in ("A", "B", "C"):
        row = fm.get(key, {})
        wav = resolve_media(evidence_root, str(row.get("path", "")), "qualification")
        if sha256_file(wav) != EXPECTED_WAV_SHA256[key] or row.get("sha256") != EXPECTED_WAV_SHA256[key]:
            raise ValueError(f"preserved music WAV {key} hash mismatch")
        wav_paths[key] = wav
    if sha256_file(wav_paths["A"]) != sha256_file(wav_paths["B"]) or sha256_file(wav_paths["A"]) == sha256_file(wav_paths["C"]):
        raise ValueError("preserved FAMILY_MUSIC_V4 A/B/C seed isolation mismatch")

    # The R3 main run already returned from compose_all_frames_v2 and completed
    # all mux operations; this is established by the operator's progress trace
    # reaching MUX_B_STARTED and STREAM_HASH_A_STARTED. That function returns
    # only after 810 frames, counts 90/630/90, 630 body-identity and 180 full
    # frame-passthrough assertions. No compositor or mux is called here.
    silent_path = qual_dir / "d_composed_silent_v2.mp4"
    if not silent_path.is_file() or (silent_path.stat().st_size, sha256_file(silent_path)) != EXPECTED_SILENT:
        raise ValueError("existing V2 silent composed video missing or hash mismatch")
    finals: dict[str, dict[str, Any]] = {}
    for key, (expected_bytes, expected_sha, filename) in EXPECTED_FINALS.items():
        path = output_root / filename
        if not path.is_file() or path.stat().st_size != expected_bytes or sha256_file(path) != expected_sha:
            raise ValueError(f"existing final {key} does not match exact R3 partial-output evidence")
        finals[key] = {"path": str(path), "bytes": expected_bytes, "sha256": expected_sha}

    ffprobe = executor.discover_binary("ffprobe.exe", args.ffprobe)
    ffmpeg = executor.discover_binary("ffmpeg.exe", args.ffmpeg, sibling_of=ffprobe)
    ffmpeg_version = executor.verify_executable(ffmpeg, "FFmpeg", ["-version"]).splitlines()[0]
    ffprobe_version = executor.verify_executable(ffprobe, "FFprobe", ["-version"]).splitlines()[0]

    silent_probe = executor.ffprobe_json(ffprobe, silent_path)
    silent_videos, silent_audios = _stream_counts(silent_probe)
    if len(silent_videos) != 1 or silent_audios:
        raise RuntimeError("existing silent video must contain exactly one video and no audio")
    validate_video_stream(silent_videos[0], "silent intermediate")
    native_probe = executor.ffprobe_json(ffprobe, native_source)
    native_videos, native_audios = _stream_counts(native_probe)
    if len(native_videos) != 1 or native_audios or int(native_videos[0].get("nb_read_frames", -1)) != TOTAL_FRAMES:
        raise RuntimeError("preserved native source FFprobe must be one silent 810-frame video")
    if (int(native_videos[0].get("width", 0)), int(native_videos[0].get("height", 0)), str(native_videos[0].get("avg_frame_rate"))) != (WIDTH, HEIGHT, "30/1"):
        raise RuntimeError("preserved native source dimensions/FPS mismatch")

    final_probe_rows = {}
    for key in ("A", "B", "C"):
        probe = executor.ffprobe_json(ffprobe, Path(finals[key]["path"]))
        checked = validate_final_probe(probe, f"final {key}")
        finals[key].update(checked)
        final_probe_rows[key] = probe

    # Recompute only elementary stream hashes (no encoding/remuxing).
    video_hashes, audio_hashes = {}, {}
    for key in ("A", "B", "C"):
        video_hashes[key] = executor.stream_hash(ffmpeg, Path(finals[key]["path"]), "v", qual_dir / f"recovery_video_stream_hash_{key}.log")
        audio_hashes[key] = executor.stream_hash(ffmpeg, Path(finals[key]["path"]), "a", qual_dir / f"recovery_audio_stream_hash_{key}.log")
    if len(set(video_hashes.values())) != 1:
        raise RuntimeError("existing A/B/C video elementary streams are not identical")
    if audio_hashes["A"] != audio_hashes["B"] or audio_hashes["A"] == audio_hashes["C"]:
        raise RuntimeError("existing audio elementary streams do not preserve A/B repeat and C change")
    if audio_hashes != EXPECTED_AAC_STREAM_SHA256:
        raise RuntimeError(f"existing AAC elementary stream hashes differ from the accepted source CLI receipt: {audio_hashes}")

    # This is the only FFmpeg operation that writes media in recovery: 7 still PNGs.
    review_frames = extract_review_frames(ffmpeg, Path(finals["A"]["path"]), review_dir, qual_dir)
    post_pins = executor._source_pins(intent, root)
    if sorted(post_pins, key=lambda r: r.get("path", "")) != old_pins:
        raise RuntimeError("E1 source pins changed during review-output recovery")

    composition = {
        "frames_expected": 810, "frames_composed": 810,
        "phase_counts": {"PRE_ROLL": 90, "GAME": 630, "END_CTA": 90},
        "game_native_body_pixel_identity_frames": 630,
        "native_full_frame_passthrough_frames": 180,
        "sampled_frames": [],
        "silent_video_path": str(silent_path),
        "silent_video_sha256": EXPECTED_SILENT[1], "silent_video_bytes": EXPECTED_SILENT[0],
        "recovered_from_original_completed_composition": True,
        "original_run_progress_reached": ["FRAME_COMPOSITION=810/810", "MUX_B_STARTED", "STREAM_HASH_A_STARTED"],
        "pixel_identity_guard_contract": "compose_all_frames_v2 returns only after all 630 GAME body pixel comparisons, 180 PRE_ROLL/END_CTA full-frame passthrough comparisons, exact phase counts and successful FFmpeg decoder/encoder exits",
    }
    result = {
        "schema": "C11E-E4C-DRILL-V2-EXISTING-MEDIA-REQUALIFICATION-RECEIPT-V1",
        "status": "PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE",
        "request_id": RUN_ID,
        "source_request_id": "E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8",
        "source_receipt_sha256": EXPECTED_RECEIPT_SHA256,
        "source_native_mp4_sha256": EXPECTED_NATIVE_SHA256,
        "source_music_wav_sha256": EXPECTED_WAV_SHA256,
        "native_capture_reused": True, "godot_invoked": False, "c11c_launcher_invoked": False,
        "new_native_capture": False, "family_music_generation_invoked": False,
        "family_music_wavs_reused": True, "d_executor_replaced": False,
        "recovered_from_partial_run": True,
        "recovery_method": "VERIFY_EXISTING_MEDIA_REPROBE_REHASH_AND_EXTRACT_REVIEW_FRAMES_ONLY",
        "frame_composition_repeated": False, "audio_mux_repeated": False,
        "d_consumer_contract": "V2_SOCIAL_BODY_PIXEL_EXACT",
        "geometry": {"header": [0, 0, 720, 192], "body": [0, 192, 720, 896], "footer": [0, 1088, 720, 192]},
        "presentation_profile_sha256": EXPECTED_PRESENTATION_PROFILE_SHA256,
        "e1_source_pins": {"count": len(old_pins), "pre": old_pins, "post": post_pins, "unchanged": True},
        "d_composition": composition,
        "native_source_ffprobe": native_probe,
        "silent_video_ffprobe": silent_probe,
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
    receipt_out = output_root / "E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json"
    write_json(receipt_out, result)
    write_json(output_root / "V2_REQUALIFICATION_PROGRESS.json", {
        "schema": "C11E-E4C-V2-REQUALIFICATION-PROGRESS-V1", "stage": "COMPLETE",
        "updated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "request_id": RUN_ID, "technical_status": result["status"],
        "final_outputs": ["A", "B", "C"], "review_frame_count": len(review_frames),
        "source_pins_unchanged": True, "recovered_from_partial_run": True,
        "frame_composition_repeated": False, "audio_mux_repeated": False,
        "release_authority": "NONE",
    })
    checklist = (
        "# E4C Drill V2 operator review\n\n"
        "Review the three A/B/C outputs and seven extracted frames. Confirm: (1) PRE_ROLL is complete native frame; "
        "(2) GAME native tracking body is preserved and native header/footer are absent; (3) D title/subtitle in top band and CTA in bottom band; "
        "(4) END_CTA is complete native frame; (5) A/B audio match and C differs; (6) no A/V sync, clipping or playback artefacts.\n\n"
        "Technical status is PASS_PENDING_OPERATOR_REVIEW. This recovery performed no frame composition or audio mux; it validated the exact existing R3 outputs. "
        "Human visual and listening acceptance is required before this selector counts toward 20/20. No production dispatch or release authority is granted.\n"
    )
    (output_root / "OPERATOR_REVIEW_CHECKLIST.md").write_text(checklist, encoding="utf-8", newline="\n")
    audit = {
        "schema": "C11E-E4C-V2-EXISTING-OUTPUT-RECOVERY-AUDIT-V1", "status": "PASS_EXISTING_OUTPUT_RECOVERY",
        "request_id": RUN_ID, "source_receipt_sha256": EXPECTED_RECEIPT_SHA256,
        "intent_sha256": EXPECTED_INTENT_SHA256, "composition_plan_sha256": EXPECTED_PLAN_SHA256,
        "silent_output": {"bytes": EXPECTED_SILENT[0], "sha256": EXPECTED_SILENT[1]},
        "final_output_inventory": {k: {"bytes": EXPECTED_FINALS[k][0], "sha256": EXPECTED_FINALS[k][1]} for k in EXPECTED_FINALS},
        "stream_hashes": {"video": video_hashes, "audio": audio_hashes},
        "review_frames": review_frames, "source_pin_count": 91,
        "ffmpeg_version": ffmpeg_version, "ffprobe_version": ffprobe_version,
        "frame_composition_repeated": False, "audio_mux_repeated": False,
        "new_native_capture": False, "family_music_generation": False,
        "production_dispatch": False, "release_authority": "NONE",
    }
    write_json(output_root / "V2_EXISTING_OUTPUT_RECOVERY_AUDIT.json", audit)

    # Compact operator-review bundle: three final videos, seven PNGs and receipts.
    bundle = output_root / "E4C_V2_OPERATOR_REVIEW_BUNDLE.zip"
    bundle_inputs = [receipt_out, output_root / "OPERATOR_REVIEW_CHECKLIST.md",
                     output_root / "V2_REQUALIFICATION_PROGRESS.json", output_root / "V2_EXISTING_OUTPUT_RECOVERY_AUDIT.json"]
    bundle_inputs += [Path(finals[k]["path"]) for k in ("A", "B", "C")]
    bundle_inputs += [Path(r["path"]) for r in review_frames]
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for p in bundle_inputs:
            zf.write(p, p.relative_to(output_root).as_posix())
    result["operator_review_bundle"] = str(bundle)
    result["operator_review_bundle_sha256"] = sha256_file(bundle)
    write_json(receipt_out, result)
    print(json.dumps({
        "status": result["status"], "request_id": RUN_ID,
        "frames_composed_reused": 810, "game_body_identity_frames_attested": 630,
        "full_frame_passthrough_frames_attested": 180,
        "final_mp4s": {k: finals[k]["path"] for k in finals},
        "stream_hashes": {"video": video_hashes, "audio": audio_hashes},
        "review_frames": review_frames,
        "operator_review_bundle": str(bundle), "operator_review_bundle_sha256": result["operator_review_bundle_sha256"],
        "frame_composition_repeated": False, "audio_mux_repeated": False,
        "production_dispatch": False, "release_authority": "NONE",
    }, ensure_ascii=False, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--output-id", required=True)
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    args = parser.parse_args()
    try:
        run(args)
        return 0
    except Exception as exc:
        payload = {"schema": "C11E-E4C-V2-EXISTING-OUTPUT-RECOVERY-FAILURE-V1", "status": "FAIL_CLOSED_EXISTING_OUTPUT_RECOVERY",
                   "request_id": args.output_id, "error_type": type(exc).__name__, "error": str(exc),
                   "frame_composition_repeated": False, "audio_mux_repeated": False,
                   "production_dispatch": False, "release_authority": "NONE"}
        print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
