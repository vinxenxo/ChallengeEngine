# AGENTS.md — ChallengeEngineV01_STATELESS

## Current authority

**C11-C 2.19.12 — FINAL CONSOLIDATED ACCEPTANCE PASS achieved; freeze is the only remaining C11-C seal step.**

The current baseline for this pre-freeze hardening pass is:
`ChallengeEngineV01_STATELESS-C11-C2.19.12-V33-STABLE.zip`

After the Maintenance freeze package is sealed, that exact archive and its SHA-256 become the immutable C11-D entry baseline.

## First reads

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md`
4. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md`
5. `docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md`
6. `docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md`
7. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`
8. `docs/current/suite/C11C_SUITE_CURRENT_RULES.md`
9. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
10. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md` after C11-C freeze
11. `docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS.md` after C11-C freeze

## Frozen engine boundary

Do not modify without an explicit checkpoint, contract update, focused regression and rollback evidence:

- simulation mathematics and mechanic truth;
- RNG algorithm, streams and ownership;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 authoring semantics;
- logical 540x960 C11-B social geometry.

The final pre-freeze work is restricted to documentation, repository organization and QA/Maintenance tooling.

## C11-C manufacturing contract

- Visual Loops: 5 families / 27 grammars.
- Historical family crosswalk: `geometric`, `fractal`, `kaleidoscope`, `particle_flow`, `vector_field`.
- Editorial names: Geometric Waves, Fractal Bloom, Sacred Symmetry, Living Particles, Invisible Forces.
- Visual Drills: Tracking, Saccade, Pursuit, Peripheral Scan.
- Review corpus: 27 Loops + 20 Drills + 5 Longforms = 52 videos.
- Review delivery: 720x1280 @ 30 FPS.
- Master delivery profile: `MASTER_1080` / 1080x1920.
- Producer: 0.9.7.
- Suite application: 0.1.4; current Suite rules are maintained separately from the application version.
- Art Direction review: `Workers=7` genuine concurrency, private worker Godot roots, worker-local `.godot` and capture override state.

## Operator parity

`c11c-suite` is the canonical GUI operator shell. GUI actions delegate to the same canonical PowerShell/Python/Godot launchers used directly from the command line.

For D, GUI and CLI are intended to be used simultaneously during authoring/testing; no GUI-only backend or GUI-only state may be introduced.

## Test discipline

Focused checks come before expensive aggregate execution. Any new `*Test.gd` is registered in `tests/run_all.py`; any new QA/Maintenance operation has a direct console launcher and a Suite surface where appropriate.

## D entry

Do not begin D implementation against the unfrozen workspace. Seal C11-C first, then verify archive SHA-256 and use that exact archive as the D baseline.
