# C11-B.0.2 — Presentation Framing Contract v1

This delta fixes the C11-B.0.1 diagnostic path without changing simulation mathematics.

## What changed
- Added `PresentationFramer.gd`.
- Added declarative `presentation.framing_policy` resolution.
- `PRIMARY_FOCUS` computes one constant presentation offset from the real winning-frame Sprite2D geometry.
- That offset is applied to the **actual Sprite2D positions** for the runtime, not merely to audit dictionaries.
- The visibility gate reads the post-framing geometry and applies the policy.
- `STATIC_CANVAS` remains the default.
- `FIT_ENTITIES` is reserved and intentionally not implemented by this delta.

## Important
Do not hardcode `CHALLENGE_001` inside the auditor. Add this presentation-only field to the challenge definition copy used for C11-B:

```json
"presentation": {
  "coordinate_space": "CANVAS_1080X1920",
  "secondary_binding": "static_position",
  "static_target_position": [540.0, 960.0],
  "profile": "social_default_v1",
  "framing_policy": "PRIMARY_FOCUS"
}
```

This changes presentation metadata only; it does not alter `generation`, mechanics, RNG or winning-frame math.

## Execution
1. Run the existing contract test if desired.
2. Run:
`.\tools\run_c11b_body_visibility_audit.ps1`

Expected audit result: `54/54`.

Do not accept a PASS unless the `[C11B_VISIBILITY_JSON]` records show:
- `framing_policy = PRIMARY_FOCUS` for CHALLENGE_001.
- non-zero `presentation_frame_offset` for those runs.
- `object_actual_position` equal to the post-framing runtime position.
- the audited `object.screen_rect` is inside `body_rect`.

## Additional verification

Optional installation check:
`.\tools\verify_c11b02_installation.ps1`

Optional contract test:
`godot --headless --path . -s .\tests\C11B02PresentationFramingContractTest.gd`


## v2 corrections

v2 fixes two integration defects found by real Godot 4.7.1 execution:

1. The contract test uses explicit Vector2/Rect2 typing so GDScript 4.7.1 does not reject Variant inference.
2. `build_winning_entity_audit()` now measures the post-framing Sprite2D in `PresentationUI` presentation space using the sprite global transform; it no longer compares `GestorJuego`-local geometry against the social BodyRegion. A defensive `force_update_transform()` is used immediately before reading the transform.

Do not close C11-B.0.2 from the installer PASS alone. Required order remains: installation -> contract test PASS -> visibility audit.
