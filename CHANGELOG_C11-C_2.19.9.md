# C11-C 2.19 — Consolidated Changelog

## Status

**2.19.9 REPAIR CANDIDATE CONSOLIDATED — NOT FROZEN.**

Individual 2.19.x patches are historical evidence. The active 2.19 branch is represented by the consolidated tooling/review surface plus the workstation source tree into which this candidate is applied.

## Consolidated lineage

- **2.19.0** — restored the proven temporary-AVI review capture route.
- **2.19.1** — corrected canonical social-hook lookup to `profiles/presentation/c11c_visual_hooks.json`.
- **2.19.2** — aligned Art Direction hygiene and Visual Drill capture contracts; the historical 2.19.2 freeze receipt is no longer authoritative for final freeze because later workstation acceptance exposed tooling inconsistencies.
- **2.19.3** — consolidated C11-A.1 isolation, Visual Drill duration, longform contract-test and QA-mode acceptance repairs.
- **2.19.4** — introduced/validated real per-worker review isolation: each concurrent worker operates from its own temporary Godot project root and private `.godot`/`override.cfg` state; no global mutex and no serialization fallback.
- **2.19.5–2.19.7** — repair/consolidation lineage for the Suite, review orchestration, launcher surfaces and acceptance preparation.
- **2.19.8** — consolidated the active 2.19 documentation, Suite launchers, canonical 52-video review and launcher audit.
- **2.19.9** — fixes the remaining Visual Drill envelope-root regression and adds an explicit focused contract test.

## 2.19.9 fixes

1. `C11CVisualDrillReviewEnvelopeGenerator.gd` now preserves absolute Windows/OS paths and only calls `ProjectSettings.globalize_path()` for project-relative roots.
2. The same generator now uses `17.0s` for non-Tracking Drill gameplay and `21.0s` for Tracking, matching the established review contract.
3. A new `C11CVisualDrillReviewEnvelopePathContractTest.gd` is registered in `tests/run_all.py` and surfaced by the Suite self-test.
4. The canonical Suite launcher surface remains `c11c-suite`; `c11c-studio` remains retired and untouched.
5. The real `Workers=7` Art Direction model is retained: private temporary Godot project roots per worker, concurrent capture, no global mutex, no one-at-a-time fallback.

## Explicit non-goals

No changes to C11-B simulation truth, RNG ownership/algorithm/streams, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio ownership/contracts, C9 semantics or logical 540x960 social geometry.
