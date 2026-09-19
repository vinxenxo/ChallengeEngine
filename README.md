<!-- C11_FREEZE_STATUS_START -->

## C11 FREEZE â€” Current Status

**C11 is CLOSED / CERTIFIED / FROZEN.**

The C11 cycle unified challenge and visual presentation around a common 540x960 social structure:

- Header: 0..144
- Body: 144..816
- Footer: 816..960

The deterministic simulation boundary is unchanged. Presentation maps and renders existing truth; it does not calculate mechanics, winning frames or RNG outcomes.

Freeze evidence includes the 103/103 logical corpus, 54/54 retrocompatibility, 576 stress executions, 2/2 physical smoke exports and 54/54 QA video renders. The C7-A2 mixed-audio rule remains authoritative and is intentionally outside the video-only QA matrix.

The next active scope is **C11-C Art Direction**, restricted to presentation and visual assets.

<!-- C11_FREEZE_STATUS_END -->

# C10-C â€” Visual Authoring -> Runtime -> Physical Export

## Scope

C10-C is an integration checkpoint. It consumes the already-certified C10 authoring layer and the frozen C6-F0.8 visual runtime/presentation contracts.

It does **not** modify:

- Visual Loop/Drill generator math
- RNG stream registration/ownership
- `RenderedFrameStream`
- `ContentRuntimeRegistry`
- binders/renderers
- `VisualContentPlayer`
- Movie Maker strategy
- `build_factory.py`

## 1. Runtime E2E

`tests/C10CEndToEndTest.gd` generates all 9 canonical visual routes through `VisualAuthoringGenerator`, resolves each generated `ContentEnvelope V2` through `ContentRuntimeRegistry.create_default().resolve(envelope)`, and verifies:

- authoring success
- envelope identity/schema/kind/subtype
- seed and RNG version
- 60 frames / 30 FPS / 2.0 s
- runtime resolution and initialization
- `RenderedFrameStream` existence and contract validity
- stream `(kind, subtype, fps)`
- sequential frame indices `0..59`
- exact frame cardinality
- no frame after completion
- no Challenge `phase` semantics

Execution:

```powershell
godot --headless --path . -s .\tests\C10CEndToEndTest.gd
```

Expected marker:

`[C10C_VISUAL_AUTHORING_RUNTIME_E2E_SUITE] PASS â€” 9/9`

## 2. Physical export smoke

`tests/C10CPreparePhysicalFixtures.gd` writes exactly two envelopes produced by the same authoring layer:

- `visual_loop/fractal`
- `visual_drill/tracking`

`tools/run_C10C_physical_export.ps1` then uses the already-certified graphical presentation path:

`VisualContentPlayer.tscn -> Movie Maker -> AVI -> FFmpeg -> MP4 -> ffprobe`

It explicitly does **not** use `--headless` for Movie Maker.

Execution:

```powershell
.\tools\run_C10C_physical_export.ps1
```

The smoke asserts:

- non-zero AVI
- 540x960
- 30/1 FPS
- 60 frames
- ~2.0 seconds
- non-zero MP4
- SHA-256 captured for AVI and MP4
- a test-only `C10C_PHYSICAL_SMOKE_MANIFEST.json`

Expected marker:

`[C10C_PHYSICAL_EXPORT_SMOKE] PASS â€” 2/2`

The generated smoke manifest is explicitly marked `production_manifest = false`; it does not replace or mutate the production manifest contract.

## Important

This package is **prepared, not certified**. Final certification requires the real Godot/Windows execution supplied by the user.

