#!/usr/bin/env python3
"""C11-C.1 prototype-only deterministic music bed.

Generates a 10-second stereo WAV from mathematical oscillators.
No external audio assets are required. This does not modify C7.
"""
from __future__ import annotations

import math
import sys
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44_100
DURATION = 10.0
FRAMES = int(round(SAMPLE_RATE * DURATION))
SEED = 314159

# A restrained electronic / generative bed: D minor-ish palette.
NOTES = {
    "D2": 73.4162,
    "A2": 110.0000,
    "C3": 130.8128,
    "D3": 146.8324,
    "F3": 174.6141,
    "A3": 220.0000,
    "C4": 261.6256,
    "D4": 293.6648,
    "F4": 349.2282,
    "A4": 440.0000,
    "C5": 523.2511,
    "D5": 587.3295,
}


def osc(freq: float, t: float, phase: float = 0.0) -> float:
    return math.sin(2.0 * math.pi * freq * t + phase)


def env(t: float, start: float, end: float, attack: float = 0.03, release: float = 0.10) -> float:
    if t < start or t >= end:
        return 0.0
    local = t - start
    remain = end - t
    a = min(1.0, local / max(attack, 1e-6))
    r = min(1.0, remain / max(release, 1e-6))
    return min(a, r)


def build(path: Path, seed: int = 314159) -> None:
    # Five-bar structure at 120 BPM => exactly 10 seconds.
    beat = 0.5
    bar = 2.0
    chords = [
        (NOTES["D3"], NOTES["F3"], NOTES["A3"]),
        (NOTES["C3"], NOTES["F3"], NOTES["A3"]),
        (NOTES["A2"], NOTES["C3"], NOTES["E4"] if "E4" in NOTES else NOTES["D4"]),
        (NOTES["C3"], NOTES["D3"], NOTES["A3"]),
        (NOTES["D3"], NOTES["F3"], NOTES["A3"]),
    ]
    arp = [NOTES["D4"], NOTES["A4"], NOTES["C5"], NOTES["F4"], NOTES["A4"], NOTES["D5"], NOTES["C5"], NOTES["A4"]]

    rng_phase = ((seed * 1103515245 + 12345) & 0x7FFFFFFF) / 0x7FFFFFFF
    master_gain = 0.38
    left: list[float] = []
    right: list[float] = []

    for i in range(FRAMES):
        t = i / SAMPLE_RATE
        u = t / DURATION
        sample_l = 0.0
        sample_r = 0.0

        # Soft harmonic pad whose modulation is exactly periodic over 10 s.
        chord_idx = min(4, int(t / bar))
        root, third, fifth = chords[chord_idx]
        slow = 0.5 + 0.5 * math.sin(2.0 * math.pi * u + rng_phase)
        for n, gain in ((root, 0.20), (third, 0.12), (fifth, 0.14)):
            sample_l += gain * osc(n, t) * (0.72 + 0.28 * slow)
            sample_r += gain * osc(n, t, 0.18) * (0.72 + 0.28 * slow)

        # Five-bar arpeggio: 20 quarter-note slots, repeating exactly at t=10.
        slot = int((t % DURATION) / beat)
        note = arp[slot % len(arp)]
        note_start = slot * beat
        e = env(t, note_start, note_start + beat * 0.92, 0.025, 0.12)
        tone = 0.12 * (0.72 * osc(note, t) + 0.28 * osc(note * 2.0, t)) * e
        sample_l += tone
        sample_r += tone * 0.94

        # Sub-bass pulse once per beat, musically quiet.
        bass = root / 2.0
        phase = (t % beat) / beat
        pulse = math.exp(-7.0 * phase)
        bass_tone = 0.11 * osc(bass, t) * pulse
        sample_l += bass_tone
        sample_r += bass_tone

        # Air/high harmonic locked to the same 10 s phase.
        shimmer = 0.025 * math.sin(2.0 * math.pi * 0.7 * t + 4.0 * math.pi * u)
        sample_l += shimmer
        sample_r -= shimmer * 0.8

        fade = min(1.0, t / 0.16, (DURATION - t) / 0.16)
        fade = max(0.0, min(1.0, fade))
        sample_l *= master_gain * fade
        sample_r *= master_gain * fade
        left.append(max(-1.0, min(1.0, sample_l)))
        right.append(max(-1.0, min(1.0, sample_r)))

    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        pcm = bytearray()
        for l, r in zip(left, right):
            pcm.extend(struct.pack("<hh", int(l * 32767), int(r * 32767)))
        wf.writeframes(pcm)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("seed", nargs="?", type=int, default=314159)
    args = parser.parse_args()
    build(args.output, args.seed)
    print(f"[C11-C.1-AUDIO] WAV generated: {args.output}")
