import hashlib
import math
import struct
import sys
import wave
from pathlib import Path
import json

SAMPLE_RATE = 44100
CHANNELS = 2
TARGET_PEAK = 0.20
TAU = 2.0 * math.pi
CHORD_RATIOS = {
    "FLOWING_VECTOR": [(1.0, 1.189207, 1.498307, 1.781797),(1.0,1.259921,1.498307,1.887749),(1.0,1.189207,1.33484,1.681793)],
    "CIRCUIT_PULSE": [(1.0,1.259921,1.498307,1.887749),(1.0,1.189207,1.498307,1.781797),(1.0,1.33484,1.587401,2.0)],
    "ORGANIC_BLOOM": [(1.0,1.259921,1.498307,1.781797),(1.0,1.122462,1.33484,1.681793),(1.0,1.189207,1.414214,1.781797)],
    "ORBITAL_RITUAL": [(1.0,1.259921,1.5,1.887749),(1.0,1.189207,1.498307,1.781797),(1.0,1.33484,1.5,2.0)],
    "PRISMATIC_MEMORY": [(1.0,1.189207,1.414214,1.781797),(1.0,1.259921,1.498307,2.0),(1.0,1.33484,1.587401,1.887749)],
}
PROFILE_GAINS = {"FLOWING_VECTOR":0.90,"CIRCUIT_PULSE":0.86,"ORGANIC_BLOOM":0.92,"ORBITAL_RITUAL":0.84,"PRISMATIC_MEMORY":0.88}
PROFILE_DATA_PATH = Path(__file__).resolve().parents[3] / "profiles" / "presentation" / "c11c_visual_music_profiles.json"

def load_profile_roots():
    data = json.loads(PROFILE_DATA_PATH.read_text(encoding="utf-8"))
    return {str(entry["id"]): float(entry["root_hz"]) for entry in data.get("profiles", []) if isinstance(entry, dict) and "id" in entry and "root_hz" in entry}

PROFILE_ROOTS = load_profile_roots()

def smoothstep(x):
    x=max(0.0,min(1.0,float(x))); return x*x*(3.0-2.0*x)

def unit_phase(seed,family,profile):
    key=f"{int(seed)}|{family}|{profile}".encode("utf-8")
    value=int.from_bytes(hashlib.sha256(key).digest()[:8],"big")
    return (value % 1000000) / 1000000.0 * TAU

def generate(path, seed, family, profile_id, loop_cycles=1, duration=18.0, kind="loop"):
    if profile_id not in PROFILE_ROOTS:
        raise ValueError(f"Unknown music profile: {profile_id}")
    duration=max(1.0,float(duration))
    total=int(SAMPLE_RATE*duration)
    root=PROFILE_ROOTS[profile_id]
    chords=CHORD_RATIOS[profile_id]
    phase=unit_phase(seed,family,profile_id)
    gain_scale=PROFILE_GAINS[profile_id]
    cycle_period=max(4.0,min(18.0,duration/max(1,int(loop_cycles))))
    raw=[]; peak=0.0
    for i in range(total):
        t=i/SAMPLE_RATE
        pos=(t/cycle_period)%1.0
        section=min(len(chords)-1,int(pos*len(chords)))
        local=(pos*len(chords))-section
        next_section=(section+1) % len(chords)
        w=smoothstep(max(0.0,(local-0.72)/0.28)) if section<len(chords)-1 else 0.0
        a=chords[section]; b=chords[next_section]
        if kind == "loop":
            breath=0.78+0.10*math.sin(TAU*pos+phase)
            drift=1.0+0.025*math.sin(TAU*2.0*pos+phase*0.7)
        else:
            breath=0.78+0.10*math.sin(TAU*0.052*t+phase)
            drift=1.0+0.025*math.sin(TAU*0.087*t+phase*0.7)
        left=right=0.0
        wa=1.0-w
        wb=w
        for h,r in enumerate(a):
            f=root*r; amp=(0.070,0.032,0.018,0.010)[h]*gain_scale
            ph=phase+(0.21,0.48,0.79,1.13)[h]
            left+=amp*wa*math.sin(TAU*f*t+ph); right+=amp*wa*math.sin(TAU*f*t+ph+0.024)
        for h,r in enumerate(b):
            f=root*r; amp=(0.070,0.032,0.018,0.010)[h]*gain_scale
            ph=phase+(0.21,0.48,0.79,1.13)[h]
            left += amp*wb*math.sin(TAU*f*t+ph); right += amp*wb*math.sin(TAU*f*t+ph+0.024)
        # Subtle profile character; no percussion or exact event timing.
        if profile_id == "FLOWING_VECTOR":
            mod = (TAU*2.0*pos + phase*0.3) if kind == "loop" else (TAU*0.9*t + phase*0.3)
            left += 0.008*math.sin(TAU*146.83*t+phase*0.3)*0.96 + 0.0015*math.sin(mod)
            right += 0.0075*math.sin(TAU*146.83*t+phase*0.3+0.03)*0.96 + 0.0014*math.sin(mod)
        elif profile_id == "CIRCUIT_PULSE":
            mod = (TAU*3.0*pos + phase) if kind == "loop" else (TAU*0.42*t+phase)
            pulse=0.004*(0.5+0.5*math.sin(mod)); left += pulse; right += pulse*0.98
        elif profile_id == "ORGANIC_BLOOM":
            mod = (TAU*2.0*pos+0.7) if kind == "loop" else (TAU*0.09*t+0.7)
            shimmer=0.006*math.sin(TAU*220.0*t+phase*0.5)*math.sin(mod); left += shimmer; right += shimmer*0.94
        elif profile_id == "ORBITAL_RITUAL":
            mod = (TAU*1.0*pos+1.4) if kind == "loop" else (TAU*0.071*t+1.4)
            shimmer=0.005*math.sin(TAU*164.81*t+phase*0.6)*math.sin(mod); left += shimmer; right += shimmer*0.97
        else:
            mod = (TAU*2.0*pos+phase*0.9) if kind == "loop" else (TAU*0.11*t+phase*0.9)
            ref=0.006*math.sin(TAU*196.0*t+phase*0.9) + 0.0015*math.sin(mod); left += ref; right -= ref*0.55
        left*=breath*drift; right*=breath*drift
        if kind == "drill" and t >= duration-3.0:
            q=smoothstep((t-(duration-3.0))/3.0)
            left*=1.0-0.14*q; right*=1.0-0.14*q
        fade_in=smoothstep(min(1.0,t/1.2))
        fade_out=smoothstep(min(1.0,(duration-t)/1.0))
        left*=fade_in*fade_out; right*=fade_in*fade_out
        raw.append((left,right)); peak=max(peak,abs(left),abs(right))
    peak=max([max(abs(a),abs(b)) for a,b in raw] or [0.0])
    norm=TARGET_PEAK/peak if peak>1e-9 else 1.0
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as wf:
        wf.setnchannels(CHANNELS); wf.setsampwidth(2); wf.setframerate(SAMPLE_RATE)
        buf=bytearray()
        for left,right in raw:
            li=max(-32768,min(32767,int(left*norm*32767.0))); ri=max(-32768,min(32767,int(right*norm*32767.0)))
            buf.extend(struct.pack('<hh',li,ri))
        wf.writeframes(buf)

if __name__=='__main__':
    if len(sys.argv)<7:
        raise SystemExit('usage: generate_c11c_family_music.py OUTPUT.wav SEED FAMILY PROFILE_ID DURATION_SECONDS KIND[loop|drill]')
    generate(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4],1,float(sys.argv[5]),sys.argv[6])
    print(f'[C11-C-AUDIO] FAMILY_MUSIC_V3 generated: {sys.argv[1]} | family={sys.argv[3]} | profile={sys.argv[4]} | kind={sys.argv[6]}')
