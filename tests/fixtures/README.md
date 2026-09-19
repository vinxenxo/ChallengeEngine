# Test Fixtures

Fixtures are test inputs, not generated output. They are part of the regression surface and must be removed only through an explicit compatibility decision.

- `c7/challenges/` — C7 audio corpus consumed by active C7 regression tests.
- `c7_a2_mixed/` — explicit mixed-audio fixtures for C7-A2 policy tests.
- `C7_VIDEO_ONLY_CHALLENGE_001.json` — C7 video-only fixture produced by the dedicated QA helper when needed.
- `seeds/stress_v1.json` — deterministic seed corpus used by the C11 stress and video-matrix gates.
