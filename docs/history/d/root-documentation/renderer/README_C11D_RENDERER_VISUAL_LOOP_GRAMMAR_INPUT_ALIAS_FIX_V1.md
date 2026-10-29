# C11-D Visual Loop Grammar Binding — Profile Input Alias Fix V1

This is a minimal corrective overlay for the first Windows Godot 4.7.1 run of `C11D_RENDERER_VISUAL_LOOP_GRAMMAR_BINDING_AUDIT_OVERLAY_V1`.

## Confirmed defect

The frozen C11-C geometric variation profile emits the field `glow`, while the renderer-facing projected style parameter is named `glow_strength`. The original D-owned probe checked the 20 output parameter names against the source profile input dictionary before projecting them. That incorrectly rejected the profile because `glow_strength` is not an input key, even though the explicit mapping from `value["glow"]` to output `glow_strength` is correct.

## Repair

- Preserve `STYLE_KEYS` as the 20 renderer/shader output names and their canonical order.
- Add `PROFILE_INPUT_KEYS` for the 20 source profile input names, where the glow field is `glow`.
- Validate source profile completeness against `PROFILE_INPUT_KEYS`.
- Strengthen the static audit and Python regression test to pin the input list and explicit `glow` -> `glow_strength` mapping.
- Update the D-owned checkpoint to record the runtime defect and the required rerun.

## Boundaries

No C11-C source or manifest is changed. No renderer/material/shader is instantiated or executed. No renderer-native input, receipt file, payload file, or media is emitted. The family-level Visual Loop payload limitation remains open and `exact_selector_payload_materialized=false` remains authoritative.

## Local evidence

The updated Python test passes 14/14 tests in the preparation tree. The real Godot 4.7.1 runtime probe must be rerun in the user's Windows checkout after applying this overlay; this package does not claim that runtime gate has passed.
