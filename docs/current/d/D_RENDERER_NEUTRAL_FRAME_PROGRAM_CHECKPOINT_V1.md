# C11-D Renderer-Neutral Frame Program — Checkpoint V1

**State:** `PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN`  
**Date:** 2026-10-10  
**Depends on:** `D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1`  
**Owner boundary:** C11-D only; the frozen C11-C 2.19.12 source and historical manifest are immutable.

## Objective

Add a separate renderer-neutral declarative stage after logical composition. It converts the validated logical text elements into a deterministic, ordered set of semantic binding declarations. It does not construct engine commands, frames, images, audio, video or a dispatchable renderer input.

This increment is a design and contract boundary, not approval of semantic regions or of a renderer baseline.

## What the candidate represents

- `HEADER`, `FOOTER`, and `CHALLENGE_OVERLAY` are region IDs only. All remain `PROPOSED_NOT_APPROVED`; geometry is `UNRESOLVED_NO_COORDINATES`.
- Each instruction is a `DECLARE_SEMANTIC_TEXT_BINDING` declaration. It carries the exact canonical `text_value`, its SHA-256, locale, source field, semantic role, region ID and source z-order.
- Instructions are ordered by the logical composition's ascending z-order and element ID.
- Challenge has five declarations; Visual Loop and Visual Drill have three each.
- The canvas is delivery-profile metadata only. This increment emits no pixel coordinates, frame ranges, duration, transitions or schedule: `schedule_state=NOT_DEFINED`.
- The source chain is hash-bound from canonical request, editorial, plan, bridge, adapter envelope and binding preview through logical composition.
- Visual declarations are not seed-derived. Gameplay and music seed domains remain separate. Simulation truth and derived telemetry remain unbound.

## New files

- `definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1.json` — strict contract, region proposals, source and execution locks.
- `definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_SCHEMA_V1.json` — Draft 2020-12 strict output schema.
- `tools/c11d/d9/d_renderer_frame_program.py` — in-memory builder and independent validator; revalidates logical composition lineage and recomputes the whole expected program.
- `tools/c11d/d9/test_d_renderer_frame_program.py` — positive, deterministic, editorial-flow, schema and fail-closed regression coverage.

## Preparation-workspace verification

Observed in the preparation workspace:

```text
C11-D RENDERER-NEUTRAL FRAME PROGRAM PASS | content_types=3/3 | deterministic=3/3 | editorial_flow=3/3 | negative=19/19 | schema=3/3 | jsonschema=3/3 | renderer_input=NOT_EMITTED | frame_schedule=NOT_DEFINED | pixel_coordinates=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE
```

Python compilation passes. The Draft 2020-12 schema validates all three fixtures in that environment. These are preparation-workspace results; Windows verification of this new increment remains required.

## Windows verification

Run from the active checkout:

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_frame_program.py .\tools\c11d\d9\test_d_renderer_frame_program.py
python .\tools\c11d\d9\test_d_renderer_frame_program.py
python .\tools\c11d\d9\test_d_renderer_logical_composition.py
python .\tools\c11d\d9\test_d_renderer_candidate.py
python .\tools\c11d\d9\test_editorial_render_bridge.py
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Expected focused output: content types 3/3; deterministic 3/3; editorial flow 3/3; negative 19/19; structural schema 3/3. If `jsonschema` is not installed, the test explicitly reports that condition and still runs strict structural checks; do not misreport it as full JSON Schema validation.

The new focused test is not registered in the 22-step aggregate Suite. Keep it separate until the increment has Windows acceptance and technical review.

## Mandatory boundaries

- `D9.10` adapter stays `PREPARE_ONLY`; its envelope is not renderer-native input.
- `program_executable=false`; no dispatch, no renderer activation, no persistence/output path, no media, no Godot/FFmpeg launch.
- No frame timeline or pixel coordinates are invented. Do not treat delivery width/height/FPS as render authorization.
- No semantic region is promoted from `PROPOSED_NOT_APPROVED`; do not import or modify C11-C's frozen geometry implementation.
- No simulation truth, `winning_frame`, `close_calls`, or derived telemetry is bound.
- C11-C 2.19.12 manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D4.8 remains BLOCKED; renderer OFF; media false; `release_authority=NONE`; D9 OPEN; D10 BLOCKED. Renderer-baseline approval and C11-D freeze eligibility remain false.

## Next design review

After Windows acceptance, review the semantic role/region vocabulary independently. Only after that review may a subsequent increment propose a temporal schedule contract. Do not implement an image/video backend or dispatch adapter in this step.
