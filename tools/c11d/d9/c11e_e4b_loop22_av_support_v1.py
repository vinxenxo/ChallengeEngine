"""Loop22 AV support primitives derived from the already reviewed R1V AV helper set.
FFmpeg 9 decode uses -fps_mode passthrough. No D renderer code is imported or invoked.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import uuid
import wave
import zipfile
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path, PureWindowsPath
from typing import Any
BASE_RELATIVE = "tools/c11d/d9/c11e_r1v_five_family_qualification_v3.py"
BASE_RUNNER_BYTES = 89479
BASE_RUNNER_SHA256 = "9d1baba14ca8cf96e3f2f466cedc104ec4b9cf1b94ef4b11690abe7a6de9e019"
FROZEN_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
AUDIO_SOURCE_PINS = {
    "tools/prototypes/c11c_common/C11CSafeAmbient.py": {
        "bytes": 1739, "sha256": "c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c"},
    "tools/prototypes/c11c_common/generate_c11c_family_music.py": {
        "bytes": 16382, "sha256": "41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d"},
    "profiles/presentation/c11c_visual_music_profiles.json": {
        "bytes": 7038, "sha256": "b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58"},
}
class AVQualificationError(RuntimeError):
    pass
def require(condition: bool, message: str) -> None:
    if not condition:
        raise AVQualificationError(message)
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): canonical(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [canonical(v) for v in value]
    return value
def canonical_json(value: Any) -> str:
    return json.dumps(canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)
def canonical_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))
def dump_json(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
                    encoding="utf-8", newline="\n")
    return sha256_file(path)
def load_json(path: Path) -> Any:
    require(path.is_file(), f"Required JSON missing: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise AVQualificationError(f"Invalid JSON {path}: {exc}") from exc
def decode_godot_log(raw: bytes) -> str:
    """Decode the UTF-16LE BOM written by Godot Movie Maker on this Windows host."""
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16", errors="strict")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig", errors="strict")
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        # No guessing through a lossy UTF-8 replacement: a UTF-16 stream without
        # a BOM is accepted only when the NUL distribution is strongly characteristic.
        even_nuls = sum(raw[i] == 0 for i in range(0, len(raw), 2))
        odd_nuls = sum(raw[i] == 0 for i in range(1, len(raw), 2))
        pairs = max(1, len(raw) // 2)
        if odd_nuls / pairs > 0.35:
            return raw.decode("utf-16le", errors="strict")
        if even_nuls / pairs > 0.35:
            return raw.decode("utf-16be", errors="strict")
        raise AVQualificationError("Godot log encoding is neither valid UTF-8 nor BOM/shape-identified UTF-16")
def parse_godot_capture_log(raw: bytes, expected_width: int, expected_height: int,
                            expected_fps: int, expected_frames: int) -> dict[str, Any]:
    text = decode_godot_log(raw)
    dimension_pattern = rf"recording movie in\s+{expected_width}\s*[×xX]\s*{expected_height}\s*@\s*{expected_fps}\s*FPS"
    require(re.search(dimension_pattern, text, re.IGNORECASE) is not None,
            f"Godot Movie Maker log lacks {expected_width}×{expected_height}@{expected_fps}:FPS signature")
    frame_matches = re.findall(r"(?m)^\s*(\d+)\s+frames at\s+(\d+)\s+FPS\b", text, re.IGNORECASE)
    require(frame_matches, "Godot log lacks completed frame-count line")
    last_frames, last_fps = map(int, frame_matches[-1])
    require(last_frames == expected_frames and last_fps == expected_fps,
            f"Godot completed {last_frames} frames at {last_fps} FPS; expected {expected_frames}@{expected_fps}")
    require(not re.search(r"SCRIPT ERROR|Parse Error|SHADER ERROR|Shader compilation failed|ERROR:", text, re.I),
            "Godot log contains script/parse/shader error")
    return {"encoding": "utf-16le-bom" if raw.startswith(b"\xff\xfe") else "utf-8-or-utf16-detected",
            "dimensions_signature": f"{expected_width}x{expected_height}@{expected_fps}",
            "completed_frames": last_frames, "completed_fps": last_fps,
            "decoded_log_sha256": sha256_bytes(text.encode("utf-8"))}
def validate_source_pixel_format(stream: dict[str, Any]) -> str:
    pix_fmt = str(stream.get("pix_fmt", ""))
    color_range = str(stream.get("color_range", ""))
    # C11-C 2.16.3's pinned silent H.264 encode path reports full-range yuvj420p
    # on the observed Godot/AVI input. Accept the matching legacy yuvj420p/pc
    # representation, or yuv420p/tv only if a future pinned launcher explicitly
    # reports that format. Any other combination fails closed.
    allowed = {("yuvj420p", "pc"), ("yuv420p", "tv")}
    require((pix_fmt, color_range) in allowed,
            f"Unexpected C11-C source pixel/range pair: {pix_fmt}/{color_range}; expected yuvj420p/pc or yuv420p/tv")
    return pix_fmt
def read_exact(stream, size: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < size:
        part = stream.read(size - len(chunks))
        if not part:
            break
        chunks.extend(part)
    return bytes(chunks)
def run_process(command: list[str], cwd: Path, timeout: int = 3600) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=timeout, check=False)
def load_base_module(project_root: Path):
    path = project_root / BASE_RELATIVE
    require(path.is_file(), f"Pinned R1V V3 core missing: {path}")
    require(path.stat().st_size == BASE_RUNNER_BYTES and sha256_file(path) == BASE_RUNNER_SHA256,
            "R1V V3 shared validation core differs from the reviewed V4 installation")
    spec = importlib.util.spec_from_file_location("c11e_r1v_shared_core_v3", path)
    require(spec is not None and spec.loader is not None, "Cannot load pinned R1V V3 shared core")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def verify_audio_source_pins(project_root: Path) -> dict[str, Any]:
    results = []
    for relative, pin in AUDIO_SOURCE_PINS.items():
        path = project_root / Path(*relative.split("/"))
        require(path.is_file(), f"C11-C family audio source missing: {relative}")
        size = path.stat().st_size
        digest = sha256_file(path)
        require(size == pin["bytes"] and digest == pin["sha256"], f"C11-C family audio source pin mismatch: {relative}")
        results.append({"path": relative, "bytes": size, "sha256": digest})
    return {"pin_count": len(results), "pins": results}
def decode_audio_metrics(wav_path: Path, duration: float, rules: dict[str, Any]) -> dict[str, Any]:
    require(wav_path.is_file() and wav_path.stat().st_size > 44, f"Family music WAV missing/empty: {wav_path}")
    with wave.open(str(wav_path), "rb") as wf:
        channels, width, rate, frames = wf.getnchannels(), wf.getsampwidth(), wf.getframerate(), wf.getnframes()
        raw = wf.readframes(frames)
    require(channels == 2 and width == 2 and rate == 44100, "C11-C family WAV must be PCM s16le / 44100 Hz / stereo")
    expected_frames = int(round(duration * rate))
    require(frames == expected_frames, f"C11-C music WAV frame count {frames} != expected {expected_frames}")
    require(len(raw) == frames * channels * width, "C11-C music WAV PCM byte count is inconsistent")
    values = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    peak = max(abs(v) for v in values) / 32767.0 if values else 0.0
    rms = math.sqrt(sum((v / 32767.0) ** 2 for v in values) / len(values)) if values else 0.0
    max_peak = float(rules.get("max_peak", 0.36))
    min_rms = float(rules.get("target_rms_min", 0.08))
    max_rms = float(rules.get("target_rms_max", 0.16))
    require(peak > 0 and peak <= max_peak + 0.001, f"Family music peak out of range: {peak:.6f}")
    require(min_rms <= rms <= max_rms, f"Family music RMS out of range: {rms:.6f} not in [{min_rms},{max_rms}]")
    return {"sample_rate": rate, "channels": channels, "sample_width_bytes": width,
            "sample_frames": frames, "duration_seconds": frames / rate,
            "peak": peak, "rms": rms, "pcm_sha256": sha256_bytes(raw),
            "wav_sha256": sha256_file(wav_path), "wav_bytes": wav_path.stat().st_size}
def build_music_command(python_exe: str, helper: Path, wav_path: Path, selector: dict[str, Any]) -> list[str]:
    return [python_exe, str(helper), str(wav_path), str(selector["music_seed"]),
            str(selector["loop_cycles"]), f"{selector['duration_seconds']:.1f}",
            selector["internal_family_id"], "loop", selector["grammar_id"]]
def ffprobe_json(ffprobe_exe: str, path: Path, cwd: Path, output_path: Path | None = None) -> dict[str, Any]:
    args = ["-v", "error", "-show_entries",
            "format=filename,format_name,start_time,duration,size,bit_rate:stream=index,codec_type,codec_name,profile,width,height,pix_fmt,color_range,r_frame_rate,avg_frame_rate,time_base,start_time,duration,nb_frames,sample_rate,channels,channel_layout,bit_rate",
            "-of", "json", str(path)]
    proc = run_process([ffprobe_exe, *args], cwd, timeout=600)
    if output_path:
        output_path.write_bytes(proc.stdout)
        output_path.with_suffix(output_path.suffix + ".stderr.log").write_bytes(proc.stderr)
    require(proc.returncode == 0, f"FFprobe failed for {path.name}, exit={proc.returncode}: {proc.stderr[:500]!r}")
    try:
        return json.loads(proc.stdout.decode("utf-8-sig"))
    except Exception as exc:
        raise AVQualificationError(f"FFprobe returned invalid JSON for {path}: {exc}") from exc
def hash_encoded_stream(ffmpeg_exe: str, media_path: Path, stream_selector: str, output_format: str,
                        cwd: Path) -> str:
    proc = run_process([ffmpeg_exe, "-v", "error", "-i", str(media_path), "-map", stream_selector,
                        "-c", "copy", "-f", output_format, "pipe:1"], cwd, timeout=1800)
    require(proc.returncode == 0, f"FFmpeg stream-copy extraction failed for {media_path.name}: {proc.stderr[:500]!r}")
    require(bool(proc.stdout), f"FFmpeg returned empty {output_format} stream for {media_path.name}")
    return sha256_bytes(proc.stdout)
def inspect_source_video(base: Any, project_root: Path, output_root: Path, selector: dict[str, Any], repeat: str,
                         tools: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
    stem = f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['source_output_tag']}"
    video_path = output_root / f"{stem}.mp4"
    authoring_path = output_root / f"{stem}_authoring.json"
    manifest_path = output_root / f"{stem}_manifest.json"
    godot_log_path = output_root / f"{stem}_godot.log"
    social_path = output_root / f"{stem}_social.txt"
    launcher_probe_path = output_root / f"{stem}_ffprobe.json"
    for p in (video_path, authoring_path, manifest_path, godot_log_path, social_path, launcher_probe_path):
        require(p.is_file() and p.stat().st_size > 0, f"C11-C source capture artifact missing/empty: {p}")
    require(not list(output_root.glob("*.wav")), "Source capture folder contains WAV; native launcher was not silent")
    require(not list(output_root.glob("*.gif")) and not list(output_root.glob("*.avi")), "Source capture folder retains forbidden GIF/AVI")

    authoring = load_json(authoring_path)
    manifest = load_json(manifest_path)
    base.validate_c11c_sidecars(authoring, manifest, selector, repeat)
    godot_info = parse_godot_capture_log(godot_log_path.read_bytes(), 720, 1280, 30,
                                        selector["frame_count_consistency_only"])
    launcher_probe = load_json(launcher_probe_path)
    launcher_streams = launcher_probe.get("streams", [])
    require(len(launcher_streams) == 1 and launcher_streams[0].get("codec_type") == "video"
            and int(launcher_streams[0].get("width", 0)) == 720
            and int(launcher_streams[0].get("height", 0)) == 1280
            and launcher_streams[0].get("r_frame_rate") == "30/1"
            and int(launcher_streams[0].get("nb_frames", -1)) == selector["frame_count_consistency_only"],
            f"C11-C launcher FFprobe sidecar violates the silent source contract: {selector['family_id']} {repeat}")

    metadata = ffprobe_json(tools["ffprobe"]["path"], video_path, project_root,
                            output_root / f"{stem}_r1v_source_ffprobe.json")
    streams = metadata.get("streams", [])
    require(len(streams) == 1 and streams[0].get("codec_type") == "video", "Silent C11-C MP4 must contain exactly one video stream")
    stream = streams[0]
    require(stream.get("codec_name") == "h264" and int(stream.get("width", 0)) == 720
            and int(stream.get("height", 0)) == 1280 and stream.get("r_frame_rate") == "30/1",
            "Silent C11-C MP4 H.264/720x1280/30 contract mismatch")
    source_pix_fmt = validate_source_pixel_format(stream)
    require(int(stream.get("nb_frames", -1)) == selector["frame_count_consistency_only"], "Source FFprobe frame count mismatch")
    duration = float(metadata.get("format", {}).get("duration", stream.get("duration", 0)))
    require(abs(duration - selector["duration_seconds"]) <= 0.05, "Source MP4 duration differs from R1P timing")

    frames_args = ["-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries",
                   "frame=media_type,stream_index,key_frame,pict_type,pts,pts_time,best_effort_timestamp,best_effort_timestamp_time,pkt_dts,pkt_dts_time,pkt_duration,pkt_duration_time,width,height,pix_fmt",
                   "-of", "json", str(video_path)]
    frame_proc = run_process([tools["ffprobe"]["path"], *frames_args], project_root, timeout=1800)
    (output_root / f"{stem}_r1v_frames.stdout.json").write_bytes(frame_proc.stdout)
    (output_root / f"{stem}_r1v_frames.stderr.log").write_bytes(frame_proc.stderr)
    require(frame_proc.returncode == 0, "FFprobe frame inventory command failed")
    frame_rows = json.loads(frame_proc.stdout.decode("utf-8-sig")).get("frames", [])
    require(len(frame_rows) == selector["frame_count_consistency_only"], "Measured FFprobe frame count differs from R1P timing")
    time_base = Fraction(str(stream.get("time_base", "0/1")))
    require(time_base > 0, "Source video has invalid time_base")
    pts_rows = []
    for index, row in enumerate(frame_rows):
        token = row.get("best_effort_timestamp", row.get("pts"))
        require(token is not None, f"Frame {index} lacks PTS")
        pts = int(token)
        if pts_rows:
            require(pts > pts_rows[-1]["pts"], f"Non-increasing PTS at frame {index}")
            delta = (pts - pts_rows[-1]["pts"]) * time_base
            require(abs(float(delta) - 1.0 / 30.0) <= 0.00001, f"Non-uniform PTS interval at frame {index}")
        ts = Fraction(pts) * time_base
        pts_rows.append({"frame_index": index, "pts": pts, "time_base": f"{time_base.numerator}/{time_base.denominator}",
                         "timestamp_fraction": f"{ts.numerator}/{ts.denominator}", "timestamp_seconds": float(ts),
                         "pkt_duration": row.get("pkt_duration"), "pkt_duration_time": row.get("pkt_duration_time"),
                         "key_frame": row.get("key_frame"), "pict_type": row.get("pict_type")})

    raw_frame_size = 720 * 1280 * 3 // 2
    decode_args = ["-v", "error", "-i", str(video_path), "-map", "0:v:0", "-fps_mode", "passthrough",
                   "-pix_fmt", "yuv420p", "-f", "rawvideo", "pipe:1"]
    decode_stderr_path = output_root / f"{stem}_r1v_pixel_decode.stderr.log"
    frame_hashes = []
    global_hasher = hashlib.sha256()
    decoded_bytes = 0
    with decode_stderr_path.open("wb") as err:
        proc = subprocess.Popen([tools["ffmpeg"]["path"], *decode_args], cwd=str(project_root),
                                stdout=subprocess.PIPE, stderr=err)
        assert proc.stdout is not None
        try:
            index = 0
            while True:
                raw = read_exact(proc.stdout, raw_frame_size)
                if not raw:
                    break
                require(len(raw) == raw_frame_size, f"Truncated raw pixel frame {index}")
                digest = sha256_bytes(raw)
                frame_hashes.append(digest)
                global_hasher.update(raw)
                decoded_bytes += len(raw)
                index += 1
        finally:
            proc.stdout.close()
        decode_exit = proc.wait(timeout=1800)
    require(decode_exit == 0 and len(frame_hashes) == len(frame_rows), "FFmpeg in-memory pixel decode failed or frame count differs")
    pixel_manifest = {"schema": "C11E-R1V-PIXEL-HASH-MANIFEST-V1", "source_mp4_sha256": sha256_file(video_path),
                      "source_pixel_format": source_pix_fmt, "decode_pixel_format": "yuv420p",
                      "width": 720, "height": 1280, "frame_count": len(frame_hashes),
                      "raw_bytes_decoded": decoded_bytes, "frame_hashes": frame_hashes,
                      "global_decoded_stream_sha256": global_hasher.hexdigest(), "frames_written_to_disk": False}
    pixel_manifest_path = output_root / f"{stem}_r1v_pixel_hashes.json"
    pixel_sha = dump_json(pixel_manifest_path, pixel_manifest)
    inventory = {"schema": "C11E-R1V-ACTUAL-SOURCE-FRAME-INVENTORY-V1", "selector": selector,
                 "repeat": repeat, "source_video": {"path": str(video_path), "bytes": video_path.stat().st_size,
                 "sha256": sha256_file(video_path), "immutable": True},
                 "metadata": metadata, "godot_log_parse": godot_info,
                 "timing": {"time_base": f"{time_base.numerator}/{time_base.denominator}",
                            "frame_count": len(pts_rows), "pts": pts_rows},
                 "pixel_identity": {"pixel_format": "yuv420p (FFmpeg decoded memory representation)",
                                    "source_pixel_format": source_pix_fmt, "frame_hashes_sha256": pixel_sha,
                                    "global_decoded_stream_sha256": global_hasher.hexdigest()},
                 "launcher_sidecars": {"authoring_sha256": sha256_file(authoring_path),
                     "manifest_sha256": sha256_file(manifest_path), "godot_log_sha256": sha256_file(godot_log_path),
                     "social_sha256": sha256_file(social_path), "launcher_ffprobe_sha256": sha256_file(launcher_probe_path)},
                 "decode": {"exit_code": decode_exit, "stderr_sha256": sha256_file(decode_stderr_path),
                            "raw_pixel_bytes": decoded_bytes, "frames_written_to_disk": False}}
    inventory_path = output_root / f"{stem}_r1v_frame_inventory.json"
    inventory_sha = dump_json(inventory_path, inventory)
    final_source_sha = sha256_file(video_path)
    require(final_source_sha == pixel_manifest["source_mp4_sha256"], "Source MP4 changed during read-only inspection")
    return {"family_id": selector["family_id"], "grammar_id": selector["grammar_id"], "repeat": repeat,
            "source_output_root": str(output_root), "source_video_path": str(video_path),
            "source_video_sha256": final_source_sha, "source_video_bytes": video_path.stat().st_size,
            "frame_count": len(pts_rows), "pts": [x["pts"] for x in pts_rows],
            "time_base": f"{time_base.numerator}/{time_base.denominator}",
            "pixel_frame_hashes": frame_hashes, "global_pixel_stream_sha256": global_hasher.hexdigest(),
            "inventory_path": str(inventory_path), "inventory_sha256": inventory_sha,
            "pixel_manifest_path": str(pixel_manifest_path), "pixel_manifest_sha256": pixel_sha,
            "source_video_stream": stream, "source_container_duration": duration,
            "launcher_sidecars_sha256": inventory["launcher_sidecars"], "godot_log_parse": godot_info,
            "decode_exit_code": decode_exit, "decode_stderr_sha256": sha256_file(decode_stderr_path)}
