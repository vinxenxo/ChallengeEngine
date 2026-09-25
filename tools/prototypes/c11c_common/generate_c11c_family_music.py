import hashlib
import math
import struct
import sys
import wave
from pathlib import Path
import json

SAMPLE_RATE = 44100
CHANNELS = 2
TARGET_PEAK = 0.35
AUDIO_REVISION = "4.1.1"
TAU = 2.0 * math.pi
PENTATONIC_HZ = [110.0, 130.81, 146.83, 164.81, 196.0, 220.0, 261.63, 293.66, 329.63]
A2_HZ = 110.0
PENTATONIC_RATIOS = [f / A2_HZ for f in PENTATONIC_HZ]

PROFILE_ROOTS_PATH = Path(__file__).resolve().parents[3] / "profiles" / "presentation" / "c11c_visual_music_profiles.json"

STYLE = {
    "FLOWING_VECTOR": {"attack": 1.8, "release": 2.4, "cutoff": 1800.0, "width": 0.18, "notes": 4, "octave": 0, "texture": 0.020},
    "CIRCUIT_PULSE": {"attack": 0.65, "release": 1.8, "cutoff": 2500.0, "width": 0.12, "notes": 8, "octave": 1, "texture": 0.028},
    "ORGANIC_BLOOM": {"attack": 2.2, "release": 2.8, "cutoff": 1500.0, "width": 0.24, "notes": 3, "octave": 0, "texture": 0.018},
    "ORBITAL_RITUAL": {"attack": 2.0, "release": 2.6, "cutoff": 1350.0, "width": 0.20, "notes": 5, "octave": 0, "texture": 0.015},
    "PRISMATIC_MEMORY": {"attack": 1.4, "release": 2.2, "cutoff": 2200.0, "width": 0.30, "notes": 6, "octave": 1, "texture": 0.024},
}

PROFILE_GAINS = {
    "FLOWING_VECTOR": 0.95,
    "CIRCUIT_PULSE": 0.93,
    "ORGANIC_BLOOM": 0.98,
    "ORBITAL_RITUAL": 0.90,
    "PRISMATIC_MEMORY": 0.94,
}

PROFILE_BED_LEVELS = {
    "FLOWING_VECTOR": 0.55,
    "CIRCUIT_PULSE": 0.52,
    "ORGANIC_BLOOM": 1.30,
    "ORBITAL_RITUAL": 0.68,
    "PRISMATIC_MEMORY": 0.54,
}

# Musical motifs: pentatonic note indices, chosen to remain consonant while clearly differentiating the families.
MOTIFS = {
    "FLOWING_VECTOR": [[0, 2, 4, 5], [0, 3, 5, 4], [2, 4, 5, 7]],
    "CIRCUIT_PULSE": [[0, 2, 3, 5, 3, 2, 5, 7], [0, 3, 2, 5, 7, 5, 3, 2], [2, 4, 5, 4, 7, 5, 4, 2]],
    "ORGANIC_BLOOM": [[0, 2, 5], [0, 3, 5], [2, 4, 7]],
    "ORBITAL_RITUAL": [[0, 4, 5, 7, 4], [0, 3, 5, 7, 5], [0, 2, 4, 7, 5]],
    "PRISMATIC_MEMORY": [[0, 2, 4, 7, 5, 3], [0, 3, 5, 7, 4, 2], [2, 4, 7, 5, 3, 0]],
}


def load_profile_roots():
    data = json.loads(PROFILE_ROOTS_PATH.read_text(encoding="utf-8"))
    return {str(e["id"]): float(e["root_hz"]) for e in data.get("profiles", []) if isinstance(e, dict) and "id" in e and "root_hz" in e}


PROFILE_ROOTS = load_profile_roots()


def stable_u(seed: int, family: str, profile: str, grammar: str, salt: str) -> float:
    key = f"{int(seed)}|{family}|{profile}|{grammar}|{salt}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    return int.from_bytes(digest[:8], "big") / float(2**64 - 1)


def smoothstep(x: float) -> float:
    x = max(0.0, min(1.0, float(x)))
    return x * x * (3.0 - 2.0 * x)


def cyclic_value_noise_1d(t: float, period_seconds: float, seed: int, family: str, profile: str, grammar: str) -> float:
    period = max(float(period_seconds), 1.0)
    phase = (float(t) / period) % 1.0
    segments = 8
    position = phase * segments
    cell = int(math.floor(position)) % segments
    frac = position - math.floor(position)
    a = stable_u(seed, family, profile, grammar, f"cyclic_n{cell}") * 2.0 - 1.0
    b = stable_u(seed, family, profile, grammar, f"cyclic_n{(cell + 1) % segments}") * 2.0 - 1.0
    f = smoothstep(frac)
    return a + (b - a) * f


def value_noise_1d(t: float, seed: int, family: str, profile: str, grammar: str) -> float:
    return cyclic_value_noise_1d(t, 1.0 / 0.06, seed, family, profile, grammar)

def lowpass_pair(left: float, right: float, state: tuple[float, float], cutoff: float) -> tuple[float, float, tuple[float, float]]:
    alpha = (TAU * cutoff) / (TAU * cutoff + SAMPLE_RATE)
    lp_l = state[0] + alpha * (left - state[0])
    lp_r = state[1] + alpha * (right - state[1])
    return lp_l, lp_r, (lp_l, lp_r)


def low_pass_periodic_modulated(left: float, right: float, state: tuple[float, float], base_cutoff: float, noise: float) -> tuple[float, float, tuple[float, float]]:
    modulation = 0.84 + 0.20 * ((float(noise) + 1.0) * 0.5)
    cutoff = max(700.0, min(3400.0, float(base_cutoff) * modulation))
    return lowpass_pair(left, right, state, cutoff)


def note_envelope(local_t: float, length: float, attack: float, release: float) -> float:
    a = smoothstep(local_t / max(attack, 1e-6))
    r = smoothstep((length - local_t) / max(release, 1e-6))
    sustain = 0.86
    return min(a, r) * sustain


def generate(path, seed, family, profile_id, loop_cycles=1, duration=18.0, kind="loop", grammar=""):
    if profile_id not in PROFILE_ROOTS:
        raise ValueError(f"Unknown music profile: {profile_id}")
    style = STYLE[profile_id]
    duration = max(1.0, float(duration))
    total = int(SAMPLE_RATE * duration)
    root = PROFILE_ROOTS[profile_id]
    gain_scale = PROFILE_GAINS[profile_id]
    cycles = max(1, int(loop_cycles))
    cycle_period = max(4.0, min(18.0, duration / cycles if kind == "loop" else duration))

    motif_bank = MOTIFS[profile_id]
    motif_selector = int(stable_u(seed, family, profile_id, grammar, "motif") * len(motif_bank)) % len(motif_bank)
    motif = list(motif_bank[motif_selector])
    # Grammar is deliberately part of the selection, so every visual subtype can receive a distinct arrangement.
    shift = int(stable_u(seed, family, profile_id, grammar, "shift") * 5.0) - 2
    motif = [max(0, min(8, n + shift if (i + motif_selector) % 3 == 0 else n)) for i, n in enumerate(motif)]
    direction = -1 if stable_u(seed, family, profile_id, grammar, "direction") < 0.5 else 1
    if direction < 0:
        motif = list(reversed(motif))
    grammar_octave = 1 if stable_u(seed, family, profile_id, grammar, "grammar_octave") > 0.74 else 0
    grammar_sustain = 0.90 + 0.08 * stable_u(seed, family, profile_id, grammar, "grammar_sustain")

    note_count = len(motif)
    raw = []
    peak = 0.0
    filter_state = (0.0, 0.0)
    phase_seed = stable_u(seed, family, profile_id, grammar, "phase") * TAU
    stereo_phase = stable_u(seed, family, profile_id, grammar, "stereo") * TAU

    for i in range(total):
        t = i / SAMPLE_RATE
        pos = (t / cycle_period) % 1.0
        segment = min(note_count - 1, int(pos * note_count))
        local = (pos * note_count - segment) * (cycle_period / note_count)
        note_len = cycle_period / note_count
        note_idx = motif[segment]
        freq = root * PENTATONIC_RATIOS[note_idx] * (2.0 ** (style["octave"] + grammar_octave))

        env = note_envelope(local, note_len, min(style["attack"], note_len * 0.70), min(style["release"], note_len * 0.85)) * grammar_sustain
        if profile_id == "CIRCUIT_PULSE":
            # Distinct but soft transient envelope for the saccadic family.
            env *= 0.72 + 0.28 * math.sin(math.pi * min(1.0, local / max(note_len, 1e-6)))
        elif profile_id == "ORBITAL_RITUAL":
            env *= 0.82 + 0.18 * math.sin(TAU * (t / max(cycle_period, 1e-6)) + 0.7)

        # Pentagon-pure tone bed with profile-specific timbral identity.
        carrier_phase = TAU * freq * t + phase_seed
        if profile_id == "FLOWING_VECTOR":
            voice = math.sin(carrier_phase) + 0.10 * math.sin(2.0 * carrier_phase + 0.31) + 0.035 * math.sin(3.0 * carrier_phase + 1.07)
        elif profile_id == "CIRCUIT_PULSE":
            voice = math.sin(carrier_phase) + 0.34 * math.sin(2.0 * carrier_phase + 0.15) + 0.10 * math.sin(4.0 * carrier_phase + 0.51)
        elif profile_id == "ORGANIC_BLOOM":
            detune = 0.9975 + 0.0045 * ((stable_u(seed, family, profile_id, grammar, "detune") - 0.5) * 2.0)
            voice = math.sin(carrier_phase) + 0.45 * math.sin(TAU * freq * detune * t + phase_seed * 0.93) + 0.10 * math.sin(3.0 * carrier_phase + 0.73)
        elif profile_id == "ORBITAL_RITUAL":
            voice = math.sin(carrier_phase) + 0.14 * math.sin(3.0 * carrier_phase + 0.42) + 0.045 * math.sin(5.0 * carrier_phase + 0.91)
        else:
            voice = math.sin(carrier_phase) + 0.30 * math.sin(2.0 * carrier_phase + 0.25) + 0.13 * math.sin(4.0 * carrier_phase + 0.67) + 0.035 * math.sin(7.0 * carrier_phase + 1.11)
        layer_freq = root * PENTATONIC_RATIOS[(note_idx + 2 + motif_selector) % len(PENTATONIC_RATIOS)]
        layer_amount = 0.12 if profile_id == "ORBITAL_RITUAL" else (0.22 if profile_id == "FLOWING_VECTOR" else 0.30)
        layer = layer_amount * math.sin(TAU * layer_freq * t + phase_seed * 0.71)
        s = (voice + layer) * env * gain_scale

        # Continuous family bed keeps mobile playback audible without percussion.
        bed_level = PROFILE_BED_LEVELS[profile_id]
        bed_freq = root * (2.0 if profile_id in ("CIRCUIT_PULSE", "PRISMATIC_MEMORY") else 1.0)
        bed_mod = 0.92 + 0.08 * math.sin(TAU * (t / max(cycle_period, 1e-6)) + phase_seed * 0.41)
        if profile_id == "CIRCUIT_PULSE":
            bed_wave = math.sin(TAU * bed_freq * t + phase_seed * 0.21) + 0.12 * math.sin(TAU * bed_freq * 2.0 * t + phase_seed * 0.63)
        elif profile_id == "ORBITAL_RITUAL":
            bed_wave = math.sin(TAU * bed_freq * t + phase_seed * 0.21) + 0.18 * math.sin(TAU * bed_freq * 0.5 * t + phase_seed * 0.63)
        elif profile_id == "ORGANIC_BLOOM":
            bed_wave = math.sin(TAU * bed_freq * t + phase_seed * 0.21) + 0.36 * math.sin(TAU * bed_freq * 1.5 * t + phase_seed * 0.63)
        else:
            bed_wave = math.sin(TAU * bed_freq * t + phase_seed * 0.21) + 0.24 * math.sin(TAU * bed_freq * 1.5 * t + phase_seed * 0.63)
        bed = bed_level * bed_mod * bed_wave
        s += bed

        # Family-specific musical motion. This is the audible coupling to the visual grammar, without reading gameplay truth.
        if profile_id == "FLOWING_VECTOR":
            motion = math.sin(TAU * (t / cycle_period) + stereo_phase) * 0.10
            left = s * (1.0 + motion)
            right = s * (1.0 - motion)
        elif profile_id == "CIRCUIT_PULSE":
            gate = 0.82 + 0.18 * math.sin(TAU * note_count * pos + stereo_phase)
            left = s * gate
            right = s * (0.92 + 0.08 * math.sin(TAU * note_count * pos + stereo_phase + 0.55))
        elif profile_id == "ORGANIC_BLOOM":
            swell = 0.88 + 0.12 * math.sin(TAU * (t / cycle_period) + phase_seed * 0.3)
            left = s * swell
            right = s * (0.95 + 0.05 * math.sin(TAU * (t / cycle_period) + phase_seed * 0.3 + 0.8))
        elif profile_id == "ORBITAL_RITUAL":
            orbit = 0.12 * math.sin(TAU * (t / cycle_period) + stereo_phase)
            left = s * (1.0 + orbit)
            right = s * (1.0 - orbit)
        else:
            mirror = 0.14 * math.sin(TAU * 2.0 * (t / cycle_period) + stereo_phase)
            left = s * (1.0 + mirror)
            right = s * (1.0 - mirror)

        # Slow loop-safe deterministic noise drives a periodic low-pass cutoff.
        n = cyclic_value_noise_1d(t, cycle_period, seed, family, profile_id, grammar)
        left, right, filter_state = low_pass_periodic_modulated(left, right, filter_state, style["cutoff"], n)

        # Very restrained high-frequency air; profile/grammar-specific, never per-particle static.
        air_phase = TAU * (root * 2.0) * t + phase_seed * 0.37
        air = style["texture"] * math.sin(air_phase) * (0.35 + 0.65 * env)
        left += air
        right -= air * (0.55 if profile_id == "PRISMATIC_MEMORY" else 0.25)

        if kind == "drill" and t >= duration - 3.0:
            q = smoothstep((t - (duration - 3.0)) / 3.0)
            left *= 1.0 - 0.18 * q
            right *= 1.0 - 0.18 * q

        fade_in = smoothstep(min(1.0, t / 1.25))
        fade_out = smoothstep(min(1.0, (duration - t) / 1.75))
        left *= fade_in * fade_out
        right *= fade_in * fade_out
        raw.append((left, right))
        peak = max(peak, abs(left), abs(right))

    norm = TARGET_PEAK / peak if peak > 1e-9 else 1.0
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        buf = bytearray()
        for left, right in raw:
            li = max(-32768, min(32767, int(left * norm * 32767.0)))
            ri = max(-32768, min(32767, int(right * norm * 32767.0)))
            buf.extend(struct.pack('<hh', li, ri))
        wf.writeframes(buf)


if __name__ == '__main__':
    if len(sys.argv) < 7:
        raise SystemExit('usage: generate_c11c_family_music.py OUTPUT.wav SEED FAMILY PROFILE_ID DURATION_SECONDS KIND[loop|drill] [GRAMMAR]')
    grammar = sys.argv[7] if len(sys.argv) > 7 else ''
    generate(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], 1, float(sys.argv[5]), sys.argv[6], grammar)
    print(f'[C11-C-AUDIO] FAMILY_MUSIC_V4 generated: {sys.argv[1]} | family={sys.argv[3]} | profile={sys.argv[4]} | kind={sys.argv[6]} | grammar={grammar}')
