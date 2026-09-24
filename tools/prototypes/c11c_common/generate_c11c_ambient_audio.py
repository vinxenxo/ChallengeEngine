import math
import struct
import sys
import wave

# C11-C 2.9.0 — global Visual Drill motion ambient.
# One shared, deterministic master across all four drill families.
# The audio deliberately ignores family/seed identity so the soundtrack itself is
# not an additional gameplay-randomness channel and never reveals authored events.
SAMPLE_RATE = 44100
CHANNELS = 2
DEFAULT_DURATION = 27.0
TARGET_PEAK = 0.22

# Low-mid, mobile-safe harmonic bed. No kick/snare/high-frequency transients.
CHORDS = [
    (73.4162, (1.0, 1.189207, 1.498307, 1.781797)),  # D minor-ish
    (65.4064, (1.0, 1.259921, 1.498307, 1.887749)),  # C6 colour
    (87.3071, (1.0, 1.189207, 1.498307, 1.781797)),  # F minor-ish
    (73.4162, (1.0, 1.259921, 1.498307, 1.781797)),  # D major-ish resolve
]


def smoothstep(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def chord_weights(t: float, duration: float):
    section = duration / 4.0
    idx = min(3, int(t / section))
    local = (t - idx * section) / section
    cross = 0.0
    if local > 0.72 and idx < 3:
        cross = smoothstep((local - 0.72) / 0.28)
    return idx, cross


def generate(path: str, seed: int, family: str, loop_cycles: int = 1, duration: float = DEFAULT_DURATION) -> None:
    duration = max(1.0, float(duration))
    sample_count = int(SAMPLE_RATE * duration)
    samples = []
    peak = 0.0

    for i in range(sample_count):
        t = i / float(SAMPLE_RATE)
        idx, cross = chord_weights(t, duration)
        chord_a = CHORDS[idx]
        chord_b = CHORDS[min(3, idx + 1)]

        # Long breathing envelope: expressive enough to accompany movement,
        # but never tied to any exact target/event timing.
        breath = 0.78 + 0.10 * math.sin(2.0 * math.pi * 0.075 * t - 0.4)
        drift = 1.0 + 0.025 * math.sin(2.0 * math.pi * 0.113 * t + 1.2)
        gain = breath * drift

        left_a = 0.0
        right_a = 0.0
        left_b = 0.0
        right_b = 0.0
        for harmonic_index, ratio in enumerate(chord_a[1]):
            freq = chord_a[0] * ratio
            amp = (0.070, 0.032, 0.018, 0.010)[harmonic_index]
            phase = (0.0, 0.35, 0.72, 1.10)[harmonic_index]
            left_a += amp * math.sin(2.0 * math.pi * freq * t + phase)
            right_a += amp * math.sin(2.0 * math.pi * freq * t + phase + 0.028)
        for harmonic_index, ratio in enumerate(chord_b[1]):
            freq = chord_b[0] * ratio
            amp = (0.055, 0.025, 0.014, 0.008)[harmonic_index]
            phase = (0.18, 0.48, 0.82, 1.18)[harmonic_index]
            left_b += amp * math.sin(2.0 * math.pi * freq * t + phase)
            right_b += amp * math.sin(2.0 * math.pi * freq * t + phase + 0.028)
        wa = 1.0 - cross
        wb = cross
        left = left_a * wa + left_b * wb
        right = right_a * wa + right_b * wb

        # Very soft upper air. It stays below the range where phone speakers
        # tend to become harsh and contains no event-locked pulse.
        air = 0.0045 * math.sin(2.0 * math.pi * 880.0 * t + 0.4)
        air += 0.0020 * math.sin(2.0 * math.pi * 1320.0 * t + 1.0)
        left += air
        right += air * 0.96

        # Final 3 seconds: settle into the fourth chord so the CTA feels like a
        # deliberate end state instead of an abrupt cut.
        if t >= duration - 3.0:
            q = smoothstep((t - (duration - 3.0)) / 3.0)
            settle = 1.0 + 0.025 * q
            left *= (1.0 - 0.12 * q) * settle
            right *= (1.0 - 0.12 * q) * settle

        # Fade only at hard file boundaries.
        fade_in = smoothstep(min(1.0, t / 1.2))
        fade_out = smoothstep(min(1.0, (duration - t) / 1.0))
        left *= gain * fade_in * fade_out
        right *= gain * fade_in * fade_out

        samples.append((left, right))
        peak = max(peak, abs(left), abs(right))

    gain = TARGET_PEAK / peak if peak > 1e-9 else 1.0
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        raw = bytearray()
        for left, right in samples:
            li = max(-32768, min(32767, int(left * gain * 32767.0)))
            ri = max(-32768, min(32767, int(right * gain * 32767.0)))
            raw.extend(struct.pack('<hh', li, ri))
        wf.writeframes(raw)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise SystemExit('usage: generate_c11c_ambient_audio.py OUTPUT.wav SEED FAMILY [LOOP_CYCLES] [DURATION_SECONDS]')
    loop_cycles = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    duration = float(sys.argv[5]) if len(sys.argv) > 5 else DEFAULT_DURATION
    generate(sys.argv[1], int(sys.argv[2]), sys.argv[3], loop_cycles, duration)
    print('[C11-C-AUDIO] Global Visual Drill motion ambient WAV generated: ' + sys.argv[1])
