#!/usr/bin/env python3
"""C6-E Step 0 physical output contract test.

Does not execute Godot. It validates that the factory's declared source/master
contract and FFmpeg transcode produce a real 1080x1920 H.264 master from a
540x960 source movie, while preserving frame rate and frame count.
"""
from pathlib import Path
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from build_factory import (  # noqa: E402
    SOURCE_VIDEO_WIDTH, SOURCE_VIDEO_HEIGHT,
    MASTER_OUTPUT_WIDTH, MASTER_OUTPUT_HEIGHT,
    run_ffprobe,
)

assert (SOURCE_VIDEO_WIDTH, SOURCE_VIDEO_HEIGHT) == (540, 960)
assert (MASTER_OUTPUT_WIDTH, MASTER_OUTPUT_HEIGHT) == (1080, 1920)

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    source = tmp / "source.avi"
    master = tmp / "master.mp4"

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=540x960:r=60",
        "-frames:v", "60",
        "-c:v", "rawvideo", "-pix_fmt", "yuv420p",
        str(source),
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    src_probe = run_ffprobe(source)
    assert "error" not in src_probe, src_probe
    assert (src_probe["width"], src_probe["height"]) == (540, 960), src_probe
    assert src_probe["nb_frames"] == 60, src_probe
    assert src_probe["r_frame_rate"] == "60/1", src_probe

    subprocess.run([
        "ffmpeg", "-y", "-i", str(source),
        "-vf", "scale=1080:1920:flags=lanczos",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        str(master),
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    master_probe = run_ffprobe(master)
    assert "error" not in master_probe, master_probe
    assert (master_probe["width"], master_probe["height"]) == (1080, 1920), master_probe
    assert master_probe["codec_name"] == "h264", master_probe
    assert master_probe["pix_fmt"] in ("yuv420p", "yuvj420p"), master_probe
    assert master_probe["nb_frames"] == 60, master_probe
    assert master_probe["r_frame_rate"] == "60/1", master_probe

print("[C6E_OUTPUT_CONTRACT_SUITE] PASS — 540x960 source -> 1080x1920 H.264 master")
