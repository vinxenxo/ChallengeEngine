# AGENTS.md — ChallengeEngineV01_STATELESS

## Current authority

**C11-C 2.19.6 is the active consolidated FINAL REPAIR CANDIDATE. It is NOT FROZEN.**

The former 2.19.2 freeze claim is historical and invalidated for final-freeze purposes. The 2.19.3-v2 global mutex experiment is rejected and must never be revived.

Read first, in this order:

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `C11C_2.19.6_CONTEXT_INDEX.md`
4. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.6_CONSOLIDATED.md`
5. `docs/master-prompts/START_PROMPT_C11C_2.19.6_CONSOLIDATED.md`
6. `docs/current/c11c/C11-C_2.19.6_CONSOLIDATED_STATE.md`
7. `docs/current/c11c/C11-C_2.19.6_ACCEPTANCE_GATE.md`
8. `docs/current/c11c/C11-C_2.19.6_REPAIR_MANIFEST.json`
9. `docs/current/c11c/C11-C_2.19.6_DOCUMENTATION_INDEX.md`
10. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
11. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
12. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`

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
- Single Drill = temporary AVI → video-only MP4 → deterministic family music → final delivery.
- Canonical hooks = `profiles/presentation/c11c_visual_hooks.json`.

## Parallel Art Direction worker contract — 2.19.6

`run_c11c_art_direction_batch_v4.ps1 -Workers 7` must execute genuine concurrent Movie Maker captures. Each worker receives its own temporary Godot project root. The source `.godot` directory is intentionally excluded; immediately after copy, each worker performs one headless Godot editor bootstrap:

```text
godot.exe --headless --editor --path <worker> --audio-driver Dummy --quit
```

The bootstrap must produce `<worker>/.godot/global_script_class_cache.cfg` and contain `PresentationProfile`. This initialization is sequential only while preparing the pool. Once all worker roots are ready, Movie Maker captures remain concurrent.

There is no global mutex and no one-at-a-time fallback. Runtime evidence must show `MAX_OBSERVED_CONCURRENCY > 1`.

`c11c-studio/` is retired and must not be modified or used. All active Suite code and launcher surfaces live under `c11c-suite/`.

## Test discipline

Every new `*Test.gd` must be registered in `tests/run_all.py`. Every new QA/operational function must have a corresponding direct console route and relevant Suite/GUI route. Focused validation comes before full acceptance.

Canonical candidate gate:

```powershell
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```

Do not declare a new freeze until the complete workstation gate and the C11-C-specific freeze seal are green.

## D status

D is blocked until C11-C 2.19.6 (or a later consolidated C11-C candidate) is formally accepted and frozen.
