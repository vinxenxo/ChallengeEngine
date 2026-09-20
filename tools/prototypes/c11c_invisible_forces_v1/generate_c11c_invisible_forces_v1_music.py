import sys
import math, struct, sys, wave

def main(path: str) -> None:
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 314159
    seed_phase = 2.0 * math.pi * ((seed & 0xFFFFFFFF) / 0xFFFFFFFF)
    sr = 44100; duration = 10.0; frames = int(sr * duration)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        buf = bytearray()
        for n in range(frames):
            t = n / sr
            low = 0.08 * math.sin(2*math.pi*55*t + 0.3*math.sin(2*math.pi*t/5.0 + seed_phase))
            sweep = 0.045 * math.sin(2*math.pi*(160 + 25*math.sin(2*math.pi*t/10.0))*t)
            pulse_env = 0.5 + 0.5*math.sin(2*math.pi*t/2.0 + seed_phase)
            pulse = 0.038 * math.sin(2*math.pi*880*t) * pulse_env
            s = max(-0.92, min(0.92, low+sweep+pulse))
            v = int(s*32767)
            buf.extend(struct.pack('<hh', v, v))
        w.writeframes(buf)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('missing OUTPUT.wav')
    main(sys.argv[1])
