#!/usr/bin/env python3
"""C11-E E4A.4 bounded Challenge audiovisual review pilot.

Uses the already accepted E4A.2 normalized CHALLENGE_004 review MP4 as an
immutable video source. It prepares sealed E1 TEST intents, explicitly invokes
D3 Music V5 for test-only audio, applies the accepted D3.3 mastering pattern,
then stream-copies video into test-only A/B/C muxes. It never dispatches a
C11-C generator, a D renderer, or the production service.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import traceback
import uuid
import zipfile
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

REPO_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
E4A2_RUN_ID = "RUN_20261104_002559_542bcf60"
E4A2_RECEIPT_SHA = "b23a5f0c1557b52b724c99ac90a671e0a8d8457dcd5e605f8d097c517f366308"
E4A2_REPORT_SHA = "e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159"
BASE_MP4_SHA = "edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e"
E4A3_RUN_ID = "RUN_20261104_021444_0cfefef6"
E4A3_RECEIPT_SHA = "3670428feae3b34766677b4cdba3985babecbda9ee781eebe4cc57c318cd9f1c"
E4A3_REPORT_SHA = "ee1be803f4d0433347778793aab12228301aea5108f426011836c27dc268dc08"
E3_PIPELINE_SHA = "46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d"
E1_SERVICE_SHA = "f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0"
D9_RESOLVER_SHA = "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1"
D9_EDITORIAL_SHA = "5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5"
D9_GUI_REQUEST_SHA = "0e95109ffd3ba5655d28292309196349470ab7958a467f096543a2c98c22976e"
D3_ENGINE_SHA = "03ae7e2997796e0c67ca15c8886b1e5b290791a142b6631a572d1cba6eba4eb1"
D3_SPEC_SHA = "8970f4e93c878285b727697f3d269f5ee464b6029fe79eabc5fcbf4245e9dbf2"
D3_PROFILE_SHA = "0c877cbe6e1c288890da31fc4481a58e1051749b45a50b2290cbef5d1120d2de"
D3_CONTRACT_SHA = "12c59ce2a2135a49ce0d5968a29905a1e5890743507db1ee0039da1374efcfe8"
APPROVED_POLICY_SHA = "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
GAMEPLAY_SEED = 314159
MUSIC_SEED_A = 840001
MUSIC_SEED_C = 840002
TEMPO_BPM_FIXTURE = 104  # Historical D9.2 audio-pilot fixture only; not a product default.
VARIATION_INDEX = 0

class E4A4Error(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise E4A4Error(f"Expected JSON object: {path}")
    return value


def assert_pin(root: Path, rel: str, expected: str) -> dict[str, Any]:
    path = root / Path(*rel.split("/"))
    if not path.is_file() or path.is_symlink():
        raise E4A4Error(f"Required pinned source missing or unsafe: {rel}")
    actual = sha256_file(path)
    if actual != expected:
        raise E4A4Error(f"Source pin mismatch for {rel}: expected {expected}, actual {actual}")
    return {"path": rel, "sha256": actual, "bytes": path.stat().st_size}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise E4A4Error(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def validate_evidence_inputs(root: Path, base_run: Path, compositor_run: Path, ffprobe: str, e3: Any, run_root: Path):
    manifest = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    if not manifest.is_file() or manifest.stat().st_size != 796318 or sha256_file(manifest) != REPO_MANIFEST_SHA:
        raise E4A4Error("Frozen C11-C manifest does not match the immutable authority pin")

    e4a2_receipt_path = base_run / "C11E_E4A_REAL_BODY_PIXEL_RUNNER_RECEIPT.json"
    e4a2_report_path = base_run / "C11E_E4A_REAL_BODY_PIXEL_REPORT.json"
    if sha256_file(e4a2_receipt_path) != E4A2_RECEIPT_SHA or sha256_file(e4a2_report_path) != E4A2_REPORT_SHA:
        raise E4A4Error("Accepted E4A.2 receipt/report identity mismatch")
    e4a2_receipt, e4a2_report = load_json(e4a2_receipt_path), load_json(e4a2_report_path)
    if e4a2_receipt.get("status") != "PASS_ISOLATED_REAL_C11C_BODY_PIXEL_PROOF_TEST_ONLY":
        raise E4A4Error("E4A.2 base receipt is not accepted")
    if e4a2_receipt.get("normalized_review_video_sha256") != BASE_MP4_SHA:
        raise E4A4Error("E4A.2 normalized video pin mismatch")
    base_video = base_run / "review_delivery/CHALLENGE_004_REVIEW_720_30FPS_TEST_ONLY.mp4"
    if not base_video.is_file() or sha256_file(base_video) != BASE_MP4_SHA:
        raise E4A4Error("E4A.2 normalized review MP4 missing or hash mismatch")
    if e4a2_report.get("status") != "PASS_ISOLATED_REAL_C11C_BODY_PIXEL_PROOF_TEST_ONLY":
        raise E4A4Error("E4A.2 report status mismatch")

    e4a3_receipt_path = compositor_run / "C11E_E4A_D_COMPOSITOR_PIXEL_RECEIPT.json"
    e4a3_report_path = compositor_run / "C11E_E4A_D_COMPOSITOR_PIXEL_REPORT.json"
    if sha256_file(e4a3_receipt_path) != E4A3_RECEIPT_SHA or sha256_file(e4a3_report_path) != E4A3_REPORT_SHA:
        raise E4A4Error("Accepted E4A.3 receipt/report identity mismatch")
    e4a3_receipt, e4a3_report = load_json(e4a3_receipt_path), load_json(e4a3_report_path)
    if e4a3_receipt.get("status") != "PASS_ISOLATED_D_OWNED_GODOT_LAYER_REAL_BODY_PIXEL_PROOF_TEST_ONLY":
        raise E4A4Error("E4A.3 compositor receipt is not accepted")
    if e4a3_receipt.get("godot_exit_code") != 0 or e4a3_receipt.get("pixel_png_count") != 18 or e4a3_receipt.get("pixel_comparison_count") != 12:
        raise E4A4Error("E4A.3 compositor run is incomplete")
    if e4a3_receipt.get("base_run_receipt_sha256") != E4A2_RECEIPT_SHA:
        raise E4A4Error("E4A.3 does not reference the accepted E4A.2 receipt")
    if e4a3_receipt.get("normalized_review_mp4_sha256_before_after") != BASE_MP4_SHA:
        raise E4A4Error("E4A.3 does not preserve the accepted normalized video")
    if e4a3_report.get("test_only_visual_layout_disposition", {}).get("visual_placement_approved") is not False:
        raise E4A4Error("E4A.3 layout disposition unexpectedly changed; human review required")
    if e4a3_report.get("test_only_visual_layout_disposition", {}).get("production_compositor_layout_acceptance") != "NOT_GRANTED":
        raise E4A4Error("E4A.3 report no longer records layout acceptance as withheld")

    probe_run = e3._run(
        [ffprobe, "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(base_video)],
        stage="source_video_ffprobe", evidence_root=run_root, timeout_seconds=60,
    )
    probe = json.loads(probe_run.stdout)
    videos = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
    audios = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
    if len(videos) != 1 or audios:
        raise E4A4Error("E4A.2 source must be exactly one video stream and no audio")
    v = videos[0]
    fps = float(Fraction(str(v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1")))
    duration = float(v.get("duration") or probe.get("format", {}).get("duration") or 0.0)
    frames = int(v.get("nb_read_frames", 0))
    if (v.get("codec_name"), int(v.get("width", 0)), int(v.get("height", 0)), v.get("pix_fmt")) != ("h264", 720, 1280, "yuv420p"):
        raise E4A4Error("E4A.2 input video codec/dimensions/pixel format mismatch")
    if frames != 450 or abs(fps - 30.0) > 0.0001 or abs(duration - 15.0) > 0.02:
        raise E4A4Error("E4A.2 input video duration/frame-rate/frame-count mismatch")
    return {
        "base_video": base_video,
        "base_video_sha256": BASE_MP4_SHA,
        "e4a2_receipt_sha256": E4A2_RECEIPT_SHA,
        "e4a2_report_sha256": E4A2_REPORT_SHA,
        "e4a3_receipt_sha256": E4A3_RECEIPT_SHA,
        "e4a3_report_sha256": E4A3_REPORT_SHA,
        "video_probe": {"codec": v.get("codec_name"), "width": 720, "height": 1280, "pixel_format": v.get("pix_fmt"), "fps": fps, "frames": frames, "duration_seconds": duration, "audio_stream_count": 0},
        "e4a3_layout_review": {
            "visual_placement_approved": False,
            "production_compositor_layout_acceptance": "NOT_GRANTED",
            "existing_c11c_hook_content_overlap_observed": True,
            "disposition": "AUDIO_MUX_REVIEW_ONLY_DO_NOT_TREAT_BASE_VIDEO_AS_D_OVERLAY_COMPOSITE",
        },
    }


def prepare_e1_intents(root: Path, run_root: Path, seeds: tuple[int, int, int], run_id: str):
    service_dir = root / "c11c-suite/c11c-producer"
    if str(service_dir) not in sys.path:
        sys.path.insert(0, str(service_dir))
    import c11e_production_service as service
    resolver = service._load_d9_resolver(root)
    intents = {}
    labels = ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED")
    for label, music_seed in zip(labels, seeds):
        request_id = f"E4A4-CH004-{label}-{run_id}"
        raw_request = {
            "schema": resolver.REQUEST_SCHEMA_ID,
            "schema_version": "1.0",
            "request_id": request_id,
            "mode": "REVIEW",
            "selection": {"content_type": "challenges", "family_id": "parking_v2", "variant_id": "CHALLENGE_004"},
            "seed": GAMEPLAY_SEED,
            "music_seed": music_seed,
            "delivery_profile_id": "REVIEW_720",
            "presentation_profile_id": "social_default_v1",
            "variation_index": VARIATION_INDEX,
            "audio_enabled": True,
            "personalization_enabled": False,
            "editorial_profile": {},
            "production_override": {},
            "provenance": {"source_revision": "C11D-D9.10-PRODUCER-0.11.1", "request_origin": "TEST"},
        }
        prepared = service.prepare_c11e_production_intent(raw_request, root, request_origin="TEST", resolver_module=resolver)
        intent = prepared["intent"]
        validation = service.validate_c11e_production_intent(intent, root)
        music = intent.get("music_contract", {})
        if validation.get("status") != "PASS_E1_PREPARATION_ONLY":
            raise E4A4Error(f"E1 validation did not pass for {label}")
        if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED" or intent.get("request_origin") != "TEST":
            raise E4A4Error(f"E1 intent state/origin mismatch for {label}")
        if intent.get("delivery", {}).get("audio_enabled") is not True:
            raise E4A4Error(f"E1 audio_enabled is not true for {label}")
        domains = intent.get("seed_domains", {})
        if domains.get("gameplay", {}).get("value") != GAMEPLAY_SEED or domains.get("music", {}).get("value") != music_seed or domains.get("independent_domains") is not True:
            raise E4A4Error(f"E1 independent seed domains mismatch for {label}")
        if music.get("status") != "PLANNED_NOT_RENDERED" or music.get("dispatchable") is not False or music.get("engine_invoked") is not False or music.get("audio_created") is not False:
            raise E4A4Error(f"E1 music planning boundary mismatch for {label}")
        if intent.get("execution_boundary", {}).get("dispatch_authorized") is not False or intent.get("execution_boundary", {}).get("production_execution") is not False:
            raise E4A4Error(f"E1 execution boundary mismatch for {label}")
        engine_request = music.get("engine_request")
        if not isinstance(engine_request, dict) or engine_request.get("music_seed") != music_seed or engine_request.get("variation_index") != VARIATION_INDEX:
            raise E4A4Error(f"E1 V5 request binding mismatch for {label}")
        write_json(run_root / f"e1_intent_{label}.json", intent)
        intents[label] = {"intent": intent, "validation": validation, "raw_request_sha256": hashlib.sha256(json.dumps(raw_request, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()}
    return intents


def run(root: Path, base_run: Path, compositor_run: Path) -> Path:
    root = root.resolve()
    base_run = base_run.resolve()
    compositor_run = compositor_run.resolve()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{stamp}-{uuid.uuid4().hex[:8].upper()}"
    evidence_parent = root / "artifacts/tests/c11e/e4a_audio_mux_review"
    evidence_parent.mkdir(parents=True, exist_ok=True)
    run_root = evidence_parent / f"RUN_{run_id}"
    run_root.mkdir(parents=False, exist_ok=False)
    receipt: dict[str, Any] = {
        "schema": "C11E-E4A4-CHALLENGE-AUDIO-MUX-RECEIPT-V1",
        "schema_version": "1.0",
        "run_id": run_id,
        "status": "BLOCKED",
        "result": "FAIL",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "ISOLATED_CHALLENGE_004_D3_V5_AUDIO_MUX_REVIEW_TEST_ONLY",
        "production_dispatch": False,
        "production_renderer": False,
        "production_media_created": False,
        "gameplay_rerendered": False,
        "c11c_generator_modified": False,
        "core_audio_modified": False,
        "d3_engine_modified": False,
        "frozen_c11c_manifest_sha256": REPO_MANIFEST_SHA,
        "release_authority": "NONE",
    }
    try:
        print("E4A4_STAGE=VERIFYING_PRIOR_EVIDENCE", flush=True)
        paths = {
            "manifest": ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", REPO_MANIFEST_SHA),
            "e1_service": ("c11c-suite/c11c-producer/c11e_production_service.py", E1_SERVICE_SHA),
            "d9_resolver": ("tools/c11d/d9/universal_producer.py", D9_RESOLVER_SHA),
            "d9_editorial": ("tools/c11d/d9/universal_editorial_model.py", D9_EDITORIAL_SHA),
            "d9_gui_request": ("c11c-suite/c11c-producer/c11d_gui_request.py", D9_GUI_REQUEST_SHA),
            "e3_audio_pipeline": ("c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py", E3_PIPELINE_SHA),
            "d3_engine": ("tools/c11d/d3/c11d_music_engine_v5.py", D3_ENGINE_SHA),
            "d3_spec": ("definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json", D3_SPEC_SHA),
            "d3_profile": ("definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json", D3_PROFILE_SHA),
            "d3_contract": ("definitions/c11e/music/C11E_E3_2_D3_V5_E1_MUSIC_CONTRACT_V1.json", D3_CONTRACT_SHA),
            "approved_policy": ("definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json", APPROVED_POLICY_SHA),
        }
        source_pins = {key: assert_pin(root, rel, sha) for key, (rel, sha) in paths.items()}
        e3_path = root / "c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py"
        e3 = load_module("c11e_e3_audio_pipeline_e4a4", e3_path)
        ffmpeg, ffprobe = e3._resolve_tool("ffmpeg"), e3._resolve_tool("ffprobe")
        versions = {}
        for label, executable in (("ffmpeg", ffmpeg), ("ffprobe", ffprobe)):
            proc = e3._run([executable, "-version"], stage=f"{label}_version", evidence_root=run_root, timeout_seconds=30)
            versions[label] = (proc.stdout or "").splitlines()[0] if proc.stdout else "UNKNOWN"
        d3_pins = e3._verify_source_pins(root)
        source = validate_evidence_inputs(root, base_run, compositor_run, ffprobe, e3, run_root)
        base_video = Path(source.pop("base_video")).resolve()
        source["base_video_path"] = str(base_video)
        duration = float(source["video_probe"]["duration_seconds"])
        frames = int(source["video_probe"]["frames"])
        print("E4A4_STAGE=PREPARING_THREE_SEALED_E1_TEST_INTENTS", flush=True)
        intents = prepare_e1_intents(root, run_root, (MUSIC_SEED_A, MUSIC_SEED_A, MUSIC_SEED_C), run_id)
        print("E4A4_STAGE=RENDERING_D3_V5_TEST_AUDIO", flush=True)
        engine = e3._load_engine(root / "tools/c11d/d3/c11d_music_engine_v5.py")
        spec = load_json(root / "definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json")
        profile = load_json(root / "definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json")
        labels = ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED")
        seed_values = (MUSIC_SEED_A, MUSIC_SEED_A, MUSIC_SEED_C)
        renders, raw_paths = {}, {}
        for label, seed in zip(labels, seed_values):
            raw_path = run_root / f"{label}_raw.wav"
            base_request = dict(intents["A" if label == "A" else "B_REPEAT" if label == "B_REPEAT" else "C_CHANGED_MUSIC_SEED"]["intent"]["music_contract"]["engine_request"])
            engine_request = {
                "style_profile_id": base_request["style_profile_id"],
                "style_profile_version": base_request["style_profile_version"],
                "tempo_bpm": TEMPO_BPM_FIXTURE,
                "duration_seconds": duration,
                "variation_index": base_request["variation_index"],
                "music_seed": seed,
            }
            record = engine.render(engine_request, spec, profile, raw_path)
            digest = sha256_file(raw_path)
            if record.get("output_hash") != digest:
                raise E4A4Error(f"D3 V5 output hash mismatch: {label}")
            renders[label] = {**record, "engine_request": engine_request, "file_sha256": digest, "bytes": raw_path.stat().st_size}
            raw_paths[label] = raw_path
        raw_repeat = renders["A"]["file_sha256"] == renders["B_REPEAT"]["file_sha256"] and renders["A"].get("parameter_hash") == renders["B_REPEAT"].get("parameter_hash")
        raw_seed_changes = renders["A"]["file_sha256"] != renders["C_CHANGED_MUSIC_SEED"]["file_sha256"]
        if not (raw_repeat and raw_seed_changes):
            raise E4A4Error("D3 V5 raw audio determinism/music-seed control failed")

        print("E4A4_STAGE=D3_3_MASTERING_AND_QA", flush=True)
        final_audio, final_audio_metrics, masters = {}, {}, {}
        for label in labels:
            raw = raw_paths[label]
            qa_window = run_root / f"{label}_D3_3_QA_WINDOW.wav"
            e3._run([ffmpeg, "-hide_banner", "-nostats", "-y", "-stream_loop", "-1", "-i", str(raw), "-t", "30", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(qa_window)], stage=f"d3_3_qa_window_{label.lower()}", evidence_root=run_root)
            master = run_root / f"{label}_D3_3_MASTER_30S.wav"
            e3._run([ffmpeg, "-hide_banner", "-nostats", "-y", "-i", str(qa_window), "-filter_complex", "loudnorm=I=-14:TP=-1:LRA=7:print_format=summary", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(master)], stage=f"d3_3_loudnorm_{label.lower()}", evidence_root=run_root)
            master_qa = e3._master_qa(master, ffmpeg, ffprobe, run_root, label)
            if not master_qa.get("overall_pass"):
                raise E4A4Error(f"D3.3 30-second master QA failed for {label}")
            delivery = run_root / f"{label}_D3_3_MASTER_{duration:.3f}s.wav"
            e3._run([ffmpeg, "-hide_banner", "-nostats", "-y", "-i", str(master), "-af", f"atrim=duration={duration:.6f},asetpts=PTS-STARTPTS", "-t", f"{duration:.6f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(delivery)], stage=f"d3_3_trim_{label.lower()}", evidence_root=run_root)
            metrics = e3._audio_metrics(delivery, ffmpeg, ffprobe, run_root, f"delivery_audio_{label.lower()}")
            if metrics.get("codec") != "pcm_s16le" or metrics.get("sample_rate_hz") != 48000 or metrics.get("channels") != 2 or abs(metrics.get("duration_seconds", 0.0) - duration) > 0.03 or not metrics.get("non_silent"):
                raise E4A4Error(f"D3.3 delivery master QA failed for {label}")
            final_audio[label], final_audio_metrics[label], masters[label] = delivery, metrics, master_qa
        masters_repeat = final_audio_metrics["A"]["sha256"] == final_audio_metrics["B_REPEAT"]["sha256"]
        masters_seed_changes = final_audio_metrics["A"]["sha256"] != final_audio_metrics["C_CHANGED_MUSIC_SEED"]["sha256"]
        if not (masters_repeat and masters_seed_changes):
            raise E4A4Error("D3.3 delivery mastering determinism/music-seed control failed")

        print("E4A4_STAGE=FFMPEG_MUX_AND_FFPROBE_QA", flush=True)
        muxed, mux_qa, mux_audio_qa = {}, {}, {}
        for label in labels:
            out = run_root / f"CHALLENGE_004_C11C_REVIEW_BASE_WITH_AUDIO_{label}.mp4"
            e3._run([ffmpeg, "-hide_banner", "-v", "error", "-y", "-i", str(base_video), "-i", str(final_audio[label]), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", str(out)], stage=f"ffmpeg_mux_{label.lower()}", evidence_root=run_root)
            pr = e3._run([ffprobe, "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(out)], stage=f"final_ffprobe_{label.lower()}", evidence_root=run_root)
            probe = json.loads(pr.stdout)
            mux_qa[label] = e3._validate_mux_probe(probe, label=label, expected_video_duration=duration, expected_video_frames=frames, expected_video_fps=30.0)
            mux_audio_qa[label] = e3._audio_metrics(out, ffmpeg, ffprobe, run_root, f"muxed_audio_{label.lower()}")
            if mux_audio_qa[label].get("codec") != "aac" or mux_audio_qa[label].get("sample_rate_hz") != 48000 or mux_audio_qa[label].get("channels") != 2 or not mux_audio_qa[label].get("non_silent"):
                raise E4A4Error(f"Final mux audio QA failed for {label}")
            muxed[label] = out

        print("E4A4_STAGE=VERIFYING_VIDEO_IDENTITY_AND_AUDIO_SEED_ISOLATION", flush=True)
        source_video_hash = e3._extract_video_bitstream(base_video, run_root / "source_video.h264", ffmpeg, run_root, "source")
        mux_video_hashes = {label: e3._extract_video_bitstream(path, run_root / f"{label.lower()}_video.h264", ffmpeg, run_root, label.lower()) for label, path in muxed.items()}
        video_identical = all(v == source_video_hash for v in mux_video_hashes.values())
        decoded_hashes = {label: e3._extract_decoded_audio(path, run_root / f"{label.lower()}_decoded_audio.s16le", ffmpeg, run_root, label.lower()) for label, path in muxed.items()}
        decoded_repeat = decoded_hashes["A"] == decoded_hashes["B_REPEAT"]
        decoded_seed_changes = decoded_hashes["A"] != decoded_hashes["C_CHANGED_MUSIC_SEED"]
        if not (video_identical and decoded_repeat and decoded_seed_changes):
            raise E4A4Error("Final mux failed source-video identity or decoded-audio repeatability/seed-isolation")

        receipt.update({
            "status": "PASS_ISOLATED_E4A4_CHALLENGE_AUDIO_MUX_TEST_ONLY",
            "result": "PASS",
            "source_identity": source,
            "source_pins": source_pins,
            "d3_source_pins": d3_pins["sources"],
            "music_contract_sha256": d3_pins["contract_sha256"],
            "tools": versions,
            "test_parameters": {
                "family": "challenges", "variant_id": "CHALLENGE_004", "gameplay_seed": GAMEPLAY_SEED,
                "music_seed_A_B": MUSIC_SEED_A, "music_seed_C": MUSIC_SEED_C,
                "independent_seed_domains": True, "variation_index": VARIATION_INDEX,
                "style_profile_id": "challenge_8bit_v1", "style_profile_version": "1.0",
                "tempo_bpm": TEMPO_BPM_FIXTURE, "tempo_role": "HISTORICAL_D9_2_PILOT_FIXTURE_NOT_PRODUCT_DEFAULT",
                "duration_seconds": duration, "duration_source": "FFPROBE_450_FRAMES_DIVIDED_BY_30FPS",
                "fullframe_d_compositor_embedded_in_mp4": False,
                "d_layer_pngs_are_separate_e4a3_samples": True,
            },
            "e1_intents": {label: {"intent_sha256": item["intent"]["intent_sha256"], "request_id": item["intent"]["request"]["request_id"], "validation_status": item["validation"]["status"], "request_origin": item["intent"]["request_origin"], "gameplay_seed": item["intent"]["seed_domains"]["gameplay"]["value"], "music_seed": item["intent"]["seed_domains"]["music"]["value"], "audio_enabled": item["intent"]["delivery"]["audio_enabled"], "dispatch_authorized": item["intent"]["execution_boundary"]["dispatch_authorized"], "raw_request_sha256": item["raw_request_sha256"]} for label, item in intents.items()},
            "d3_v5": {"renders": renders, "raw_repeatable": raw_repeat, "changed_music_seed_changes_raw_wav": raw_seed_changes},
            "d3_3_mastering": {"by_label": {label: {"qa": masters[label], "delivery_master": final_audio_metrics[label]} for label in labels}, "delivery_repeatable": masters_repeat, "changed_music_seed_changes_delivery_master": masters_seed_changes},
            "mux": {label: {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path), "ffprobe": mux_qa[label], "audio_quality": mux_audio_qa[label]} for label, path in muxed.items()},
            "invariants": {"source_video_h264_stream_identical_in_all_muxes": video_identical, "source_video_h264_sha256": source_video_hash, "mux_video_h264_sha256": mux_video_hashes, "decoded_aac_A_equals_B": decoded_repeat, "decoded_aac_A_differs_C": decoded_seed_changes, "decoded_aac_sha256": decoded_hashes, "gameplay_video_not_rerendered": True, "C11C_generators_unchanged": True, "D_layer_not_embedded": True},
            "governance": {"renderer": False, "dispatch": False, "production_media": False, "test_media": True, "d4_8": "BLOCKED", "d9_10": "PREPARE_ONLY", "d10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE"},
            "human_review": {"operator_video_review": "PENDING", "operator_audio_listening_review": "PENDING", "layout_approval": "NOT_GRANTED", "instruction": "Review A/B/C for audible artefacts and sync; review the separate E4A.3 PNGs for visual overlap. Do not infer D overlays are present in these MP4s."},
        })
        report = {
            "schema": "C11E-E4A4-CHALLENGE-AUDIO-MUX-REPORT-V1", "schema_version": "1.0", "status": receipt["status"],
            "run_id": run_id, "summary": "D3 V5 / D3.3 / FFmpeg mux and FFprobe verified on the immutable E4A.2 normalized CHALLENGE_004 review video; no D overlay is embedded and no layout is approved.",
            "source": source, "test_parameters": receipt["test_parameters"], "mux": receipt["mux"],
            "quality_checks": {"d3_v5_raw_repeatability": raw_repeat, "music_seed_changes_raw_wav": raw_seed_changes, "d3_3_master_repeatability": masters_repeat, "music_seed_changes_delivery_master": masters_seed_changes, "source_h264_identical": video_identical, "decoded_audio_repeatability": decoded_repeat, "decoded_audio_changes_with_music_seed": decoded_seed_changes, "all_three_muxes_pass_ffprobe": True},
            "visual_boundary": {"fullframe_compositor_embedded": False, "layout_approval": "NOT_GRANTED", "e4a3_existing_hook_collision": True, "next_required_work": "Resolve D1.5/D1.1/D1.7 geometry and safe typography before any fullframe D composited audiovisual render."},
            "governance": receipt["governance"],
            "human_review": receipt["human_review"],
        }
        report_path = run_root / "C11E_E4A4_CHALLENGE_AUDIO_MUX_REPORT.json"
        write_json(report_path, report)
        receipt["report_sha256"] = sha256_file(report_path)
        write_json(run_root / "C11E_E4A4_CHALLENGE_AUDIO_MUX_RECEIPT.json", receipt)
        (run_root / "C11E_E4A4_CHALLENGE_AUDIO_MUX_RECEIPT.json.sha256").write_text(sha256_file(run_root / "C11E_E4A4_CHALLENGE_AUDIO_MUX_RECEIPT.json") + "  C11E_E4A4_CHALLENGE_AUDIO_MUX_RECEIPT.json\n", encoding="ascii")
        sums=[]
        for p in sorted(run_root.rglob("*")):
            if p.is_file() and p.name != "SHA256SUMS.txt":
                sums.append(f"{sha256_file(p)}  {p.relative_to(run_root).as_posix()}")
        (run_root / "SHA256SUMS.txt").write_text("\n".join(sums)+"\n",encoding="utf-8")
        zip_path = evidence_parent / f"{run_root.name}.zip"
        with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(run_root.rglob("*")):
                if p.is_file(): z.write(p, f"{run_root.name}/{p.relative_to(run_root).as_posix()}")
        zip_sha=sha256_file(zip_path)
        (zip_path.with_suffix(zip_path.suffix+".sha256")).write_text(f"{zip_sha}  {zip_path.name}\n",encoding="ascii")
        print(f"E4A4_EVIDENCE_DIR={run_root}", flush=True)
        print(f"E4A4_RECEIPT_SHA256={sha256_file(run_root / 'C11E_E4A4_CHALLENGE_AUDIO_MUX_RECEIPT.json')}", flush=True)
        print(f"E4A4_ZIP={zip_path}", flush=True)
        print(f"E4A4_ZIP_SHA256={zip_sha}", flush=True)
        print("C11E_E4A4_CHALLENGE_AUDIO_MUX=PASS_ISOLATED_TEST_ONLY", flush=True)
        return zip_path
    except Exception as exc:
        receipt["status"] = "BLOCKED"
        receipt["result"] = "FAIL"
        receipt["failure"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
        write_json(run_root / "C11E_E4A4_CHALLENGE_AUDIO_MUX_RECEIPT.json", receipt)
        (run_root / "FAILURE.txt").write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
        print(f"E4A4_FAILED stage output retained at {run_root}: {exc}", flush=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--base-run", type=Path, default=None)
    parser.add_argument("--compositor-run", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    base_run = args.base_run or (root / "artifacts/tests/c11e/e4a_real_body_pixel_review" / E4A2_RUN_ID)
    compositor_run = args.compositor_run or (root / "artifacts/tests/c11e/e4a_d_compositor_pixel_review" / E4A3_RUN_ID)
    run(root, base_run, compositor_run)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
