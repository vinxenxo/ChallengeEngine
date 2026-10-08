# Tools Map

## Freeze and certification

`tools/c11freeze/` contains the canonical checkpoint/release gates: core suite, C11 suite, retrocompatibility, seed stress, physical export and video matrix.

## QA helpers

- `tools/qa/c7/` — C7-specific fixtures and policies.
- `tools/qa/c10/` — C10 physical export smoke.
- `tools/qa/c11/` — C11 qualification, framing and visibility utilities.

## Maintenance

`tools/maintenance/` contains routine repository maintenance. `tools/maintenance/legacy/` contains one-off historical scripts and is not part of the normal execution path.

New production or QA automation should have one canonical location and one documented artifact output root.

## Current D7/D8 state

C11-C 2.19.12 is frozen. C11-D D7 is PASS/CLOSED and FROZEN; D8.0 is the next phase. The active C11-D baseline is `ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip` (SHA-256 `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`).

## Directory contents

### Subdirectories
- `c11c_hotfix/`
- `c11d/`
- `c11freeze/`
- `maintenance/`
- `prototypes/`
- `qa/`

### Representative files
- None; this directory currently serves as a container for subdirectories.
