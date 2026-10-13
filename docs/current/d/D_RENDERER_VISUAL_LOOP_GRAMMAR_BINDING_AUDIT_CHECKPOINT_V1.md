# C11-D — Visual Loop Grammar Binding Audit Checkpoint V1

**Updated interpretation (2026-10-13):** this document describes the standalone, read-only selector-to-prototype source audit; its own receipt correctly remains `exact_selector_payload_materialized=false` because it does not build the dynamic composite. The existing dynamic request→payload binder now composes the pinned `harmonic_membrane@0` parameter instance into a D-owned in-memory composite for that one selector. See `D_RENDERER_VISUAL_LOOP_COMPOSITE_PAYLOAD_INTEGRATION_CHECKPOINT_V1.md` for its separate strict contract and Windows acceptance gate.


**State:** `SOURCE_TRACE_PINNED_RUNTIME_PROFILE_PROBE_REPAIR_REQUIRED_NOT_EXACT_PAYLOAD`  
**Purpose:** verify the exact `harmonic_membrane` selector-to-prototype-grammar trace without claiming a D renderer payload instance.  
**Scope:** one fixed Visual Loop selector, four deterministic gameplay seeds, source-only contract plus a Godot in-memory profile probe.

## Findings this audit is designed to prove

1. The D9.9 selector is `visual_loops / c11c_geometric_waves_v1 / harmonic_membrane`.
2. The Producer registry, frozen C11-C `GRAMMAR_IDS`, and geometric `C11CVariationProfile` use the same five grammar IDs in the same order.
3. The frozen prototype's `C11C_VISUAL_GRAMMAR` override explicitly maps the selected grammar to its numeric index. `harmonic_membrane` maps to `grammar_mode=0`.
4. The frozen `GeometricWavesRenderer.set_style` consumes 20 ordered style arguments and maps `grammar_mode` to the shader uniform. The shader maps index 0 to `field_harmonic_membrane`.
5. The seed-derived family profile is deterministic, and the selected grammar identity remains independent of the seed when the explicit grammar override is applied to a copy of the profile.

## Critical remaining limitation

This does **not** execute the frozen prototype's `_apply_grammar_override`, create its scene/renderer/material, execute the shader, or instantiate the D renderer input. It projects 20 style parameter values in memory by matching the pinned setter clamps and orders. The upstream family authoring envelope remains subtype `geometric`; this standalone audit’s own `exact_selector_payload_materialized=false` remains truthful. The separate dynamic composite’s selector-materialization claim is governed by the strict contract in the composite checkpoint, not by this probe.

The audit therefore proves the source route from selector identity to the existing prototype grammar branch, but it does not yet prove an integrated grammar-specific D payload, media output, or production readiness.

## Runtime seeds

The headless Godot probe uses `12345`, `54321`, `0`, and `2147483646`. For each seed it checks same-seed determinism, the canonical grammar override to index 0, and a 20-parameter style projection digest. The selected grammar must remain `harmonic_membrane` across all seeds, and at least two style digests must differ.

## Scope and governance

- No files from C11-C are edited.
- The probe only calls `C11CVariationProfile.build("geometric", seed)` and creates dictionaries/hashes in memory.
- It does not instantiate the prototype or renderer, does not create a `ShaderMaterial`, does not execute the shader, does not write a receipt/payload, and creates no media.
- `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`.
- D9.14/D9.16 remain blocked as required; D9.17 remains NO-GO; D10 remains BLOCKED. Renderer baseline approval and D baseline approval remain missing.

## Runtime probe defect found on Windows — repair V1

The first actual Godot 4.7.1 run failed before hashing the projected parameters. The frozen C11-C profile exposes the field `glow`, while the renderer/shader output name is `glow_strength`. The initial probe incorrectly checked all renderer output names against the source profile dictionary, so the input completeness guard returned an empty projection. This was a D-owned probe defect; it did not indicate invalid gameplay seeds and required no C11-C change.

Repair V1 separates `PROFILE_INPUT_KEYS` from `STYLE_KEYS`. The former reflects the profile's 20 source fields (`glow` included); the latter preserves the renderer/shader's 20 output parameter names (`glow_strength` included). The static audit and regression test now explicitly pin this alias mapping. The real Godot probe must be rerun after applying the repair; runtime closure is not claimed until that run passes.

## Windows verification

Run from the repository root:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_visual_loop_grammar_binding_audit.py
python -B .\tools\c11d\d9\d_renderer_visual_loop_grammar_binding_audit.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120
```

Expected probe result: `runtime_seeds=4/4`, `style_parameters=20/20`, `selector_to_prototype_grammar=PASS`, `family_envelope_grammar_gap=OPEN`, `exact_selector_payload_materialized=false`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`.

## Relationship to the composite payload gate

The separate D-owned parameter-instance probe is now consumed by the existing dynamic request→payload composite only for `harmonic_membrane`. Re-run the composite checkpoint’s Windows acceptance, then reconcile the resulting evidence with the candidate I/O gap audit and candidate identity inventory. This standalone audit still must not instantiate or dispatch the renderer. No visual editor/consumer, renderer-native input, render dispatch, or media creation is authorized by this checkpoint.
