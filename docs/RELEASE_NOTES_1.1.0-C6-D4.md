# RELEASE_NOTES_1.1.0-C6-D4.md

## Feature
Declarative phase-duration control for generated videos.

### Contract
- `0 s` => phase omitted.
- `>0 s` => phase active.
- `GAME > 0` is mandatory.
- Effective order remains `HOOK -> GAME -> REVEAL -> CTA`.

### Included fixture changes
- `CHALLENGE_001`: GAME -> CTA.
- `CHALLENGE_002`: HOOK -> GAME.
- `CHALLENGE_005`: GAME only.
- `CHALLENGE_006`: GAME -> CTA.
- `CHALLENGE_007`: HOOK -> GAME.

### Architecture
No simulation, RNG, winning-frame mathematics, or validation logic has been redesigned for this feature. `VideoTimeline` is the temporal source of truth.

### Verification
A standalone Python contract audit is included at `tests/phase_duration_contract_test.py`. Full Godot E2E rendering must be executed in a Godot-equipped environment before final production certification.
