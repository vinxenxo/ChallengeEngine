import math
import random
import struct
import sys
import wave

SR = 44100
TAU = 2.0 * math.pi

# Five intentionally different harmonic grammars. Every oscillator uses integer
# frequencies and integer temporal cycles so the 18-second loop closes naturally.
PROFILES = {
    "geometric_waves": {
        "base": 168.0,
        "partials": ((1.0, 0.54), (4.0 / 3.0, 0.22), (3.0 / 2.0, 0.15), (2.0, 0.08)),
        "air": (672.0, 1008.0),
        "air_level": 0.018,
        "lfo_cycles": 2.0,
        "motion_cycles": 5.0,
        "event_level": 0.055,
    },
    "fractal": {
        "base": 160.0,
        "partials": ((1.0, 0.48), (5.0 / 4.0, 0.18), (3.0 / 2.0, 0.16), (15.0 / 8.0, 0.10), (2.0, 0.06)),
        "air": (480.0, 960.0),
        "air_level": 0.016,
        "lfo_cycles": 3.0,
        "motion_cycles": 7.0,
        "event_level": 0.070,
    },
    "sacred_symmetry": {
        "base": 144.0,
        "partials": ((1.0, 0.44), (5.0 / 4.0, 0.20), (4.0 / 3.0, 0.17), (3.0 / 2.0, 0.11), (2.0, 0.06)),
        "air": (576.0, 864.0),
        "air_level": 0.012,
        "lfo_cycles": 2.0,
        "motion_cycles": 4.0,
        "event_level": 0.050,
    },
    "living_particles": {
        "base": 192.0,
        "partials": ((1.0, 0.43), (6.0 / 5.0, 0.20), (4.0 / 3.0, 0.16), (3.0 / 2.0, 0.12), (2.0, 0.05)),
        "air": (768.0, 1152.0),
        "air_level": 0.017,
        "lfo_cycles": 5.0,
        "motion_cycles": 9.0,
        "event_level": 0.060,
    },
    "invisible_forces": {
        "base": 180.0,
        "partials": ((1.0, 0.49), (4.0 / 3.0, 0.19), (3.0 / 2.0, 0.15), (5.0 / 3.0, 0.10), (2.0, 0.06)),
        "air": (720.0, 1080.0),
        "air_level": 0.014,
        "lfo_cycles": 3.0,
        "motion_cycles": 6.0,
        "event_level": 0.065,
    },
}


def main() -> None:
    if len(sys.argv) < 5:
        raise SystemExit("usage: output.wav seed loop_cycles duration [family]")
    out = sys.argv[1]
    seed = int(sys.argv[2])
    cycles = int(sys.argv[3])
    dur = float(sys.argv[4])
    family = sys.argv[5] if len(sys.argv) > 5 else "geometric_waves"
    profile = PROFILES.get(family, PROFILES["geometric_waves"])

    n = int(round(SR * dur))
    rng = random.Random(seed * 7919 + cycles * 104729)
    phases = [rng.random() * TAU for _ in profile["partials"]]
    aux_phase = rng.random() * TAU
    pan_phase = rng.random() * TAU
    air_phase_a = rng.random() * TAU
    air_phase_b = rng.random() * TAU

    frames = []
    peak = 0.0
    base = profile["base"]
    lfo_cycles = profile["lfo_cycles"] + float(cycles % 2)
    motion_cycles = profile["motion_cycles"] + float(seed % 3)

    for i in range(n):
        t = i / SR
        u = t / dur

        # Slow breathing envelope: fully periodic at the loop edges.
        breath = 0.84 + 0.10 * math.sin(TAU * lfo_cycles * u + aux_phase)
        drift = 0.018 * math.sin(TAU * motion_cycles * u + aux_phase * 0.71)
        midpoint = math.sin(math.pi * u) ** 8

        bed = 0.0
        for (ratio, amp), phase in zip(profile["partials"], phases):
            freq = base * ratio * (1.0 + drift * (0.30 + 0.70 * ratio / 2.0))
            bed += amp * math.sin(TAU * freq * t + phase)

        air_a, air_b = profile["air"]
        air = profile["air_level"] * (
            0.58 * math.sin(TAU * air_a * t + air_phase_a)
            + 0.42 * math.sin(TAU * air_b * t + air_phase_b)
        )

        # Family motion is felt as a subtle timbral response rather than noise.
        event = profile["event_level"] * midpoint
        shimmer = event * (
            math.sin(TAU * (base * 2.0) * t + aux_phase * 0.41)
            + 0.55 * math.sin(TAU * (base * 3.0) * t + aux_phase)
        )

        # Invisible Forces gets a gentle beating pair; Living Particles gets a soft pulse.
        if family == "invisible_forces":
            beat = 0.045 * math.sin(TAU * (base * 4.0 + 3.0) * t + aux_phase) * math.sin(TAU * 0.65 * u)
        else:
            beat = 0.0

        if family == "living_particles":
            pulse = 0.045 * (0.5 + 0.5 * math.sin(TAU * 1.0 * u + aux_phase)) * math.sin(TAU * base * 1.5 * t + phases[1])
        else:
            pulse = 0.0

        sample = (bed * breath + air + shimmer + beat + pulse) * 0.19
        pan = 0.88 + 0.08 * math.sin(TAU * 1.0 * u + pan_phase)
        left = sample * (1.0 + 0.04 * pan)
        right = sample * (1.0 - 0.04 * pan)
        frames.append((left, right))
        peak = max(peak, abs(left), abs(right))

    target_peak = 0.24
    gain = min(target_peak / peak, 1.0) if peak else 1.0

    with wave.open(out, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        buf = bytearray()
        for left, right in frames:
            lv = int(max(-1.0, min(1.0, left * gain)) * 32767)
            rv = int(max(-1.0, min(1.0, right * gain)) * 32767)
            buf.extend(struct.pack("<hh", lv, rv))
        wf.writeframes(buf)

    print(
        f"[C11-C-AUDIO] FAMILY-SYNC AMBIENT generated: {out} | {dur:.2f}s | "
        f"{SR}Hz stereo | family={family} | grammar=family_harmonic_midrange"
    )


if __name__ == "__main__":
    main()
