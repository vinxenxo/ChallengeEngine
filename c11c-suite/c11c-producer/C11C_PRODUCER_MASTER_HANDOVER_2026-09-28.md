# C11-C Producer 0.9.7 — Master Handover — 2026-09-28

**Current authority:** C11-C 2.19.6 FINAL REPAIR CANDIDATE — NOT FROZEN.

Producer implementation remains **0.9.7**. The active Suite and launcher surface is `c11c-suite/`; `c11c-studio/` is retired and must not be modified or used.

## Active ownership

- Producer GUI/schema/launchers: `c11c-suite/c11c-producer/`.
- Art Direction batch: `tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1`.
- Worker isolation: `tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1`.
- Movie capture: `tools/prototypes/c11c_common/C11CMovieCapture.ps1`.
- Acceptance: `FULL_ACCEPTANCE_C11C_2.19.6.ps1`.
- Freeze seal: `tools/c11freeze/finalize_c11c_2_19_6_freeze.ps1`.

## 2.19.6 worker repair

Each worker gets a real temporary Godot project root. Source `.godot` is excluded, then the worker runs one headless editor bootstrap and requires `.godot/global_script_class_cache.cfg` containing `PresentationProfile`. This fixes the fresh-worker parse failure without sharing generated state. Captures then run concurrently across the 7 workers.

No global mutex and no one-at-a-time fallback is permitted.

## Boundaries

Do not reopen C11-B simulation truth/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry.

## Runtime status

2.19.6 remains unfrozen until Windows/Godot focused worker proof, full 7-worker Art Direction, logical/retro/physical acceptance and the formal freeze seal all pass.
