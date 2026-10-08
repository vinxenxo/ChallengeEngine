# Test Fixtures

Fixtures are test inputs, not generated output. They are part of the regression surface and must be removed only through an explicit compatibility decision.

- `c7/challenges/` — C7 audio corpus consumed by active C7 regression tests.
- `c7_a2_mixed/` — explicit mixed-audio fixtures for C7-A2 policy tests.
- `C7_VIDEO_ONLY_CHALLENGE_001.json` — C7 video-only fixture produced by the dedicated QA helper when needed.
- `seeds/stress_v1.json` — deterministic seed corpus used by the C11 stress and video-matrix gates.

## Current D7/D8 state

C11-C 2.19.12 is frozen. C11-D D7 is PASS/CLOSED and FROZEN; D8.0 is the next phase. The active C11-D baseline is `ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip` (SHA-256 `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`).

## Directory contents

### Subdirectories
- `c7/`
- `c7_a2_mixed/`
- `seeds/`

### Representative files
- `C7_AUDIO_CHALLENGE_002.json`
- `C7_VIDEO_ONLY_CHALLENGE_001.json`
