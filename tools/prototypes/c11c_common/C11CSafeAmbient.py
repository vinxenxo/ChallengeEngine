import math, random, struct, sys, wave

SR=44100
TAU=2*math.pi
BASE={"geometric":110.0,"fractal":92.0,"sacred_symmetry":82.0,"living_particles":98.0,"invisible_forces":87.0}


def main():
    if len(sys.argv)<5:
        raise SystemExit('usage: output.wav seed loop_cycles duration family')
    out=sys.argv[1]; seed=int(sys.argv[2]); cycles=int(sys.argv[3]); dur=float(sys.argv[4]); family=sys.argv[5] if len(sys.argv)>5 else 'generic'
    n=int(round(SR*dur)); rng=random.Random(seed*7919+cycles*104729)
    base=BASE.get(family,96.0)
    # Safe mobile profile: no sub-bass, no hard transients, no phase-inverted stereo,
    # low crest factor, gently filtered noise, and slow periodic modulation.
    phase=rng.random()*TAU
    phase2=rng.random()*TAU
    last_l=last_r=0.0
    hp_l=hp_r=0.0
    out_frames=[]
    maxabs=0.0
    for i in range(n):
        t=i/SR; u=t/dur
        env=min(1.0,t/1.8)*min(1.0,(dur-t)/2.0)
        # Broad, quiet air bed: correlated but not identical stereo.
        noise=rng.uniform(-1,1)
        last_l=0.985*last_l+0.015*noise
        last_r=0.985*last_r+0.015*(0.94*noise+0.06*rng.uniform(-1,1))
        air_l=last_l*0.16; air_r=last_r*0.16
        # Soft harmonic bed. Frequencies are comfortably above phone resonance/sub-bass zones.
        slow=0.5+0.5*math.sin(TAU*cycles*u+phase)
        vib=0.22*math.sin(TAU*(cycles/dur)*t+phase2)
        f1=base*(1+0.002*vib)
        f2=f1*1.5
        f3=f1*2.0
        s1=math.sin(TAU*f1*t+phase)
        s2=math.sin(TAU*f2*t+phase2)
        s3=math.sin(TAU*f3*t+0.37*phase)
        # Slow movement, not a pulse/beep.
        bed=(0.42*s1 + 0.16*s2 + 0.055*s3)*(0.58+0.16*slow)
        # Very soft upper harmonic prevents the sound becoming a bass-only rumble.
        shimmer=0.018*math.sin(TAU*(f1*3.0)*t+0.73)
        l=(air_l*0.72 + bed + shimmer)*env*0.105
        r=(air_r*0.72 + bed*0.97 + shimmer*0.8)*env*0.105
        # Gentle high-pass/DC removal.
        hp_l=0.995*hp_l + 0.005*l
        hp_r=0.995*hp_r + 0.005*r
        l-=hp_l*0.15; r-=hp_r*0.15
        maxabs=max(maxabs,abs(l),abs(r))
        out_frames.append((l,r))
    gain=min(0.92/maxabs,1.0) if maxabs else 1.0
    with wave.open(out,'wb') as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
        buf=bytearray()
        for l,r in out_frames:
            buf.extend(struct.pack('<hh',int(max(-1,min(1,l*gain))*32767),int(max(-1,min(1,r*gain))*32767)))
        wf.writeframes(buf)
    print(f'[C11-C-AUDIO] SAFE MOBILE AMBIENT generated: {out} | {dur:.2f}s | {SR}Hz stereo | family={family}')

if __name__=='__main__': main()
