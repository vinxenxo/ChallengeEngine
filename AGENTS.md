# AGENTS.md — ChallengeEngineV01_STATELESS

## Authority / current state

**C11-C 2.19.5 is the active consolidated REPAIR CANDIDATE. It is NOT FROZEN yet.** The old 2.19.2 freeze is invalidated for final-freeze purposes because workstation acceptance later exposed test/capture/tooling inconsistencies. Do not use 2.19.2 as the current acceptance authority.

Read first, in this order:

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.5_CONSOLIDATED.md`
4. `docs/master-prompts/START_PROMPT_C11C_2.19.5_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`
7. `docs/current/c11c/C11-C_2.19.5_REPAIR_MANIFEST.json`
8. `docs/current/c11c/README.md`
9. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
10. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
11. `docs/current/c11c/C11-C_2.19.5_DOCUMENTATION_INDEX.md`
12. `docs/current/d/README.md` only after C11-C receives a final freeze

## Architecture invariant

```text
Definitions
    ↓
deterministic simulation
    ↓
SimulationResult / FrameSnapshot
    ↓
passive presentation
    ↓
RenderedFrameStream
    ↓
production/export orchestration
```

Presentation cannot calculate gameplay truth. Producer cannot become a second runtime. Structural RNG cannot be consumed by cosmetic rendering.

## Frozen C boundary

Do not modify without an explicit checkpoint:

- simulation mathematics and mechanic semantics;
- RNG algorithm, streams and ownership;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 semantics;
- logical 540×960 C11-B/C social geometry.

A checkpoint must state contract, reason, alternatives rejected, affected tests, migration risk and rollback path.

## C11-C manufacturing contracts

- 27 Visual Loop grammars / 5 families.
- `geometric` → Geometric Waves; `fractal` → Fractal Bloom; `kaleidoscope` → Sacred Symmetry; `particle_flow` → Living Particles; `vector_field` → Invisible Forces.
- 4 Visual Drill families.
- Tracking = 27 s / 810 frames at 30 FPS.
- Saccade, Pursuit and Peripheral Scan = 23 s / 690 frames.
- 5 Longforms = 180 s each.
- Review capture = 720×1280 @ 30 FPS.
- Default master = `MASTER_1080` / 1080×1920.
- Producer = `c11c-suite/c11c-producer/`, version 0.9.7.
- Single Drill = temporary AVI → video-only MP4 → separate deterministic family music → final delivery.
- Canonical hooks = `profiles/presentation/c11c_visual_hooks.json`.

## Review concurrency contract — 2.19.5

`run_c11c_art_direction_batch_v4.ps1 -Workers 7` must execute genuinely concurrently. It uses one temporary Godot project root per worker. Each worker owns its own `override.cfg` and `.godot` state. There is no project-global mutex and no global serialization workaround.

The retired `the retired legacy operator surface/` tree is not an operational surface and must not be updated. Active suite code/launchers live under `c11c-suite/`; operational suite launcher sources must not reference `the retired legacy operator surface`.

## Test discipline

Every new `*Test.gd` must be registered in `tests/run_all.py`. Every new QA/operational function must have a corresponding Suite/GUI surface and direct console route. Focused validation comes before full acceptance.

Canonical candidate gate:

```powershell
.\FULL_ACCEPTANCE_C11C_2.19.5.ps1
```

Do not declare a new freeze until the candidate gate is green on the workstation and its evidence is recorded.

## D status

D is blocked until C11-C 2.19.5 (or a later consolidated C11-C candidate) is formally accepted and frozen. The existing C11-D prompts are retained as historical planning material, not current authority.
