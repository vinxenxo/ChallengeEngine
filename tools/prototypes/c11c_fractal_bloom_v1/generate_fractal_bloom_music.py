import math
import struct
import sys
import wave

SAMPLE_RATE = 44100
DURATION = 10.0
CHANNELS = 2
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 314159


def seed_unit(seed: int, salt: int) -> float:
    x = (seed ^ salt) & 0xFFFFFFFF
    x ^= (x >> 16)
    x = (x * 0x7FEB352D) & 0xFFFFFFFF
    x ^= (x >> 15)
    x = (x * 0x846CA68B) & 0xFFFFFFFF
    x ^= (x >> 16)
    return x / 0xFFFFFFFF


def write_wav(path: str) -> None:
    count = int(SAMPLE_RATE * DURATION)
    rng_a = seed_unit(SEED, 17)
    rng_b = seed_unit(SEED, 43)
    base = 48.0 + 6.0 * rng_a
    fifth = base * 1.5
    upper = base * 2.0 + 2.0 * rng_b

    frames = bytearray()
    for i in range(count):
        t = i / SAMPLE_RATE
        u = t / DURATION

        # Slow, seamless breathing envelope: zero derivative at both ends.
        breath = 0.5 - 0.5 * math.cos(2.0 * math.pi * u)
        pulse = 0.5 - 0.5 * math.cos(4.0 * math.pi * u)

        pad = (
            0.55 * math.sin(2.0 * math.pi * base * t)
            + 0.24 * math.sin(2.0 * math.pi * fifth * t + 0.8 * math.sin(2.0 * math.pi * u))
            + 0.13 * math.sin(2.0 * math.pi * upper * t + 0.7)
        )
        sub = 0.12 * math.sin(2.0 * math.pi * (base * 0.5) * t)
        shimmer = 0.035 * math.sin(2.0 * math.pi * (upper * 4.0) * t) * (0.15 + 0.85 * breath)
        signal = (pad + sub + shimmer) * (0.34 + 0.28 * breath + 0.08 * pulse)

        # Soft stereo drift; deterministic and periodic.
        pan = 0.18 * math.sin(2.0 * math.pi * u)
        left = signal * (1.0 - pan)
        right = signal * (1.0 + pan)

        # Four-cosine fade to avoid click at the file boundary.
        edge = min(1.0, u / 0.06, (1.0 - u) / 0.06)
        edge = max(0.0, 0.5 - 0.5 * math.cos(math.pi * edge))
        left *= edge
        right *= edge

        left_i = max(-32768, min(32767, int(left * 32767.0)))
        right_i = max(-32768, min(32767, int(right * 32767.0)))
        frames.extend(struct.pack('<hh', left_i, right_i))

    with wave.open(path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(frames)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('usage: generate_fractal_bloom_music.py OUTPUT.wav [SEED]')
    write_wav(sys.argv[1])
    print(f'[C11-C.2-AUDIO] WAV generated: {sys.argv[1]}')
