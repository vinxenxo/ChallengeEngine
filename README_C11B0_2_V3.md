# C11-B.0.2 v3 — Pure Mathematical Presentation Framing

## Purpose

Replace the v2 SceneTree/Sprite2D-transform geometry audit with a pure mathematical
presentation geometry pipeline.

The audit never reads `global_transform`, `get_global_transform()`, rendering state,
VisibilityNotifier state, or a post-render transform.

## Contract

Simulation remains sovereign:

- no SimulationResult changes;
- no FrameSnapshot changes;
- no RNG access;
- no winning-frame recalculation;
- no detector changes.

Presentation pipeline:

`FrameSnapshot` → `CoordinateMapper` → `PresentationFramer` → `WinningFrameVisibilityGate`

The entity rectangle is derived from the existing `FrameSnapshot` fields:

- position;
- rotation;
- scale;
- asset dimensions;
- presentation calibration.

No new `FrameSnapshot.entities[*].rect` field is introduced.

## CHALLENGE_001 policy

Add presentation metadata to `challenges/CHALLENGE_001.json`:

```json
"presentation": {
  "coordinate_space": "CANVAS_1080X1920",
  "secondary_binding": "static_position",
  "static_target_position": [540.0, 960.0],
  "profile": "social_default_v1",
  "framing_policy": "PRIMARY_FOCUS"
}
```

Do not add a hardcoded challenge-id branch to the presentation code.

## Verification

```powershell
.\tools\verify_c11b02_installation.ps1
godot --headless --path . -s .\tests\C11B02PresentationFramingContractTest.gd
.\tools\run_c11b_body_visibility_audit.ps1
```

No video rerender is required.
