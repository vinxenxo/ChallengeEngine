# C11-C Bulk / Review / Production Toolchain — v2.1.4

## Canonical commands

Preflight:
```powershell
.\tools\prototypes\c11c_bulk\validate_c11c_preflight.ps1
```

New art-direction review corpus (5 random seeds × 5 families = 25 renders):
```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -ResetReviewAssets
```

Fixed five seeds:
```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -Seeds 1234567,2345678,3456789,4567890,5678901 -ResetReviewAssets
```

Single product:
```powershell
.\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family c11c_invisible_forces_v1 -Seed 271828
```

## Delivery contract

- 720x1280, 9:16
- 30 FPS
- 540 frames
- 18.00 s review baseline
- default audio ON
- `-NoSound` / `-Silent` disables audio
- one canonical final MP4 per run
- social sidecar required

## Godot capture

Each family launcher passes the movie resolution to Godot as **one argument**:

`--resolution 720x1280`

The frozen `project.godot` is not modified. A temporary `override.cfg` adjusts effective viewport/window settings and is restored/removed after capture.

## Separation

Review generation does not clean prototype artifacts. `-ResetReviewAssets` affects only `artifacts\prototypes\c11c_review_assets`.

Production is stored under `artifacts\production\audiovisual` and is not targeted by review cleanup/reset.
