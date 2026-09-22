import sys

from pathlib import Path

COMMON_DIR = Path(__file__).resolve().parent
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from generate_c11c_ambient_audio import generate


def main():
    if len(sys.argv)<5:
        raise SystemExit('usage: output.wav seed loop_cycles duration family')
    out=sys.argv[1]
    seed=int(sys.argv[2])
    cycles=int(sys.argv[3])
    dur=float(sys.argv[4])
    family=sys.argv[5] if len(sys.argv)>5 else 'generic'

    # Compatibility wrapper: the canonical generator now owns the single
    # global ambient bed. The legacy CLI remains stable for all five Loop
    # launchers, but seed/family/cycle values intentionally do not alter audio.
    generate(out, seed, family, cycles, dur)
    print(f'[C11-C-AUDIO] GLOBAL AMBIENT generated: {out} | {dur:.2f}s | family-independent')

if __name__=='__main__': main()
