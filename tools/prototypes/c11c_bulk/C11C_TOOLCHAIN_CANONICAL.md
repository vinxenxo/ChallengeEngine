# C11-C Canonical Toolchain — v2.1.4

## Responsibilities

- Family `run_prototype.ps1`: render one deterministic family loop. No cleanup.
- `run_c11c_multiseed_bulk.ps1`: render supplied seeds across all five families. No cleanup.
- `run_c11c_art_direction_review.ps1`: generate a 5-seed × 5-family review corpus. Optional `-ResetReviewAssets` resets only `artifacts\prototypes\c11c_review_assets`.
- `run_c11c_production.ps1`: publish one validated product under `artifacts\production\audiovisual`.
- `run_c11c_production_bulk.ps1`: publish a seed set for one family.
- `clean_c11c_artifacts.ps1`: explicit manual cleanup of regenerable prototype media.
- `reset_c11c_artifacts.ps1`: explicit reset of C11-C prototype workspace only.

## PowerShell orchestration

All child `.ps1` scripts are invoked directly with `&` plus hashtable splatting. No nested `powershell.exe -File` is used to transport typed arrays/switches.

## Godot capture

The movie capture CLI argument is exactly:

`--resolution 720x1280`

It is one argument. `project.godot` remains untouched. A temporary root `override.cfg` supplies effective viewport/window dimensions and is restored/removed after capture.

## Review delivery baseline

- 720x1280 / 9:16
- 30 FPS
- 540 frames
- 18.00 s
- audio ON by default
- `-NoSound` / `-Silent` disables sound
- one final MP4
- social metadata sidecar

## Production protection

Final products live under:

`artifacts\production\audiovisual`

Review/cleanup tools must never target that root.

## Canonical validation

```powershell
.\tools\prototypes\c11c_bulk\validate_c11c_preflight.ps1
```

## Canonical review

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -ResetReviewAssets
```
