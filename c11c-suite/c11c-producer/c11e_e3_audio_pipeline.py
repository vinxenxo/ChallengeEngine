from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping


class C11EE3AudioPilotError(RuntimeError):
    """A fail-closed E3 test-pilot error."""


CONTRACT_REL = Path("definitions/c11e/music/C11E_E3_2_D3_V5_E1_MUSIC_CONTRACT_V1.json")
ENGINE_REL = Path("tools/c11d/d3/c11d_music_engine_v5.py")
SPEC_REL = Path("definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json")
PROFILE_REL = Path("definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json")
E1_SERVICE_DIR_REL = Path("c11c-suite/c11c-producer")
R4_EXPECTED_RECEIPT_SHA256 = "2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f"
R4_EXPECTED_VIDEO_SHA256 = "3d72e52cc7f7f8fc4b32c8719ab9800ba622e6069c7fa956526c108defce1afd"
R4_EXPECTED_VIDEO_BYTES = 195690
PILOT_TEMPO_BPM = 104.0  # D9.2 fixed pilot fixture only; never a global production default.
PILOT_VARIATION_INDEX = 0
PILOT_GAMEPLAY_SEED = 193847
PILOT_MUSIC_SEED = 840001
PILOT_CHANGED_MUSIC_SEED = 840002
D9_2_AV_DRIFT_TOLERANCE_SECONDS = 0.15


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve_tool(name: str) -> str:
    candidates = [name]
    if os.name == "nt" and not name.lower().endswith(".exe"):
        candidates.insert(0, name + ".exe")
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise C11EE3AudioPilotError(f"Required media tool not found on PATH: {name}")


def _run(
    argv: list[str],
    *,
    stage: str,
    evidence_root: Path,
    timeout_seconds: int = 180,
) -> subprocess.CompletedProcess[str]:
    evidence_root.mkdir(parents=True, exist_ok=True)
    command_record = {"stage": stage, "argv": [str(x) for x in argv], "cwd": str(evidence_root)}
    _write_json(evidence_root / f"{stage}.command.json", command_record)
    try:
        result = subprocess.run(
            [str(x) for x in argv],
            cwd=str(evidence_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except Exception as exc:
        (evidence_root / f"{stage}.stdout.log").write_text("", encoding="utf-8")
        (evidence_root / f"{stage}.stderr.log").write_text(str(exc) + "\n", encoding="utf-8")
        (evidence_root / f"{stage}.exitcode.txt").write_text("START_OR_TIMEOUT_ERROR\n", encoding="ascii")
        raise C11EE3AudioPilotError(f"{stage} could not execute: {exc}") from exc
    (evidence_root / f"{stage}.stdout.log").write_text(result.stdout or "", encoding="utf-8")
    (evidence_root / f"{stage}.stderr.log").write_text(result.stderr or "", encoding="utf-8")
    (evidence_root / f"{stage}.exitcode.txt").write_text(str(result.returncode) + "\n", encoding="ascii")
    if result.returncode != 0:
        raise C11EE3AudioPilotError(
            f"{stage} failed with exit code {result.returncode}; see {stage}.stderr.log"
        )
    return result


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise C11EE3AudioPilotError(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise C11EE3AudioPilotError(f"Expected a JSON object: {path}")
    return value


def _load_engine(path: Path):
    spec = importlib.util.spec_from_file_location("c11e_e3_d3_music_engine_v5", path)
    if spec is None or spec.loader is None:
        raise C11EE3AudioPilotError(f"Cannot load reviewed D3 V5 engine: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _verify_source_pins(root: Path) -> dict[str, Any]:
    contract_path = root / CONTRACT_REL
    contract = _load_json(contract_path)
    if contract.get("schema") != "C11E-E3.2-D3-V5-E1-MUSIC-CONTRACT":
        raise C11EE3AudioPilotError("E3.2 music contract identity mismatch")
    if contract.get("schema_version") != "1.0":
        raise C11EE3AudioPilotError("Unsupported E3.2 music contract schema version")
    expected = {
        ENGINE_REL.as_posix(): contract["engine"]["sha256"],
        SPEC_REL.as_posix(): contract["engine"]["spec_sha256"],
        PROFILE_REL.as_posix(): contract["style_profile"]["sha256"],
    }
    observed: dict[str, Any] = {}
    for relative, wanted in expected.items():
        target = root / Path(*relative.split("/"))
        if not target.is_file():
            raise C11EE3AudioPilotError(f"Pinned source missing: {relative}")
        actual = sha256_file(target)
        if actual != wanted:
            raise C11EE3AudioPilotError(f"Pinned source SHA-256 mismatch: {relative}")
        observed[relative] = {"sha256": actual, "bytes": target.stat().st_size}
    return {"contract": contract, "sources": observed, "contract_sha256": sha256_file(contract_path)}


def _validate_e1_intent(intent: Mapping[str, Any], root: Path) -> dict[str, Any]:
    service_dir = root / E1_SERVICE_DIR_REL
    if str(service_dir) not in sys.path:
        sys.path.insert(0, str(service_dir))
    try:
        from c11e_production_service import validate_c11e_production_intent

        validation = validate_c11e_production_intent(dict(intent), root)
    except Exception as exc:
        raise C11EE3AudioPilotError(f"E1 intent validation failed: {exc}") from exc
    if validation.get("status") != "PASS_E1_PREPARATION_ONLY":
        raise C11EE3AudioPilotError("E1 intent did not validate as preparation-only")
    if intent.get("schema") != "C11-E-PRODUCTION-INTENT-V1" or intent.get("schema_version") != "1.1":
        raise C11EE3AudioPilotError("Unexpected E1 intent schema/version")
    if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise C11EE3AudioPilotError("E1 intent is not in the expected preparation-only state")
    request = intent.get("request", {})
    selection = request.get("selection", {})
    if request.get("content_type") != "challenges" or selection.get("variant_id") != "CHALLENGE_001":
        raise C11EE3AudioPilotError("This E3 pilot only accepts Challenge / CHALLENGE_001")
    if intent.get("delivery", {}).get("resolved_profile_id") != "REVIEW_720":
        raise C11EE3AudioPilotError("E3 R4 pilot requires REVIEW_720")
    if intent.get("delivery", {}).get("audio_enabled") is not True:
        raise C11EE3AudioPilotError("E3 pilot request has audio disabled; engine invocation is forbidden")
    domains = intent.get("seed_domains", {})
    gameplay_seed = domains.get("gameplay", {}).get("value")
    music_seed = domains.get("music", {}).get("value")
    if gameplay_seed != PILOT_GAMEPLAY_SEED:
        raise C11EE3AudioPilotError(
            f"R4 video provenance requires gameplay seed {PILOT_GAMEPLAY_SEED}; received {gameplay_seed}"
        )
    if music_seed != PILOT_MUSIC_SEED:
        raise C11EE3AudioPilotError(
            f"The fixed D9.2 pilot fixture requires music seed {PILOT_MUSIC_SEED}; received {music_seed}"
        )
    if domains.get("independent_domains") is not True:
        raise C11EE3AudioPilotError("E1 did not confirm independent gameplay/music seed domains")
    music = intent.get("music_contract", {})
    if music.get("status") != "PLANNED_NOT_RENDERED" or music.get("dispatchable") is not False:
        raise C11EE3AudioPilotError("E1 D3 V5 binding is not the expected non-dispatchable planning contract")
    if music.get("engine_invoked") is not False or music.get("audio_created") is not False:
        raise C11EE3AudioPilotError("E1 intent incorrectly claims prior engine execution/audio creation")
    engine_request = music.get("engine_request")
    if not isinstance(engine_request, Mapping):
        raise C11EE3AudioPilotError("E1 music engine request is missing")
    if engine_request.get("music_seed") != PILOT_MUSIC_SEED or engine_request.get("variation_index") != PILOT_VARIATION_INDEX:
        raise C11EE3AudioPilotError("E1 music seed/variation do not match the fixed E3 pilot case")
    return {
        "status": validation["status"],
        "request_id": request.get("request_id"),
        "request_origin": intent.get("request_origin"),
        "intent_sha256": intent.get("intent_sha256"),
        "request_hash": intent.get("identity", {}).get("request_hash"),
        "editorial_hash": intent.get("identity", {}).get("editorial_hash"),
        "plan_hash": intent.get("identity", {}).get("plan_hash"),
        "gameplay_seed": gameplay_seed,
        "music_seed": music_seed,
        "variation_index": engine_request.get("variation_index"),
    }


def _verify_r4_source(video: Path, receipt_path: Path, sidecar_path: Path, ffprobe: str, evidence_root: Path) -> dict[str, Any]:
    for path in (video, receipt_path, sidecar_path):
        if not path.is_file():
            raise C11EE3AudioPilotError(f"Required R4 fixture is missing: {path}")
    receipt_sha = sha256_file(receipt_path)
    if receipt_sha != R4_EXPECTED_RECEIPT_SHA256:
        raise C11EE3AudioPilotError("R4 receipt SHA-256 does not match the accepted evidence pin")
    sidecar = sidecar_path.read_text(encoding="utf-8-sig").strip()
    if not sidecar.startswith(receipt_sha):
        raise C11EE3AudioPilotError("R4 receipt checksum sidecar mismatch")
    video_sha = sha256_file(video)
    if video_sha != R4_EXPECTED_VIDEO_SHA256 or video.stat().st_size != R4_EXPECTED_VIDEO_BYTES:
        raise C11EE3AudioPilotError("R4 A video fixture SHA-256 or size mismatch")
    receipt = _load_json(receipt_path)
    if receipt.get("schema") != "C11E-E2-CHALLENGE-TITLE-AB-RENDER-RECEIPT-V1":
        raise C11EE3AudioPilotError("Unexpected R4 receipt schema")
    if receipt.get("request_id") != "C11E-E2-CH001-AB-20261101-V9-R4":
        raise C11EE3AudioPilotError("Unexpected R4 request identity")
    if receipt.get("status") != "E2_AUTOMATED_TITLE_TO_PIXELS_AND_GAMEPLAY_INVARIANCE_PASS_HUMAN_REVIEW_PENDING":
        raise C11EE3AudioPilotError("R4 source receipt is not the accepted bounded E2 result")
    if receipt.get("release_authority") != "NONE" or receipt.get("baseline_promotion") is not False:
        raise C11EE3AudioPilotError("R4 source receipt crosses release/promotion authority")
    row = next((item for item in receipt.get("render_rows", []) if item.get("label") == "A"), None)
    if not isinstance(row, Mapping) or row.get("final_mp4_sha256") != video_sha:
        raise C11EE3AudioPilotError("R4 A video is not the artifact referenced by the receipt")
    if receipt.get("seed_domains", {}).get("gameplay") != PILOT_GAMEPLAY_SEED:
        raise C11EE3AudioPilotError("R4 gameplay seed provenance mismatch")
    if receipt.get("delivery", {}).get("audio") != "NONE_E2":
        raise C11EE3AudioPilotError("R4 input is not a video-only E2 artifact")
    probe_run = _run(
        [ffprobe, "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(video)],
        stage="source_ffprobe",
        evidence_root=evidence_root,
    )
    try:
        probe = json.loads(probe_run.stdout)
    except Exception as exc:
        raise C11EE3AudioPilotError(f"Cannot parse source FFprobe JSON: {exc}") from exc
    streams = probe.get("streams", [])
    videos = [item for item in streams if item.get("codec_type") == "video"]
    audios = [item for item in streams if item.get("codec_type") == "audio"]
    if len(videos) != 1 or audios:
        raise C11EE3AudioPilotError("R4 source must have exactly one video stream and no audio stream")
    stream = videos[0]
    if int(stream.get("width", 0)) != 720 or int(stream.get("height", 0)) != 1280:
        raise C11EE3AudioPilotError("R4 source dimensions are not 720x1280")
    if stream.get("codec_name") != "h264":
        raise C11EE3AudioPilotError("R4 source codec is not H.264")
    fps_text = stream.get("avg_frame_rate") or stream.get("r_frame_rate")
    try:
        fps = float(Fraction(str(fps_text)))
        frames = int(stream.get("nb_read_frames"))
    except Exception as exc:
        raise C11EE3AudioPilotError("R4 source does not provide a valid frame-rate/frame-count pair") from exc
    if abs(fps - 30.0) > 0.0001 or frames != 270:
        raise C11EE3AudioPilotError(f"R4 source timing mismatch: fps={fps_text}; frames={frames}")
    derived_duration = frames / fps
    source_reported_duration = float(stream.get("duration") or probe.get("format", {}).get("duration") or 0.0)
    if abs(source_reported_duration - derived_duration) > 0.05:
        raise C11EE3AudioPilotError(
            f"R4 source duration disagrees with frame-derived duration: {source_reported_duration} vs {derived_duration}"
        )
    return {
        "path": str(video),
        "bytes": video.stat().st_size,
        "sha256": video_sha,
        "receipt_path": str(receipt_path),
        "receipt_sha256": receipt_sha,
        "request_id": receipt["request_id"],
        "gameplay_seed": receipt["seed_domains"]["gameplay"],
        "music_seed_recorded_but_unused_in_e2": receipt["seed_domains"]["music"],
        "source_fps": fps,
        "source_frames": frames,
        "derived_duration_seconds": derived_duration,
        "container_duration_seconds": float(probe.get("format", {}).get("duration") or 0.0),
        "codec": stream.get("codec_name"),
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "video_stream_count": len(videos),
        "audio_stream_count": len(audios),
        "r4_human_review_recorded_at_run_time": receipt.get("human_visual_review"),
        "r4_formal_closure_is_separate_historical_authority": True,
    }


def _parse_metric(text: str, pattern: str) -> float | None:
    found = re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not found:
        return None
    try:
        return float(found[-1])
    except (TypeError, ValueError):
        return None


def _audio_metrics(path: Path, ffmpeg: str, ffprobe: str, evidence_root: Path, prefix: str) -> dict[str, Any]:
    probe_run = _run(
        [ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        stage=f"{prefix}_ffprobe",
        evidence_root=evidence_root,
    )
    probe = json.loads(probe_run.stdout)
    audio_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
    if len(audio_streams) != 1:
        raise C11EE3AudioPilotError(f"{prefix} must contain exactly one audio stream")
    stream = audio_streams[0]
    vol = _run(
        [ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", os.devnull],
        stage=f"{prefix}_volumedetect",
        evidence_root=evidence_root,
    )
    metrics_text = (vol.stdout or "") + "\n" + (vol.stderr or "")
    max_db = _parse_metric(metrics_text, r"max_volume:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*dB")
    mean_db = _parse_metric(metrics_text, r"mean_volume:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*dB")
    if max_db is None or mean_db is None or max_db <= -90 or mean_db <= -90:
        raise C11EE3AudioPilotError(f"{prefix} is silent or FFmpeg volume metrics are unavailable")
    return {
        "codec": stream.get("codec_name"),
        "sample_rate_hz": int(stream.get("sample_rate", 0)),
        "channels": int(stream.get("channels", 0)),
        "duration_seconds": float(stream.get("duration") or probe.get("format", {}).get("duration") or 0.0),
        "max_sample_db": max_db,
        "mean_volume_db": mean_db,
        "non_silent": True,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
    }


def _master_qa(master: Path, ffmpeg: str, ffprobe: str, run_root: Path, label: str) -> dict[str, Any]:
    prefix = f"master_{label.lower()}"
    master_metrics = _audio_metrics(master, ffmpeg, ffprobe, run_root, prefix)
    ebur = _run(
        [ffmpeg, "-hide_banner", "-nostats", "-i", str(master), "-filter_complex", "ebur128=peak=true", "-f", "null", os.devnull],
        stage=f"{prefix}_ebur128",
        evidence_root=run_root,
    )
    ebur_text = (ebur.stdout or "") + "\n" + (ebur.stderr or "")
    integrated_lufs = _parse_metric(ebur_text, r"I:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*LUFS")
    true_peak_db = _parse_metric(ebur_text, r"Peak:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*dBFS")
    if integrated_lufs is None or true_peak_db is None:
        raise C11EE3AudioPilotError("Could not parse D3.3 integrated loudness/true peak from FFmpeg")
    mono = run_root / "master_mono_check.wav"
    _run(
        [ffmpeg, "-hide_banner", "-v", "error", "-y", "-i", str(master), "-ac", "1", "-c:a", "pcm_s16le", str(mono)],
        stage=f"{prefix}_mono_downmix",
        evidence_root=run_root,
    )
    mono_metrics = _audio_metrics(mono, ffmpeg, ffprobe, run_root, f"{prefix}_mono")
    sample_rate_ok = master_metrics["sample_rate_hz"] >= 44100
    container_ok = (
        master_metrics["codec"] == "pcm_s16le"
        and master_metrics["sample_rate_hz"] == 48000
        and master_metrics["channels"] == 2
        and master_metrics["duration_seconds"] >= 20.0
    )
    loudness_ok = -18.0 <= integrated_lufs <= -12.0
    true_peak_ok = true_peak_db <= -1.0
    hard_clip_ok = master_metrics["max_sample_db"] < 0.0
    mono_ok = mono_metrics["max_sample_db"] < 0.0 and -60.0 <= mono_metrics["mean_volume_db"] <= -3.0
    passed = container_ok and sample_rate_ok and loudness_ok and true_peak_ok and hard_clip_ok and mono_ok
    return {
        "status": "PASS" if passed else "FAIL",
        "method": "D3.3 deterministic 30-second repeated measurement window + FFmpeg loudnorm",
        "targets": {"integrated_lufs": -14.0, "true_peak_dbfs": -1.0, "lra": 7.0, "sample_rate_hz": 48000, "channels": 2},
        "measured": {
            "integrated_lufs": integrated_lufs,
            "true_peak_dbfs": true_peak_db,
            "max_sample_db": master_metrics["max_sample_db"],
            "mean_volume_db": master_metrics["mean_volume_db"],
            "mono_max_sample_db": mono_metrics["max_sample_db"],
            "mono_mean_volume_db": mono_metrics["mean_volume_db"],
            "duration_seconds": master_metrics["duration_seconds"],
            "sample_rate_hz": master_metrics["sample_rate_hz"],
            "channels": master_metrics["channels"],
            "codec": master_metrics["codec"],
        },
        "checks": {
            "container": container_ok,
            "sample_rate": sample_rate_ok,
            "integrated_loudness_range": loudness_ok,
            "true_peak": true_peak_ok,
            "no_hard_clipping": hard_clip_ok,
            "mono_compatibility_and_audibility": mono_ok,
        },
        "mono_artifact": {"sha256": mono_metrics["sha256"], "bytes": mono_metrics["bytes"]},
        "overall_pass": passed,
    }


def _extract_video_bitstream(video: Path, target: Path, ffmpeg: str, run_root: Path, label: str) -> str:
    _run(
        [ffmpeg, "-hide_banner", "-v", "error", "-i", str(video), "-map", "0:v:0", "-c:v", "copy", "-f", "h264", str(target)],
        stage=f"video_stream_extract_{label}",
        evidence_root=run_root,
    )
    return sha256_file(target)


def _extract_decoded_audio(video: Path, target: Path, ffmpeg: str, run_root: Path, label: str) -> str:
    _run(
        [ffmpeg, "-hide_banner", "-v", "error", "-i", str(video), "-map", "0:a:0", "-f", "s16le", "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2", str(target)],
        stage=f"decoded_audio_extract_{label}",
        evidence_root=run_root,
    )
    return sha256_file(target)


def run_e3_audio_pilot(
    *,
    project_root: Path | str,
    e1_intent_path: Path | str,
    source_video_path: Path | str,
    source_receipt_path: Path | str,
    source_receipt_sha_path: Path | str,
    output_root: Path | str,
    operator_gui_invoked: bool = False,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    intent_path = Path(e1_intent_path).resolve()
    source_video = Path(source_video_path).resolve()
    source_receipt = Path(source_receipt_path).resolve()
    source_sidecar = Path(source_receipt_sha_path).resolve()
    out = Path(output_root).resolve()
    if out.exists():
        raise C11EE3AudioPilotError(f"Output root already exists; overwrite is forbidden: {out}")
    if not root.is_dir():
        raise C11EE3AudioPilotError(f"Project root does not exist: {root}")
    if not intent_path.is_file():
        raise C11EE3AudioPilotError(f"E1 intent file is missing: {intent_path}")
    out.mkdir(parents=True, exist_ok=False)
    run_root = out
    receipt_path = run_root / "C11E_E3_AUDIO_PILOT_RECEIPT.json"
    receipt: dict[str, Any] = {
        "schema": "C11E-E3-CHALLENGE-AUDIO-PILOT-RECEIPT-V1",
        "status": "RUNNING",
        "request_scope": "ONE_R4_CHALLENGE_001_VIDEO_FIXTURE_THREE_MUSIC_RENDER_CASES",
        "project_root": str(root),
        "output_root": str(run_root),
        "release_authority": "NONE",
        "baseline_promotion": False,
        "production_product_created": False,
        "gameplay_renderer_invoked": False,
        "gameplay_rerendered": False,
        "c11c_generator_modified": False,
        "core_audio_modified": False,
        "d9_governance_modified": False,
        "ffmpeg_mux_invoked": False,
    }
    try:
        ffmpeg = _resolve_tool("ffmpeg")
        ffprobe = _resolve_tool("ffprobe")
        versions = {}
        for label, executable in (("ffmpeg", ffmpeg), ("ffprobe", ffprobe)):
            version_run = _run([executable, "-version"], stage=f"{label}_version", evidence_root=run_root, timeout_seconds=30)
            versions[label] = (version_run.stdout or "").splitlines()[0] if version_run.stdout else "UNKNOWN"

        pin_report = _verify_source_pins(root)
        intent = _load_json(intent_path)
        e1 = _validate_e1_intent(intent, root)
        source = _verify_r4_source(source_video, source_receipt, source_sidecar, ffprobe, run_root)

        if source["gameplay_seed"] != e1["gameplay_seed"]:
            raise C11EE3AudioPilotError("E1 gameplay seed does not identify the R4 visual source")
        duration = float(source["derived_duration_seconds"])
        tempo = PILOT_TEMPO_BPM
        variation = PILOT_VARIATION_INDEX
        spec_path = root / SPEC_REL
        profile_path = root / PROFILE_REL
        engine_path = root / ENGINE_REL
        engine = _load_engine(engine_path)
        spec = _load_json(spec_path)
        profile = _load_json(profile_path)
        request_base = {
            "style_profile_id": "challenge_8bit_v1",
            "style_profile_version": "1.0",
            "tempo_bpm": tempo,
            "duration_seconds": duration,
            "variation_index": variation,
        }
        seeds = (PILOT_MUSIC_SEED, PILOT_MUSIC_SEED, PILOT_CHANGED_MUSIC_SEED)
        labels = ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED")
        renders: dict[str, dict[str, Any]] = {}
        raw_paths: dict[str, Path] = {}
        for label, seed in zip(labels, seeds):
            raw_path = run_root / f"{label}_raw.wav"
            engine_request = dict(request_base, music_seed=seed)
            render_record = engine.render(engine_request, spec, profile, raw_path)
            if render_record.get("output_hash") != sha256_file(raw_path):
                raise C11EE3AudioPilotError(f"D3 V5 engine output hash mismatch for render {label}")
            renders[label] = render_record
            raw_paths[label] = raw_path
        same_repeat_hash = renders["A"]["output_hash"] == renders["B_REPEAT"]["output_hash"]
        same_repeat_parameters = renders["A"]["parameter_hash"] == renders["B_REPEAT"]["parameter_hash"]
        changed_seed_changes_wav = renders["A"]["output_hash"] != renders["C_CHANGED_MUSIC_SEED"]["output_hash"]
        if not (same_repeat_hash and same_repeat_parameters and changed_seed_changes_wav):
            raise C11EE3AudioPilotError("D3 V5 repeatability/changed-music-seed comparison failed")

        # D3.3 requires a deterministic 30-second measurement window for each seed.
        # That QA window is never muxed untrimmed; a separate video-duration master is created below.
        final_audio_paths: dict[str, Path] = {}
        final_audio_metrics: dict[str, Any] = {}
        master_qa_by_label: dict[str, Any] = {}
        for label in ("A", "B_REPEAT", "C_CHANGED_MUSIC_SEED"):
            # Each seed receives its own D3.3 delivery master, preserving its raw WAV.
            source_raw = raw_paths[label]
            per_window = run_root / f"{label}_D3_3_QA_WINDOW.wav"
            _run(
                [ffmpeg, "-hide_banner", "-nostats", "-y", "-stream_loop", "-1", "-i", str(source_raw), "-t", "30", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(per_window)],
                stage=f"d3_3_build_qa_window_{label.lower()}",
                evidence_root=run_root,
            )
            per_master = run_root / f"{label}_D3_3_MASTER_30S.wav"
            _run(
                [ffmpeg, "-hide_banner", "-nostats", "-y", "-i", str(per_window), "-filter_complex", "loudnorm=I=-14:TP=-1:LRA=7:print_format=summary", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(per_master)],
                stage=f"d3_3_loudnorm_mastering_{label.lower()}",
                evidence_root=run_root,
            )
            final_qa_path = run_root / f"{label}_D3_3_MASTER_{duration:.3f}s.wav"
            master_qa_by_label[label] = _master_qa(per_master, ffmpeg, ffprobe, run_root, label)
            if not master_qa_by_label[label]["overall_pass"]:
                raise C11EE3AudioPilotError(f"D3.3 mastering QA failed for {label}")
            _run(
                [ffmpeg, "-hide_banner", "-nostats", "-y", "-i", str(per_master), "-af", f"atrim=duration={duration:.6f},asetpts=PTS-STARTPTS", "-t", f"{duration:.6f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(final_qa_path)],
                stage=f"d3_3_trim_delivery_audio_{label.lower()}",
                evidence_root=run_root,
            )
            metrics = _audio_metrics(final_qa_path, ffmpeg, ffprobe, run_root, f"final_audio_{label.lower()}")
            if metrics["codec"] != "pcm_s16le" or metrics["sample_rate_hz"] != 48000 or metrics["channels"] != 2:
                raise C11EE3AudioPilotError(f"Final-duration master format mismatch for {label}")
            if abs(metrics["duration_seconds"] - duration) > 0.03 or metrics["max_sample_db"] >= 0.0:
                raise C11EE3AudioPilotError(f"Final-duration master timing/clipping check failed for {label}")
            final_audio_paths[label] = final_qa_path
            final_audio_metrics[label] = metrics
        repeat_master_identical = (
            final_audio_metrics["A"]["sha256"] == final_audio_metrics["B_REPEAT"]["sha256"]
        )
        changed_seed_changes_master = (
            final_audio_metrics["A"]["sha256"] != final_audio_metrics["C_CHANGED_MUSIC_SEED"]["sha256"]
        )
        if not (repeat_master_identical and changed_seed_changes_master):
            raise C11EE3AudioPilotError("D3.3 final-duration mastering repeatability/seed control failed")

        muxed: dict[str, Path] = {}
        final_probes: dict[str, Any] = {}
        for label in labels:
            final_mp4 = run_root / f"CHALLENGE_001_R4_AUDIO_{label}.mp4"
            receipt["ffmpeg_mux_invoked"] = True
            _run(
                [ffmpeg, "-hide_banner", "-v", "error", "-y", "-i", str(source_video), "-i", str(final_audio_paths[label]), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", str(final_mp4)],
                stage=f"ffmpeg_mux_{label.lower()}",
                evidence_root=run_root,
            )
            probe_run = _run(
                [ffprobe, "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(final_mp4)],
                stage=f"final_ffprobe_{label.lower()}",
                evidence_root=run_root,
            )
            probe = json.loads(probe_run.stdout)
            videos = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
            audios = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
            if len(videos) != 1 or len(audios) != 1:
                raise C11EE3AudioPilotError(f"Final mux {label} must contain exactly one video and one audio stream")
            v, a = videos[0], audios[0]
            if (int(v.get("width", 0)), int(v.get("height", 0))) != (720, 1280):
                raise C11EE3AudioPilotError(f"Final mux {label} video dimensions changed")
            if v.get("codec_name") != "h264" or int(v.get("nb_read_frames", 0)) != 270:
                raise C11EE3AudioPilotError(f"Final mux {label} video codec/frame-count changed")
            if abs(float(Fraction(str(v.get("avg_frame_rate", "0/1")))) - 30.0) > 0.0001:
                raise C11EE3AudioPilotError(f"Final mux {label} video FPS changed")
            if a.get("codec_name") != "aac" or int(a.get("sample_rate", 0)) != 48000 or int(a.get("channels", 0)) != 2:
                raise C11EE3AudioPilotError(f"Final mux {label} audio codec/rate/channel layout mismatch")
            video_duration = float(v.get("duration") or probe.get("format", {}).get("duration") or 0.0)
            audio_duration = float(a.get("duration") or 0.0)
            av_drift = abs(video_duration - audio_duration)
            if av_drift > D9_2_AV_DRIFT_TOLERANCE_SECONDS:
                raise C11EE3AudioPilotError(f"Final mux {label} A/V duration drift {av_drift:.6f}s exceeds 0.15s")
            final_probes[label] = {
                "path": str(final_mp4),
                "bytes": final_mp4.stat().st_size,
                "sha256": sha256_file(final_mp4),
                "video": {
                    "codec": v.get("codec_name"), "profile": v.get("profile"),
                    "width": int(v["width"]), "height": int(v["height"]),
                    "avg_frame_rate": v.get("avg_frame_rate"), "frames": int(v["nb_read_frames"]),
                    "duration_seconds": video_duration,
                },
                "audio": {
                    "codec": a.get("codec_name"), "sample_rate_hz": int(a["sample_rate"]),
                    "channels": int(a["channels"]), "channel_layout": a.get("channel_layout"),
                    "duration_seconds": audio_duration,
                },
                "av_duration_drift_seconds": av_drift,
                "video_stream_count": len(videos), "audio_stream_count": len(audios),
            }
            muxed[label] = final_mp4

        source_video_bitstream = _extract_video_bitstream(source_video, run_root / "source_video.h264", ffmpeg, run_root, "source")
        output_video_bitstreams = {
            label: _extract_video_bitstream(path, run_root / f"{label.lower()}_video.h264", ffmpeg, run_root, label.lower())
            for label, path in muxed.items()
        }
        video_streams_unchanged = all(value == source_video_bitstream for value in output_video_bitstreams.values())
        if not video_streams_unchanged:
            raise C11EE3AudioPilotError("At least one mux changed the H.264 video elementary stream")

        decoded_audio_paths = {label: run_root / f"{label.lower()}_decoded_audio.s16le" for label in labels}
        decoded_audio_hashes = {
            label: _extract_decoded_audio(muxed[label], decoded_audio_paths[label], ffmpeg, run_root, label.lower())
            for label in labels
        }
        repeat_audio_identical = decoded_audio_hashes["A"] == decoded_audio_hashes["B_REPEAT"]
        changed_seed_changes_decoded_audio = decoded_audio_hashes["A"] != decoded_audio_hashes["C_CHANGED_MUSIC_SEED"]
        if not (repeat_audio_identical and changed_seed_changes_decoded_audio):
            raise C11EE3AudioPilotError("AAC decoded-sample repeatability/changed-seed comparison failed")

        receipt.update({
            "status": "PASS_E3_CHALLENGE_AUDIO_PILOT_TEST_ONLY",
            "result": "PASS",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_video": source,
            "e1_intent": e1,
            "source_pins": pin_report["sources"],
            "music_engine_contract_sha256": pin_report["contract_sha256"],
            "tool_versions": versions,
            "music": {
                "engine_id": "c11d_music_engine_v5", "engine_version": "5.0",
                "style_profile_id": "challenge_8bit_v1", "style_profile_version": "1.0",
                "tempo_bpm": tempo, "tempo_role": "D9.2_FIXED_PILOT_FIXTURE_NOT_GLOBAL_DEFAULT",
                "duration_seconds": duration, "duration_source": "FFPROBE_VERIFIED_VIDEO_FRAMES_DIVIDED_BY_FRAME_RATE",
                "variation_index": variation, "music_seed_A_B": PILOT_MUSIC_SEED,
                "music_seed_C": PILOT_CHANGED_MUSIC_SEED,
                "raw_renders": renders,
                "repeat_raw_wav_identical": same_repeat_hash,
                "repeat_parameter_hash_identical": same_repeat_parameters,
                "changed_music_seed_changes_raw_wav": changed_seed_changes_wav,
                "final_duration_masters": final_audio_metrics,
                "repeat_final_master_identical": repeat_master_identical,
                "changed_music_seed_changes_final_master": changed_seed_changes_master,
            },
            "mastering": master_qa_by_label,
            "mux": {
                "video_codec_policy": "COPY",
                "audio_codec": "AAC",
                "audio_bit_rate": "192k",
                "audio_sample_rate_hz": 48000,
                "audio_channels": 2,
                "shortest": True,
                "faststart": True,
                "outputs": final_probes,
                "decoded_audio_sha256": decoded_audio_hashes,
                "repeat_decoded_audio_identical": repeat_audio_identical,
                "changed_music_seed_changes_decoded_audio": changed_seed_changes_decoded_audio,
                "source_video_h264_sha256": source_video_bitstream,
                "muxed_video_h264_sha256": output_video_bitstreams,
                "video_bitstream_unchanged_for_all_music_seeds": video_streams_unchanged,
                "duration_tolerance_seconds": D9_2_AV_DRIFT_TOLERANCE_SECONDS,
            },
            "operator_gui_invoked": bool(operator_gui_invoked),
            "execution_origin": "PRODUCER_GUI_QPROCESS" if operator_gui_invoked else "AUTOMATED_TEST_RUNNER",
            "cli_role": "WORKER_ONLY_GUI_IS_PRIMARY_OPERATOR_SURFACE",
        })
        _write_json(run_root / "C11E_E3_AUDIO_PILOT_RECEIPT.json", receipt)
        receipt["receipt_sha256"] = sha256_file(run_root / "C11E_E3_AUDIO_PILOT_RECEIPT.json")
        (run_root / "C11E_E3_AUDIO_PILOT_RECEIPT.json.sha256").write_text(
            receipt["receipt_sha256"] + "  C11E_E3_AUDIO_PILOT_RECEIPT.json\n", encoding="ascii"
        )
        _write_json(run_root / "C11E_E3_AUDIO_PILOT_RUN_SUMMARY.json", {
            "status": receipt["status"],
            "receipt": str(run_root / "C11E_E3_AUDIO_PILOT_RECEIPT.json"),
            "receipt_sha256": receipt["receipt_sha256"],
            "release_authority": "NONE",
        })
        return receipt
    except Exception as exc:
        receipt.update({
            "status": "FAIL_E3_AUDIO_PILOT_TEST_ONLY",
            "result": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        })
        _write_json(receipt_path, receipt)
        receipt_sha = sha256_file(receipt_path)
        (run_root / "C11E_E3_AUDIO_PILOT_RECEIPT.json.sha256").write_text(
            receipt_sha + "  C11E_E3_AUDIO_PILOT_RECEIPT.json\n", encoding="ascii"
        )
        raise
