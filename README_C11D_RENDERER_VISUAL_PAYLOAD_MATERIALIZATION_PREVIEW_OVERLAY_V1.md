# C11D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_OVERLAY_V1

Purpose: build deterministic in-memory Visual Loop and Visual Drill authoring payload instances using existing C11-C sources, without rendering or writing payload files. `CHALLENGE_004` remains unresolved here and must use the frozen runtime output.

## Apply

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
Get-FileHash "$env:USERPROFILE\Downloads\C11D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_OVERLAY_V1.zip" -DestinationPath "." -Force
```

Expected ZIP SHA-256 is supplied in the delivery message.

## Validate contract and sources

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_visual_payload_materialization_preview.py .\tools\c11d\d9\test_d_renderer_visual_payload_materialization_preview.py
python .\tools\c11d\d9\test_d_renderer_visual_payload_materialization_preview.py
```

## Run actual in-memory payload materialization (Godot 4.7.1)

```powershell
godot --headless --path . --script res://tools/c11d/d9/materialize_visual_payloads_in_memory.gd
```

This calls existing `VisualAuthoringGenerator`, `C11CVariationProfile`, `C11CPaletteBank`, `C11CVisualLoopDuration`, and `VisualDrillSeedVariation` APIs in memory only. It prints summary digests and exits non-zero on a mismatch. It does not write payloads, screenshots, videos or other artifacts, does not execute `ChallengeExecutionPipeline`, and does not emit renderer-native input.

## Governed scope

- Visual Loop `c11c_geometric_waves_v1 / harmonic_membrane`, seed 12345, variation_index 0.
- Visual Drill `tracking / tier-2`, seed 12345, variation_index 0.
- Challenge `CHALLENGE_004`: not materialized in this overlay; requires frozen runtime output.
- `variation_index` is explicitly metadata-only in V1; no undocumented seed transform is introduced.
- C11-C immutable; renderer OFF; media false; D4.8 BLOCKED; release authority NONE.
