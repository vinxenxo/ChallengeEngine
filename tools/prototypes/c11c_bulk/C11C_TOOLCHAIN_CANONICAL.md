# C11-C Canonical Toolchain — v2.1.3

## Canonical responsibilities

- `run_prototype.ps1` per family: render one C11-C visual loop.
- `run_c11c_multiseed_bulk.ps1`: render multiple seeds across all five families. No cleanup.
- `run_c11c_art_direction_review.ps1`: canonical 5×5 review corpus. No prototype cleanup. Optional `-ResetReviewAssets` clears only `artifacts\prototypes\c11c_review_assets`.
- `run_c11c_production.ps1`: publish one validated product into `artifacts\production\audiovisual`.
- `run_c11c_production_bulk.ps1`: publish a seed set for one family.
- `clean_c11c_artifacts.ps1`: manual prototype media cleanup only.
- `reset_c11c_artifacts.ps1`: explicit destructive reset of C11-C prototype workspace only.

## PowerShell invocation rule

C11-C scripts call child `.ps1` scripts directly with `& $script @params`. They do not use `powershell.exe -File` for internal orchestration. This preserves typed `[int]`, `[int[]]` and switch parameters on Windows PowerShell.

## Delivery

- Capture: 720×1280, 9:16.
- Godot Movie Maker CLI: `--resolution 720 1280` (two separate arguments).
- FPS: 30.
- Current review duration baseline: 18 s / 540 frames.
- `project.godot` is not modified by C11-C launchers. A temporary root `override.cfg` provides the capture viewport/window settings and is restored/removed after each run.

## Artifact separation

`artifacts\prototypes` is disposable/review staging.
`artifacts\production\audiovisual` is protected final-product storage. Review/clean/reset tools must never target production.

## One-time tool-tree cleanup

After installing v2.1.3, optionally run:

```powershell
.\tools\prototypes\c11c_bulk\retire_legacy_c11c_tool_versions.ps1
```

This is a dry-run. Add `-Apply` only when the list is confirmed. It removes superseded versioned C11-C bulk/review launchers, not canonical tools or frozen C11-B tools.
