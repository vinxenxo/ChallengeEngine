# C10-A.1 — Visual Authoring Canonical Policies

Status: **DESIGN / INTEGRATION PACKAGE — NOT CERTIFIED**

## What this closes

C10-A.1 replaces the illustrative C10-A policies with nine declarative production authoring policies and upgrades the suite to a 9/9 matrix:

### Visual Loop
- fractal
- vector_field
- particle_flow
- kaleidoscope
- geometric

### Visual Drill
- tracking
- pursuit
- saccade
- peripheral_scan

Tier **2** is explicitly anchored to the C6-F0.8 canonical baseline: loops use `speed=1.0`, `complexity=2`, `seamless=true`, `boundary_tolerance=0.01`; drills use `difficulty_tier=2`, `speed_multiplier=1.0`, `pacing_mode=constant` and the frozen canonical stimulus/targets/distractors/trajectory/task shape.

Tiers 1/3/4/5 are **C10 product-authoring policy**, not changes to the frozen runtime or generator math.

## Real identifiers used by the production-context test

- presentation: `social_default_v1`
- coordinate space: `2d`
- assets family: `fam_001`
- audio profile: `default_procedural_music` with `enabled=false`

`fam_001` is an existing repository asset-family ID. It is intentionally not described as a dedicated visual asset family; the C6-F0.8 visual runtime does not acquire new asset-family semantics from this package.

`fake_identity` and the historical mock IDs (`f1`, `a1`, `visual_default`) are not used.

## Architecture invariant

This package modifies only `core/authoring/` plus authoring-data JSON and the C10 test. It does **not** modify:

- `core/runtime/visual/`
- `core/runtime/visual_drill/`
- generator implementations
- RNG stream mappings
- `RenderedFrameStream`
- passive renderers/binders
- Movie Maker/export code

## Apply

Copy these package paths into the project, preserving directories:

```text
core/authoring/VisualDifficultyResolver.gd
core/authoring/VisualAuthoringPolicyRegistry.gd
core/authoring/VisualAuthoringGenerator.gd
core/authoring/adapters/VisualLoopAuthoringAdapter.gd
core/authoring/adapters/VisualDrillAuthoringAdapter.gd
profiles/difficulty/visual_loop_*.json
profiles/difficulty/visual_drill_*.json
tests/C10AVisualAuthoringPipelineTest.gd
```

The original C10-A request/context/registry files remain compatible and are included here as the baseline contract.

## Real-project verification

Run in the actual Windows/Godot 4.7.1 repository:

```powershell
godot --headless --path . --editor --quit
godot --headless --path . -s .\tests\C10AVisualAuthoringPipelineTest.gd
```

Expected terminal marker after real execution:

```text
[C10A_VISUAL_AUTHORING_PIPELINE_SUITE] PASS — C10-A.1 9/9
```

Passing a package inspection or a container-side JSON check is not C10-A.1 certification.
