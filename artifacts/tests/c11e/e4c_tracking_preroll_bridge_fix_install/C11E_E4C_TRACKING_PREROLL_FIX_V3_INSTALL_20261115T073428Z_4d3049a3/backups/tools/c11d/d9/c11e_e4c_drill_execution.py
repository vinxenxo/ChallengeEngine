#!/usr/bin/env python3
"""C11-E E4C Drill shared execution adapter (D-owned, isolated qualification).

This module consumes the canonical E1 intent for one Visual Drill request,
invokes the existing C11-C Drill producer silently, applies the already accepted
D-owned Qt post-composition consumer to every native frame, generates the
existing C11-C FAMILY_MUSIC_V4 track with request.music_seed (never gameplay
seed), and muxes/probes a REVIEW_720 qualification result. GUI and CLI invoke
this exact module; it is not a parallel Producer or family binder.

This is an explicitly scoped engineering qualification route. It does not
change the E1 preparation-only contract, activate general production dispatch,
change C11-C, or grant release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
import wave
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

SCHEMA = "C11E-E4C-DRILL-SHARED-EXECUTION-RECEIPT-V1"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_MANIFEST_BYTES = 796318
EXPECTED_GODOT_VERSION = "4.7.1.stable.mono.official.a13da4feb"
FAMILIES = {"tracking", "pursuit", "saccade", "peripheral_scan"}
EXPECTED_MUSIC_PROFILE = {
    "tracking": "FLOWING_VECTOR",
    "pursuit": "ORGANIC_BLOOM",
    "saccade": "CIRCUIT_PULSE",
    "peripheral_scan": "ORBITAL_RITUAL",
}
WIDTH = 720
HEIGHT = 1280
FPS = 30
CHANNELS = 3
FRAME_BYTES = WIDTH * HEIGHT * CHANNELS
PRE_ROLL_FRAMES = 90
END_CTA_FRAMES = 90


class DrillExecutionError(RuntimeError):
    """Raised when a fail-closed E4C execution check fails."""


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DrillExecutionError(f"Invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DrillExecutionError(f"Expected JSON object: {path}")
    return value


def phase_for_final_frame(frame_index: int, gameplay_frames: int) -> tuple[str, int]:
    """Return the consumer's native phase and phase-local/global index."""
    if gameplay_frames <= 0:
        raise DrillExecutionError("gameplay_frames must be positive")
    total = PRE_ROLL_FRAMES + gameplay_frames + END_CTA_FRAMES
    if not 0 <= frame_index < total:
        raise DrillExecutionError(f"frame index outside final native stream: {frame_index}/{total}")
    if frame_index < PRE_ROLL_FRAMES:
        return "PRE_ROLL", frame_index
    if frame_index < PRE_ROLL_FRAMES + gameplay_frames:
        return "GAME", frame_index - PRE_ROLL_FRAMES
    return "END_CTA", frame_index


def changed_music_seed(seed: int, gameplay_seed: int) -> int:
    """Choose a deterministic comparison seed, never equal to gameplay or A."""
    if not (1 <= seed <= 2_147_483_646):
        raise DrillExecutionError("music seed outside canonical D9 range")
    candidate = seed + 1 if seed < 2_147_483_646 else seed - 1
    if candidate == gameplay_seed:
        candidate = candidate + 1 if candidate < 2_147_483_646 else candidate - 1
    if candidate == seed or candidate == gameplay_seed or not (1 <= candidate <= 2_147_483_646):
        raise DrillExecutionError("cannot construct a distinct changed music seed")
    return candidate


def product_id_for(family: str, gameplay_seed: int, tier: int, speed: float) -> str:
    speed_tag = int(math.floor(float(speed) * 100.0 + 0.5))
    return f"VisualDrill_{family}_seed_{gameplay_seed}_T{tier}_constant_S{speed_tag:03d}"


def format_invariant_speed_multiplier(value: float) -> str:
    """Format a locale-independent decimal for the PowerShell wrapper."""
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise DrillExecutionError("speed_multiplier is not numeric") from exc
    if not math.isfinite(number) or not 0.1 <= number <= 3.0:
        raise DrillExecutionError("speed_multiplier outside canonical 0.1..3.0 range")
    return format(number, ".5f")


def build_c11c_launcher_wrapper_script() -> str:
    """Return a PS 5.1 wrapper which passes SpeedMultiplier as a typed Double."""
    return r"""[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$LauncherPath,
    [Parameter(Mandatory=$true)][string]$Family,
    [Parameter(Mandatory=$true)][int]$Seed,
    [Parameter(Mandatory=$true)][int]$DifficultyTier,
    [Parameter(Mandatory=$true)][string]$SpeedMultiplierInvariant,
    [Parameter(Mandatory=$true)][string]$PacingMode,
    [Parameter(Mandatory=$true)][string]$DeliveryProfile,
    [Parameter(Mandatory=$true)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$culture = [System.Globalization.CultureInfo]::InvariantCulture
$speed = [double]::Parse($SpeedMultiplierInvariant, [System.Globalization.NumberStyles]::Float, $culture)
if ([double]::IsNaN($speed) -or [double]::IsInfinity($speed) -or $speed -lt 0.1 -or $speed -gt 3.0) {
    throw "SpeedMultiplier outside canonical 0.1..3.0 range: $SpeedMultiplierInvariant"
}
$thread = [System.Threading.Thread]::CurrentThread
$originalCulture = $thread.CurrentCulture
$originalUiCulture = $thread.CurrentUICulture
try {
    $thread.CurrentCulture = $culture
    $thread.CurrentUICulture = $culture
    & $LauncherPath -Family $Family -Seed $Seed -DifficultyTier $DifficultyTier -SpeedMultiplier $speed -PacingMode $PacingMode -DeliveryProfile $DeliveryProfile -NoSound -OutputRoot $OutputRoot
    if (-not $?) { throw 'C11-C Drill launcher returned an unsuccessful PowerShell status' }
}
finally {
    $thread.CurrentCulture = $originalCulture
    $thread.CurrentUICulture = $originalUiCulture
}
"""


def validate_request(raw: Mapping[str, Any]) -> tuple[str, int, int, int, int]:
    selection = raw.get("selection")
    if not isinstance(selection, Mapping) or selection.get("content_type") != "visual_drills":
        raise DrillExecutionError("E4C execution accepts only canonical visual_drills requests")
    family = str(selection.get("family_id", ""))
    variant = str(selection.get("variant_id", ""))
    match = re.fullmatch(r"tier-([1-5])", variant)
    if family not in FAMILIES or not match:
        raise DrillExecutionError("request selector is outside the exact 4-family × 5-tier matrix")
    if raw.get("mode") != "PRODUCTION":
        raise DrillExecutionError("isolated E4C A/V qualification requires mode=PRODUCTION")
    if raw.get("delivery_profile_id") != "REVIEW_720":
        raise DrillExecutionError("E4C Drill qualification is pinned to REVIEW_720")
    if raw.get("audio_enabled") is not True:
        raise DrillExecutionError("E4C A/V qualification requires audio_enabled=true")
    if raw.get("personalization_enabled") is not True:
        raise DrillExecutionError("E4C visual qualification requires personalization_enabled=true")
    gameplay_seed = raw.get("seed")
    music_seed = raw.get("music_seed")
    for label, value in (("gameplay_seed", gameplay_seed), ("music_seed", music_seed)):
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 2_147_483_646:
            raise DrillExecutionError(f"{label} must be a canonical positive integer")
    if gameplay_seed == music_seed:
        raise DrillExecutionError("gameplay and music seed domains must be numerically distinct")
    request_id = str(raw.get("request_id", ""))
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", request_id):
        raise DrillExecutionError("request_id is unsafe or outside the accepted 96-character limit")
    return family, int(match.group(1)), int(gameplay_seed), int(music_seed), int(raw.get("variation_index", 0))


def require_visible_editorial(plan: Mapping[str, Any]) -> dict[str, str]:
    """Fail closed unless at least one real D-owned text field will render in GAME."""
    text_block = plan.get("text", {})
    fields = text_block.get("visible_fields", {}) if isinstance(text_block, Mapping) else {}
    if not isinstance(fields, Mapping):
        raise DrillExecutionError("D composition plan visible_fields must be an object")
    visible: dict[str, str] = {}
    for key in ("title", "subtitle", "call_to_action"):
        value = fields.get(key)
        if isinstance(value, str) and value.strip() and value.strip().casefold() != "unknown":
            visible[key] = value.strip()
    if not visible:
        raise DrillExecutionError(
            "E4C requires at least one non-empty D editorial field (title, subtitle or call_to_action); "
            "personalization_enabled=true alone is not evidence of visible composition"
        )
    if text_block.get("phase_visibility", {}).get("GAME") is not True:
        raise DrillExecutionError("D composition plan does not declare editorial visible during GAME")
    for phase in ("PRE_ROLL", "END_CTA", "DONE"):
        if text_block.get("phase_visibility", {}).get(phase) is not False:
            raise DrillExecutionError(f"D composition plan editorial must be hidden during {phase}")
    return visible


def verify_executable(path: Path, label: str, args: list[str], timeout: int = 30) -> str:
    result = subprocess.run([str(path), *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0 or not output:
        raise DrillExecutionError(f"{label} preflight failed: exit={result.returncode}; {output[-1000:]}")
    return output


def discover_binary(name: str, explicit: str | None = None, sibling_of: Path | None = None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    env_name = "FFMPEG_BIN" if name == "ffmpeg.exe" else "FFPROBE_BIN"
    if os.environ.get(env_name):
        candidates.append(Path(os.environ[env_name]))
    if sibling_of is not None:
        candidates.append(sibling_of.parent / name)
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    candidates.append(local / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0-full_build" / "bin" / name)
    found = shutil.which(name)
    if found:
        candidates.append(Path(found))
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise DrillExecutionError(f"required executable not found: {name}")


def discover_godot(project_root: Path) -> Path:
    candidates: list[Path] = []
    if os.environ.get("GODOT_BIN"):
        candidates.append(Path(os.environ["GODOT_BIN"]))
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    candidates.append(local / "Microsoft" / "WinGet" / "Packages" / "GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe" / "Godot_v4.7.1-stable_mono_win64" / "godot.exe")
    candidates.append(project_root / "Godot_v4.7.1-stable_mono_win64" / "godot.exe")
    found = shutil.which("godot.exe") or shutil.which("godot")
    if found:
        candidates.append(Path(found))
    for candidate in candidates:
        if candidate.is_file():
            resolved = candidate.resolve()
            result = subprocess.run([str(resolved), "--version"], capture_output=True, text=True, timeout=30)
            version = (result.stdout or result.stderr).strip()
            if result.returncode != 0 or version != EXPECTED_GODOT_VERSION:
                raise DrillExecutionError(f"Godot version mismatch: {version!r}")
            return resolved
    raise DrillExecutionError("Godot 4.7.1 Mono executable not found; set GODOT_BIN")


def ffprobe_json(ffprobe: Path, media: Path) -> dict[str, Any]:
    command = [str(ffprobe), "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(media)]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    if result.returncode != 0:
        raise DrillExecutionError(f"FFprobe failed for {media}: {result.stderr[-4000:]}")
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise DrillExecutionError(f"FFprobe returned invalid JSON for {media}") from exc
    if not isinstance(value, dict):
        raise DrillExecutionError("FFprobe response is not an object")
    return value


def stream_hash(ffmpeg: Path, media: Path, stream_type: str, log_path: Path) -> str:
    command = [str(ffmpeg), "-v", "error", "-i", str(media), "-map", f"0:{stream_type}:0", "-c", "copy", "-f", "hash", "-hash", "sha256", "-"]
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=log, text=True, encoding="ascii", errors="replace", timeout=180)
    if result.returncode != 0:
        raise DrillExecutionError(f"FFmpeg {stream_type} stream hash failed for {media}; inspect {log_path}")
    match = re.search(r"SHA256=([0-9a-fA-F]{64})", result.stdout)
    if not match:
        raise DrillExecutionError(f"FFmpeg did not return a SHA-256 for {stream_type}: {result.stdout!r}")
    return match.group(1).lower()


def _read_exact(stream: Any, length: int) -> bytes:
    chunks: list[bytes] = []
    remaining = length
    while remaining:
        block = stream.read(remaining)
        if not block:
            break
        chunks.append(block)
        remaining -= len(block)
    data = b"".join(chunks)
    if len(data) != length:
        raise DrillExecutionError(f"FFmpeg raw frame ended early: expected {length} bytes, got {len(data)}")
    return data


def compose_all_frames(
    source_mp4: Path,
    target_video_mp4: Path,
    gameplay_frames: int,
    plan: Mapping[str, Any],
    project_root: Path,
    ffmpeg: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    # Import PySide6 only on the execution path; E1 preparation and CLI parity
    # remain importable/testable without Qt startup.
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    consumer_dir = project_root / "tools" / "c11d" / "d9"
    if str(consumer_dir) not in sys.path:
        sys.path.insert(0, str(consumer_dir))
    import c11e_e4c_drill_visual_composition_consumer as consumer  # type: ignore

    consumer._ensure_qt_app()
    consumer.validate_plan(plan)
    frames_expected = PRE_ROLL_FRAMES + gameplay_frames + END_CTA_FRAMES
    decoded_log = evidence_dir / "ffmpeg_decode_stderr.log"
    encoded_log = evidence_dir / "ffmpeg_encode_stderr.log"
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
        "-x264-params", "open_gop=0:keyint=90:min-keyint=90:scenecut=0", "-movflags", "+faststart", str(target_video_mp4),
    ]
    composed_counts = {"PRE_ROLL": 0, "GAME": 0, "END_CTA": 0}
    frame_rows: list[dict[str, Any]] = []
    with decoded_log.open("w", encoding="utf-8") as dec_log, encoded_log.open("w", encoding="utf-8") as enc_log:
        decoder = subprocess.Popen(decode_command, stdout=subprocess.PIPE, stderr=dec_log, cwd=str(project_root))
        encoder = subprocess.Popen(encode_command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=enc_log, cwd=str(project_root))
        try:
            if decoder.stdout is None or encoder.stdin is None:
                raise DrillExecutionError("FFmpeg raw frame pipes could not be opened")
            for frame_index in range(frames_expected):
                raw = _read_exact(decoder.stdout, FRAME_BYTES)
                phase, phase_index = phase_for_final_frame(frame_index, gameplay_frames)
                source = consumer.QImage(raw, WIDTH, HEIGHT, WIDTH * CHANNELS, consumer.QImage.Format.Format_RGB888).copy()
                if source.isNull() or source.width() != WIDTH or source.height() != HEIGHT:
                    raise DrillExecutionError(f"Qt could not construct source QImage at frame {frame_index}")
                source_sha = consumer._image_rgb_sha256(source)
                result = consumer.compose_frame(source, plan, phase, phase_index, gameplay_frames, FPS, 1, project_root)
                composed = result.get("image")
                if composed is None or composed.isNull() or (composed.width(), composed.height()) != (WIDTH, HEIGHT):
                    raise DrillExecutionError(f"D consumer returned invalid frame at {frame_index}")
                if result.get("source_unchanged") is not True or consumer._image_rgb_sha256(source) != source_sha:
                    raise DrillExecutionError(f"D consumer mutated input QImage at frame {frame_index}")
                mapping = result.get("mapping", {})
                if mapping.get("phase") != phase or mapping.get("d_editorial_visible") is not (phase == "GAME"):
                    raise DrillExecutionError(f"D consumer phase visibility mismatch at frame {frame_index}")
                expected_final = frame_index if phase != "GAME" else PRE_ROLL_FRAMES + phase_index
                if mapping.get("final_presentation_frame_index") != expected_final:
                    raise DrillExecutionError(f"D timebase mismatch at frame {frame_index}")
                encoder.stdin.write(consumer._image_rgb_bytes(composed))
                composed_counts[phase] += 1
                if frame_index in (0, PRE_ROLL_FRAMES, PRE_ROLL_FRAMES + gameplay_frames // 2, PRE_ROLL_FRAMES + gameplay_frames - 1, frames_expected - END_CTA_FRAMES):
                    frame_rows.append({
                        "frame_index": frame_index,
                        "phase": phase,
                        "phase_index": phase_index,
                        "mode": result.get("mode"),
                        "source_rgb_sha256": source_sha,
                        "composed_rgb_sha256": consumer._image_rgb_sha256(composed),
                        "final_presentation_frame_index": mapping.get("final_presentation_frame_index"),
                    })
            # There must be no extra decoded frames beyond the native timeline.
            extra = decoder.stdout.read(1)
            if extra:
                raise DrillExecutionError("FFmpeg decoded more frames than the C11-C manifest declares")
            encoder.stdin.close()
            decoder.stdout.close()
            decode_exit = decoder.wait(timeout=120)
            encode_exit = encoder.wait(timeout=300)
            if decode_exit != 0:
                raise DrillExecutionError(f"FFmpeg source decode exited {decode_exit}; inspect {decoded_log}")
            if encode_exit != 0:
                raise DrillExecutionError(f"FFmpeg D video encode exited {encode_exit}; inspect {encoded_log}")
        except Exception:
            for process in (decoder, encoder):
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=30)
            raise
    if not target_video_mp4.is_file() or target_video_mp4.stat().st_size <= 0:
        raise DrillExecutionError("D-composed silent video was not created")
    return {
        "frames_expected": frames_expected,
        "frames_composed": sum(composed_counts.values()),
        "phase_counts": composed_counts,
        "sampled_frames": frame_rows,
        "silent_composed_video_sha256": sha_file(target_video_mp4),
        "silent_composed_video_bytes": target_video_mp4.stat().st_size,
        "source_decode_log": str(decoded_log),
        "video_encode_log": str(encoded_log),
    }


def generate_family_music(
    python_exe: Path,
    wrapper: Path,
    wav_path: Path,
    seed: int,
    family: str,
    duration: float,
    cwd: Path,
    log_path: Path,
) -> dict[str, Any]:
    command = [str(python_exe), str(wrapper), str(wav_path), str(seed), "1", f"{duration:.6f}", family, "drill"]
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(command, cwd=str(cwd), stdout=log, stderr=subprocess.STDOUT, text=True, timeout=600)
    if result.returncode != 0 or not wav_path.is_file() or wav_path.stat().st_size <= 44:
        raise DrillExecutionError(f"FAMILY_MUSIC_V4 generation failed; inspect {log_path}")
    with wave.open(str(wav_path), "rb") as audio:
        params = audio.getparams()
        frames = audio.getnframes()
        duration_actual = frames / float(params.framerate)
        if params.nchannels != 2 or params.sampwidth != 2 or params.framerate != 44100:
            raise DrillExecutionError(f"FAMILY_MUSIC_V4 native PCM contract mismatch: {params}")
        if abs(duration_actual - duration) > 0.002:
            raise DrillExecutionError(f"FAMILY_MUSIC_V4 duration mismatch: {duration_actual} vs {duration}")
        pcm = audio.readframes(frames)
    # Native V4 output must be audible/non-silent and stay below full-scale.
    if not pcm:
        raise DrillExecutionError("FAMILY_MUSIC_V4 WAV is empty")
    import array
    samples = array.array("h")
    samples.frombytes(pcm)
    if sys.byteorder != "little":
        samples.byteswap()
    peak = max(abs(value) for value in samples) / 32768.0
    rms = math.sqrt(sum(value * value for value in samples) / max(1, len(samples))) / 32768.0
    if peak <= 0.01 or rms <= 0.002 or peak >= 0.999:
        raise DrillExecutionError(f"FAMILY_MUSIC_V4 level outside safe non-silence range: peak={peak} rms={rms}")
    return {
        "path": str(wav_path), "sha256": sha_file(wav_path), "bytes": wav_path.stat().st_size,
        "sample_rate_hz": params.framerate, "channels": params.nchannels, "sample_width_bytes": params.sampwidth,
        "frames": frames, "duration_seconds": duration_actual, "peak": peak, "rms": rms,
        "seed": seed, "family": family,
    }


def mux_audio(ffmpeg: Path, ffprobe: Path, silent_video: Path, wav_path: Path, target_mp4: Path, duration: float, frames: int, evidence_dir: Path) -> dict[str, Any]:
    command = [
        str(ffmpeg), "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent_video), "-i", str(wav_path),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-profile:a", "aac_low",
        "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", str(target_mp4),
    ]
    log_path = evidence_dir / (target_mp4.stem + "_mux.log")
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(command, cwd=str(evidence_dir), stdout=log, stderr=subprocess.STDOUT, timeout=600)
    if result.returncode != 0 or not target_mp4.is_file() or target_mp4.stat().st_size <= 0:
        raise DrillExecutionError(f"FFmpeg audio mux failed; inspect {log_path}")
    probe = ffprobe_json(ffprobe, target_mp4)
    streams = probe.get("streams", [])
    video = next((row for row in streams if row.get("codec_type") == "video"), None)
    audio = next((row for row in streams if row.get("codec_type") == "audio"), None)
    if not video or not audio:
        raise DrillExecutionError("FFprobe did not find exactly the expected video and audio streams")
    if len([row for row in streams if row.get("codec_type") == "video"]) != 1 or len([row for row in streams if row.get("codec_type") == "audio"]) != 1:
        raise DrillExecutionError("FFprobe stream cardinality must be one video plus one audio")
    if (int(video.get("width", 0)), int(video.get("height", 0)), str(video.get("avg_frame_rate")), str(video.get("pix_fmt"))) != (WIDTH, HEIGHT, "30/1", "yuv420p"):
        raise DrillExecutionError(f"Final video stream contract mismatch: {video}")
    if str(video.get("profile", "")).casefold() != "high" or str(video.get("color_range", "")).casefold() not in ("tv", "limited"):
        raise DrillExecutionError(f"Final H.264 profile/range mismatch: {video}")
    if int(video.get("nb_read_frames", -1)) != frames:
        raise DrillExecutionError(f"Final video frame count mismatch: {video.get('nb_read_frames')} != {frames}")
    if (audio.get("codec_name"), str(audio.get("profile", "")).casefold(), str(audio.get("sample_rate")), int(audio.get("channels", 0))) != ("aac", "lc", "48000", 2):
        raise DrillExecutionError(f"Final AAC-LC delivery stream mismatch: {audio}")
    actual_duration = float((probe.get("format") or {}).get("duration", 0.0))
    if abs(actual_duration - duration) > 0.15:
        raise DrillExecutionError(f"Final A/V duration mismatch: {actual_duration} vs {duration}")
    video_start = float(video.get("start_time", 0.0) or 0.0)
    audio_start = float(audio.get("start_time", 0.0) or 0.0)
    av_start_delta = abs(video_start - audio_start)
    if av_start_delta > 0.020:
        raise DrillExecutionError(f"Final A/V stream start offset exceeds 20ms: {av_start_delta}")
    return {
        "path": str(target_mp4), "sha256": sha_file(target_mp4), "bytes": target_mp4.stat().st_size,
        "duration_seconds": actual_duration, "video": video, "audio": audio,
        "av_start_delta_seconds": av_start_delta, "ffprobe": probe, "mux_log": str(log_path),
    }


def _source_pins(intent: Mapping[str, Any], project_root: Path) -> list[dict[str, Any]]:
    rows = intent.get("source_identity", {}).get("source_pins", [])
    if not isinstance(rows, list) or not rows:
        raise DrillExecutionError("E1 source identity pin list is missing")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise DrillExecutionError("E1 source pin row is not an object")
        rel = str(row.get("path", ""))
        posix = PurePosixPath(rel)
        if not rel or posix.is_absolute() or ".." in posix.parts or rel in seen:
            raise DrillExecutionError(f"E1 source pin path is unsafe or duplicated: {rel!r}")
        seen.add(rel)
        path = project_root / Path(*posix.parts)
        expected_bytes = row.get("bytes")
        expected_sha = row.get("sha256")
        if isinstance(expected_bytes, bool) or not isinstance(expected_bytes, int) or expected_bytes < 0 or not re.fullmatch(r"[0-9a-f]{64}", str(expected_sha)):
            raise DrillExecutionError(f"E1 source pin declaration is malformed: {rel}")
        if not path.is_file() or path.stat().st_size != expected_bytes or sha_file(path) != expected_sha:
            raise DrillExecutionError(f"E1 source pin changed during E4C run: {rel}")
        normalized.append({"path": rel, "bytes": expected_bytes, "sha256": expected_sha})
    manifest = project_root / "release" / "C11C_FREEZE_PACKAGE_MANIFEST.json"
    if manifest.stat().st_size != FROZEN_MANIFEST_BYTES or sha_file(manifest) != FROZEN_MANIFEST_SHA256:
        raise DrillExecutionError("frozen C11-C manifest changed during E4C run")
    normalized.sort(key=lambda item: item["path"])
    return normalized


def _prepare_intent_pair(raw_request: Mapping[str, Any], root: Path, origin: str, service: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    gui = service.prepare_c11e_production_intent(raw_request, root, request_origin="GUI")
    cli = service.prepare_c11e_production_intent(raw_request, root, request_origin="CLI")
    gui_intent = gui["intent"]
    cli_intent = cli["intent"]
    service.validate_c11e_production_intent(gui_intent, root)
    service.validate_c11e_production_intent(cli_intent, root)
    for field in ("request_hash", "editorial_hash", "plan_hash", "intent_hash"):
        if gui_intent.get("identity", {}).get(field) != cli_intent.get("identity", {}).get(field):
            raise DrillExecutionError(f"E1 GUI/CLI semantic identity mismatch: {field}")
    if gui_intent.get("d9_boundary_preparation") != cli_intent.get("d9_boundary_preparation"):
        raise DrillExecutionError("E1 GUI/CLI Drill family-boundary preparation mismatch")
    selected = gui_intent if origin == "GUI" else cli_intent
    return selected, {
        "status": "PASS_E1_SHARED_GUI_CLI_INTENT_PARITY",
        "gui_intent_sha256": gui_intent.get("intent_sha256"),
        "cli_intent_sha256": cli_intent.get("intent_sha256"),
        "semantic_identity_equal": True,
        "origin_used_for_execution": origin,
    }


def execute_drill_av_request(
    raw_request: Mapping[str, Any],
    project_root: Path | str,
    *,
    request_origin: str = "CLI",
    ffmpeg_path: str | None = None,
    ffprobe_path: str | None = None,
    python_executable: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise DrillExecutionError(f"project root does not exist: {root}")
    if request_origin not in ("GUI", "CLI"):
        raise DrillExecutionError("execution origin must be GUI or CLI")
    family, tier, gameplay_seed, music_seed_a, _variation = validate_request(raw_request)
    music_seed_c = changed_music_seed(music_seed_a, gameplay_seed)
    request_id = str(raw_request["request_id"])

    frozen = root / "release" / "C11C_FREEZE_PACKAGE_MANIFEST.json"
    if not frozen.is_file() or frozen.stat().st_size != FROZEN_MANIFEST_BYTES or sha_file(frozen) != FROZEN_MANIFEST_SHA256:
        raise DrillExecutionError("frozen C11-C manifest identity mismatch")

    producer_dir = root / "c11c-suite" / "c11c-producer"
    d9_dir = root / "tools" / "c11d" / "d9"
    if str(producer_dir) not in sys.path:
        sys.path.insert(0, str(producer_dir))
    if str(d9_dir) not in sys.path:
        sys.path.insert(0, str(d9_dir))
    import c11e_production_service as service  # type: ignore
    import c11e_e4c_drill_visual_composition_consumer as consumer  # type: ignore

    intent, parity = _prepare_intent_pair(raw_request, root, request_origin, service)
    validation = service.validate_c11e_production_intent(intent, root)
    pins_before = _source_pins(intent, root)
    if validation.get("status") != "PASS_E1_PREPARATION_ONLY":
        raise DrillExecutionError("E1 intent validation did not return preparation PASS")
    if intent.get("family_adapter", {}).get("status") != "NOT_CONNECTED_E1":
        raise DrillExecutionError("unexpected E1 preparation adapter state; new source review required")
    plan = consumer.build_composition_plan(intent, root)
    consumer.validate_plan(plan)
    visible_editorial = require_visible_editorial(plan)

    preparation = intent.get("d9_boundary_preparation", {})
    stage = preparation.get("drill_family_stage_contract", {})
    stage_music_profile = stage.get("native_family_music", {}).get("profile_id")
    if stage_music_profile != EXPECTED_MUSIC_PROFILE[family]:
        raise DrillExecutionError(f"E1 family music profile mismatch: {stage_music_profile}")
    music_wrapper = root / "tools" / "prototypes" / "c11c_common" / "C11CSafeAmbient.py"
    difficulty_path = root / "profiles" / "difficulty" / f"visual_drill_{family}.json"
    difficulty = read_json(difficulty_path)
    speed = (difficulty.get("tiers") or {}).get(str(tier), {}).get("speed_multiplier")
    if isinstance(speed, bool) or not isinstance(speed, (int, float)) or not 0.1 <= float(speed) <= 3.0:
        raise DrillExecutionError("selected Drill tier has no valid source-pinned speed multiplier")
    speed = float(speed)

    planned_root_rel = intent.get("output", {}).get("planned_root")
    if not isinstance(planned_root_rel, str) or not planned_root_rel.startswith("artifacts/production/c11e/"):
        raise DrillExecutionError("E1 output root is outside the C11-E isolated product namespace")
    run_root = root / Path(*PurePosixPath(planned_root_rel).parts)
    if run_root.exists():
        raise DrillExecutionError(f"E1 output root already exists; overwrite is denied: {run_root}")

    # Complete environment and source preflight before creating the E1 output root.
    ffprobe = discover_binary("ffprobe.exe", ffprobe_path)
    ffmpeg = discover_binary("ffmpeg.exe", ffmpeg_path, sibling_of=ffprobe)
    ffprobe_version = verify_executable(ffprobe, "FFprobe", ["-version"])
    ffmpeg_version = verify_executable(ffmpeg, "FFmpeg", ["-version"])
    python_exe = Path(python_executable or sys.executable).resolve()
    if not python_exe.is_file():
        raise DrillExecutionError(f"Python executable does not exist: {python_exe}")
    python_probe = verify_executable(python_exe, "Python", ["-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))"])
    if not python_probe.startswith("3.13."):
        raise DrillExecutionError(f"E4C requires the canonical Python 3.13 runtime; found {python_probe}")
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not powershell:
        raise DrillExecutionError("Windows PowerShell executable not found")
    powershell_version = verify_executable(Path(powershell), "Windows PowerShell", ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"] )
    if not powershell_version.startswith("5.1"):
        raise DrillExecutionError(f"Windows PowerShell 5.1 required; found {powershell_version!r}")
    godot = discover_godot(root)
    env = os.environ.copy()
    env["GODOT_BIN"] = str(godot)
    env["PATH"] = str(ffmpeg.parent) + os.pathsep + env.get("PATH", "")
    env["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    manifest_path = root / "profiles" / "presentation" / "c11c_visual_music_profiles.json"
    music_registry = read_json(manifest_path)
    registry_binding = (music_registry.get("bindings") or {}).get(f"visual_drill/{family}", {})
    if registry_binding.get("profile") != stage_music_profile:
        raise DrillExecutionError("FAMILY_MUSIC_V4 registry does not agree with the E1 family-stage profile")
    if not music_wrapper.is_file() or not (root / "c11c-suite" / "c11c-producer" / "run_visual_drill_production.ps1").is_file():
        raise DrillExecutionError("C11-C Drill launcher or FAMILY_MUSIC_V4 wrapper is missing")
    # Ensure Qt can be initialized before touching the output namespace.
    consumer._ensure_qt_app()

    run_root.mkdir(parents=True, exist_ok=False)
    evidence_dir = run_root / "qualification"
    evidence_dir.mkdir(parents=True, exist_ok=False)
    native_root = run_root / "native_source"
    native_root.mkdir(parents=True, exist_ok=False)
    logs_dir = run_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=False)

    product_id = product_id_for(family, gameplay_seed, tier, speed)
    native_product_root = native_root / family / product_id
    source_mp4 = native_product_root / f"{product_id}.mp4"
    source_manifest_path = native_product_root / "production_manifest.json"
    source_authoring_path = native_product_root / "authoring.json"

    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "RUNNING",
        "request_id": request_id,
        "request_origin": request_origin,
        "family": family,
        "tier": tier,
        "gameplay_seed": gameplay_seed,
        "music_seed_a": music_seed_a,
        "music_seed_b": music_seed_a,
        "music_seed_c_changed": music_seed_c,
        "delivery_profile": "REVIEW_720",
        "family_music_profile": stage_music_profile,
        "e1_validation": validation,
        "e1_gui_cli_parity": parity,
        "family_adapter_preparation_status": intent.get("family_adapter", {}).get("status"),
        "family_adapter_execution": {
            "status": "D_OWNED_EXECUTOR_CONSUMES_CANONICAL_E1_INTENT",
            "shared_entrypoint": "c11e_e4c_drill_execution.py",
            "gui_and_cli_use_same_implementation": True,
        },
        "d_consumer_plan_sha256": plan.get("plan_sha256"),
        "d_editorial_visible_fields": visible_editorial,
        "source_pins_pre_execution": pins_before,
        "toolchain_preflight": {"python": python_probe, "ffmpeg": ffmpeg_version.splitlines()[0], "ffprobe": ffprobe_version.splitlines()[0], "powershell": powershell_version, "godot": EXPECTED_GODOT_VERSION},
        "renderer_scope": "EXPLICIT_ISOLATED_E4C_QUALIFICATION_ONLY",
        "production_dispatch": False,
        "production_release": False,
        "release_authority": "NONE",
        "c11c_manifest_sha256": FROZEN_MANIFEST_SHA256,
    }
    write_json(run_root / "request.json", dict(raw_request))
    write_json(run_root / "e1_intent.json", intent)
    write_json(run_root / "e1_validation.json", validation)
    write_json(run_root / "d_composition_plan.json", plan)

    try:
        pins_immediately_pre_renderer = _source_pins(intent, root)
        if pins_immediately_pre_renderer != pins_before:
            raise DrillExecutionError("E1 source pins changed after preflight and before native C11-C capture")
        receipt["source_pins_immediately_pre_renderer"] = pins_immediately_pre_renderer
        write_json(run_root / "E4C_DRILL_AV_QUALIFICATION_RUNNING.json", receipt)
        launcher = root / "c11c-suite" / "c11c-producer" / "run_visual_drill_production.ps1"
        # The existing C11-C launcher is always silent here. Its built-in audio
        # path couples its Seed argument to the music generator; FAMILY_MUSIC_V4
        # is invoked separately below with the canonical request.music_seed.
        # Pass speed through an invariant-string wrapper. The wrapper parses it
        # using InvariantCulture, then invokes the existing C11-C script with an
        # already-typed System.Double. No locale-dependent numeric text reaches
        # the C11-C parameter binder; the pinned launcher remains unmodified.
        speed_argument = format_invariant_speed_multiplier(speed)
        launcher_wrapper = logs_dir / "invoke_c11c_drill_launcher.ps1"
        launcher_wrapper.write_text(build_c11c_launcher_wrapper_script(), encoding="utf-8")
        receipt["native_launcher_invocation"] = {
            "wrapper_path": str(launcher_wrapper),
            "wrapper_sha256": sha_file(launcher_wrapper),
            "speed_multiplier_invariant_argument": speed_argument,
            "speed_multiplier_typed_before_c11c_binding": True,
            "host_locale_used_for_numeric_formatting": False,
            "c11c_launcher_source_modified": False,
        }
        write_json(run_root / "E4C_DRILL_AV_QUALIFICATION_RUNNING.json", receipt)
        producer_command = [
            powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(launcher_wrapper),
            "-LauncherPath", str(launcher), "-Family", family, "-Seed", str(gameplay_seed),
            "-DifficultyTier", str(tier), "-SpeedMultiplierInvariant", speed_argument,
            "-PacingMode", "constant", "-DeliveryProfile", "REVIEW_720",
            "-OutputRoot", str(native_root),
        ]
        producer_log = logs_dir / "c11c_drill_producer.log"
        with producer_log.open("w", encoding="utf-8") as log:
            producer = subprocess.run(producer_command, cwd=str(root), env=env, stdout=log, stderr=subprocess.STDOUT, text=True, timeout=1800)
        if producer.returncode != 0:
            raise DrillExecutionError(f"existing C11-C Drill producer failed (exit {producer.returncode}); inspect {producer_log}")
        if not source_mp4.is_file() or not source_manifest_path.is_file() or not source_authoring_path.is_file():
            raise DrillExecutionError("C11-C Drill launcher returned without its MP4/manifest/authoring product")

        source_manifest = read_json(source_manifest_path)
        authoring = read_json(source_authoring_path)
        expected_identity = {
            "family": family,
            "seed": gameplay_seed,
            "difficulty_tier": tier,
            "delivery_profile": "REVIEW_720",
            "resolution": "720x1280",
            "fps": 30,
            "audio_enabled": False,
            "audio_mode": "OFF",
            "pacing_mode_requested": "constant",
        }
        for key, expected in expected_identity.items():
            if source_manifest.get(key) != expected:
                raise DrillExecutionError(f"C11-C source manifest identity mismatch: {key}={source_manifest.get(key)!r} expected={expected!r}")
        if abs(float(source_manifest.get("speed_multiplier", -999)) - speed) > 0.000001:
            raise DrillExecutionError("C11-C source manifest speed multiplier differs from the pinned tier policy")
        duration = float(source_manifest.get("total_duration_seconds", 0.0))
        frames_total = int(source_manifest.get("total_frames", 0))
        gameplay_frames = frames_total - PRE_ROLL_FRAMES - END_CTA_FRAMES
        if abs(duration - (frames_total / FPS)) > 0.001 or gameplay_frames <= 0:
            raise DrillExecutionError("C11-C native Drill timeline is internally inconsistent")
        if frames_total not in (690, 810):
            raise DrillExecutionError(f"unexpected C11-C Drill frame total: {frames_total}")
        native_probe = ffprobe_json(ffprobe, source_mp4)
        native_video = next((row for row in native_probe.get("streams", []) if row.get("codec_type") == "video"), None)
        if not native_video or (int(native_video.get("width", 0)), int(native_video.get("height", 0)), str(native_video.get("avg_frame_rate")), int(native_video.get("nb_read_frames", -1))) != (WIDTH, HEIGHT, "30/1", frames_total):
            raise DrillExecutionError(f"C11-C silent MP4 FFprobe contract mismatch: {native_video}")
        if any(row.get("codec_type") == "audio" for row in native_probe.get("streams", [])):
            raise DrillExecutionError("C11-C source must be silent before D/FAMILY_MUSIC_V4 post-composition")
        if int(authoring.get("difficulty_tier", -1)) != tier:
            raise DrillExecutionError("authoring.json does not preserve selected difficulty tier")
        effective_pacing = str((authoring.get("producer") or {}).get("pacing_mode_effective", ""))
        if effective_pacing not in {"constant", "authored_arc_length", "authored_polar_schedule"}:
            raise DrillExecutionError(f"unexpected effective family pacing: {effective_pacing}")

        native_identity = {
            "mp4": str(source_mp4), "mp4_sha256": sha_file(source_mp4), "mp4_bytes": source_mp4.stat().st_size,
            "manifest_sha256": sha_file(source_manifest_path), "authoring_sha256": sha_file(source_authoring_path),
            "ffprobe": native_probe, "effective_pacing": effective_pacing,
        }
        write_json(evidence_dir / "native_source_identity.json", native_identity)

        silent_d_video = evidence_dir / "d_composed_silent.mp4"
        composition = compose_all_frames(source_mp4, silent_d_video, gameplay_frames, plan, root, ffmpeg, evidence_dir)
        write_json(evidence_dir / "d_composition_receipt.json", composition)

        wav_a = evidence_dir / f"family_music_A_seed_{music_seed_a}.wav"
        wav_b = evidence_dir / f"family_music_B_repeat_seed_{music_seed_a}.wav"
        wav_c = evidence_dir / f"family_music_C_changed_seed_{music_seed_c}.wav"
        music_a = generate_family_music(python_exe, music_wrapper, wav_a, music_seed_a, family, duration, root, logs_dir / "family_music_A.log")
        music_b = generate_family_music(python_exe, music_wrapper, wav_b, music_seed_a, family, duration, root, logs_dir / "family_music_B.log")
        music_c = generate_family_music(python_exe, music_wrapper, wav_c, music_seed_c, family, duration, root, logs_dir / "family_music_C.log")
        if music_a["sha256"] != music_b["sha256"]:
            raise DrillExecutionError("FAMILY_MUSIC_V4 same-seed A/B WAV repeat did not match")
        if music_a["sha256"] == music_c["sha256"]:
            raise DrillExecutionError("FAMILY_MUSIC_V4 changed-seed C WAV did not differ")
        write_json(evidence_dir / "family_music_receipt.json", {"A": music_a, "B": music_b, "C": music_c, "same_seed_ab_identical": True, "changed_seed_c_distinct": True})

        # Prepare the C intent using the same gameplay seed and only a changed
        # music seed. This proves the E1 identity remains domain-separated.
        request_c = dict(raw_request)
        request_c["request_id"] = (request_id[:78] + "_MC" + uuid.uuid4().hex[:8])[:96]
        request_c["music_seed"] = music_seed_c
        prepared_c = service.prepare_c11e_production_intent(request_c, root, request_origin=request_origin)
        intent_c = prepared_c["intent"]
        service.validate_c11e_production_intent(intent_c, root)
        pins_c = _source_pins(intent_c, root)
        if pins_c != pins_before:
            raise DrillExecutionError("E1 source pin set changed between A and changed-music C intents")
        if intent_c.get("identity", {}).get("editorial_hash") != intent.get("identity", {}).get("editorial_hash"):
            raise DrillExecutionError("changed music seed variant altered canonical editorial identity")
        if intent_c.get("seed_domains", {}).get("gameplay", {}).get("value") != gameplay_seed:
            raise DrillExecutionError("changed music seed variant altered gameplay seed")
        if intent_c.get("seed_domains", {}).get("music", {}).get("value") != music_seed_c:
            raise DrillExecutionError("changed music seed variant did not reach E1 music domain")
        if intent_c.get("identity", {}).get("request_hash") == intent.get("identity", {}).get("request_hash"):
            raise DrillExecutionError("changed music seed did not alter the canonical E1 request identity")
        plan_c = consumer.build_composition_plan(intent_c, root)
        consumer.validate_plan(plan_c)
        write_json(evidence_dir / "changed_music_seed_c_intent.json", intent_c)
        write_json(evidence_dir / "changed_music_seed_c_composition_plan.json", plan_c)

        final_a = run_root / f"{request_id}_A_music_{music_seed_a}.mp4"
        final_c = evidence_dir / f"{request_id}_C_changed_music_{music_seed_c}.mp4"
        mux_a = mux_audio(ffmpeg, ffprobe, silent_d_video, wav_a, final_a, duration, frames_total, evidence_dir)
        mux_c = mux_audio(ffmpeg, ffprobe, silent_d_video, wav_c, final_c, duration, frames_total, evidence_dir)
        video_hash_a = stream_hash(ffmpeg, final_a, "v", logs_dir / "video_stream_hash_A.log")
        video_hash_c = stream_hash(ffmpeg, final_c, "v", logs_dir / "video_stream_hash_C.log")
        audio_hash_a = stream_hash(ffmpeg, final_a, "a", logs_dir / "audio_stream_hash_A.log")
        audio_hash_c = stream_hash(ffmpeg, final_c, "a", logs_dir / "audio_stream_hash_C.log")
        if video_hash_a != video_hash_c:
            raise DrillExecutionError("music-only seed change altered the final video bitstream")
        if audio_hash_a == audio_hash_c:
            raise DrillExecutionError("music-only seed change did not alter the final audio bitstream")

        post_pins = _source_pins(intent, root)
        if post_pins != pins_before:
            raise DrillExecutionError("E1 source pin manifest differs between pre- and post-execution checks")
        receipt.update({
            "status": "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION",
            "native_source": native_identity,
            "native_timeline": {"fps": FPS, "total_frames": frames_total, "gameplay_frames": gameplay_frames, "duration_seconds": duration, "pre_roll_frames": PRE_ROLL_FRAMES, "end_cta_frames": END_CTA_FRAMES, "effective_pacing": effective_pacing},
            "d_composition": composition,
            "family_music": {"route": "C11_C_FAMILY_MUSIC_V4", "profile_id": stage_music_profile, "A": music_a, "B": music_b, "C": music_c, "same_seed_ab_identical": True, "changed_seed_c_distinct": True},
            "final_A": mux_a,
            "final_C_changed_music": mux_c,
            "bitstream_isolation": {"video_stream_sha256_A": video_hash_a, "video_stream_sha256_C": video_hash_c, "video_stream_identical": True, "audio_stream_sha256_A": audio_hash_a, "audio_stream_sha256_C": audio_hash_c, "audio_stream_changed": True},
            "source_pins_pre_execution": pins_before,
            "source_pins_immediately_pre_renderer": pins_immediately_pre_renderer,
            "source_pins_post_execution": post_pins,
            "source_pins_pre_post_equal": True,
            "source_pin_count": len(post_pins),
            "c11c_frozen_manifest_unchanged": True,
            "c11c_source_mutation": False,
            "renderer_invoked": True,
            "renderer_kind": "EXISTING_C11C_GODOT_MOVIE_MAKER_SOURCE_CAPTURE_ONLY",
            "d_postcomposition": True,
            "ffmpeg_decode_encode_mux": True,
            "audio_generated": True,
            "production_dispatch": False,
            "production_media_scope": "ISOLATED_E4C_QUALIFICATION_OUTPUTS_ONLY",
            "d4_8": "BLOCKED_OUTSIDE_THIS_EXPLICIT_TEST_AUTHORIZATION",
            "d9_10": "PREPARE_ONLY_CANONICAL_INTENT_CONSUMED_BY_D_OWNED_EXECUTION_ADAPTER",
            "release_authority": "NONE",
            "final_product": {"path": str(final_a), "sha256": mux_a["sha256"], "bytes": mux_a["bytes"]},
            "evidence_root": str(run_root),
        })
        write_json(run_root / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json", receipt)
        summary = {
            "status": receipt["status"], "request_id": request_id, "selector": f"{family}/tier-{tier}",
            "gameplay_seed": gameplay_seed, "music_seed_A_B": music_seed_a, "music_seed_C": music_seed_c,
            "source_frames": frames_total, "composed_frames": composition["frames_composed"],
            "family_music_profile": stage_music_profile, "final_A": str(final_a), "final_A_sha256": mux_a["sha256"],
            "final_C_changed_music": str(final_c), "video_bitstream_identical_A_C": True, "audio_bitstream_changed_A_C": True,
            "receipt": str(run_root / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"),
            "evidence_root": str(run_root), "renderer": "C11C_SOURCE_CAPTURE_AND_D_POSTCOMPOSITION_QUALIFICATION",
            "production_dispatch": False, "release_authority": "NONE",
        }
        write_json(evidence_dir / "stdout_summary.json", summary)
        return summary
    except Exception as exc:
        receipt["status"] = "FAIL_CLOSED_E4C_DRILL_AV_QUALIFICATION"
        receipt["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        receipt["production_dispatch"] = False
        receipt["release_authority"] = "NONE"
        try:
            failure_pins = _source_pins(intent, root)
            receipt["source_pins_post_failure"] = failure_pins
            receipt["source_pins_match_pre_execution"] = failure_pins == pins_before
        except Exception as pin_exc:
            receipt["source_pin_post_failure_error"] = str(pin_exc)
        write_json(run_root / "E4C_DRILL_AV_QUALIFICATION_FAILURE.json", receipt)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C11-E E4C Drill D-consumer + FAMILY_MUSIC_V4 isolated A/V qualification")
    parser.add_argument("--request", required=True, help="Canonical D9.9 request JSON already resolved through the Producer GUI or CLI")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--origin", choices=("GUI", "CLI"), default="CLI")
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    parser.add_argument("--python")
    args = parser.parse_args(argv)
    request_path = Path(args.request).resolve()
    root = Path(args.project_root).resolve() if args.project_root else Path(__file__).resolve().parents[3]
    try:
        raw = read_json(request_path)
        result = execute_drill_av_request(raw, root, request_origin=args.origin, ffmpeg_path=args.ffmpeg, ffprobe_path=args.ffprobe, python_executable=args.python)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_E4C_DRILL_AV_QUALIFICATION", "error_type": type(exc).__name__, "error": str(exc), "release_authority": "NONE"}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
