import math, struct, sys, wave

def main(path: str) -> None:
    sr = 44100; duration = 10.0; frames = int(sr * duration)
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 314159
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        buf = bytearray()
        for n in range(frames):
            t = n / sr
            base = 110.0 + 13.0 * math.sin(2*math.pi*t/10.0 + seed*0.00001)
            a = 0.11 * math.sin(2*math.pi*base*t)
            b = 0.045 * math.sin(2*math.pi*(base*1.5)*t + 0.4*math.sin(t))
            bell = 0.025 * math.sin(2*math.pi*660.0*t) * math.exp(-0.45*(t % 2.5))
            pulse = 0.035 * math.sin(2*math.pi*2.0*t)
            s = max(-0.92, min(0.92, a+b+bell+pulse))
            v = int(s*32767)
            buf.extend(struct.pack('<hh', v, v))
        w.writeframes(buf)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('missing OUTPUT.wav')
    main(sys.argv[1])
