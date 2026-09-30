# C11-C Suite 0.1.1 — Architecture and Project Knowledge Map

## Authority order

1. Frozen engine/runtime and declared contracts.
2. Current repository code and current `docs/current/`.
3. Freeze/checkpoint evidence under `docs/checkpoints/` and `artifacts/`.
4. Historical material under `docs/history/` is evidence and continuity, not a current override.
5. Conversation handovers are continuity aids, never code authority.

## Scope of this suite phase

The C11-C audiovisual manufacturing backend remains untouched. This phase adds operational interfaces around it. The suite is allowed to inspect files, invoke existing commands, package the repository, and edit declared configuration files only when the operator explicitly asks it to.

The suite MUST NOT implement:

- Challenge mechanics.
- Structural or gameplay RNG.
- `SimulationResult` semantics.
- `WinningFrameDetector` or `winning_frame` calculation.
- `RenderedFrameStream` truth.
- Runtime coordinate calculations.
- Visual renderer mathematics.
- Audio ownership/contracts.
- Replacement production pipelines that bypass the canonical launchers.

## Project layers

```text
Definitions / authoring
        ↓
Deterministic runtime / mechanics
        ↓
Passive presentation
        ↓
Production orchestration
        ↓
C11-C SUITE (operator interfaces)
  ├── TEST
  ├── CATALOG
  ├── MAINTENANCE
  ├── CONFIG
  └── PRODUCER
```

The Suite is an operator layer above production orchestration, not a new engine layer.

## Historical-to-current continuity

### C6 / C6-F foundations
The project established deterministic content boundaries, temporal abstractions and the `ContentRuntimeRegistry` / `RenderedFrameStream` path. Historical docs remain under `docs/history/c6/`.

### C7
Audiovisual/audio contracts and deterministic audio generators belong to the existing audiovisual layer. The suite can inspect and invoke them but does not own their semantics.

### C9
Challenge authoring became declarative and reproducible. The suite exposes the JSON definitions and profiles without replacing authoring adapters or runtime logic.

### C10
Authoring → runtime → export became a production path. Physical Movie Maker validation remains external to logical suite execution.

### C11 Freeze
C11 froze simulation/RNG/runtime truth and established the repository/test/artifact governance. The 54-run challenge qualification, deterministic stress policy and physical gates are preserved.

### C11-C / 2.16.9+
C11-C introduced the current Visual Loop / Visual Drill / Longform manufacturing layer, delivery profiles, review batches and the Producer GUI. 2.17.x added historical Challenge production; 2.18.x stabilized Producer operations.

## Current audiovisual corpus

Visual Loops: 5 technical families / 27 grammars.

| Technical | Artistic | Production ID | Grammars |
|---|---|---|---:|
| `geometric` | Geometric Waves | `c11c_geometric_waves_v1` | 5 |
| `fractal` | Fractal Bloom | `c11c_fractal_bloom_v1` | 5 |
| `kaleidoscope` | Sacred Symmetry | `c11c_sacred_symmetry_v1` | 5 |
| `particle_flow` | Living Particles | `c11c_living_particles_v1` | 5 |
| `vector_field` | Invisible Forces | `c11c_invisible_forces_v1` | 7 |

Visual Drills: Tracking, Saccade, Pursuit, Peripheral Scan.

Tracking = 3s PRE_ROLL + 21s GAME + 3s END_CTA = 27s / 810 frames.

Saccade/Pursuit/Peripheral Scan = 3s + 17s + 3s = 23s / 690 frames.

Longforms = 180s, composed from canonical loop segments with dissolve continuity and only a final fade to black.

## Challenge corpus

Canonical Challenge definitions are `CHALLENGE_001` … `CHALLENGE_009`. Native video FPS/timing are authoritative; the GUI never normalizes them to the C11-C visual timings.

## Delivery profiles

The central delivery catalogue is `profiles/delivery/c11c_video_delivery_profiles.json`. Current profiles are `MASTER_1080`, `REVIEW_720`, `MIN_540`, `META_REELS_FINAL_V1` and `LONGFORM_1080`. `META_REELS_FINAL_V1` is an alias to `MASTER_1080`.

## Tests

`tests/run_all.py` is the explicit logical registry. The current baseline contains 134 registered suites, including the focused Producer REVIEW_720 copy-safety regression; the Suite must read the registry rather than duplicate its list. The freeze gate additionally composes core, C11, logical, retrocompatibility, physical export and deterministic stress.

Historical C11-A.1 qualification is 9 Challenges × 6 seed cases = 54 executions.

## Artifacts

`artifacts/` is the evidence/product surface. The Catalog reads it recursively. Maintenance treats only explicitly designated transient roots as safe automatic cleanup targets.

## Producer relocation

The live Producer is `c11c-suite/c11c-producer/`. Older root-level Producer material is historical only and is not part of the live source path. This is a filesystem/tooling relocation, not a backend relocation.

## Addendum 0.1.2 — test surface parity

The Suite treats `tests/run_all.py` + `KNOWN_SUITES` as the canonical logical test registry. `c11c-test` reads that registry instead of maintaining a duplicated individual-suite list. Console launchers are provided alongside the GUI so the same test corpus remains operable without PySide6.

`tests/run_all.py` + `KNOWN_SUITES` constituyen el registro canónico de suites lógicas. `c11c-test` lo consulta dinámicamente. Los lanzadores `run_all.bat` y `run_suite.bat` proporcionan la misma superficie básica sin depender del GUI.
