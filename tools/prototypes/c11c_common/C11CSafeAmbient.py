import json
import sys
from pathlib import Path

COMMON_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = COMMON_DIR.parents[2]
PROFILE_JSON = PROJECT_ROOT / "profiles" / "presentation" / "c11c_visual_music_profiles.json"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from generate_c11c_family_music import generate

def load_bindings():
    data=json.loads(PROFILE_JSON.read_text(encoding="utf-8"))
    return data.get("bindings", {})

def resolve_profile(family):
    bindings=load_bindings()
    for route in (f"visual_drill/{family}", f"visual_loop/{family}"):
        binding=bindings.get(route)
        if isinstance(binding,dict) and str(binding.get("profile","")).strip():
            return str(binding["profile"])
    raise ValueError(f"No FAMILY_MUSIC_V4 binding for family: {family}")

def main():
    if len(sys.argv)<5:
        raise SystemExit('usage: C11CSafeAmbient.py OUTPUT.wav SEED LOOP_CYCLES DURATION_SECONDS FAMILY [KIND] [GRAMMAR]')
    out=sys.argv[1]; seed=int(sys.argv[2]); cycles=int(sys.argv[3]); dur=float(sys.argv[4])
    family=sys.argv[5] if len(sys.argv)>5 else 'generic'
    kind='loop'; grammar=''
    if len(sys.argv)>6:
        token=sys.argv[6].strip().lower()
        if token in ('loop','drill'):
            kind=token
        else:
            grammar=sys.argv[6]
    if len(sys.argv)>7:
        grammar=sys.argv[7]
    profile=resolve_profile(family)
    grammar = grammar.strip() if grammar.strip() else family
    generate(out, seed, family, profile, cycles, dur, kind, grammar)
    print(f'[C11-C-AUDIO] FAMILY_MUSIC_V4 generated: {out} | {dur:.2f}s | family={family} | profile={profile} | kind={kind} | semantic={grammar}')

if __name__=='__main__': main()
