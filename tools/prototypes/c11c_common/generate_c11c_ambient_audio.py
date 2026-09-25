import sys
from pathlib import Path
COMMON_DIR=Path(__file__).resolve().parent
if str(COMMON_DIR) not in sys.path: sys.path.insert(0,str(COMMON_DIR))
from C11CSafeAmbient import resolve_profile
from generate_c11c_family_music import generate

if __name__=='__main__':
    if len(sys.argv)<4: raise SystemExit('usage: generate_c11c_ambient_audio.py OUTPUT.wav SEED FAMILY [LOOP_CYCLES] [DURATION_SECONDS] [GRAMMAR]')
    out=sys.argv[1]; seed=int(sys.argv[2]); family=sys.argv[3]
    cycles=int(sys.argv[4]) if len(sys.argv)>4 else 1; dur=float(sys.argv[5]) if len(sys.argv)>5 else 24.0
    grammar=sys.argv[6] if len(sys.argv)>6 else ''
    profile=resolve_profile(family)
    generate(out,seed,family,profile,cycles,dur,'loop',grammar)
    print('[C11-C-AUDIO] FAMILY_MUSIC_V4 generated: '+out)
