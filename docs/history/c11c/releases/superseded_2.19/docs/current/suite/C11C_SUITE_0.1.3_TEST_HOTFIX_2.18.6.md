# C11-C Suite 0.1.3 — Test Hotfix 2.18.6

## Scope

This revision fixes two C11-C regression-suite defects found during the final C freeze gate. It does not introduce a new Suite GUI feature and does not modify simulation/mechanics/RNG truth.

## Repairs

- `C11CVisualDurationPolicyContractTest.gd` now reads the duration policy as JSON and validates the current 17s non-Tracking default plus the 21s Tracking override.
- `run_c11c_visual_drill_review.ps1` now declares `$DefaultGameplayDurationSeconds=17.0`; Tracking remains `$TrackingGameplayDurationSeconds=21.0`.
- `C11CVisualLoopLongformSourceArtifactContractTest.gd` now defines `_assert()` locally, so it is a valid directly executable Godot `SceneTree` test.

## Acceptance

Focused first:

```powershell
.\c11c-suite\c11c-test\run_suite.bat C11CVisualDurationPolicyContractTest.gd
.\c11c-suite\c11c-test\run_suite.bat C11CVisualLoopLongformSourceArtifactContractTest.gd
```

Then the complete logical corpus:

```powershell
python .\tests\run_all.py
```

After the logical gate is green, perform the final Windows runtime gate required for C11-C closure.
