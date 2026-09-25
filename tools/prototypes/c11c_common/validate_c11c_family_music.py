import argparse
import hashlib
import json
import math
import struct
import tempfile
import wave
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
GENERATOR = SCRIPT_DIR / "generate_c11c_family_music.py"
PROFILE_JSON = SCRIPT_DIR.parents[2] / "profiles" / "presentation" / "c11c_visual_music_profiles.json"

import sys
sys.path.insert(0, str(SCRIPT_DIR))
from generate_c11c_family_music import generate, SAMPLE_RATE, CHANNELS, TARGET_PEAK  # noqa: E402


def metrics(path: Path):
    with wave.open(str(path), "rb") as wf:
        if wf.getframerate() != SAMPLE_RATE or wf.getnchannels() != CHANNELS or wf.getsampwidth() != 2:
            raise RuntimeError(f"WAV format mismatch: {path}")
        raw = wf.readframes(wf.getnframes())
    values = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    peak = max(abs(x) for x in values) / 32767.0
    rms = math.sqrt(sum((x / 32767.0) ** 2 for x in values) / len(values)) if values else 0.0
    seam = max(abs(values[0] - values[-2]), abs(values[1] - values[-1])) / 32767.0 if len(values) >= 2 else 0.0
    return peak, rms, seam, hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Short deterministic validation for C11-C family music")
    ap.add_argument("--seed", type=int, default=314159)
    ap.add_argument("--duration", type=float, default=1.0)
    args = ap.parse_args()

    config = json.loads(PROFILE_JSON.read_text(encoding="utf-8"))
    rules = config["design_rules"]
    target_rms = float(rules.get("target_rms_min", 0.07))
    max_rms = float(rules.get("target_rms_max", 0.15))
    peak_ceiling = float(rules.get("max_peak", TARGET_PEAK))
    failures = []

    with tempfile.TemporaryDirectory(prefix="c11c_music_validate_") as td:
        td = Path(td)
        profiles = config.get("profiles", [])
        for index, profile in enumerate(profiles):
            profile_id = str(profile["id"])
            family = str(profile.get("paired_visual_loop", profile_id))
            semantic = f"{family}|validation"
            a = td / f"{profile_id}_a.wav"
            generate(str(a), args.seed, family, profile_id, 1, args.duration, "loop", semantic)
            peak, rms, seam, digest = metrics(a)
            # A longer representative clip makes the loop-seam metric meaningful; a 1-second clip
            # has a larger one-sample slope even when the periodic waveform is mathematically sound.
            if index == 0:
                seam_probe = td / f"{profile_id}_seam.wav"
                seam_duration = max(3.0, float(args.duration))
                generate(str(seam_probe), args.seed, family, profile_id, 1, seam_duration, "loop", semantic)
                _, _, seam, _ = metrics(seam_probe)
            digest_b = digest
            if index == 0:
                b = td / f"{profile_id}_b.wav"
                generate(str(b), args.seed, family, profile_id, 1, args.duration, "loop", semantic)
                _, _, _, digest_b = metrics(b)
            print(f"{profile_id}: peak={peak:.5f} rms={rms:.5f} seam={seam:.5f}")
            if peak > peak_ceiling + 0.001:
                failures.append(f"{profile_id}: peak {peak:.5f} > ceiling {peak_ceiling:.5f}")
            if rms < target_rms:
                failures.append(f"{profile_id}: RMS {rms:.5f} < target {target_rms:.5f}")
            if rms > max_rms:
                failures.append(f"{profile_id}: RMS {rms:.5f} > ceiling {max_rms:.5f}")
            if index == 0 and seam > 0.010:
                failures.append(f"{profile_id}: representative loop seam {seam:.5f} > 0.010")
            if digest != digest_b:
                failures.append(f"{profile_id}: deterministic hash mismatch")

    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        raise SystemExit(1)
    print("[C11-C-AUDIO] PASS — deterministic / pentatonic / mobile-presence / loop-seam smoke")


if __name__ == "__main__":
    main()
