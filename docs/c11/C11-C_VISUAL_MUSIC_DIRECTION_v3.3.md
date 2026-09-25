# C11-C Visual Music Direction v3.3

## Objective
Replace the barely audible single ambient bed with deterministic, family-paired harmonic pads that remain coherent on mobile speakers and complement the visual grammar without reading gameplay events.

## Harmonic language
Use the A-minor pentatonic bank:
`110.0, 130.81, 146.83, 164.81, 196.0, 220.0, 261.63, 293.66, 329.63 Hz`.

## Envelope
Visual Loops use soft per-chord attack/release shaping inside the loop-safe phrase. Visual Drills use a global ADSR pad envelope with long attack and release and a stable sustain stage. No hard note-on/note-off edges are allowed.

## Modulation
Use deterministic low-frequency value noise. Visual Loops use cyclic noise nodes so the phrase begins and ends in the same modulation domain. Stereo motion is slow and bounded to ±0.16.

## Mobile presence
Peak ceiling: `0.36`. Target RMS: `0.085–0.16`. Harmonics deliberately emphasize low/mid content that survives small speakers. Low-pass filtering remains active and no kick/snare layer is used.

## Visual pairing
| Visual identity | Music profile | Character |
|---|---|---|
| Tracking ↔ Invisible Forces | `FLOWING_VECTOR` | airy / directional / weightless |
| Saccade ↔ Geometric Waves | `CIRCUIT_PULSE` | precise / ballistic / crystalline |
| Pursuit ↔ Fractal Bloom / Living Particles | `ORGANIC_BLOOM` | organic / expanding / luminous |
| Peripheral Scan ↔ Sacred Symmetry | `ORBITAL_RITUAL` | celestial / ritual / suspended |
| Kaleidoscope historical route | `PRISMATIC_MEMORY` | prismatic / reflective |

## Semantic inputs
For Visual Loops, music uses `seed + visual grammar`. For Visual Drills, music uses `seed + family`; the social/header hook is editorial copy only and does not drive audio. These are presentation/editorial inputs only.

Forbidden: `winning_frame`, `close_calls`, answer sheets, per-frame gameplay state and event timestamps.

## Delivery
The existing launcher-facing `C11CSafeAmbient.py` remains the compatibility entry point. It now delegates to the family-aware generator revision `3.3.0` and does not represent one global waveform shared by all families.

## Ownership
C7 audio ownership and contracts remain unchanged. C11-C only prepares presentation/delivery audio assets.


## Seeded tonal variation
The seed may select a whole-pad pitch scale between 0.80× and 1.20×. This transposes the complete consonant stack together, preserving its harmonic intervals. It is a presentation/audio parameter only and never consumes gameplay positions, events or frames.
