import math, struct, sys, wave

def main(path: str) -> None:
    sr = 44100; duration = 10.0; frames = int(sr * duration)
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 314159
    seed_phase = 2.0 * math.pi * ((seed & 0xFFFFFFFF) / 0xFFFFFFFF)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        buf = bytearray()
        for n in range(frames):
            t = n / sr
            drift = 0.25 * math.sin(2*math.pi*t/7.5 + seed_phase)
            bass = 0.095 * math.sin(2*math.pi*(73.4 + 2.0*drift)*t)
            mid = 0.055 * math.sin(2*math.pi*(146.8 + 5.0*math.sin(t + 0.17*seed_phase))*t + 0.5*math.sin(2*math.pi*t/5.0))
            shimmer = 0.020 * math.sin(2*math.pi*587.33*t) * (0.5+0.5*math.sin(2*math.pi*t/2.5))
            s = max(-0.92, min(0.92, bass+mid+shimmer))
            v = int(s*32767)
            buf.extend(struct.pack('<hh', v, v))
        w.writeframes(buf)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('missing OUTPUT.wav')
    main(sys.argv[1])
