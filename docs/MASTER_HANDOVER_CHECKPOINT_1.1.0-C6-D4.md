# MASTER_HANDOVER_CHECKPOINT_1.1.0-C6-D4.md

## Status
C6-D4 implementation prepared on top of the C6-D3 baseline.

## Frozen principles
- Simulation truth remains sovereign.
- RNG streams remain untouched by presentation changes.
- `VideoTimeline` is the only source of effective video phase boundaries.
- Phase duration `0` means omission; no sentinel phase is rendered.
- `GAME` remains mandatory.
- Factory timeline and Godot timeline must agree exactly.

## Requested fixture matrix

| Challenge | Effective phases | Total @60 FPS |
|---|---|---:|
| 001 | GAME -> CTA | 540 |
| 002 | HOOK -> GAME | 600 |
| 005 | GAME | 420 |
| 006 | GAME -> CTA | 540 |
| 007 | HOOK -> GAME | 600 |

## Pending certification
The implementation has a standalone Python contract audit. The remaining certification step is the real Godot E2E render/batch in a machine with Godot 4.7.1 and FFmpeg/FFprobe available.

## Next window objective
Start from the packaged C6-D4 repository, first perform the full repository-wide audit/documentation cleanup, then establish the product-facing presentation roadmap. Do not reopen frozen deterministic simulation contracts unless a regression proves they are broken.


## Repository-wide audit — 2026-09-02

The C6-D4 package was audited after baseline extraction. The deterministic simulation contracts, RNG semantics and winning-frame mathematics were not modified.

### Verified

- `tests/phase_duration_contract_test.py`: PASS.
- Required C6-D4 fixture matrix: 001=540, 002=600, 005=420, 006=540, 007=600 frames at 60 FPS.
- Current source factory version: `0.10.0`; manifest schema remains `1.0`.
- Nine challenge definitions are present (001–009).
- `VideoTimeline.gd` remains the effective temporal source of truth.
- Generated outputs were removed from the clean package; they are not treated as live certification evidence.

### Corrected repository hygiene

- `ChooseMechanicIsolationTest.gd` was an orphaned corpus test: it now executes as a `SceneTree` suite and is registered in `tests/run_all.py` with an explicit PASS marker.
- Current README/integration/roadmap and discipline-document “live” sections were aligned to C6-D4. Historical handovers remain historical.
- Stale 0.9.0/1.0.0 statements about FIND being a draft or fixed 660-frame production timing were corrected where they were presented as current state.
- Stale generated output manifests and media are no longer presented as current batch evidence in the clean source package.

### Certification boundary

This execution environment contains FFmpeg/FFprobe but no `godot` executable. Therefore the following remain **PENDING**, not PASS:

- complete Godot 4.7.1 regression suite;
- nine-challenge batch render;
- physical FFprobe verification of regenerated artifacts;
- final release certification.

The next machine-specific gate is exactly the sequence defined in `MASTER_START_PROMPT_1.1.0-C6-D4.md`.
