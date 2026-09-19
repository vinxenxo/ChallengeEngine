# MASTER HANDOVER — ChallengeEngineV01_STATELESS
## Checkpoint: C6-F0.8-F2/F3 — FROZEN / CLOSED

**Purpose:** preserve the complete architectural state at the exact point where C6-F0.8 is closed, so a new context can continue without reopening solved decisions, silently changing contracts, or losing continuity.

---

## 0. GOVERNING DIRECTIVE

You are taking over as Principal Programmer / Systems Architect / Continuity Auditor for the real Godot project `ChallengeEngineV01_STATELESS`.

The attached ZIP is the authoritative physical baseline. Do not infer missing files from memory when the ZIP can answer the question.

Rules:
- Audit first, modify second.
- Never silently reinterpret a contract.
- Never reopen a frozen checkpoint merely because another implementation would be cleaner.
- Do not alter Challenge simulation, deterministic RNG architecture, or already-certified Visual Content contracts without explicit evidence of a contradiction.
- Do not introduce scope creep.
- When proposing a change, identify exact files, exact contract impact, and rollback boundary.
- For code changes, provide complete files, not partial snippets, unless the user explicitly asks for a patch/diff.
- Every milestone ends in explicit PASS / FAIL / NO-GO or GO.
- Never claim certification from static reasoning alone when an executable test is required.
- The user runs Godot/PowerShell on Windows; the assistant cannot execute Godot locally. Evidence supplied by the user is the execution authority.

---

# 1. FROZEN CHECKPOINT

**Checkpoint:** `C6-F0.8-F2/F3`

**Status:** `CERTIFIED / CLOSED / FROZEN`

This checkpoint covers the complete Visual Content V2 delivery through:

1. Visual Loop domain implementation and validation.
2. Visual Drill domain implementation and validation.
3. Deterministic cosmetic RNG stream integration.
4. Passive shader-based presentation.
5. End-to-end canonical payload audits.
6. Physical Movie Maker export through real GPU rendering.
7. Cross-run physical determinism verification by SHA-256.

The architecture below is frozen unless future work produces concrete evidence of a defect.

---

# 2. CERTIFIED GLOBAL RESULT

Final corpus result immediately before closure:

**`82/82 PASS`**

This includes the corrected `C6F08F1ContentEnvelopeAuditTest.gd` and the full existing suite.

The F1 audit validates the nine canonical Content Definitions end-to-end through the production `ContentRuntimeRegistry` and domain-specific frame contracts.

---

# 3. VISUAL LOOP — FROZEN CONTRACT

Five certified visual loop types:

| Type | RNG Stream | Generator |
|---|---:|---|
| `fractal` | `2001` | `FractalGenerator` |
| `vector_field` | `2002` | `VectorFieldGenerator` |
| `particle_flow` | `2003` | `ParticleFlowGenerator` |
| `kaleidoscope` | `2004` | `KaleidoscopeGenerator` |
| `geometric` | `2005` | `GeometricGenerator` |

All use `generate_with_variation()` for runtime variation injection.

The visual loop runtime is the owner of deterministic variation sampling. Generators remain unaware of RNG architecture.

### Critical payload rule

Visual Loop data is layer-centric.

The authoritative structure is:

`payload.generator` + `payload.layers[0].parameters`

Do **not** invent or require a promoted root-level `parameters` structure.

`VisualLoopRuntime.gd` accepts either `definition.payload` or `definition.content` and internally establishes its domain payload.

It validates:
- `duration`
- `fps`
- `frame_count`
- `visual_parameters`
- valid temporal values
- `frame_count == round(duration * fps)`
- known generator type
- registered and authorized RNG stream

The runtime builds `VisualFrameState` and a `RenderedFrameStream`.

---

# 4. VISUAL DRILL — FROZEN CONTRACT

Four certified visual drill types:

| Type | RNG Stream | Generator |
|---|---:|---|
| `tracking` | `2011` | `TrackingGenerator` |
| `pursuit` | `2012` | `PursuitGenerator` |
| `saccade` | `2013` | `SaccadeGenerator` |
| `peripheral_scan` | `2014` | `PeripheralScanGenerator` |

Visual Drill uses its own domain contract and should not be forced into Visual Loop's layer-centric payload shape.

Visual Drill canonical data is root-level parameter-centric where defined by its current contract.

---

# 5. RNG REGISTRY — FROZEN

Registered visual streams:

### Visual Loop
- `2001`: fractal
  - `0=palette_variant`
  - `1=complexity_variant`
  - `2=phase_offset`
  - `3=rotation_offset`
  - consumer: `FractalGenerator`

- `2002`: vector field
  - `0=palette_variant`
  - `1=turbulence_variant`
  - consumer: `VectorFieldGenerator`

- `2003`: particle flow
  - `0=palette_variant`
  - `1=emission_variant`
  - consumer: `ParticleFlowGenerator`

- `2004`: kaleidoscope
  - `0=palette_variant`
  - `1=symmetry_variant`
  - consumer: `KaleidoscopeGenerator`

- `2005`: geometric
  - `0=palette_variant`
  - `1=shape_variant`
  - consumer: `GeometricGenerator`

### Visual Drill
- `2011`: tracking
  - `0=tracking_variant`
  - consumer: `TrackingGenerator`

- `2012`: pursuit
  - `0=pursuit_variant`
  - consumer: `PursuitGenerator`

- `2013`: saccade
  - `0=saccade_variant`
  - consumer: `SaccadeGenerator`

- `2014`: peripheral scan
  - `0=pattern_variant`
  - `1=amplitude_variant`
  - consumer: `PeripheralScanGenerator`

Do not confuse registry ownership/description with authorized consumer identity.

---

# 6. RUNTIME / REGISTRY ARCHITECTURE — FROZEN

## `ContentRuntimeRegistry`

Use:

`ContentRuntimeRegistry.create_default()`

Then:

`registry.resolve(definition)`

`resolve()` returns a Dictionary, not the executable runtime directly.

The executable runtime is:

`resolution["runtime"]`

Tests must respect this production contract.

---

# 7. VISUAL LOOP RUNTIME — CRITICAL CURRENT STATE

`VisualLoopRuntime.gd` is frozen.

It:
- validates kind
- accepts `payload` or `content`
- validates temporal fields
- resolves the generator
- initializes presentation RNG context
- samples only through authorized stream/index semantics
- builds render states
- writes domain-tagged frame payloads into `RenderedFrameStream`
- exposes current render state
- performs no challenge/simulation calculation

Do not modify this runtime merely to make F1's audit simpler.

The previous F1 audit initially made the wrong assumption that Visual Loop required root-level `payload` and `parameters`. That assumption was corrected. The actual schema is layer-centric.

This correction is **closed and frozen**.

---

# 8. PRESENTATION ARCHITECTURE — FROZEN

Core principle:

**Runtime owns semantic state. Renderer only represents it.**

Therefore:
- `ContentRendererHost` is passive.
- `PresentationBinderRegistry` resolves binders.
- `PresentationUI` is not a router.
- There is no universal RenderModel superclass requirement.
- Routing is by `RenderedFrameStream(kind, subtype)`.
- Do not route by `payload.domain`.
- Renderers must not call generators.
- Renderers must not sample RNG.
- Renderers must not calculate gameplay/mechanics.
- Renderers must not introduce their own timing/delta logic.
- Renderers must not depend on Challenge domain state.

### `VisualContentPlayer`

Current responsibilities:
- load a canonical definition from path or CLI definition argument
- resolve the production runtime registry
- mount the correct passive renderer
- advance runtime frame-by-frame
- bind semantic frame data
- forward visual domain state to the renderer host
- cooperate with Movie Maker recording

The physical export pipeline certified here is:

`definition -> VisualContentPlayer -> ContentRuntime -> RenderedFrameStream -> Binder -> passive Renderer -> GPU -> Movie Maker -> AVI`

---

# 9. CANONICAL DEFINITIONS — FROZEN SET

There are nine canonical definitions:

1. `definitions/visual_loop_fractal_canonical.json`
2. `definitions/visual_loop_vector_field_canonical.json`
3. `definitions/visual_loop_particle_flow_canonical.json`
4. `definitions/visual_loop_kaleidoscope_canonical.json`
5. `definitions/visual_loop_geometric_canonical.json`
6. `definitions/visual_drill_tracking_canonical.json`
7. `definitions/visual_drill_pursuit_canonical.json`
8. `definitions/visual_drill_saccade_canonical.json`
9. `definitions/visual_drill_peripheral_scan_canonical.json`

Canonical definitions were normalized to include:
- `seed = 12345`
- `rng_version = 2.0`

Important data distinction:
- canonical files may use `content`
- some runtimes consume `payload`
- F1 bridged `content -> payload` in memory for runtime auditing where necessary
- the ContentEnvelope contract was not rewritten to satisfy the test

Do not “fix” this by silently changing the external contract.

---

# 10. F1 E2E AUDIT — CERTIFIED

Final corrected test:

`tests/C6F08F1ContentEnvelopeAuditTest.gd`

Certification output:

`[C6F08_F1_PAYLOAD_E2E_AUDIT] PASS - 9/9 Definitions Validated`

Then:

`[BATCH-RUNNER] PASS — 82 suite(s) superaron la auditoría E2E.`

Representative validated Visual Loop parameters from the canonical seed run:

The F1 test output contained concrete parameter dictionaries for all five Visual Loop types. The exact current test output in the baseline ZIP is authoritative; this handover intentionally does not duplicate every floating-point value to avoid introducing a transcription error.

The exact files in the ZIP are authoritative if any numeric formatting differs from this prose handover.

---

# 11. PHYSICAL EXPORT DEBUGGING — ROOT CAUSE AND FIX

Initial physical batch attempts under:

`godot --headless ... --write-movie ...`

failed with:

`3221225477 / 0xC0000005`

and zero-byte AVI files.

A smoke run showed:

`Movie Maker mode enabled...`

followed by the project main scene:

`=== GENERADOR MAESTRO INICIADO ===`

and a Dummy renderer error:

`texture_2d_get`

The conclusion was that the physical export problem was not a visual-runtime/RNG defect. The invocation was exercising the project main scene under `--headless` and Dummy rendering rather than the isolated Visual Content presentation path.

### Isolation strategy that was certified

A dedicated scene was created:

`tests/F0_8MovieMakerPilot.tscn`

with:
- Node2D root
- child `VisualContentPlayer`
- canonical fractal definition

The successful invocation intentionally did **not** use `--headless`.

---

# 12. F2-B MOVIE MAKER PILOT — CERTIFIED

Successful command:

`godot --path . tests/F0_8MovieMakerPilot.tscn --write-movie .\\output_batch_audit\\pilot.avi --fixed-fps 30 --quit-after 60`

Observed:
- OpenGL 3.3 Compatibility
- Intel Arc GPU
- Movie Maker recording `540x960 @ 30 FPS`
- `VisualContentPlayer` loaded `definitions/visual_loop_fractal_canonical.json`
- ready state `[visual_loop/fractal]`
- exactly 60 frames
- 2 seconds movie
- exit success
- physical AVI size `1,532,740 bytes`

This is a real GPU-backed physical export, not a simulated test.

---

# 13. F2/F3 BATCH EXPORT + PHYSICAL DETERMINISM — CERTIFIED

The final matrix was:

**9 content definitions × 3 runs = 27 physical exports**

Seeds:
- A = `12345`
- B = `12345`
- C = `54321`

Required relation:

`A == B`

`A != C`

All 27 processes returned exit code `0` and produced non-zero AVI files.

### Observed artifacts

| Content | A size | A SHA prefix | B size | B SHA prefix | C size | C SHA prefix |
|---|---:|---|---:|---|---:|---|
| fractal | 1,532,740 | `f62459e722c4` | 1,532,740 | `f62459e722c4` | 1,530,820 | `0134c7b3c85b` |
| vector_field | 1,143,700 | `f8c6f1b4ef02` | 1,143,700 | `f8c6f1b4ef02` | 1,171,300 | `0f085a489967` |
| particle_flow | 928,780 | `96f29c5fea82` | 928,780 | `96f29c5fea82` | 928,780 | `673cc8517c79` |
| kaleidoscope | 1,073,140 | `3f8212a16fc0` | 1,073,140 | `3f8212a16fc0` | 1,067,860 | `f6abdeedad06` |
| geometric | 1,020,340 | `f172ce41ec43` | 1,020,340 | `f172ce41ec43` | 992,020 | `a69e5bc6418e` |
| tracking | 1,029,460 | `d8844c064be9` | 1,029,460 | `d8844c064be9` | 1,027,660 | `6e301cab7035` |
| pursuit | 1,000,886 | `6d321828d429` | 1,000,886 | `6d321828d429` | 1,000,506 | `f81171b6b480` |
| saccade | 971,080 | `0830db7ba326` | 971,080 | `0830db7ba326` | 971,780 | `82a723d2f225` |
| peripheral_scan | 939,006 | `b5efc358376a` | 939,006 | `b5efc358376a` | 972,954 | `0199d045d301` |

### Global certified output

`RESULTADO GLOBAL F2/F3: PASS — Matriz de exportación y determinismo físico certificada.`

Therefore:

**C6-F0.8 is CLOSED.**

---

# 14. WHAT MUST NOT BE REOPENED

Unless new evidence demonstrates a defect, do not reopen:

- visual loop generator math
- visual drill generator math
- deterministic stream registration
- generator/RNG separation
- passive renderer architecture
- `RenderedFrameStream(kind, subtype)` routing
- the layer-centric Visual Loop payload contract
- the root-centric Visual Drill parameter contract
- the F1 E2E audit correction
- the Movie Maker pilot strategy
- the fact that physical export requires the isolated graphical scene rather than the main `GeneradorMaestro` scene
- the 27-run A/B/C determinism matrix

A new task may consume these contracts. It should not rewrite them casually.

---

# 15. KNOWN TESTING LESSON

Never equate “Godot starts” with “the intended presentation pipeline starts”.

The project main scene is `GeneradorMaestro`. A `--headless` Movie Maker invocation can accidentally exercise that scene and Dummy rendering.

For future physical visual export audits, the known-good pattern is:

1. dedicated presentation scene
2. real graphical renderer
3. explicit `VisualContentPlayer`
4. `--write-movie`
5. `--fixed-fps`
6. controlled `--quit-after`
7. artifact existence/size validation
8. SHA-256 determinism verification when applicable

---

# 16. CURRENT STATUS OF `run_batch_export.py`

The final successful batch runner used the dedicated Movie Maker pilot strategy, real graphical Godot invocation, temporary definition injection, 27 runs, SHA-256 calculation, and A/B/C checks.

The exact current implementation in the ZIP is authoritative.

Important:
- do not assume an earlier failed headless driver is still the active one
- do not revert from the successful graphical-scene strategy
- preserve the successful artifact determinism behavior

---

# 17. FROZEN WORKING TREE EXPECTATIONS

Before beginning the next domain, the new context should verify the ZIP contains at least the relevant classes/tests/assets corresponding to:

- `VisualLoopRuntime`
- `VisualDrillRuntime`
- `ContentRuntimeRegistry`
- `VisualContentPlayer`
- visual generators
- visual renderers
- binder infrastructure
- RNG registry/context infrastructure
- 9 canonical definitions
- F1 audit
- playback validation tests
- Movie Maker pilot scene
- batch export runner
- batch manifest/output artifacts if intentionally retained

Do not delete successful audit artifacts during the next context unless there is a deliberate baseline hygiene step.

---

# 18. NEXT DOMAIN IS INTENTIONALLY NOT FROZEN

The next strategic domain has **not** been selected by this handover.

Candidate directions previously discussed:
- Audio Procedural
- Mecánicas de Interacción V2

Do not treat either one as pre-approved.

The next window must first perform a short baseline audit and then choose the highest-value next domain based on architecture readiness, dependency order, and remaining project objective.

The next domain must preserve all C6-F0.8 frozen contracts.

---

# 19. CONTINUITY PRIORITY ORDER

When uncertainty appears, resolve it in this order:

1. actual contents of attached ZIP
2. explicit current tests and production code in ZIP
3. frozen contracts in this handover
4. prior certified execution evidence
5. architectural reasoning

Never use generic Godot knowledge to override direct project evidence.

---

# 20. FIRST ACTION IN NEW WINDOW

Before proposing implementation:

1. inspect the attached baseline ZIP
2. inventory tree and identify project version/checkpoint
3. locate this handover
4. verify the nine canonical definitions and F1/F2/F3 tests
5. run/inspect the relevant audit commands only as needed
6. produce a concise baseline integrity verdict
7. choose the next domain strategically
8. propose the smallest safe next checkpoint

Do not start coding before this audit unless the user explicitly directs otherwise.

---

# 21. FINAL CERTIFICATION STATEMENT

At this checkpoint, the project has demonstrated:

- `82/82` automated suite PASS
- 5 Visual Loop types operational
- 4 Visual Drill types operational
- deterministic cosmetic RNG integration
- passive shader presentation architecture
- 9/9 canonical Content Definitions passing E2E audit
- real GPU-backed Movie Maker export
- 27/27 physical exports successful
- exact SHA-256 equality for repeated identical seeds
- SHA-256 inequality for changed seeds across all nine canonical types

**C6-F0.8-F2/F3 = CLOSED / CERTIFIED / FROZEN.**

The next context begins from this state. It does not begin from an earlier C6-D4/E4/F1 baseline.
