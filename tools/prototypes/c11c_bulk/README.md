# C11-C canonical toolchain — v2.1.3

This directory contains the canonical C11-C presentation/review/production tools. C11-B remains frozen.

## Canonical commands

Validate PowerShell syntax:

```powershell
.\tools\prototypes\c11c_bulk\validate_c11c_powershell.ps1
```

Validate delivery configuration:

```powershell
.\tools\prototypes\c11c_bulk\validate_c11c_delivery_configuration.ps1
```

Generate the Art Direction 2.0 corpus (5 seeds × 5 families = 25 videos):

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -ResetReviewAssets
```

Use explicit seeds when reproducibility of a review batch is required:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -Seeds 1234567,2345678,3456789,4567890,5678901 -ResetReviewAssets
```

Publish a final product:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family c11c_invisible_forces_v1 -Seed 271828
```

Review and production never perform prototype cleanup.

## Artifact policy

`artifacts\prototypes` is staging/review material.
`artifacts\production\audiovisual` is the protected final-product store.
`artifacts\legacy`, `qa`, `regression`, `releases`, `production`, and `tests` are protected evidence roots.

Manual prototype media cleanup:

```powershell
.\tools\prototypes\c11c_bulk\clean_c11c_artifacts.ps1 -Apply
```

Explicit C11-C prototype/reset cleanup:

```powershell
.\tools\prototypes\c11c_bulk\reset_c11c_artifacts.ps1 -Apply
```

Neither command touches `artifacts\production\audiovisual`.

## Resolution contract

C11-B keeps its frozen 540×960 viewport. C11-C captures at 720×1280 (9:16) by temporarily writing a root `override.cfg` with viewport and window overrides, then restoring/removing it. The prototype scene keeps the 540×960 logical composition and scales it by 4/3.

The family launcher invokes Godot with `--resolution 720 1280` (two CLI arguments) and verifies that the Godot log reports a 720×1280 Movie Maker capture before any downstream packaging continues.

## Audio and MP4 contract

Sound is enabled by default. `-NoSound` and `-Silent` disable audio. Exactly one canonical MP4 exists under the family staging directory after a successful run. Any audio-muxing intermediate is written only to the OS temporary directory and is deleted.

## Historical versioned scripts

Files named `run_*_v2.0.x.ps1` or `run_*_v2.1.0.ps1` are historical/superseded tooling from the iterative C11-C hardening process. Use the unversioned canonical commands above for current work.


## PowerShell orchestration rule

Canonical C11-C orchestrators invoke `.ps1` children directly (`& $script @params`). They do not spawn `powershell.exe -File` to transport array parameters. This avoids Windows PowerShell argument-flattening/binding problems with `[int[]]` parameters.
