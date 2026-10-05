import argparse, hashlib, json, math, struct, wave
from pathlib import Path
ENGINE_ID="c11d_music_engine_v5"; ENGINE_VERSION="5.0"; SR=22050; CH=2
def load(p):
    with open(p,"r",encoding="utf-8") as f: return json.load(f)
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True)
def shab(x): return hashlib.sha256(x).hexdigest()
def shaf(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""): h.update(b)
    return h.hexdigest()
def rnd(s): s=(s*1664525+1013904223)&0xffffffff; return s,s/4294967296.0
def hz(m): return 440.0*2.0**((m-69)/12.0)
def sq(ph,d=.5): return 1.0 if (ph%1.0)<d else -1.0
def tri(ph): x=ph%1.0; return 4.0*abs(x-.5)-1.0
def render(req,spec,profile,out):
    if spec.get("engine_id")!=ENGINE_ID or str(spec.get("engine_version"))!=ENGINE_VERSION: raise ValueError("D3.1 engine identity mismatch")
    if profile.get("style_profile_id","challenge_8bit_v1")!="challenge_8bit_v1": raise ValueError("D3.2 targets challenge_8bit_v1 only")
    seed=int(req["music_seed"])&0xffffffff; dur=float(req["duration_seconds"]); bpm=float(req["tempo_bpm"]); var=int(req.get("variation_index",0))
    n=int(round(dur*SR)); beat=60.0/bpm; half=beat/2.0; state=(seed^(var*0x9e3779b9))&0xffffffff
    motif=[72,75,79,75,70,74,77,74]; chords=[(48,52,55),(50,53,57),(43,47,50),(45,48,52)]
    state,v1=rnd(state); shift=int(v1*3)-1; state,v2=rnd(state); duty=.38+.18*v2; state,v3=rnd(state); mix=.75+.25*v3
    buf=bytearray(n*4); peak=0.0; ss=0.0; maxpcm=0
    for i in range(n):
        t=i/SR; bi=int(t/beat); hi=int(t/half); bar=bi//4; chord=chords[bar%4]
        note=motif[(hi+var)%8]+shift; lf=hz(note)
        # six layers: timbre, harmony, rhythm, motif, texture, spatial_treatment
        timbre=.075*sq(t*lf,duty)+.025*tri(t*lf*.5)
        harmony=sum(.018*tri(t*hz(x)) for x in chord)*(0.9+0.1*math.sin(2*math.pi*t/(beat*4)))
        rhythm=0.0; p=t%beat
        if p<.055: rhythm+=.11*math.exp(-48*p)*math.sin(2*math.pi*(105-55*p/.055)*p)
        if bi%2==1 and p<.07: state,r1=rnd(state); state,r2=rnd(state); rhythm+=.055*((r1*2-1)-.35*(r2*2-1))*math.exp(-42*p)
        if hi%2==1 and (t%half)<.025: rhythm+=.025*math.sin(2*math.pi*1900*t)*math.exp(-120*((t%half)/half))
        motif_layer=.045*sq(t*lf*(1+.003*var),duty)*(1.0 if hi%4==0 else .72)
        bass=.050*tri(t*hz(chord[hi%3]-12)); arp=.018*sq(t*hz(chord[(hi+bar)%3]+12)); texture=mix*(bass+arp)
        mono=.82*(timbre+harmony+rhythm+motif_layer+texture)
        pan=.18*math.sin(2*math.pi*(t/max(dur,.001))+.31*var); L=max(-.92,min(.92,mono*(1-pan))); R=max(-.92,min(.92,mono*(1+pan)))
        peak=max(peak,abs(L),abs(R)); ss+=L*L+R*R; li=int(L*32767); ri=int(R*32767); maxpcm=max(maxpcm,abs(li),abs(ri)); buf[i*4:i*4+4]=struct.pack("<hh",li,ri)
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(out),"wb") as w: w.setnchannels(CH); w.setsampwidth(2); w.setframerate(SR); w.writeframes(buf)
    reqhash=shab(canon({"engine":spec,"profile":profile,"request":req}).encode())
    return {"engine_id":ENGINE_ID,"engine_version":ENGINE_VERSION,"style_profile_id":profile.get("style_profile_id","challenge_8bit_v1"),"style_profile_version":str(profile.get("style_profile_version","1.0")),"music_seed":seed,"tempo_bpm":bpm,"duration_seconds":dur,"variation_index":var,"sample_rate":SR,"channels":CH,"frame_count":n,"parameter_hash":reqhash,"output_hash":shaf(out),"peak_linear":peak,"rms_linear":math.sqrt(ss/max(1,n*CH)),"max_abs_pcm":maxpcm}
def main():
    a=argparse.ArgumentParser(); a.add_argument("--engine",required=True); a.add_argument("--profile",required=True); a.add_argument("--output",required=True); a.add_argument("--seed",type=int,required=True); a.add_argument("--tempo",type=float,default=104); a.add_argument("--duration",type=float,default=4); a.add_argument("--variation",type=int,default=0); x=a.parse_args()
    spec=load(x.engine); profile=load(x.profile); req={"music_seed":x.seed,"style_profile_id":profile.get("style_profile_id","challenge_8bit_v1"),"style_profile_version":str(profile.get("style_profile_version","1.0")),"tempo_bpm":x.tempo,"duration_seconds":x.duration,"variation_index":x.variation}
    print(json.dumps(render(req,spec,profile,x.output),sort_keys=True))
if __name__=="__main__": main()