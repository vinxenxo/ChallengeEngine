import math
import struct
import sys
import wave

SAMPLE_RATE = 44100
DURATION = 18.0
CHANNELS = 2
N = int(SAMPLE_RATE * DURATION)

FAMILY_BASE = {
    "geometric": 54.0,
    "fractal": 43.0,
    "sacred_symmetry": 39.0,
    "living_particles": 47.0,
    "invisible_forces": 35.0,
}
FAMILY_HARMONICS = {
    "geometric": (1, 2, 3, 5),
    "fractal": (1, 3, 5, 8),
    "sacred_symmetry": (1, 2, 4, 6),
    "living_particles": (1, 2, 3, 7),
    "invisible_forces": (1, 2, 5, 7),
}

def unit(seed: int, salt: int) -> float:
    x = (seed ^ (salt * 374761393)) & 0xFFFFFFFF
    x ^= x >> 13
    x = (x * 1274126177) & 0xFFFFFFFF
    x ^= x >> 16
    x = (x * 2246822519) & 0xFFFFFFFF
    x ^= x >> 13
    return (x & 0xFFFFFFFF) / 4294967295.0

def circular_distance(a: float, b: float) -> float:
    d = abs(a - b)
    return min(d, 1.0 - d)

def resonant_bell(u: float, center: float, width: float, freq_hz: int, amp: float, duration: float) -> float:
    d = circular_distance(u, center)
    env = math.exp(-((d / width) ** 2))
    local_time = ((u - center) % 1.0) * duration
    phase = 2.0 * math.pi * float(freq_hz) * local_time
    # A small inharmonic-like partial stack, but every carrier is an integer Hz loop.
    return amp * env * (
        0.72 * math.sin(phase)
        + 0.20 * math.sin(2.0 * phase + 0.35)
        + 0.08 * math.sin(3.0 * phase + 0.72)
    )

def generate(path: str, seed: int, family: str, loop_cycles: int = 1, duration: float = DURATION) -> None:
    base = FAMILY_BASE.get(family, 44.0) + 3.0 * unit(seed, 17)
    h = FAMILY_HARMONICS.get(family, (1,2,3,5))
    loop_cycles = max(1, int(loop_cycles))
    root_harmonic = 3 + int(unit(seed, 31) * 4)
    root_cycles = loop_cycles * max(1, root_harmonic)
    family_bias = unit(seed, 43)

    duration = max(1.0, float(duration))
    sample_count = int(SAMPLE_RATE * duration)
    frames = bytearray()
    for i in range(sample_count):
        u = i / float(N)
        breath = 0.5 - 0.5 * math.cos(2.0 * math.pi * u)
        slow = 0.5 - 0.5 * math.cos(4.0 * math.pi * u)
        left = 0.0
        right = 0.0

        # Deep continuous ambient bed: every oscillator completes an integer number of cycles.
        left += 0.34 * math.sin(2.0 * math.pi * root_cycles * u)
        right += 0.34 * math.sin(2.0 * math.pi * root_cycles * u + 0.035)
        left += 0.12 * math.sin(2.0 * math.pi * (root_cycles + h[1]) * u + 0.4)
        right += 0.12 * math.sin(2.0 * math.pi * (root_cycles + h[1]) * u + 0.55)
        left += 0.065 * math.sin(2.0 * math.pi * (root_cycles + h[2]) * u + 0.8)
        right += 0.065 * math.sin(2.0 * math.pi * (root_cycles + h[2]) * u + 0.95)

        # Slow resonant singing-bowl strikes anchored to the visual loop landmarks.
        strike_amp = 0.075 + 0.035 * family_bias
        bowl_root = 174 + int(unit(seed, 59) * 88)
        bowl_root = max(1, bowl_root)
        for j in range(loop_cycles):
            center = float(j) / float(loop_cycles)
            freq_hz = int(bowl_root + ((seed + j * 11) % 7))
            strike = resonant_bell(u, center, 0.020 + 0.005 * unit(seed, 61+j), freq_hz, strike_amp, duration)
            left += strike * (0.88 + 0.04 * math.sin(2.0 * math.pi * loop_cycles * u))
            right += strike * (0.88 + 0.04 * math.cos(2.0 * math.pi * loop_cycles * u))

        # Family-linked pulse: always periodic on the complete loop.
        pulse = 0.5 - 0.5 * math.cos(2.0 * math.pi * loop_cycles * u)

        low_cycles = max(1, root_cycles // 2)
        low = 0.020 * math.sin(2.0 * math.pi * low_cycles * u)
        shimmer_hz = root_cycles + 17
        left += low + 0.018 * pulse * math.sin(2.0 * math.pi * shimmer_hz * u)
        right += low + 0.015 * pulse * math.sin(2.0 * math.pi * shimmer_hz * u + 0.25)

        gain = 0.48 + 0.08 * breath + 0.04 * slow
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
    duration = float(sys.argv[5]) if len(sys.argv) > 5 else DURATION
    generate(sys.argv[1], int(sys.argv[2]), sys.argv[3], loop_cycles, duration)
    print('[C11-C-AUDIO] Ambient WAV generated: ' + sys.argv[1])
