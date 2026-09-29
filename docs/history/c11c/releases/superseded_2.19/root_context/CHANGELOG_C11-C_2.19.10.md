# C11-C 2.19.10 — Consolidated repair candidate

## Fixed

- `C11CVisualDrillReviewEnvelopePathContractTest.gd`: `_ready()` -> `_initialize()` for correct `SceneTree --script` lifecycle.
- `c11c-suite/self_test.py`: regression guard prevents the test from returning to `_ready()`.
- Canonical `c11c-suite` launchers refreshed, including direct `run_suite.bat`.
- Acceptance references moved to `FULL_ACCEPTANCE_C11C_2.19.10.ps1`.
- 2.19 documentation and continuity prompts consolidated around the 2.19.10 candidate.

## Preserved

- Real 7-worker Art Direction capture with private worker project roots.
- No global mutex.
- No one-at-a-time fallback.
- `c11c-studio` untouched and non-operational.
- C11-B/C7/C9 frozen boundaries untouched.
