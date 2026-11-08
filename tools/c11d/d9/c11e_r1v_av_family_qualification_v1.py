#!/usr/bin/env python3
"""C11-E R1V integrated Visual Loop A/V qualification.

One bounded, fail-closed workflow for five first-family selectors, repeats A/B.
It reuses the already-produced Fractal Bloom A silent source capture, creates the
remaining nine C11-C silent source captures with the original pinned launchers,
then immediately generates the existing C11-C FAMILY_MUSIC_V4 soundtrack using
the R1P music_seed and muxes it into a separate A/V MP4. Video is stream-copied;
there are no filters, video re-encodes, D composition, D3 V5, or production dispatch.
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

HERE = Path(__file__).resolve().parent
BASE_RELATIVE = "tools/c11d/d9/c11e_r1v_five_family_qualification_v3.py"
BASE_RUNNER_BYTES = 89479
BASE_RUNNER_SHA256 = "9d1baba14ca8cf96e3f2f466cedc104ec4b9cf1b94ef4b11690abe7a6de9e019"
FROZEN_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
STATIC_AUDIT_SHA256 = "600c22dafe2e377cb02b4a69f8823a44745d705b71cdb0d6bcec38da52df3e92"
R1P_RECOVERED_ZIP_SHA256 = "d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52"
R1P_RUN_ID = "E4B_R1P_20261107_032743_5F75045C"
OPTION_C_REPORT_SHA256 = "ba76c626d92736c2f139380ec2b93d865015e8ef7e53f2881fdb16b6c4a54246"
OPTION_C_PROCESS_RECEIPT_SHA256 = "db1cc4b8393f84d944391efdd6daa325e0ed9a5aac69ce7b0d7efc9ed9ea9355"
OPTION_C_INSTALL_RECEIPT_SHA256 = "30c6531129a08d3ce347432ddb4d5a26155f92dc89863828398cbfc2a8dfe6a7"
OPTION_C_PACKAGE_MANIFEST_SHA256 = "b34bd464f0e23c8bba592d8620a56801b54c35f75d9140567949c0622447e695"
R1V_SILENT_POLICY_SHA256 = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
R1V_SILENT_APPROVAL_RAW_SHA256 = "fc26f9af81658f4a4e24977c5f3dbcd800bc11eb511062cff3918d1d69ae5789"
AUDIO_SCOPE_POLICY_SHA256 = "c0a6a1e2391b0528347fc3a0a8e5b10b0c691e90131d0a0afbaaacfd15ec9905"
AUDIO_SCOPE_APPROVAL_RAW_SHA256 = "6a0081a5a769a1b2efdc2cc6c2f807e57fd8af541bbba211c310cf6781e3c132"
C11D_PRODUCTION_POLICY_SHA256 = "cf970424b1b079d80cda41085a700129e094e90c87e48b04122c5acdabebae16"
PRIOR_R1V_RUN_ID = "R1V_Q5_20261107_235828_6DE382A1"
PRIOR_R1V_REPORT_SHA256 = "19b96a87be957a3c97f57828991651aaa72baec08a33a099f145263d89f71ebb"
PRIOR_R1V_PROCESS_RECEIPT_SHA256 = "c22404dca13f34216769d87b311ae81670adc6102fda72851d3156ed83907134"
PRIOR_FRACTAL_A_MP4_SHA256 = "7971ced1d9cdbb7dd76a0d8d76e766faa9a051fc27419c9e737c41264796f659"
PRIOR_FRACTAL_A_STDOUT_SHA256 = "76fd7a7a1f2be677046e7e1954129ad2ac16544fb68d908ee70700dc377b35ae"

AUDIO_SOURCE_PINS = {
    "tools/prototypes/c11c_common/C11CSafeAmbient.py": {
        "bytes": 1739, "sha256": "c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c"},
    "tools/prototypes/c11c_common/generate_c11c_family_music.py": {
        "bytes": 16382, "sha256": "41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d"},
    "profiles/presentation/c11c_visual_music_profiles.json": {
        "bytes": 7038, "sha256": "b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58"},
}

EXPECTED_AUDIO_ROUTE = {
    "fractal": "ORGANIC_BLOOM",
    "geometric": "CIRCUIT_PULSE",
    "invisible_forces": "FLOWING_VECTOR",
    "living_particles": "ORGANIC_BLOOM",
    "sacred_symmetry": "ORBITAL_RITUAL",
}

class AVQualificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AVQualificationError(message)


def build_run_id(now: datetime | None = None, token: str | None = None) -> str:
    """Use a compact, collision-resistant run folder ID to stay below Win32 MAX_PATH.

    The full UTC timestamp remains in every receipt. The 6-hex random suffix and
    existing fail-closed output-root collision check preserve uniqueness.
    """
    moment = now or datetime.now()
    suffix = (token or uuid.uuid4().hex[:6]).upper()
    require(bool(re.fullmatch(r"[0-9A-F]{6}", suffix)), "R1V run token must be exactly six hexadecimal characters")
    return f"Q5_{moment.strftime('%H%M%S')}_{suffix}"


def windows_path_budget(project_root: str | Path, run_id: str, selectors: list[dict[str, Any]],
                        prior_source_tag: str) -> dict[str, Any]:
    """Calculate the longest planned artifact path using Win32 path semantics."""
    root = PureWindowsPath(str(project_root))
    evidence_root = root / "artifacts" / "tests" / "c11e" / "r1v_av_five_family_qualification" / run_id
    candidates: list[tuple[str, int]] = []
    for selector in selectors:
        key = selector["source_folder_key"]
        for repeat in ("A", "B"):
            tag = f"{run_id}_{key.upper()}_{repeat}"
            source_tag = prior_source_tag if selector["family_id"] == "c11c_fractal_bloom_v1" and repeat == "A" else tag
            stem = f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{source_tag}"
            source_root = evidence_root / "source" / key / repeat
            audio_root = evidence_root / "audio" / key / repeat
            delivery_root = evidence_root / "delivery" / key / repeat
            source_names = [f"{stem}.mp4", f"{stem}_authoring.json", f"{stem}_manifest.json",
                            f"{stem}_godot.log", f"{stem}_social.txt", f"{stem}_ffprobe.json",
                            f"{stem}_r1v_source_ffprobe.json", f"{stem}_r1v_source_ffprobe.json.stderr.log",
                            f"{stem}_r1v_frames.stdout.json", f"{stem}_r1v_frames.stderr.log",
                            f"{stem}_r1v_pixel_decode.stderr.log"]
            for name in source_names:
                p = source_root / name
                candidates.append((str(p), len(str(p))))
            wav = audio_root / f"{tag}_family_music.wav"
            mux = delivery_root / f"{tag}_C11C_FAMILY_MUSIC_AV.mp4"
            final_probe = delivery_root / f"{tag}_final_av_ffprobe.json.stderr.log"
            candidates.extend((str(p), len(str(p))) for p in (wav, mux, final_probe))
    longest = max(candidates, key=lambda item: item[1])
    return {"max_path_chars": longest[1], "max_allowed_chars": 259,
            "longest_path": longest[0], "candidate_path_count": len(candidates),
            "run_id_chars": len(run_id), "windows_max_path_guard": "PASS" if longest[1] <= 259 else "FAIL"}


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


def verify_audio_scope_amendment(project_root: Path, policy_path: Path, approval_path: Path) -> dict[str, Any]:
    policy = load_json(policy_path)
    approval = load_json(approval_path)
    approval_input = dict(approval)
    observed_approval_digest = approval_input.pop("approval_record_sha256", None)
    canonical_approval_digest = canonical_sha256(approval_input)
    require(approval.get("schema") == "C11E-D4.8-R1V-FAMILY-AUDIO-APPROVAL-AMENDMENT-V1"
            and approval.get("decision") == "APPROVE_BOUNDED_R1V_FAMILY_NATIVE_AUDIO_AV_TESTS",
            "Operator family-audio approval amendment is invalid")
    require(observed_approval_digest == canonical_approval_digest == policy.get("approval", {}).get("approval_record_sha256"),
            "Family-audio approval amendment canonical SHA mismatch")
    require(policy.get("schema") == "C11E-D4.8-R1V-FAMILY-AUDIO-SCOPE-AMENDMENT-V1"
            and policy.get("status") == "APPROVED_BOUNDED_R1V_FAMILY_NATIVE_AUDIO_AV_TESTS"
            and policy.get("execution_authorized") is True,
            "R1V family-audio scope amendment is not approved")
    require(sha256_file(policy_path) == AUDIO_SCOPE_POLICY_SHA256, "R1V family-audio scope policy raw SHA mismatch")
    require(sha256_file(approval_path) == AUDIO_SCOPE_APPROVAL_RAW_SHA256
            and sha256_file(approval_path) == policy.get("approval", {}).get("approval_record_raw_sha256"),
            "R1V family-audio approval raw SHA mismatch")
    required_scope = {
        "selector_count": 5, "repeat_count_per_selector": 2, "av_outputs": 10,
        "reused_prior_fractal_bloom_a_capture": 1, "new_c11c_launcher_invocations": 9,
        "audio_generator": "C11C_FAMILY_MUSIC_V4",
        "audio_helper": "tools/prototypes/c11c_common/C11CSafeAmbient.py",
        "gameplay_seed_source": "R1P.seed_domains.gameplay_seed",
        "music_seed_source": "R1P.seed_domains.music_seed",
        "music_seed_is_distinct_from_gameplay_seed": True,
        "music_kind": "loop", "grammar_bound": True,
        "wav_sample_rate": 44100, "wav_channels": 2, "wav_sample_width_bits": 16,
        "aac_codec": "aac", "aac_bitrate": 192000, "aac_sample_rate": 44100, "aac_channels": 2,
        "video_mux_mode": "-c:v copy", "video_filters": False,
        "d3_v5": False, "d_compositor": False, "d9_10_dispatch": False,
        "general_d4_8_production": False, "release_or_promotion": False,
    }
    require(policy.get("scope") == required_scope, "R1V family-audio policy scope differs from the exact bounded approval")
    require(approval.get("scope") == required_scope, "Operator family-audio approval scope differs from policy")
    require(policy.get("governance", {}).get("d4_8_general_production") == "BLOCKED"
            and policy.get("governance", {}).get("renderer_activation_policy_state") == "DISABLED"
            and policy.get("governance", {}).get("runtime_authority") == "NONE"
            and policy.get("governance", {}).get("d9_10") == "PREPARE_ONLY"
            and policy.get("governance", {}).get("release_authority") == "NONE",
            "R1V audio amendment improperly changes general D4.8/D9.10/release governance")
    require(policy.get("supersedes_only") == "R1V_V2_AUDIO_AND_MUX_PROHIBITION_FOR_THIS_BOUNDED_TEST_SCOPE",
            "R1V amendment supersession scope is too broad")
    return {"policy_sha256": sha256_file(policy_path), "approval_raw_sha256": sha256_file(approval_path),
            "approval_record_canonical_sha256": canonical_approval_digest,
            "approval_timestamp": approval.get("approval_timestamp"),
            "selector_count": 5, "repeat_count": 2, "av_outputs": 10,
            "reused_prior_capture_count": 1, "new_launcher_invocations": 9,
            "audio_route": "C11C_FAMILY_MUSIC_V4", "d3_v5": False}


def load_r1p_audio_selector_data(project_root: Path, r1p_archive: Path, base: Any,
                                 audio_registry_path: Path) -> list[dict[str, Any]]:
    r1p = base.verify_r1p_archive(project_root, r1p_archive)
    registry = json.loads(audio_registry_path.read_text(encoding="utf-8-sig"))
    bindings = registry.get("bindings", {})
    rules = registry.get("design_rules", {})
    profiles = {str(p.get("id")): p for p in registry.get("profiles", []) if isinstance(p, dict)}
    require(registry.get("mode") == "FAMILY_MUSIC_V4" and registry.get("version") == "4.3.0",
            "Pinned C11-C music registry is not FAMILY_MUSIC_V4 revision 4.3.0")
    require((rules.get("sample_rate"), rules.get("channels"), rules.get("delivery_codec"))
            == (44100, 2, "AAC 192k loops / AAC 128k drills"), "C11-C loop music technical profile changed")
    result = []
    with zipfile.ZipFile(r1p_archive, "r") as archive:
        for selector in base.SELECTOR_EXPECTATIONS:
            receipt_raw = archive.read(selector["receipt_file"])
            receipt = json.loads(receipt_raw.decode("utf-8-sig"))
            seeds = receipt.get("seed_domains", {})
            timing = receipt.get("timing", {})
            family = selector["internal_family_id"]
            route = bindings.get(f"visual_loop/{family}")
            profile_id = str(receipt.get("family_music_profile_id", ""))
            require(isinstance(route, dict) and route.get("profile") == profile_id == EXPECTED_AUDIO_ROUTE[family],
                    f"R1P family music profile and frozen C11-C registry differ: {family}")
            require(int(seeds.get("gameplay_seed", -1)) == selector["gameplay_seed"]
                    and int(seeds.get("music_seed", -1)) != selector["gameplay_seed"]
                    and seeds.get("music_seed_consumed_by_visual_parameters") is False,
                    f"R1P seed-domain isolation mismatch: {family}")
            require(float(timing.get("duration_seconds", 0)) == selector["duration_seconds"]
                    and int(timing.get("fps", 0)) == selector["fps"]
                    and int(timing.get("frame_count", 0)) == selector["frame_count_consistency_only"],
                    f"R1P family timing mismatch: {family}")
            cycles = int(timing.get("loop_cycles", 0))
            require(cycles >= 1, f"R1P loop cycle count missing: {family}")
            require(profile_id in profiles, f"C11-C music profile definition missing: {profile_id}")
            canonical_receipt_sha = str(receipt.get("receipt_sha256", ""))
            sidecar_name = selector["receipt_file"] + ".sha256"
            sidecar_text = archive.read(sidecar_name).decode("ascii").strip().split()[0]
            require(canonical_receipt_sha == sidecar_text,
                    f"R1P per-selector receipt SHA sidecar mismatch: {selector['receipt_file']}")
            result.append({**selector, "music_seed": int(seeds["music_seed"]),
                           "loop_cycles": cycles, "music_profile_id": profile_id,
                           "music_profile": profiles[profile_id],
                           "r1p_receipt_sha256": canonical_receipt_sha,
                           "r1p_receipt_raw_sha256": sha256_bytes(receipt_raw),
                           "r1p_music_seed_domain": seeds})
    require(len(result) == 5, "R1P audio selector projection must contain exactly five selectors")
    return result


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


def build_mux_command(ffmpeg_exe: str, source_mp4: Path, wav_path: Path, output_mp4: Path) -> list[str]:
    return [ffmpeg_exe, "-y", "-hide_banner", "-loglevel", "error", "-i", str(source_mp4), "-i", str(wav_path),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart", str(output_mp4)]


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


def validate_final_av_probe(probe: dict[str, Any], selector: dict[str, Any], source_stream: dict[str, Any]) -> dict[str, Any]:
    streams = probe.get("streams", [])
    require(len(streams) == 2, f"Final A/V MP4 must have exactly two streams; found {len(streams)}")
    video = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    require(len(video) == 1 and len(audio) == 1, "Final A/V MP4 must contain one video and one audio stream")
    v, a = video[0], audio[0]
    require(v.get("codec_name") == "h264" and int(v.get("width", 0)) == 720 and int(v.get("height", 0)) == 1280,
            "Final A/V video codec/geometry mismatch")
    require(v.get("r_frame_rate") == "30/1" and int(v.get("nb_frames", -1)) == selector["frame_count_consistency_only"],
            "Final A/V video rate/frame count mismatch")
    require(v.get("pix_fmt") == source_stream.get("pix_fmt") and v.get("color_range") == source_stream.get("color_range"),
            "Final A/V mux changed the source video's pixel format/color range")
    require(a.get("codec_name") == "aac" and a.get("sample_rate") == "44100"
            and int(a.get("channels", 0)) == 2 and a.get("channel_layout") == "stereo",
            "Final A/V audio must be AAC 44.1 kHz stereo")
    vdur = float(v.get("duration", 0))
    adur = float(a.get("duration", 0))
    fdur = float(probe.get("format", {}).get("duration", 0))
    expected = float(selector["duration_seconds"])
    require(abs(vdur - expected) <= 0.05 and abs(adur - expected) <= 0.05 and abs(fdur - expected) <= 0.05,
            f"A/V durations differ from expected {expected}s: video={vdur}, audio={adur}, container={fdur}")
    vstart = float(v.get("start_time", 0) or 0)
    astart = float(a.get("start_time", 0) or 0)
    require(abs(vstart) <= 0.001 and abs(astart) <= 0.001 and abs(vdur - adur) <= (1.0 / 30.0),
            f"A/V start/duration alignment failure: v={vstart}/{vdur}, a={astart}/{adur}")
    return {"video_stream": v, "audio_stream": a, "container_duration_seconds": fdur,
            "start_offset_seconds": abs(vstart - astart), "av_duration_delta_seconds": abs(vdur - adur),
            "two_stream_contract": True}


def hash_encoded_stream(ffmpeg_exe: str, media_path: Path, stream_selector: str, output_format: str,
                        cwd: Path) -> str:
    proc = run_process([ffmpeg_exe, "-v", "error", "-i", str(media_path), "-map", stream_selector,
                        "-c", "copy", "-f", output_format, "pipe:1"], cwd, timeout=1800)
    require(proc.returncode == 0, f"FFmpeg stream-copy extraction failed for {media_path.name}: {proc.stderr[:500]!r}")
    require(bool(proc.stdout), f"FFmpeg returned empty {output_format} stream for {media_path.name}")
    return sha256_bytes(proc.stdout)


def build_pixel_decode_args(video_path: Path) -> list[str]:
    """Build FFmpeg 9-compatible, timestamp-preserving in-memory pixel decode argv.

    ``-vsync 0`` was removed in FFmpeg 9. ``-fps_mode passthrough`` is the
    per-output-stream replacement and keeps every decoded frame without CFR
    duplication/drop. Frames remain on stdout only; no PNG/AVI intermediates.
    """
    return ["-v", "error", "-i", str(video_path), "-map", "0:v:0",
            "-fps_mode", "passthrough", "-pix_fmt", "yuv420p", "-f", "rawvideo", "pipe:1"]


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
    decode_args = build_pixel_decode_args(video_path)
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
    decode_stderr = decode_stderr_path.read_bytes()
    decode_stderr_text = decode_stderr.decode("utf-8", errors="replace").strip()
    require(decode_exit == 0,
            f"FFmpeg in-memory pixel decode failed (exit={decode_exit}, decoded_frames={len(frame_hashes)}/{len(frame_rows)}); "
            f"stderr={decode_stderr_text[:1000]!r}")
    require(len(frame_hashes) == len(frame_rows),
            f"FFmpeg decoded {len(frame_hashes)} pixel frames but FFprobe measured {len(frame_rows)}")
    pixel_manifest = {"schema": "C11E-R1V-PIXEL-HASH-MANIFEST-V1", "source_mp4_sha256": sha256_file(video_path),
                      "source_pixel_format": source_pix_fmt, "decode_pixel_format": "yuv420p",
                      "ffmpeg_video_sync_mode": "fps_mode_passthrough",
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


def verify_prior_fractal_a(project_root: Path) -> dict[str, Any]:
    evidence_root = project_root / "artifacts/tests/c11e/r1v_five_family_qualification" / PRIOR_R1V_RUN_ID
    report_path = evidence_root / "r1v_report.json"
    process_path = evidence_root / "r1v_process_receipt.json"
    require(report_path.is_file() and process_path.is_file(), "Prior Fractal Bloom A report/receipt missing; refusing to rerender or fabricate reuse")
    require(sha256_file(report_path) == PRIOR_R1V_REPORT_SHA256, "Prior failed R1V report SHA mismatch")
    require(sha256_file(process_path) == PRIOR_R1V_PROCESS_RECEIPT_SHA256, "Prior failed R1V process receipt SHA mismatch")
    report = load_json(report_path)
    process_receipt = load_json(process_path)
    require(report.get("run_id") == PRIOR_R1V_RUN_ID and report.get("completed_launcher_invocations") == 1
            and report.get("completed_frame_inventories") == 0
            and report.get("status") == "FAIL_R1V_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED",
            "Prior R1V run is not the documented one-capture fail-closed attempt")
    approval = report.get("approval", {})
    governance = report.get("governance", {})
    require(report.get("preflight") == "PASS_R1V_PRELAUNCH_PREFLIGHT"
            and report.get("r1p", {}).get("recovered_zip_sha256") == R1P_RECOVERED_ZIP_SHA256
            and report.get("option_c", {}).get("report_sha256") == OPTION_C_REPORT_SHA256
            and approval.get("policy_sha256") == R1V_SILENT_POLICY_SHA256
            # The accepted R1V V3 report stores the production-policy state
            # under approval.d4_8_production_policy_state. Its governance object
            # uses d4_8_general_production=BLOCKED; do not query a field that
            # does not exist in that schema or weaken the actual production lock.
            and approval.get("d4_8_production_policy_state") == "DISABLED_UNCHANGED"
            and governance.get("d4_8_general_production") == "BLOCKED"
            and governance.get("d_renderer_dispatch") == "OFF"
            and governance.get("release_authority") == "NONE",
            "Prior R1V report does not retain its accepted parent/policy lineage")
    require(process_receipt.get("run_id") == PRIOR_R1V_RUN_ID and process_receipt.get("launcher_process_count") == 1
            and len(process_receipt.get("processes", [])) == 1
            and process_receipt["processes"][0].get("exit_code") == 0
            and process_receipt.get("report_sha256") == PRIOR_R1V_REPORT_SHA256
            and process_receipt.get("r1p_recovered_zip_sha256") == R1P_RECOVERED_ZIP_SHA256
            and process_receipt.get("option_c_report_sha256") == OPTION_C_REPORT_SHA256,
            "Prior R1V process receipt does not prove one successful launcher and correct parents")
    p = report.get("processes", [])
    require(len(p) == 1, "Prior R1V must contain exactly the Fractal Bloom A process")
    process = p[0]
    selector = next(s for s in _selectors_from_base(project_root) if s["family_id"] == "c11c_fractal_bloom_v1")
    require(process.get("family_id") == selector["family_id"] and process.get("grammar_id") == "radial_bloom"
            and process.get("repeat") == "A" and process.get("seed") == 100006 and process.get("exit_code") == 0,
            "Prior launcher is not the successful Fractal Bloom A source capture")
    require(process.get("stdout_sha256") == PRIOR_FRACTAL_A_STDOUT_SHA256 and process.get("stderr_sha256") == hashlib.sha256(b"").hexdigest(),
            "Prior Fractal A process log hashes mismatch")
    output_root = Path(process["output_root"])
    require(output_root.is_absolute() and output_root.resolve().is_relative_to(project_root.resolve()),
            "Prior Fractal A source root is outside active project")
    tag_index = process.get("arguments", []).index("-OutputTag") + 1
    original_tag = process["arguments"][tag_index]
    stem = f"FractalBloom_v1_seed_100006_{original_tag}"
    source = output_root / f"{stem}.mp4"
    required = [source, output_root / f"{stem}_authoring.json", output_root / f"{stem}_manifest.json",
                output_root / f"{stem}_godot.log", output_root / f"{stem}_social.txt", output_root / f"{stem}_ffprobe.json"]
    for path in required:
        require(path.is_file() and path.stat().st_size > 0, f"Prior Fractal A artifact missing: {path}")
    require(sha256_file(source) == PRIOR_FRACTAL_A_MP4_SHA256, "Prior Fractal A MP4 SHA mismatch")
    require(b"[C11-C-2.16.3] PASS" in Path(process["stdout_path"]).read_bytes(),
            "Prior Fractal A stdout no longer contains the original C11-C PASS marker")
    parse_godot_capture_log((output_root / f"{stem}_godot.log").read_bytes(), 720, 1280, 30, 660)
    prior_stdout = Path(process["stdout_path"])
    prior_stderr = Path(process["stderr_path"])
    for path, expected in ((prior_stdout, PRIOR_FRACTAL_A_STDOUT_SHA256), (prior_stderr, process["stderr_sha256"])):
        require(path.is_file() and sha256_file(path) == expected, f"Prior Fractal A process log missing or hash mismatch: {path}")
    return {"report_path": str(report_path), "report_sha256": PRIOR_R1V_REPORT_SHA256,
            "process_receipt_path": str(process_path), "process_receipt_sha256": PRIOR_R1V_PROCESS_RECEIPT_SHA256,
            "source_output_root": str(output_root), "source_video_path": str(source),
            "source_video_sha256": PRIOR_FRACTAL_A_MP4_SHA256, "source_output_tag": original_tag,
            "stdout_path": str(prior_stdout), "stdout_sha256": PRIOR_FRACTAL_A_STDOUT_SHA256,
            "stderr_path": str(prior_stderr), "stderr_sha256": process["stderr_sha256"],
            "launcher_exit_code": 0, "reused_without_relaunch": True}


def _selectors_from_base(project_root: Path) -> list[dict[str, Any]]:
    base = load_base_module(project_root)
    return base.SELECTOR_EXPECTATIONS


def compare_av_repeats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["family_id"], {})[row["repeat"]] = row
    comparisons = []
    for family_id, pair in grouped.items():
        require(set(pair) == {"A", "B"}, f"Missing A/B A/V pair for {family_id}")
        a, b = pair["A"], pair["B"]
        checks = {
            "source_frame_count_equal": a["source_inventory"]["frame_count"] == b["source_inventory"]["frame_count"],
            "source_pts_equal": a["source_inventory"]["pts"] == b["source_inventory"]["pts"],
            "source_pixel_hashes_equal": a["source_inventory"]["pixel_frame_hashes"] == b["source_inventory"]["pixel_frame_hashes"],
            "source_global_pixel_stream_equal": a["source_inventory"]["global_pixel_stream_sha256"] == b["source_inventory"]["global_pixel_stream_sha256"],
            "music_wav_sha_equal": a["audio"]["wav_sha256"] == b["audio"]["wav_sha256"],
            "aac_stream_sha_equal": a["audio"]["aac_stream_sha256"] == b["audio"]["aac_stream_sha256"],
            "music_seed_same": a["music_seed"] == b["music_seed"],
            "gameplay_seed_same": a["gameplay_seed"] == b["gameplay_seed"],
            "gameplay_music_seed_distinct": a["gameplay_seed"] != a["music_seed"] and b["gameplay_seed"] != b["music_seed"],
        }
        require(all(checks.values()), f"A/B visual/music repeat mismatch {family_id}: {checks}")
        comparisons.append({"family_id": family_id, "checks": checks,
                            "source_mp4_sha256_a": a["source_inventory"]["source_video_sha256"],
                            "source_mp4_sha256_b": b["source_inventory"]["source_video_sha256"],
                            "source_mp4_byte_identical": a["source_inventory"]["source_video_sha256"] == b["source_inventory"]["source_video_sha256"],
                            "wav_sha256": a["audio"]["wav_sha256"], "aac_stream_sha256": a["audio"]["aac_stream_sha256"]})
    require(len(comparisons) == 5, "A/V repeat comparison must cover all five families")
    return {"family_pairs": comparisons, "pairs_passed": sum(all(x["checks"].values()) for x in comparisons)}


def verify_all_source_pins(base: Any, project_root: Path, r1p_archive: Path, silent_policy: Path,
                           silent_approval: Path, audio_policy: Path, audio_approval: Path) -> dict[str, Any]:
    base_result = base.verify_source_pins_after_capture(project_root, r1p_archive, silent_policy, silent_approval)
    audio_result = verify_audio_source_pins(project_root)
    scope = verify_audio_scope_amendment(project_root, audio_policy, audio_approval)
    require(base_result["total_source_pin_validations"] == 61 and audio_result["pin_count"] == 3,
            "R1V A/V source pin cardinality mismatch")
    return {"base_r1v_pins": 61, "family_audio_pins": 3, "total_source_pins": 64,
            "base_pin_digest": base_result, "audio_pins": audio_result, "audio_scope": scope}


def run_av_qualification(project_root: Path, r1p_archive: Path, audio_policy_path: Path,
                         audio_approval_path: Path) -> dict[str, Any]:
    require(project_root.is_dir(), f"ProjectRoot missing: {project_root}")
    project_root = project_root.resolve(strict=True)
    require(sys.platform == "win32", "R1V physical A/V qualification runs only on Windows")
    require(sys.version_info[:2] == (3, 13), f"Python 3.13 required; found {sys.version.split()[0]}")
    base = load_base_module(project_root)
    silent_policy_path = project_root / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
    silent_approval_path = project_root / "definitions/c11d/production/C11E_D4_8_R1V_OPERATOR_APPROVAL_RECORD_20261107_V1.json"
    silent_approval = base.verify_approval_policy(project_root, silent_policy_path, silent_approval_path)
    audio_scope = verify_audio_scope_amendment(project_root, audio_policy_path, audio_approval_path)
    r1p_meta = load_r1p_audio_selector_data(project_root, r1p_archive, base,
                                            project_root / "profiles/presentation/c11c_visual_music_profiles.json")
    option_c = base.verify_option_c_evidence(project_root)
    tools = base._tool_preflight(project_root)
    source_pins_pre = verify_all_source_pins(base, project_root, r1p_archive, silent_policy_path,
                                             silent_approval_path, audio_policy_path, audio_approval_path)
    prior_a = verify_prior_fractal_a(project_root)

    run_id = build_run_id()
    evidence_parent = project_root / "artifacts/tests/c11e/r1v_av_five_family_qualification"
    evidence_root = evidence_parent / run_id
    require(not evidence_root.exists(), f"A/V evidence run root collision: {evidence_root}")
    source_parent = evidence_root / "source"
    audio_parent = evidence_root / "audio"
    delivery_parent = evidence_root / "delivery"
    jobs = []
    for selector_meta in r1p_meta:
        for repeat in ("A", "B"):
            tag = f"{run_id}_{selector_meta['source_folder_key'].upper()}_{repeat}"
            output_root = source_parent / selector_meta["source_folder_key"] / repeat
            av_root = delivery_parent / selector_meta["source_folder_key"] / repeat
            wav_root = audio_parent / selector_meta["source_folder_key"] / repeat
            source_tag = prior_a["source_output_tag"] if selector_meta["family_id"] == "c11c_fractal_bloom_v1" and repeat == "A" else tag
            jobs.append({"selector": selector_meta, "repeat": repeat, "tag": tag,
                         "source_output_tag": source_tag, "output_root": output_root,
                         "wav_root": wav_root, "av_root": av_root,
                         "reuse_prior": selector_meta["family_id"] == "c11c_fractal_bloom_v1" and repeat == "A"})
    path_budget = windows_path_budget(project_root, run_id, r1p_meta, prior_a["source_output_tag"])
    require(path_budget["max_path_chars"] <= path_budget["max_allowed_chars"],
            f"Planned Windows artifact path exceeds MAX_PATH safety budget: {path_budget['max_path_chars']} > 259: {path_budget['longest_path']}")
    for job in jobs:
        for path in (job["output_root"], job["wav_root"], job["av_root"]):
            require(not path.exists(), f"R1V A/V output leaf already exists; refusing cleanup/overwrite: {path}")
    new_capture_jobs = [j for j in jobs if not j["reuse_prior"]]
    for job in new_capture_jobs:
        selector = job["selector"]
        stem = f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['tag']}"
        temp_silent = Path(tempfile.gettempdir()) / f"C11C_{stem}_silent.mp4"
        temp_avi_glob = f"{stem}_*.avi"
        job["temp_silent_path"] = temp_silent
        job["temp_avi_glob"] = temp_avi_glob
        require(not temp_silent.exists(), f"C11-C launcher would overwrite pre-existing temp MP4: {temp_silent}")
        require(not list(Path(tempfile.gettempdir()).glob(temp_avi_glob)), f"C11-C launcher temp AVI pattern not empty: {temp_avi_glob}")
    require(not (audio_parent.exists() or delivery_parent.exists() or source_parent.exists()), "Run output parent unexpectedly exists")

    lock_token = sha256_bytes(str(project_root).lower().encode("utf-8"))[:16]
    lock_path = Path(tempfile.gettempdir()) / f"C11E_R1V_{lock_token}.lock"
    try:
        lock_fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise AVQualificationError(f"Another R1V run holds the exclusive project lock: {lock_path}") from exc

    try:
        evidence_root.mkdir(parents=True, exist_ok=False)
        (evidence_root / "processes").mkdir()
        for selector_meta in r1p_meta:
            (source_parent / selector_meta["source_folder_key"]).mkdir(parents=True, exist_ok=True)
            (audio_parent / selector_meta["source_folder_key"]).mkdir(parents=True, exist_ok=True)
            (delivery_parent / selector_meta["source_folder_key"]).mkdir(parents=True, exist_ok=True)
        override_path = project_root / "override.cfg"
        override_preexisting_backups = base.temp_file_state("C11C_override_backup_*.cfg")
        override_existed = override_path.exists()
        override_bytes = override_path.read_bytes() if override_existed else None
        override_evidence = {"path": str(override_path), "existed_before": override_existed,
                             "sha256_before": sha256_bytes(override_bytes) if override_bytes is not None else None,
                             "restored_after_each_launcher": True,
                             "temp_backup_preimage": override_preexisting_backups}
        if override_existed:
            (evidence_root / "override_cfg_preimage.bin").write_bytes(override_bytes or b"")
        shutil.copy2(prior_a["report_path"], evidence_root / "prior_r1v_report.json")
        shutil.copy2(prior_a["process_receipt_path"], evidence_root / "prior_r1v_process_receipt.json")
        shutil.copy2(prior_a["stdout_path"], evidence_root / "prior_fractal_a_launcher.stdout.log")
        shutil.copy2(prior_a["stderr_path"], evidence_root / "prior_fractal_a_launcher.stderr.log")

        run_manifest = {"schema": "C11E-R1V-AV-FIVE-FAMILY-RUN-MANIFEST-V1", "run_id": run_id,
            "started_utc": datetime.now(timezone.utc).isoformat(), "project_root": str(project_root),
            "scope": {"selector_count": 5, "repeat_count": 2, "av_outputs": 10,
                      "reused_prior_capture_slots": 1, "new_launcher_invocations": 9,
                      "integrated_per_slot_pipeline": ["C11-C silent visual capture/reuse", "actual frame inventory",
                         "C11-C FAMILY_MUSIC_V4 with R1P music_seed", "AAC 192k mux with video stream copy", "FFprobe A/V QA"],
                      "d3_v5": False, "d_compositor": False, "d9_10_dispatch": False,
                      "filters": False, "video_reencode_after_source_capture": False,
                      "audio_seed_passed_to_visual_launcher": False},
            "windows_path_budget": path_budget,
            "authority": {"r1p_run_id": R1P_RUN_ID, "r1p_recovered_zip_sha256": R1P_RECOVERED_ZIP_SHA256,
                          "option_c_report_sha256": OPTION_C_REPORT_SHA256,
                          "silent_policy_sha256": R1V_SILENT_POLICY_SHA256,
                          "audio_policy_sha256": audio_scope["policy_sha256"],
                          "audio_approval_sha256": audio_scope["approval_raw_sha256"]},
            "source_pins": source_pins_pre, "runtime_executables": tools,
            "prior_reused_capture": prior_a,
            "jobs": [{"family_id": j["selector"]["family_id"], "grammar_id": j["selector"]["grammar_id"],
                       "repeat": j["repeat"], "gameplay_seed": j["selector"]["gameplay_seed"],
                       "music_seed": j["selector"]["music_seed"], "music_profile_id": j["selector"]["music_profile_id"],
                       "loop_cycles": j["selector"]["loop_cycles"], "duration_seconds": j["selector"]["duration_seconds"],
                       "reuse_prior_source": j["reuse_prior"], "source_output_tag": j["source_output_tag"],
                       "new_output_tag": j["tag"]} for j in jobs],
            "governance": {"c11c_test_scope": "AUTHORIZED_BOUNDED_R1V_AV_QUALIFICATION_ONLY",
                           "d4_8_general_production": "BLOCKED", "renderer_activation_policy": "DISABLED",
                           "runtime_authority": "NONE", "d_renderer_dispatch": "OFF", "d9_10": "PREPARE_ONLY",
                           "d9_14": "BLOCKED", "d9_16": "BLOCKED", "d9_17": "BLOCKED_NO_GO",
                           "d10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE"}}
        run_manifest_sha = dump_json(evidence_root / "r1v_av_run_manifest.json", run_manifest)
        dump_json(evidence_root / "preflight_report.json", {"status": "PASS_R1V_AV_PRELAUNCH_PREFLIGHT",
            "run_id": run_id, "reused_prior_capture": prior_a, "new_launchers": 9,
            "av_output_slots": 10, "source_roots_all_nonexistent": True, "audio_and_delivery_roots_all_nonexistent": True,
            "temp_paths_empty": True, "windows_path_budget": path_budget,
            "source_pins": source_pins_pre, "runtime_executables": tools})
    except Exception:
        os.close(lock_fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass
        raise

    process_records = []
    source_rows = []
    av_rows = []
    failure = None
    try:
        audio_helper = project_root / "tools/prototypes/c11c_common/C11CSafeAmbient.py"
        audio_rules = json.loads((project_root / "profiles/presentation/c11c_visual_music_profiles.json").read_text(encoding="utf-8-sig"))["design_rules"]
        for slot_index, job in enumerate(jobs, start=1):
            selector = job["selector"]
            repeat = job["repeat"]
            output_root = job["output_root"]
            output_root.mkdir(parents=True, exist_ok=False)
            if job["reuse_prior"]:
                prior_source_root = Path(prior_a["source_output_root"])
                source_stem = f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['source_output_tag']}"
                copy_names = [f"{source_stem}.mp4", f"{source_stem}_authoring.json", f"{source_stem}_manifest.json",
                              f"{source_stem}_godot.log", f"{source_stem}_social.txt", f"{source_stem}_ffprobe.json"]
                for name in copy_names:
                    shutil.copy2(prior_source_root / name, output_root / name)
                launcher_record = {"slot": slot_index, "family_id": selector["family_id"], "repeat": repeat,
                    "reused_prior_capture": True, "launcher_invoked": False, "source_video_sha256": PRIOR_FRACTAL_A_MP4_SHA256,
                    "prior_run_id": PRIOR_R1V_RUN_ID, "prior_stdout_sha256": PRIOR_FRACTAL_A_STDOUT_SHA256}
                process_records.append(launcher_record)
            else:
                stem_new = f"{selector['output_prefix']}_seed_{selector['gameplay_seed']}_{job['tag']}"
                command = base.build_launcher_command(tools["powershell"]["path"],
                    base.safe_project_file(project_root, selector["launcher_path"]), selector, output_root, job["tag"])
                start_utc = datetime.now(timezone.utc).isoformat()
                start_epoch = time.time()
                capture = run_process(command, project_root, timeout=3600)
                process_key = f"{slot_index:02d}_{selector['source_folder_key']}_{repeat}_C11C"
                stdout_path = evidence_root / "processes" / f"{process_key}.stdout.log"
                stderr_path = evidence_root / "processes" / f"{process_key}.stderr.log"
                stdout_path.write_bytes(capture.stdout)
                stderr_path.write_bytes(capture.stderr)
                launcher_record = {"slot": slot_index, "family_id": selector["family_id"], "repeat": repeat,
                    "reused_prior_capture": False, "launcher_invoked": True, "command": command,
                    "started_utc": start_utc, "started_epoch": start_epoch,
                    "completed_utc": datetime.now(timezone.utc).isoformat(), "exit_code": capture.returncode,
                    "stdout_path": str(stdout_path), "stdout_sha256": sha256_file(stdout_path),
                    "stderr_path": str(stderr_path), "stderr_sha256": sha256_file(stderr_path)}
                process_records.append(launcher_record)
                require(capture.returncode == 0, f"C11-C launcher failed {selector['family_id']} {repeat}: exit={capture.returncode}")
                require(b"[C11-C-2.16.3] PASS" in capture.stdout, f"C11-C launcher missing PASS marker: {selector['family_id']} {repeat}")
                override_result = base.restore_known_c11c_override_state(override_path, override_existed, override_bytes)
                if override_result not in ("PASS_ORIGINAL_PREIMAGE_PRESENT", "PASS_ORIGINALLY_ABSENT"):
                    override_evidence["restored_after_each_launcher"] = False
                    raise AVQualificationError(f"override.cfg did not restore exact original state after {selector['family_id']} {repeat}")
                source_pins = verify_all_source_pins(base, project_root, r1p_archive, silent_policy_path,
                                                     silent_approval_path, audio_policy_path, audio_approval_path)
                require(source_pins["total_source_pins"] == 64, "Post-launch source pin count differs from 64")
                require(not job["temp_silent_path"].exists() and not list(Path(tempfile.gettempdir()).glob(job["temp_avi_glob"])),
                        "C11-C silent/AVI temp artifacts remain after launcher")
                launcher_record["post_launch_source_pin_count"] = source_pins["total_source_pins"]
            # C11-C sidecars remain a silent-source receipt even after the separate A/V consumer runs.
            source_inventory = inspect_source_video(base, project_root, output_root, selector, repeat, tools, job)
            source_rows.append(source_inventory)
            (evidence_root / "source_inventory_index").mkdir(exist_ok=True)
            dump_json(evidence_root / "source_inventory_index" / f"{slot_index:02d}_{selector['source_folder_key']}_{repeat}.json",
                      {k: v for k, v in source_inventory.items() if k != "pixel_frame_hashes"})
            launcher_record["source_inventory_sha256"] = source_inventory["inventory_sha256"]
            launcher_record["source_video_sha256"] = source_inventory["source_video_sha256"]

            # Integrated per-slot native family music generation; it is not a separate test phase.
            wav_root = job["wav_root"]
            av_root = job["av_root"]
            wav_root.mkdir(parents=True, exist_ok=False)
            av_root.mkdir(parents=True, exist_ok=False)
            wav_path = wav_root / f"{job['tag']}_family_music.wav"
            music_command = build_music_command(sys.executable, audio_helper, wav_path, selector)
            music_proc = run_process(music_command, project_root, timeout=3600)
            music_key = f"{slot_index:02d}_{selector['source_folder_key']}_{repeat}_MUSIC"
            music_out = evidence_root / "processes" / f"{music_key}.stdout.log"
            music_err = evidence_root / "processes" / f"{music_key}.stderr.log"
            music_out.write_bytes(music_proc.stdout)
            music_err.write_bytes(music_proc.stderr)
            require(music_proc.returncode == 0, f"C11-C FAMILY_MUSIC_V4 failed for {selector['family_id']} {repeat}: exit={music_proc.returncode}")
            require(b"FAMILY_MUSIC_V4 generated" in music_proc.stdout, "C11-C family audio helper omitted generation PASS marker")
            audio_metrics = decode_audio_metrics(wav_path, selector["duration_seconds"], audio_rules)
            audio_metrics.update({"music_seed": selector["music_seed"], "music_profile_id": selector["music_profile_id"],
                                  "loop_cycles": selector["loop_cycles"], "grammar_id": selector["grammar_id"],
                                  "helper_sha256": AUDIO_SOURCE_PINS["tools/prototypes/c11c_common/C11CSafeAmbient.py"]["sha256"],
                                  "generator_sha256": AUDIO_SOURCE_PINS["tools/prototypes/c11c_common/generate_c11c_family_music.py"]["sha256"],
                                  "registry_sha256": AUDIO_SOURCE_PINS["profiles/presentation/c11c_visual_music_profiles.json"]["sha256"]})
            mux_path = av_root / f"{job['tag']}_C11C_FAMILY_MUSIC_AV.mp4"
            require(not mux_path.exists(), f"A/V output collision: {mux_path}")
            mux_command = build_mux_command(tools["ffmpeg"]["path"], Path(source_inventory["source_video_path"]), wav_path, mux_path)
            mux_proc = run_process(mux_command, project_root, timeout=3600)
            mux_out = evidence_root / "processes" / f"{slot_index:02d}_{selector['source_folder_key']}_{repeat}_MUX.stdout.log"
            mux_err = evidence_root / "processes" / f"{slot_index:02d}_{selector['source_folder_key']}_{repeat}_MUX.stderr.log"
            mux_out.write_bytes(mux_proc.stdout)
            mux_err.write_bytes(mux_proc.stderr)
            require(mux_proc.returncode == 0 and mux_path.is_file() and mux_path.stat().st_size > 0,
                    f"Native AAC mux failed: {selector['family_id']} {repeat}, exit={mux_proc.returncode}")
            final_probe = ffprobe_json(tools["ffprobe"]["path"], mux_path, project_root,
                av_root / f"{job['tag']}_final_av_ffprobe.json")
            av_qa = validate_final_av_probe(final_probe, selector, source_inventory["source_video_stream"])
            source_h264_sha = hash_encoded_stream(tools["ffmpeg"]["path"], Path(source_inventory["source_video_path"]), "0:v:0", "h264", project_root)
            final_h264_sha = hash_encoded_stream(tools["ffmpeg"]["path"], mux_path, "0:v:0", "h264", project_root)
            require(source_h264_sha == final_h264_sha, "A/V mux re-encoded or altered the immutable C11-C H.264 bitstream")
            aac_sha = hash_encoded_stream(tools["ffmpeg"]["path"], mux_path, "0:a:0", "adts", project_root)
            audio_metrics.update({"aac_stream_sha256": aac_sha, "aac_mux_command": mux_command,
                                  "wav_generation_exit_code": music_proc.returncode,
                                  "music_stdout_sha256": sha256_file(music_out), "music_stderr_sha256": sha256_file(music_err),
                                  "mux_exit_code": mux_proc.returncode, "mux_stdout_sha256": sha256_file(mux_out),
                                  "mux_stderr_sha256": sha256_file(mux_err), "source_h264_elementary_sha256": source_h264_sha,
                                  "final_h264_elementary_sha256": final_h264_sha, "video_bitstream_preserved": True})
            av_record = {"family_id": selector["family_id"], "grammar_id": selector["grammar_id"], "repeat": repeat,
                         "gameplay_seed": selector["gameplay_seed"], "music_seed": selector["music_seed"],
                         "music_profile_id": selector["music_profile_id"], "source_inventory": source_inventory,
                         "audio": audio_metrics, "final_av_path": str(mux_path), "final_av_sha256": sha256_file(mux_path),
                         "final_av_bytes": mux_path.stat().st_size, "final_av_probe": av_qa,
                         "reused_prior_source_capture": job["reuse_prior"]}
            av_rows.append(av_record)
            dump_json(evidence_root / "progress.json", {"run_id": run_id, "status": "RUNNING_FAIL_CLOSED_ON_NEXT_ERROR",
                "completed_av_outputs": len(av_rows), "completed_frame_inventories": len(source_rows),
                "completed_new_launchers": sum(1 for p in process_records if p.get("launcher_invoked")),
                "last_completed_slot": f"{selector['family_id']} {repeat}"})
            # Verify the frozen base, prior accepted gates, source/music dependencies and policy after each A/V slot.
            post_guard = verify_all_source_pins(base, project_root, r1p_archive, silent_policy_path,
                                                silent_approval_path, audio_policy_path, audio_approval_path)
            require(post_guard["total_source_pins"] == 64, "Post-slot pin guard did not validate 64 source files")
    except Exception as exc:
        failure = str(exc)
    finally:
        try:
            override_result = base.restore_known_c11c_override_state(override_path, override_existed, override_bytes)
            override_evidence["final_guard_result"] = override_result
            if override_result not in ("PASS_ORIGINAL_PREIMAGE_PRESENT", "PASS_ORIGINALLY_ABSENT") and failure is None:
                failure = f"override.cfg final restoration result: {override_result}"
        except Exception as exc:
            override_evidence["final_guard_result"] = f"FAIL_PRESERVED_UNKNOWN_STATE:{exc}"
            if failure is None:
                failure = str(exc)
        override_evidence["temp_backup_files_after"] = base.temp_file_state("C11C_override_backup_*.cfg")
        os.close(lock_fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass

    comparisons = None
    if failure is None:
        try:
            comparisons = compare_av_repeats(av_rows)
            require(comparisons["pairs_passed"] == 5, "Not all five integrated A/V A/B pairs passed")
        except Exception as exc:
            failure = str(exc)
    final_pins = None
    try:
        final_pins = verify_all_source_pins(base, project_root, r1p_archive, silent_policy_path,
                                            silent_approval_path, audio_policy_path, audio_approval_path)
        require(final_pins["total_source_pins"] == 64, "Final 64-source-pin guard failed")
        require(final_pins["audio_scope"]["audio_route"] == "C11C_FAMILY_MUSIC_V4", "Family audio route changed after run")
        require(base.temp_file_state("C11C_override_backup_*.cfg") == override_preexisting_backups,
                "C11CMovieCapture temporary override backup inventory changed")
        require(all(not j.get("temp_silent_path", Path("/nonexistent")).exists() for j in new_capture_jobs),
                "A C11-C temp silent file remains after the run")
        require(all(not list(Path(tempfile.gettempdir()).glob(j["temp_avi_glob"])) for j in new_capture_jobs),
                "A C11-C temporary AVI remains after the run")
    except Exception as exc:
        if failure is None:
            failure = str(exc)

    status = ("PASS_R1V_AV_FIVE_FAMILY_QUALIFICATION_10_OF_10_PENDING_OPERATOR_VISUAL_AUDIO_REVIEW"
              if failure is None and len(av_rows) == 10 and len(source_rows) == 10 and len(process_records) == 10
              else "FAIL_R1V_AV_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED")
    # process_records has ten slot records, but exactly nine include launcher_invoked=true.
    new_invocations = sum(1 for p in process_records if p.get("launcher_invoked"))
    report = {"schema": "C11E-R1V-AV-FIVE-FAMILY-REPORT-V1", "run_id": run_id, "status": status,
              "r1v_run_manifest_sha256": run_manifest_sha, "failure": failure,
              "completed_av_outputs": len(av_rows), "completed_source_inventories": len(source_rows),
              "completed_slot_records": len(process_records), "new_c11c_launcher_invocations": new_invocations,
              "reused_prior_source_capture_slots": sum(1 for p in process_records if p.get("reused_prior_capture")),
              "audio_generation_count": len(av_rows), "aac_mux_count": len(av_rows),
              "r1p": {"run_id": R1P_RUN_ID, "recovered_zip_sha256": R1P_RECOVERED_ZIP_SHA256,
                      "receipt_count": 27, "selected_selectors": [{"family_id": s["family_id"], "grammar_id": s["grammar_id"],
                        "gameplay_seed": s["gameplay_seed"], "music_seed": s["music_seed"],
                        "music_profile_id": s["music_profile_id"], "loop_cycles": s["loop_cycles"],
                        "duration_seconds": s["duration_seconds"], "r1p_receipt_sha256": s["r1p_receipt_sha256"]} for s in r1p_meta]},
              "silent_scope_approval": silent_approval, "family_audio_scope_amendment": audio_scope,
              "option_c": option_c, "processes": process_records,
              "source_inventories": [{k: v for k, v in x.items() if k not in ("pixel_frame_hashes",)} for x in source_rows],
              "audiovisual_outputs": [{k: v for k, v in x.items() if k != "source_inventory"} | {
                    "source_inventory_sha256": x["source_inventory"]["inventory_sha256"]} for x in av_rows],
              "repeat_determinism": comparisons, "source_pins_after_run": final_pins,
              "override_cfg_integrity": override_evidence,
              "human_review": {"fractal_bloom_A_visual": "OPERATOR_CONFIRMED_PASS",
                               "other_visual_slots": "PENDING_OPERATOR_REVIEW",
                               "audio_listening_all_slots": "PENDING_OPERATOR_REVIEW"},
              "scope": {"C11C_visual_source_capture": True, "C11C_family_music_v4": True,
                        "R1P_music_seed_consumed_by_audio_only": True, "gameplay_music_seed_domains_separate": True,
                        "native_aac_mux": True, "video_stream_copy_only": True, "video_bitstream_reencode": False,
                        "filters": False, "D3_V5": False, "D_compositor": False, "D9_10_dispatch": False,
                        "frame_pngs_written": False, "R1V_pixel_decode_pipe_to_memory": True},
              "governance": {"d4_8_general_production": "BLOCKED", "renderer_activation_policy": "DISABLED",
                "runtime_authority": "NONE", "d_renderer_dispatch": "OFF", "d9_10": "PREPARE_ONLY",
                "d9_14": "BLOCKED", "d9_16": "BLOCKED", "d9_17": "BLOCKED_NO_GO",
                "d10": "BLOCKED_FOR_PROMOTION", "release_authority": "NONE"}}
    report_path = evidence_root / "r1v_av_report.json"
    report_sha = dump_json(report_path, report)
    (evidence_root / "r1v_av_report.sha256").write_text(f"{report_sha}  r1v_av_report.json\n", encoding="ascii")
    process_receipt = {"schema": "C11E-R1V-AV-PROCESS-RECEIPT-V1", "run_id": run_id,
        "python_version": sys.version.split()[0], "python_executable": sys.executable,
        "python_executable_sha256": sha256_file(Path(sys.executable)), "runtime_executables": tools,
        "planned_av_outputs": 10, "completed_av_outputs": len(av_rows),
        "new_launcher_invocations": new_invocations, "reused_capture_invocations": 1,
        "report_sha256": report_sha, "exit_code": 0 if status.startswith("PASS_") else 1,
        "status": status, "failure": failure}
    receipt_path = evidence_root / "r1v_av_process_receipt.json"
    receipt_sha = dump_json(receipt_path, process_receipt)
    (evidence_root / "r1v_av_process_receipt.sha256").write_text(f"{receipt_sha}  r1v_av_process_receipt.json\n", encoding="ascii")
    zip_path = evidence_parent / f"{run_id}_EVIDENCE.zip"
    require(not zip_path.exists(), f"Evidence ZIP collision: {zip_path}")
    with zipfile.ZipFile(zip_path, "x", compression=zipfile.ZIP_STORED, allowZip64=True) as bundle:
        for path in sorted(evidence_root.rglob("*")):
            if path.is_file():
                bundle.write(path, arcname=path.relative_to(evidence_root).as_posix())
    with zipfile.ZipFile(zip_path, "r") as bundle:
        require(bundle.testzip() is None, "Integrated A/V evidence ZIP CRC failure")
    return {"status": status, "run_id": run_id, "new_launcher_invocations": new_invocations,
            "reused_prior_captures": 1, "av_outputs": len(av_rows), "source_inventories": len(source_rows),
            "report_path": str(report_path), "report_sha256": report_sha,
            "process_receipt_path": str(receipt_path), "process_receipt_sha256": receipt_sha,
            "evidence_zip": str(zip_path), "evidence_zip_sha256": sha256_file(zip_path), "failure": failure}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-root", type=Path, required=True)
    ap.add_argument("--r1p-recovered-zip", type=Path, required=True)
    ap.add_argument("--audio-policy", type=Path, required=True)
    ap.add_argument("--audio-approval", type=Path, required=True)
    args = ap.parse_args()
    try:
        result = run_av_qualification(args.project_root, args.r1p_recovered_zip, args.audio_policy, args.audio_approval)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"].startswith("PASS_") else 1
    except Exception as exc:
        print(json.dumps({"status": "FAIL_R1V_AV_PREFLIGHT_OR_EXECUTION", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
