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
