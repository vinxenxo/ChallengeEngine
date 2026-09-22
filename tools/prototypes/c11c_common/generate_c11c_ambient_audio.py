import math
import struct
import sys
import wave

SAMPLE_RATE = 44100
CHANNELS = 2
MASTER_DURATION = 18.0  # Fixed master bed. Shorter renders are exact prefixes; longer renders loop this bed.


def generate(path: str, seed: int, family: str, loop_cycles: int = 1, duration: float = 18.0) -> None:
    """Generate the single shared C11-C ambient bed.

    `seed`, `family` and `loop_cycles` remain in the public signature for
    compatibility with existing family launchers, but they intentionally do
    not alter the generated audio. Duration is the only physical variable.
    """
    _ = seed
    _ = family
    _ = loop_cycles
    duration = max(1.0, float(duration))
    master_count = max(2, int(round(SAMPLE_RATE * MASTER_DURATION)))
    output_count = max(2, int(round(SAMPLE_RATE * duration)))
    frames = bytearray()

    # Fixed harmonic bed: low-intrusion, mobile-safe and family-independent.
    base = 144.0
    partials = ((1.0, 0.46), (4.0 / 3.0, 0.20), (3.0 / 2.0, 0.14), (2.0, 0.07))
    air_freqs = (576.0, 864.0)
    for i in range(output_count):
        master_i = i % master_count
        u = float(master_i) / float(master_count - 1)
        t = float(master_i) / float(SAMPLE_RATE)

        # Smooth periodic envelopes. All phase movement is deterministic.
        breath = 0.5 - 0.5 * math.cos(2.0 * math.pi * u)
        swell = 0.5 - 0.5 * math.cos(4.0 * math.pi * u)
        left = 0.0
        right = 0.0

        for ratio, amplitude in partials:
            freq = base * ratio
            phase_offset = 0.035 if ratio > 1.0 else 0.0
            left += amplitude * math.sin(2.0 * math.pi * freq * t)
            right += amplitude * math.sin(2.0 * math.pi * freq * t + phase_offset)

        # Quiet sub layer keeps the bed audible on small mobile speakers without a sharp transient.
        sub = 0.032 * math.sin(2.0 * math.pi * (base * 0.5) * t)
        left += sub
        right += sub

        air = 0.010 * breath * math.sin(2.0 * math.pi * air_freqs[0] * t)
        air += 0.006 * swell * math.sin(2.0 * math.pi * air_freqs[1] * t + 0.22)
        left += air
        right += air * 0.92

        # Gentle global gain. The final level intentionally stays unobtrusive.
        gain = 0.13 + 0.025 * breath + 0.012 * swell
        left *= gain
        right *= gain

        li = max(-32768, min(32767, int(left * 32767.0)))
        ri = max(-32768, min(32767, int(right * 32767.0)))
        frames.extend(struct.pack('<hh', li, ri))

    with wave.open(path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(frames)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise SystemExit('usage: generate_c11c_ambient_audio.py OUTPUT.wav SEED FAMILY [LOOP_CYCLES] [DURATION_SECONDS]')
    loop_cycles = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    duration = float(sys.argv[5]) if len(sys.argv) > 5 else 18.0
    generate(sys.argv[1], int(sys.argv[2]), sys.argv[3], loop_cycles, duration)
    print('[C11-C-AUDIO] Shared global ambient WAV generated: ' + sys.argv[1])
