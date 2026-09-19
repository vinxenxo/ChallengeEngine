# MASTER HANDOVER — ChallengeEngineV01_STATELESS
## CHECKPOINT: C6-F0.8-F2/F3 — FROZEN / CLOSED / CERTIFIED

**Purpose:** This document is the authoritative continuity contract for the next context window.

---

## 0. NON-NEGOTIABLE CONTINUITY RULE

The attached ZIP is the **official baseline** for continuation.

The baseline is defined by the **last stable, tested and explicitly frozen project state**, not by the highest or lowest numeric version label found in filenames, documentation or branches.

During development, revision/version labels may legitimately move forward or backward when branches are consolidated, families are added, patches are rebased, or a cleaner tested state is restored. This is **not evidence of regression** by itself.

Therefore:

> **Do not infer project chronology from version numbers alone.**
>
> The authoritative state is the ZIP + this Master Handover + the certified test evidence.

The ZIP supplied with this handover has been prepared specifically as the continuation baseline and must be treated as the source of truth unless direct inspection proves an integrity problem.

---

# 1. CURRENT CHECKPOINT

## C6-F0.8-F2/F3

Status:

**FROZEN / CLOSED / CERTIFIED**

This checkpoint closes the current Visual Content chapter after:

- Visual Loop families
- Visual Drill families
- cosmetic deterministic variation
- runtime integration
- passive shader renderers
- presentation binding
- E2E envelope auditing
- physical Movie Maker export
- physical determinism verification

No new implementation is authorised until the continuation audit has accepted the attached baseline.

---

# 2. CERTIFICATION EVIDENCE

## Global test corpus

**82/82 PASS**

This is the final certified global test state at freeze.

## Canonical content

Exactly nine canonical content definitions are part of the certified Visual Content corpus:

### Visual Loops

1. `visual_loop_fractal_canonical.json`
2. `visual_loop_vector_field_canonical.json`
3. `visual_loop_particle_flow_canonical.json`
4. `visual_loop_kaleidoscope_canonical.json`
5. `visual_loop_geometric_canonical.json`

### Visual Drills

6. `visual_drill_tracking_canonical.json`
7. `visual_drill_pursuit_canonical.json`
8. `visual_drill_saccade_canonical.json`
9. `visual_drill_peripheral_scan_canonical.json`

---

# 3. VISUAL LOOP CONTRACT

Certified loop families:

- `fractal` → RNG stream `2001` → `FractalGenerator`
- `vector_field` → RNG stream `2002` → `VectorFieldGenerator`
- `particle_flow` → RNG stream `2003` → `ParticleFlowGenerator`
- `kaleidoscope` → RNG stream `2004` → `KaleidoscopeGenerator`
- `geometric` → RNG stream `2005` → `GeometricGenerator`

All use the deterministic variation injection path through `generate_with_variation()`.

The generators do not own RNG state.

The renderer does not generate procedural state.

The binder does not own RNG state.

The runtime owns the presentation RNG context and supplies variation values to the generator.

---

# 4. VISUAL DRILL CONTRACT

Certified drill families:

- `tracking` → RNG stream `2011` → `TrackingGenerator`
- `pursuit` → RNG stream `2012` → `PursuitGenerator`
- `saccade` → RNG stream `2013` → `SaccadeGenerator`
- `peripheral_scan` → RNG stream `2014` → `PeripheralScanGenerator`

All use deterministic variation injection through `generate_with_variation()`.

---

# 5. RNG STREAM CONTRACT

Frozen streams:

### Visual Loops

- `2001`: `0=palette_variant, 1=complexity_variant, 2=phase_offset, 3=rotation_offset`
- `2002`: `0=palette_variant, 1=turbulence_variant`
- `2003`: `0=palette_variant, 1=emission_variant`
- `2004`: `0=palette_variant, 1=symmetry_variant`
- `2005`: `0=palette_variant, 1=shape_variant`

### Visual Drills

- `2011`: `0=tracking_variant`
- `2012`: `0=pursuit_variant`
- `2013`: `0=saccade_variant`
- `2014`: `0=pattern_variant, 1=amplitude_variant`

Each stream has an authorised consumer. Do not repurpose or silently reassign a stream.

---

# 6. RUNTIME ARCHITECTURE — FROZEN

`ContentRuntimeRegistry.create_default()` is the production registry construction path.

`resolve(definition)` returns a dictionary containing:

- `success`
- `error_code`
- `runtime`
- `route`

The executable runtime is `resolution["runtime"]`.

## VisualLoopRuntime

The Visual Loop payload is layer-centric.

The runtime accepts the definition content through the existing envelope bridge and must **not** be modified to falsely promote layer fields to root-level fields just to satisfy a test assumption.

The certified frame model uses:

- frame index
- loop frame
- loop iteration
- generator type
- layer states
- loop metadata

## Visual Drill Runtime

Visual Drill uses its own established payload structure and parameter contract.

Do not homogenise the two domains merely for aesthetic symmetry.

---

# 7. PRESENTATION ARCHITECTURE — FROZEN

The following principles are mandatory:

- Challenge is sovereign.
- Simulation/RNG remain isolated from presentation.
- `ContentRendererHost` is passive.
- `PresentationUI` is not a router.
- No universal `RenderModel` superclass is to be introduced without an explicit architectural decision.
- `RenderedFrameStream` is authoritative for routing using `(kind, subtype)`.
- Routing must not be inferred from `payload.domain`.
- Renderers are representational only.
- Renderers do not recalculate mechanics.
- Renderers do not advance simulation time.
- Renderers do not call generators.
- Renderers do not depend on Challenge runtime internals.

---

# 8. VISUAL CONTENT PLAYER

`VisualContentPlayer.gd` is the established playback host for physical visual export.

It:

1. loads a definition;
2. resolves the production runtime registry;
3. obtains the rendered frame stream;
4. resolves the binder;
5. mounts the correct passive renderer;
6. advances playback;
7. forwards bound domain state into the renderer host.

The physical Movie Maker path was validated through a dedicated scene rather than through the default project scene.

---

# 9. PHYSICAL MOVIE EXPORT

## Certified pilot

The isolated Movie Maker scene was:

`tests/F0_8MovieMakerPilot.tscn`

The successful physical pilot recorded:

- 60 frames
- 30 FPS
- 540×960
- non-headless real GPU rendering
- non-zero AVI output
- successful completion

Observed pilot artifact:

`pilot.avi`

Size observed during certification:

**1,532,740 bytes**

---

# 10. HEADLESS EXPORT FAILURE — HISTORICAL / DO NOT REOPEN BLINDLY

An earlier attempt used:

`godot --headless --write-movie ...`

This caused:

- Dummy renderer initialisation
- default `GeneradorMaestro` startup
- missing CLI challenge configuration
- texture access failure
- Windows access violation `0xC0000005` / `3221225477`

This was isolated as an invocation/environment problem, not as evidence that the Visual Content runtime, generators or shaders were mathematically broken.

The successful method is the one frozen by the pilot:

- explicit visual pilot scene
- normal graphical renderer
- Movie Maker
- fixed FPS
- controlled frame count

Do not reintroduce `--headless` into physical visual export unless a new architectural need is explicitly established and independently tested.

---

# 11. PHYSICAL DETERMINISM CERTIFICATION

The final batch matrix contained:

**9 content types × 3 runs = 27 physical exports**

For each content:

- A = seed `12345`
- B = seed `12345`
- C = seed `54321`

Required invariants:

`A == B`

and

`A != C`

## Final certified result

**27/27 physical runs PASS**

All 27 executions returned exit code `0`.

All 27 artifacts were non-zero.

All 9 content types satisfied:

- same-seed export hash equality
- different-seed export hash inequality

Therefore physical deterministic variation is certified across all 9 canonical visual content families.

---

# 12. IMPORTANT BASELINE INTERPRETATION

The next context must understand the distinction between:

### Certified checkpoint

The functional state that was explicitly tested and closed.

### Baseline archive

The ZIP provided with this handover. This is the exact project state to continue from.

### Working-tree history

Previous experiments, branches, patches, or temporary version labels do not override the baseline merely because their filenames contain a higher or lower version number.

A higher numbered historical branch does not automatically supersede the frozen baseline.

A lower numbered branch does not automatically mean the project regressed.

**Tests + explicit freeze decision + attached ZIP define truth.**

---

# 13. WHAT MUST NOT BE REOPENED

Unless a continuity audit proves an actual defect, do not reopen:

- the Visual Loop generator mathematics;
- the Visual Drill generator mathematics;
- RNG stream allocation;
- `VisualLoopRuntime` payload structure;
- `VisualDrillRuntime` payload structure;
- passive renderer architecture;
- binder architecture;
- `RenderedFrameStream` routing;
- deterministic variation semantics;
- Movie Maker invocation model;
- the 82/82 certified corpus;
- the 27-run physical determinism proof.

Do not refactor certified code merely to make it aesthetically cleaner.

---

# 14. FIRST TASK IN THE NEW CONTEXT

The first task is **continuity audit only**.

Do not implement anything immediately.

The new context must:

1. inspect the supplied ZIP;
2. verify that `project.godot` and the expected project structure exist;
3. identify the actual baseline state from files and tests, not version numbers;
4. verify the nine canonical definitions;
5. verify the Visual Loop and Visual Drill runtime paths;
6. verify RNG stream registration and authorised consumers;
7. verify the frozen test corpus and physical export evidence;
8. compare the result against this handover;
9. issue a formal GO / NO-GO verdict.

Only after a clean GO may implementation continue.

---

# 15. NO SILENT RECOVERY RULE

If the new context finds discrepancies:

- do not silently patch them;
- do not assume missing files are recoverable;
- do not infer that a later version is automatically authoritative;
- do not rewrite contracts to make tests pass;
- report the discrepancy and classify it as:
  - packaging issue;
  - documentation issue;
  - test harness issue;
  - baseline integrity issue;
  - genuine architectural regression.

The assistant must make this classification explicitly.

---

# 16. DEVELOPMENT DISCIPLINE FOR NEXT PHASE

For all future changes:

- work in explicit checkpoints;
- define the contract before implementation;
- keep simulation deterministic;
- keep presentation passive;
- add tests before declaring a phase closed;
- run the full relevant suite;
- record exact evidence;
- freeze only after PASS;
- create a new handover at major boundaries.

No scope expansion by accident.

No “helpful” refactor outside the active checkpoint.

No assumption that the next domain is predetermined.

---

# 17. NEXT DOMAIN

The next strategic domain is intentionally **OPEN**.

Candidates previously discussed include:

- Audio Procedural
- Mecánicas de Interacción V2

The next context must choose based on the architecture and the current product roadmap after completing the continuity audit. It must not assume that one of those candidates was preselected merely because it appears here.

---

# 18. FINAL FREEZE STATEMENT

**C6-F0.8-F2/F3 is closed.**

The frozen Visual Content architecture and its evidence are the foundation for the next chapter.

The next context starts from the supplied ZIP, verifies it, and proceeds only from a clean baseline.

**END OF MASTER HANDOVER**
