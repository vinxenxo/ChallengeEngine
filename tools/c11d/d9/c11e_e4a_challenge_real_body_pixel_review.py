#!/usr/bin/env python3
"""C11-E E4A.2 test-only pixel review over one real C11-C Challenge render.

The C11-C generator remains unmodified and writes only to a fresh artifacts/tests
root. The D-owned test consumer reads E1/D9.9 intents and the approved E4A field
policy, then applies test-only header/footer overlays to selected decoded frames.
It does not call D9.10 dispatch or create a production deliverable.
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
import uuid
import zlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
PREVIOUS_RUNNER = Path("tools/c11d/d9/c11e_e4a_challenge_pixel_review.py")
PREVIOUS_RUNNER_SHA256 = "939a12f369df9eaa0dbaf5b06b0635a0d4dc906e14fd7d5bdf9c12b3ec2b97a0"
E1_SERVICE = Path("c11c-suite/c11c-producer/c11e_production_service.py")
E1_SERVICE_SHA256 = "f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0"
D99_RESOLVER = Path("tools/c11d/d9/universal_producer.py")
D99_RESOLVER_SHA256 = "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1"
C11C_RENDERER = Path("tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1")
MAIN_SOURCE = Path("c11c-suite/c11c-producer/main.py")
MAIN_SOURCE_SHA256 = "f0adc54de884d6d812396707cd6ced49038df0f52e4a9bc516a9ca5e6a0ddcd3"
CHALLENGE_SOURCE = Path("challenges/CHALLENGE_004.json")
APPROVAL_SOURCE = Path("definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json")
LAYOUT_SOURCE = Path("docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md")
MANIFEST_SOURCE = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")

MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CHALLENGE_SHA256 = "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
APPROVAL_SHA256 = "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
LAYOUT_SHA256 = "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
DELIVERY_PROFILE = "REVIEW_720"
DELIVERY_FPS = 30
DELIVERY_WIDTH = 720
DELIVERY_HEIGHT = 1280
EXPECTED_DELIVERY_FRAMES = 450

REGIONS = {
    "HEADER": (0, 0, 720, 192),
    "BODY": (0, 192, 720, 1088),
    "FOOTER": (0, 1088, 720, 1280),
}

class RealBodyReviewError(RuntimeError):
    pass

@dataclass(frozen=True)
class Png:
    width: int
    height: int
    channels: int
    pixels: bytes


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise RealBodyReviewError(f"Expected JSON object: {path}")
    return value


def import_previous_runner(root: Path = ROOT):
    path = root / PREVIOUS_RUNNER
    spec = importlib.util.spec_from_file_location("c11e_e4a_previous_pixel_runner", path)
    if spec is None or spec.loader is None:
        raise RealBodyReviewError("Cannot load the existing E4A E1/D9.9 intent helper")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_authorities(root: Path = ROOT) -> dict[str, str]:
    prior = import_previous_runner(root)
    prior.validate_static_authorities(root)
    pins = {
        "frozen_manifest": (MANIFEST_SOURCE, MANIFEST_SHA256),
        "challenge_004": (CHALLENGE_SOURCE, CHALLENGE_SHA256),
        "approved_policy": (APPROVAL_SOURCE, APPROVAL_SHA256),
        "d1_5_layout": (LAYOUT_SOURCE, LAYOUT_SHA256),
    }
    observed: dict[str, str] = {}
    for label, (relative, expected) in pins.items():
        path = root / relative
        actual = sha256_file(path)
        if actual != expected:
            raise RealBodyReviewError(f"Authority pin mismatch for {relative.as_posix()}: {actual}")
        observed[label] = actual
    for rel in (C11C_RENDERER, MAIN_SOURCE, PREVIOUS_RUNNER, E1_SERVICE, D99_RESOLVER):
        if not (root / rel).is_file():
            raise RealBodyReviewError(f"Required current-checkout source is missing: {rel.as_posix()}")
    source_pins = {
        "producer_main": (MAIN_SOURCE, MAIN_SOURCE_SHA256),
        "previous_e4a_runner": (PREVIOUS_RUNNER, PREVIOUS_RUNNER_SHA256),
        "shared_e1_service": (E1_SERVICE, E1_SERVICE_SHA256),
        "canonical_d99_resolver": (D99_RESOLVER, D99_RESOLVER_SHA256),
    }
    for label, (relative, expected) in source_pins.items():
        actual = sha256_file(root / relative)
        if actual != expected:
            raise RealBodyReviewError(f"Source pin mismatch for {relative.as_posix()}: {actual}")
        observed[label] = actual
    return observed


def source_timeline(challenge: Mapping[str, Any]) -> tuple[list[dict[str, Any]], int, float]:
    video = challenge.get("video")
    if not isinstance(video, Mapping):
        raise RealBodyReviewError("CHALLENGE_004 has no video timeline")
    source_fps = video.get("fps")
    if isinstance(source_fps, bool) or not isinstance(source_fps, (int, float)) or source_fps <= 0:
        raise RealBodyReviewError("Challenge source fps is invalid")
    phases = [("HOOK", "hook_duration"), ("GAME", "game_duration"), ("REVEAL", "reveal_duration"), ("CTA", "cta_duration")]
    cursor = 0.0
    result: list[dict[str, Any]] = []
    for name, key in phases:
        duration = video.get(key)
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration <= 0:
            raise RealBodyReviewError(f"Challenge phase duration is invalid: {key}")
        start = cursor
        cursor += float(duration)
        result.append({
            "phase": name,
            "start_seconds": start,
            "end_seconds": cursor,
            "start_source_frame": round(start * float(source_fps)),
            "end_source_frame_exclusive": round(cursor * float(source_fps)),
        })
    total_source_frames = round(cursor * float(source_fps))
    return result, int(source_fps), cursor


def sample_frames(timeline: list[dict[str, Any]], delivery_fps: int) -> list[dict[str, Any]]:
    by_name = {row["phase"]: row for row in timeline}
    result = []
    for name, sample in (
        ("HOOK", "first"), ("HOOK", "last"), ("GAME", "first"),
        ("REVEAL", "first"), ("CTA", "first"), ("CTA", "last"),
    ):
        phase = by_name[name]
        start = round(phase["start_seconds"] * delivery_fps)
        end_exclusive = round(phase["end_seconds"] * delivery_fps)
        index = start if sample == "first" else end_exclusive - 1
        result.append({
            "sample": f"{name.lower()}_{sample}",
            "phase": name,
            "boundary": sample,
            "delivery_frame": index,
            "source_time_seconds": index / delivery_fps,
        })
    return result


def e1_intent_map(intents: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result = {str(item.get("id")): item.get("intent", {}) for item in intents}
    if set(result) != {"A", "B", "C"}:
        raise RealBodyReviewError("E1 intent family must contain A/B/C")
    a, b, c = (result[k] for k in ("A", "B", "C"))
    for field in ("title", "subtitle", "call_to_action"):
        if b["editorial"].get(field) != c["editorial"].get(field):
            raise RealBodyReviewError(f"B/C visible field mismatch: {field}")
    if b["editorial"].get("language") == c["editorial"].get("language"):
        raise RealBodyReviewError("B/C language metadata did not vary")
    for item in (a, b, c):
        if item.get("status") != "PREPARED_E1_NOT_DISPATCHED":
            raise RealBodyReviewError("An E1 intent crossed the dispatch boundary")
    return result


def approved_draw_fields(policy: Mapping[str, Any], editorial: Mapping[str, Any], phase: str) -> list[dict[str, str]]:
    rows = {row.get("field"): row for row in policy.get("fields", []) if isinstance(row, Mapping)}
    result: list[dict[str, str]] = []
    for field in ("title", "subtitle", "call_to_action"):
        row = rows.get(field, {})
        value = editorial.get(field)
        if not isinstance(value, str) or not value.strip():
            continue
        if phase in row.get("source_phase_windows", []) and row.get("region") in ("HEADER", "FOOTER"):
            result.append({"field": field, "value": value, "region": str(row["region"])})
    return result


def _filter_path(path: Path | str) -> str:
    raw = str(path)
    # Preserve explicit Windows drive paths even when unit-tested on POSIX.
    if not (len(raw) >= 3 and raw[0].isalpha() and raw[1] == ":" and raw[2] in ("/", "\\")):
        raw = str(Path(raw).resolve())
    value = raw.replace("\\", "/")
    if len(value) >= 2 and value[1] == ":":
        value = value[0] + r"\:" + value[2:]
    return value.replace("'", r"\'")


def build_drawtext_filter(frame_index: int, draws: list[dict[str, str]], text_files: Mapping[str, Path], font_file: Path) -> str:
    filters = [f"select=eq(n\\,{int(frame_index)})"]
    font = _filter_path(font_file)
    for draw in draws:
        field = draw["field"]
        textfile = _filter_path(text_files[field])
        if draw["region"] == "HEADER":
            if field == "title":
                size, y = 34, 28
            else:
                size, y = 25, 91
        elif draw["region"] == "FOOTER":
            size, y = 34, "h-78"
        else:
            raise RealBodyReviewError(f"Field escaped approved regions: {field}")
        filters.append(
            "drawtext="
            f"fontfile='{font}':textfile='{textfile}':fontsize={size}:fontcolor=white:"
            f"borderw=2:bordercolor=black:x=(w-text_w)/2:y={y}"
        )
    return ",".join(filters)


def decode_png(path: Path) -> Png:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise RealBodyReviewError(f"Not a PNG file: {path.name}")
    offset = 8
    width = height = bit_depth = color_type = interlace = None
    idat = bytearray()
    while offset + 12 <= len(data):
        length = int.from_bytes(data[offset:offset + 4], "big")
        tag = data[offset + 4:offset + 8]
        chunk = data[offset + 8:offset + 8 + length]
        if len(chunk) != length:
            raise RealBodyReviewError(f"Truncated PNG chunk: {path.name}")
        if tag == b"IHDR":
            width = int.from_bytes(chunk[0:4], "big")
            height = int.from_bytes(chunk[4:8], "big")
            bit_depth, color_type = chunk[8], chunk[9]
            interlace = chunk[12]
        elif tag == b"IDAT":
            idat.extend(chunk)
        elif tag == b"IEND":
            break
        offset += length + 12
    if not width or not height or bit_depth != 8 or color_type not in (2, 6) or interlace != 0:
        raise RealBodyReviewError(f"Unsupported PNG encoding in {path.name}; expected 8-bit RGB/RGBA, non-interlaced")
    channels = 3 if color_type == 2 else 4
    stride = width * channels
    raw = zlib.decompress(bytes(idat))
    if len(raw) != height * (stride + 1):
        raise RealBodyReviewError(f"Unexpected PNG decompressed size in {path.name}")
    rows: list[bytearray] = []
    pos = 0
    for y in range(height):
        filter_type = raw[pos]
        pos += 1
        scan = bytearray(raw[pos:pos + stride])
        pos += stride
        prev = rows[y - 1] if y else bytearray(stride)
        if filter_type == 1:
            for x in range(stride):
                left = scan[x - channels] if x >= channels else 0
                scan[x] = (scan[x] + left) & 255
        elif filter_type == 2:
            for x in range(stride):
                scan[x] = (scan[x] + prev[x]) & 255
        elif filter_type == 3:
            for x in range(stride):
                left = scan[x - channels] if x >= channels else 0
                scan[x] = (scan[x] + ((left + prev[x]) // 2)) & 255
        elif filter_type == 4:
            for x in range(stride):
                left = scan[x - channels] if x >= channels else 0
                up = prev[x]
                upper_left = prev[x - channels] if x >= channels else 0
                p = left + up - upper_left
                pa, pb, pc = abs(p - left), abs(p - up), abs(p - upper_left)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else upper_left
                scan[x] = (scan[x] + predictor) & 255
        elif filter_type != 0:
            raise RealBodyReviewError(f"Unknown PNG row filter {filter_type} in {path.name}")
        rows.append(scan)
    return Png(width, height, channels, b"".join(rows))


def pixel_compare(a: Png, b: Png, allowed_rect: tuple[int, int, int, int] | None) -> dict[str, int]:
    if (a.width, a.height, a.channels) != (b.width, b.height, b.channels):
        raise RealBodyReviewError("PNG dimensions or channel count differ")
    changed = inside = outside = body = 0
    for y in range(a.height):
        for x in range(a.width):
            start = (y * a.width + x) * a.channels
            if a.pixels[start:start + a.channels] == b.pixels[start:start + a.channels]:
                continue
            changed += 1
            if allowed_rect is not None and allowed_rect[0] <= x < allowed_rect[2] and allowed_rect[1] <= y < allowed_rect[3]:
                inside += 1
            else:
                outside += 1
            if REGIONS["BODY"][0] <= x < REGIONS["BODY"][2] and REGIONS["BODY"][1] <= y < REGIONS["BODY"][3]:
                body += 1
    return {"changed_pixels": changed, "changed_inside_allowed_region": inside, "changed_outside_allowed_region": outside, "changed_body_pixels": body}


def run_command(command: list[str], cwd: Path, stdout_path: Path, stderr_path: Path) -> int:
    process = subprocess.run(command, cwd=str(cwd), capture_output=True, check=False)
    stdout_path.write_bytes(process.stdout)
    stderr_path.write_bytes(process.stderr)
    return int(process.returncode)


def parse_rate(value: str) -> float:
    try:
        num, den = value.split("/", 1)
        return float(num) / float(den)
    except Exception as exc:
        raise RealBodyReviewError(f"Invalid frame rate: {value}") from exc


def probe_video(ffprobe: str, video_path: Path, evidence_dir: Path, root: Path) -> dict[str, Any]:
    command = [ffprobe, "-v", "error", "-count_frames", "-show_entries",
               "stream=codec_type,codec_name,width,height,pix_fmt,avg_frame_rate,r_frame_rate,nb_read_frames,duration",
               "-show_entries", "format=duration", "-of", "json", str(video_path)]
    proc = subprocess.run(command, cwd=str(root), capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    (evidence_dir / "ffprobe.stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (evidence_dir / "ffprobe.stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise RealBodyReviewError(f"FFprobe failed ({proc.returncode}): {proc.stderr[-2000:]}")
    payload = json.loads(proc.stdout)
    streams = payload.get("streams", [])
    if len(streams) != 1 or streams[0].get("codec_type") != "video":
        raise RealBodyReviewError(f"Expected exactly one video stream and no audio, got {streams}")
    stream = streams[0]
    frames = int(stream.get("nb_read_frames", -1))
    rate = parse_rate(str(stream.get("avg_frame_rate", "0/0")))
    duration = float(payload.get("format", {}).get("duration", stream.get("duration", 0)))
    metadata = {"codec_name": stream.get("codec_name"), "width": stream.get("width"), "height": stream.get("height"),
                "pix_fmt": stream.get("pix_fmt"), "avg_frame_rate": stream.get("avg_frame_rate"),
                "nb_read_frames": frames, "duration_seconds": duration, "video_path": str(video_path)}
    if metadata["codec_name"] != "h264" or metadata["width"] != DELIVERY_WIDTH or metadata["height"] != DELIVERY_HEIGHT:
        raise RealBodyReviewError(f"Unexpected C11-C review video codec/geometry: {metadata}")
    if metadata["pix_fmt"] != "yuv420p":
        raise RealBodyReviewError(f"Unexpected C11-C review pixel format: {metadata['pix_fmt']}; expected yuv420p")
    if abs(rate - DELIVERY_FPS) > 0.0001 or frames != EXPECTED_DELIVERY_FRAMES or abs(duration - 15.0) > 0.08:
        raise RealBodyReviewError(f"Unexpected C11-C review timebase/duration: {metadata}")
    return metadata


def extract_frame(ffmpeg: str, video_path: Path, frame_index: int, output: Path,
                  draws: list[dict[str, str]] | None, text_files: Mapping[str, Path], font_file: Path,
                  root: Path, evidence_dir: Path, label: str) -> dict[str, Any]:
    filters = f"select=eq(n\\,{frame_index})"
    if draws:
        filters = build_drawtext_filter(frame_index, draws, text_files, font_file)
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(video_path), "-vf", filters,
               "-frames:v", "1", "-fps_mode", "passthrough", "-y", str(output)]
    logbase = evidence_dir / "commands" / label
    logbase.parent.mkdir(parents=True, exist_ok=True)
    exit_code = run_command(command, root, logbase.with_suffix(".stdout.txt"), logbase.with_suffix(".stderr.txt"))
    if exit_code != 0 or not output.is_file():
        err = logbase.with_suffix(".stderr.txt").read_text(encoding="utf-8", errors="replace")
        raise RealBodyReviewError(f"FFmpeg frame extraction failed ({label}, exit={exit_code}): {err[-2000:]}")
    return {"command": command, "exit_code": exit_code, "sha256": sha256_file(output), "path": str(output)}


def generate_run(root: Path, ffmpeg_arg: str | None, ffprobe_arg: str | None, powershell_arg: str | None) -> int:
    authorities = validate_authorities(root)
    powershell = powershell_arg or shutil.which("powershell.exe") or shutil.which("powershell")
    ffmpeg = ffmpeg_arg or os.environ.get("C11E_FFMPEG_EXECUTABLE") or shutil.which("ffmpeg.exe") or shutil.which("ffmpeg")
    ffprobe = ffprobe_arg or os.environ.get("C11E_FFPROBE_EXECUTABLE") or shutil.which("ffprobe.exe") or shutil.which("ffprobe")
    if not powershell:
        raise RealBodyReviewError("powershell.exe is required to invoke the existing C11-C generator")
    if not ffmpeg or not ffprobe:
        raise RealBodyReviewError("FFmpeg and FFprobe must be resolvable on PATH or passed explicitly")
    font_file = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / "arial.ttf"
    if not font_file.is_file():
        raise RealBodyReviewError(f"Test font not found: {font_file}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    evidence_dir = root / "artifacts" / "tests" / "c11e" / "e4a_real_body_pixel_review" / ("RUN_" + stamp)
    evidence_dir.mkdir(parents=True, exist_ok=False)
    base_dir = evidence_dir / "c11c_base_render"
    base_dir.mkdir()

    previous = import_previous_runner(root)
    challenge = load_json(root / CHALLENGE_SOURCE)
    policy = load_json(root / APPROVAL_SOURCE)
    timeline, source_fps, total_seconds = source_timeline(challenge)
    if total_seconds != 15.0 or source_fps != 60:
        raise RealBodyReviewError(f"Pinned CHALLENGE_004 timebase drift: fps={source_fps}, duration={total_seconds}")
    samples = sample_frames(timeline, DELIVERY_FPS)
    intents = previous.build_three_e1_intents(root)
    intent_by_id = e1_intent_map(intents)
    for item in intents:
        write_json(evidence_dir / f"e1_intent_{item['id']}.json", item["intent"])

    script = root / C11C_RENDERER
    frozen_manifest_path = root / MANIFEST_SOURCE
    frozen_manifest_before = sha256_file(frozen_manifest_path)
    if frozen_manifest_before != MANIFEST_SHA256:
        raise RealBodyReviewError("Frozen C11-C manifest does not match the accepted baseline")
    c11c_script_sha_before = sha256_file(script)
    main_source_sha_before = sha256_file(root / MAIN_SOURCE)
    base_command = [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                    "-ChallengeId", "CHALLENGE_004", "-Seed", "314159", "-DeliveryProfile", DELIVERY_PROFILE,
                    "-OutputRoot", str(base_dir), "-NoSound"]
    render = subprocess.run(base_command, cwd=str(root), capture_output=True, text=True,
                            encoding="utf-8", errors="replace", check=False)
    (evidence_dir / "c11c_generator.stdout.txt").write_text(render.stdout, encoding="utf-8")
    (evidence_dir / "c11c_generator.stderr.txt").write_text(render.stderr, encoding="utf-8")
    if render.returncode != 0:
        raise RealBodyReviewError(f"Existing C11-C Challenge generator failed (exit={render.returncode}); evidence={evidence_dir}")
    frozen_manifest_after = sha256_file(frozen_manifest_path)
    c11c_script_sha_after = sha256_file(script)
    main_source_sha_after = sha256_file(root / MAIN_SOURCE)
    if frozen_manifest_after != frozen_manifest_before:
        raise RealBodyReviewError("Frozen C11-C manifest changed during isolated test generation")
    if c11c_script_sha_after != c11c_script_sha_before or main_source_sha_after != main_source_sha_before:
        raise RealBodyReviewError("C11-C producer source changed during isolated test generation")
    mp4s = sorted(base_dir.rglob("*.mp4"))
    if len(mp4s) != 1:
        raise RealBodyReviewError(f"Expected exactly one test-only C11-C MP4 under {base_dir}; found {len(mp4s)}")
    video_path = mp4s[0]
    manifest_path = video_path.parent / "production_manifest.json"
    if not manifest_path.is_file():
        raise RealBodyReviewError("C11-C test output is missing its production_manifest.json")
    c_manifest = load_json(manifest_path)
    if c_manifest.get("delivery_profile") != DELIVERY_PROFILE:
        raise RealBodyReviewError("C11-C output production_manifest.json delivery_profile is not REVIEW_720")
    video = probe_video(ffprobe, video_path, evidence_dir, root)

    text_dir = evidence_dir / "text"
    text_dir.mkdir()
    text_files: dict[str, Path] = {}
    for field in ("title", "subtitle", "call_to_action"):
        text_path = text_dir / f"{field}.txt"
        text_path.write_text(str(intent_by_id["B"]["editorial"].get(field, "")), encoding="utf-8")
        text_files[field] = text_path

    image_dir = evidence_dir / "png"
    image_dir.mkdir()
    artifacts: list[dict[str, Any]] = []
    for sample in samples:
        phase = sample["phase"]
        frame_index = sample["delivery_frame"]
        for variant in ("A", "B", "C"):
            out = image_dir / f"{variant}_{sample['sample']}.png"
            draws = [] if variant == "A" else approved_draw_fields(policy, intent_by_id[variant]["editorial"], phase)
            details = extract_frame(ffmpeg, video_path, frame_index, out, draws, text_files, font_file,
                                    root, evidence_dir, f"{variant}_{sample['sample']}")
            png = decode_png(out)
            if (png.width, png.height) != (DELIVERY_WIDTH, DELIVERY_HEIGHT):
                raise RealBodyReviewError(f"Unexpected PNG dimensions: {out.name} {png.width}x{png.height}")
            artifacts.append({"variant": variant, "sample": sample["sample"], "phase": phase,
                              "delivery_frame": frame_index, "width": png.width, "height": png.height,
                              "sha256": details["sha256"], "path": str(out.relative_to(root)).replace("\\", "/")})

    artifact_map = {(x["variant"], x["sample"]): root / x["path"] for x in artifacts}
    comparisons: list[dict[str, Any]] = []
    for sample in samples:
        name, phase = sample["sample"], sample["phase"]
        a = decode_png(artifact_map[("A", name)])
        b = decode_png(artifact_map[("B", name)])
        c = decode_png(artifact_map[("C", name)])
        allowed = REGIONS["HEADER"] if phase == "HOOK" else REGIONS["FOOTER"] if phase == "CTA" else None
        ab = pixel_compare(a, b, allowed)
        bc = pixel_compare(b, c, None)
        positive = phase in ("HOOK", "CTA")
        success = (ab["changed_pixels"] > 0 and ab["changed_outside_allowed_region"] == 0
                   and ab["changed_body_pixels"] == 0) if positive else (ab["changed_pixels"] == 0)
        if bc["changed_pixels"] != 0:
            success = False
        comparisons.append({"comparison": f"A_TO_B_{name.upper()}", "allowed_region": phase if positive else "NONE",
                            **ab, "success": success})
        comparisons.append({"comparison": f"B_TO_C_{name.upper()}_METADATA_AND_BLOCKED_FIELDS_NO_PIXELS",
                            "allowed_region": "NONE", **bc, "success": bc["changed_pixels"] == 0})
        if not success or bc["changed_pixels"] != 0:
            raise RealBodyReviewError(f"Real-body pixel comparison failed at {name}: A/B={ab}; B/C={bc}")

    body_hashes = []
    for sample in samples:
        for variant in ("A", "B", "C"):
            image = decode_png(artifact_map[(variant, sample["sample"])])
            x0, y0, x1, y1 = REGIONS["BODY"]
            rows = []
            stride = image.width * image.channels
            for y in range(y0, y1):
                rows.append(image.pixels[y * stride + x0 * image.channels:y * stride + x1 * image.channels])
            body_hashes.append({"variant": variant, "sample": sample["sample"],
                                "body_crop_sha256": sha256_bytes(b"".join(rows))})

    report = {
        "schema": "C11E-E4A-REAL-BODY-PIXEL-REPORT-V1", "status": "PASS_ISOLATED_REAL_C11C_BODY_PIXEL_PROOF_TEST_ONLY",
        "scope": "CHALLENGE_004_ONE_C11C_REVIEW_720_TEST_MP4_WITH_D_POLICY_DRIVEN_STILL_FRAME_OVERLAYS",
        "authorities": authorities,
        "challenge": {"id": "CHALLENGE_004", "mechanic": "parking_v2", "source_fps": source_fps,
                      "timeline": timeline, "duration_seconds": total_seconds},
        "c11c_generator": {"source_script": C11C_RENDERER.as_posix(), "source_script_sha256": c11c_script_sha_before,
                           "source_script_sha256_after": c11c_script_sha_after,
                           "producer_main_sha256": main_source_sha_before, "producer_main_sha256_after": main_source_sha_after,
                           "frozen_manifest_sha256_before": frozen_manifest_before,
                           "frozen_manifest_sha256_after": frozen_manifest_after, "command": base_command,
                           "exit_code": render.returncode, "test_media_path": str(video_path),
                           "test_media_sha256": sha256_file(video_path), "test_manifest_sha256": sha256_file(manifest_path)},
        "delivery_video": video,
        "sample_frames": samples,
        "regions_720x1280": {k: {"x0": v[0], "y0": v[1], "x1": v[2], "y1": v[3]} for k, v in REGIONS.items()},
        "field_dispositions": [
            {"field": "title", "status": "TEST_PIXEL_DRAW", "region": "HEADER", "phase": "HOOK"},
            {"field": "subtitle", "status": "TEST_PIXEL_DRAW", "region": "HEADER", "phase": "HOOK"},
            {"field": "call_to_action", "status": "TEST_PIXEL_DRAW", "region": "FOOTER", "phase": "CTA"},
            {"field": "player_name", "status": "BLOCKED_GEOMETRY_UNRESOLVED", "region": "CHALLENGE_OVERLAY"},
            {"field": "challenge_label", "status": "BLOCKED_GEOMETRY_UNRESOLVED", "region": "CHALLENGE_OVERLAY"},
            {"field": "language", "status": "METADATA_ONLY"},
        ],
        "pixel_artifacts": artifacts, "pixel_comparisons": comparisons, "body_crop_hashes": body_hashes,
        "invariants": {"real_gameplay_body_rasterized": True, "body_pixels_A_B_identical_at_all_six_samples": True,
                       "body_pixels_A_B_identical_at_sampled_gameplay_and_reveal": True,
                       "only_approved_header_hook_and_footer_cta_regions_changed": True,
                       "language_has_no_pixel_effect": True, "challenge_overlay_has_no_pixel_effect": True,
                       "c11c_source_mutation": False, "d9_10_dispatch_invoked": False,
                       "d_production_renderer_activated": False, "production_media_created": False,
                       "test_media_created": True, "test_only_typography_not_production_layout": True},
        "governance": {"production_renderer": False, "production_dispatch": False, "production_media_created": False,
                       "test_media_created": True, "d4_8": "BLOCKED", "d9_10": "PREPARE_ONLY",
                       "d9_14": "BLOCKED", "d9_16": "BLOCKED", "d9_17": "BLOCKED_NO_GO",
                       "d10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE"},
    }
    report_path = evidence_dir / "C11E_E4A_REAL_BODY_PIXEL_REPORT.json"
    write_json(report_path, report)
    receipt = {
        "schema": "C11E-E4A-REAL-BODY-PIXEL-RUNNER-RECEIPT-V1", "status": report["status"],
        "c11c_generator_exit_code": render.returncode, "c11c_generator_stdout_sha256": sha256_file(evidence_dir / "c11c_generator.stdout.txt"),
        "c11c_generator_stderr_sha256": sha256_file(evidence_dir / "c11c_generator.stderr.txt"),
        "ffprobe_report_path": str((evidence_dir / "ffprobe.stdout.txt").relative_to(root)).replace("\\", "/"),
        "ffprobe_exit_code": 0,
        "ffprobe_stdout_sha256": sha256_file(evidence_dir / "ffprobe.stdout.txt"),
        "ffprobe_stderr_sha256": sha256_file(evidence_dir / "ffprobe.stderr.txt"),
        "base_video_sha256": video["video_path"] and sha256_file(video_path),
        "pixel_png_count": len(artifacts), "pixel_comparison_count": len(comparisons),
        "body_crop_hash_count": len(body_hashes), "report_sha256": sha256_file(report_path),
        "governance": report["governance"],
    }
    receipt_path = evidence_dir / "C11E_E4A_REAL_BODY_PIXEL_RUNNER_RECEIPT.json"
    write_json(receipt_path, receipt)
    sums = []
    for path in sorted(evidence_dir.rglob("*")):
        if path.is_file() and path.name not in ("SHA256SUMS.txt",):
            sums.append(f"{sha256_file(path)}  {path.relative_to(root).as_posix()}")
    (evidence_dir / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print("C11E_E4A_REAL_BODY_PIXEL_REVIEW=PASS_ISOLATED_TEST_ONLY")
    print("C11C_BASE=1_REVIEW_720_H264_720x1280_30FPS_450_FRAMES")
    print("REAL_GAMEPLAY_BODY=RASTERIZED")
    print("PIXEL_PNGS=18/18 @ 720x1280")
    print("PIXEL_COMPARISONS=12/12")
    print("BODY_PIXEL_IDENTITY=PASS_AT_6_SAMPLED_SOURCE_TIMEPOINTS")
    print("D_FIELDS=title/subtitle=HEADER/HOOK; call_to_action=FOOTER/CTA")
    print("CHALLENGE_OVERLAY=BLOCKED_GEOMETRY_UNRESOLVED")
    print("PRODUCTION_RENDERER=false; D9.10=PREPARE_ONLY; RELEASE_AUTHORITY=NONE")
    print(f"EVIDENCE_DIR={evidence_dir}")
    print(f"RECEIPT_SHA256={sha256_file(receipt_path)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", help="FFmpeg executable; defaults to PATH")
    parser.add_argument("--ffprobe", help="FFprobe executable; defaults to PATH")
    parser.add_argument("--powershell", help="PowerShell executable; defaults to PATH")
    args = parser.parse_args()
    try:
        return generate_run(ROOT, args.ffmpeg, args.ffprobe, args.powershell)
    except Exception as exc:
        print(f"C11E_E4A_REAL_BODY_PIXEL_REVIEW=FAIL {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
