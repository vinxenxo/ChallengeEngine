import hashlib
import math
import random
import struct
import sys
import wave

SR = 44100
TAU = 2.0 * math.pi
DURATION_DEFAULT = 18.0
TARGET_PEAK = 0.52

# Family profiles are intentionally distinct. A grammar key and the render seed
# perturb the timbre deterministically so family and subfamily do not collapse to
# one generic fog/noise bed.
PROFILES = {
    "geometric_waves": {
        "base": 220.0,
        "ratios": (1.0, 1.25, 1.5, 2.0, 2.5),
        "weights": (0.62, 0.20, 0.11, 0.055, 0.020),
        "air": (660.0, 990.0),
        "air_level": 0.007,
        "breath": 2.0,
        "motion": 3.0,
        "event": 0.095,
        "style": "harmonic phase weave / interference shimmer / midpoint convergence",
    },
    "fractal_bloom": {
        "base": 164.0,
        "ratios": (1.0, 1.2, 1.5, 1.875, 2.0, 2.5, 3.0),
        "weights": (0.50, 0.18, 0.14, 0.10, 0.065, 0.036, 0.016),
        "air": (930.0, 1480.0),
        "air_level": 0.006,
        "breath": 4.0,
        "motion": 6.0,
        "event": 0.120,
        "style": "recursive harmonic bloom / filament overtones / midpoint expansion",
    },
    "sacred_symmetry": {
        "base": 196.0,
        "ratios": (1.0, 1.25, 1.5, 2.0, 2.5, 3.0),
        "weights": (0.43, 0.21, 0.15, 0.11, 0.065, 0.028),
        "air": (784.0, 1318.0),
        "air_level": 0.004,
        "breath": 2.0,
        "motion": 4.0,
        "event": 0.105,
        "style": "soft astrolabe chime / metallic harmonic wheel / midpoint alignment",
    },
    "living_particles": {
        "base": 174.0,
        "ratios": (1.0, 1.2, 1.3333333333, 1.5, 1.6666666667, 2.0),
        "weights": (0.50, 0.21, 0.15, 0.10, 0.055, 0.022),
        "air": (522.0, 783.0),
        "air_level": 0.005,
        "breath": 5.0,
        "motion": 8.0,
        "event": 0.110,
        "style": "fluid particle pulse / warm matter pad / attractor swell",
    },
    "invisible_forces": {
        "base": 147.0,
        "ratios": (1.0, 1.25, 1.5, 1.75, 2.0),
        "weights": (0.58, 0.20, 0.12, 0.065, 0.030),
        "air": (441.0, 661.0),
        "air_level": 0.004,
        "breath": 3.0,
        "motion": 7.0,
        "event": 0.120,
        "style": "low-mid force drone / beating harmonics / pressure swell",
    },
}


def _stable_int(text: str) -> int:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "little") & 0x7FFFFFFF


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _soft_clip(value: float) -> float:
    # Smooth limiter-like saturation; no hard digital clipping.
    return math.tanh(value * 1.15) / math.tanh(1.15)


def main() -> None:
    if len(sys.argv) < 6:
        raise SystemExit("usage: output.wav seed loop_cycles duration family grammar")

    out = sys.argv[1]
    seed = int(sys.argv[2])
    cycles = int(sys.argv[3])
    dur = float(sys.argv[4])
    family = str(sys.argv[5]).strip().lower()
    grammar = str(sys.argv[6]).strip().lower() if len(sys.argv) > 6 else "default"

    profile = PROFILES.get(family, PROFILES["geometric_waves"])
    n = int(round(SR * dur))

    grammar_hash = _stable_int(f"{family}|{grammar}")
    combined_seed = (seed * 7919 + cycles * 104729 + grammar_hash * 31) & 0x7FFFFFFF
    rng = random.Random(combined_seed)

    base = profile["base"] * (0.96 + 0.08 * rng.random())
    breath_cycles = profile["breath"] + float(grammar_hash % 3)
    motion_cycles = profile["motion"] + float(seed % 3)
    phase_offset = rng.random() * TAU
    secondary_phase = rng.random() * TAU
    pan_phase = rng.random() * TAU
    air_phase_a = rng.random() * TAU
    air_phase_b = rng.random() * TAU
    partial_phases = [rng.random() * TAU for _ in profile["ratios"]]

    # Grammar classes alter interval emphasis and event color without introducing
    # non-deterministic state. This is intentionally subtle within a family.
    grammar_variant = grammar_hash % 5
    interval_bias = (0.0, 0.018, -0.014, 0.028, -0.022)[grammar_variant]
    second_gain = (1.00, 1.08, 0.94, 1.12, 1.04)[grammar_variant]
    event_gain = (1.00, 1.12, 0.96, 1.18, 1.07)[grammar_variant]

    frames = []
    peak = 0.0
    for i in range(n):
        t = i / SR
        u = t / dur

        breath = 0.90 + 0.08 * math.sin(TAU * breath_cycles * u + phase_offset)
        drift = interval_bias + 0.016 * math.sin(TAU * motion_cycles * u + secondary_phase)
        midpoint = math.sin(math.pi * u) ** 8

        pad = 0.0
        for idx, (ratio, weight) in enumerate(zip(profile["ratios"], profile["weights"])):
            freq = base * ratio * (1.0 + drift * (0.35 + 0.65 * min(ratio / 2.0, 1.5)))
            amp = weight
            if idx == 1:
                amp *= second_gain
            pad += amp * math.sin(TAU * freq * t + partial_phases[idx])

        # Family + grammar-specific musical identity.
        if family == "sacred_symmetry":
            angle = 0.5 + 0.5 * math.sin(TAU * 0.5 * u + secondary_phase)
            accent_freq = base * (2.0 + 0.5 * angle)
            metallic = math.sin(TAU * accent_freq * t + phase_offset) + 0.33 * math.sin(TAU * accent_freq * 2.0 * t + partial_phases[2])
            accent = 0.045 * metallic * (0.34 + 0.66 * midpoint)
        elif family == "fractal_bloom":
            bloom = 0.55 + 0.45 * math.sin(TAU * (0.5 + (grammar_hash % 3)) * u + secondary_phase)
            accent_freq = base * (3.0 + 0.75 * bloom)
            accent = 0.052 * math.sin(TAU * accent_freq * t + partial_phases[-1]) * (0.18 + 0.82 * bloom)
        elif family == "geometric_waves":
            weave = 0.5 + 0.5 * math.sin(TAU * (1.0 + (grammar_hash % 2)) * u + phase_offset)
            accent_freq = base * (1.25 + 0.75 * weave)
            accent = 0.055 * math.sin(TAU * accent_freq * t + secondary_phase) * (0.22 + 0.78 * weave)
        elif family == "living_particles":
            pulse = 0.5 + 0.5 * math.sin(TAU * (1.0 + (grammar_hash % 2)) * u + secondary_phase)
            accent_freq = base * (1.3333333333 + 0.3333333333 * pulse)
            accent = 0.064 * pulse * math.sin(TAU * accent_freq * t + partial_phases[1])
        else:
            pressure = 0.5 + 0.5 * math.sin(TAU * (0.5 + (grammar_hash % 2) * 0.25) * u + secondary_phase)
            beat_freq = base * (1.5 + 0.25 * pressure)
            accent = 0.062 * math.sin(TAU * beat_freq * t + phase_offset) * (0.24 + 0.76 * pressure)

        air_a, air_b = profile["air"]
        air = profile["air_level"] * (
            0.62 * math.sin(TAU * air_a * t + air_phase_a)
            + 0.38 * math.sin(TAU * air_b * t + air_phase_b)
        )

        event_freq = base * 2.0 * (1.0 + 0.015 * math.sin(TAU * motion_cycles * u + phase_offset))
        event = profile["event"] * event_gain * midpoint * math.sin(TAU * event_freq * t + secondary_phase)
        if family == "sacred_symmetry":
            event *= 1.10 + 0.25 * midpoint
        elif family == "fractal_bloom":
            event *= 1.05 + 0.35 * midpoint
        elif family == "living_particles":
            event *= 0.92 + 0.48 * midpoint
        elif family == "invisible_forces":
            event *= 1.10 + 0.20 * midpoint

        sample = (pad * breath * 0.58 + accent + event + air) * 0.78
        sample *= 0.94 + 0.06 * math.sin(TAU * 0.5 * u + pan_phase)
        sample = _soft_clip(sample)

        stereo_motion = 0.06 * math.sin(TAU * 0.75 * u + pan_phase)
        left = sample * (0.985 + stereo_motion)
        right = sample * (0.985 - stereo_motion)
        frames.append((left, right))
        peak = max(peak, abs(left), abs(right))

    gain = TARGET_PEAK / peak if peak > 1.0e-9 else 1.0

    with wave.open(out, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        buf = bytearray()
        for left, right in frames:
            lv = int(_clamp(left * gain, -1.0, 1.0) * 32767.0)
            rv = int(_clamp(right * gain, -1.0, 1.0) * 32767.0)
            buf.extend(struct.pack("<hh", lv, rv))
        wf.writeframes(buf)

    print(
        f"[C11-C-AUDIO] FAMILY+GRAMMAR AMBIENT generated: {out} | {dur:.2f}s | "
        f"{SR}Hz stereo | family={family} | grammar={grammar} | peak={TARGET_PEAK:.2f}"
    )


if __name__ == "__main__":
    main()
