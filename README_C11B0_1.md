# C11-B.0.1 — Presentation Space Audit / Local Sprite Geometry

Purpose: correct the audit-space mismatch discovered in C11-B.0.

The previous gate derived a Rect2 through `Sprite2D.get_global_transform()` and then converted it through `PresentationUILayer`. That is not the same coordinate space in which `CoordinateMapper` writes gameplay sprite positions.

This delta audits `Sprite2D.transform * Sprite2D.get_rect()` in `GestorJuego` local presentation space. It also emits:

- `object_logical_position`
- `object_expected_position`
- `object_actual_position`
- `audit_space`

No simulation/RNG/SimulationResult mathematics is changed.

## Apply

Copy the delta files into the project, preserving paths. Then run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\tools\verify_c11b01_installation.ps1
```

Then:

```powershell
godot --headless --path . -s .\tests\C11B0UnifiedSocialFrameContractTest.gd
.\tools\run_c11b_body_visibility_audit.ps1
```

Do not re-render C11-A or C11-A.1.
