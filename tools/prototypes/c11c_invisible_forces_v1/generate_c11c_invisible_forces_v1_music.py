import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "c11c_common"))
from generate_c11c_ambient_audio import generate

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: generate_c11c_invisible_forces_v1_music.py OUTPUT.wav [SEED]")
    out = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 314159
    loop_cycles = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    duration = float(sys.argv[4]) if len(sys.argv) > 4 else 18.0
    generate(out, seed, "invisible_forces", loop_cycles, duration)
    print("[C11-C-AUDIO] INVISIBLE FORCES ambient WAV generated: " + out)
