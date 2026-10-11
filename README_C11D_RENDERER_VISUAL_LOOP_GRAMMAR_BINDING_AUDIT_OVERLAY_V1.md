# C11-D Visual Loop Grammar Binding Audit Overlay V1

This is an additive, read-only audit of the Visual Loop selector-to-prototype-grammar route for the pinned `c11c_geometric_waves_v1 / harmonic_membrane` review selector.

## Contents

- Strict audit contract and Draft 2020-12 schema.
- Strict Godot probe-receipt schema.
- Python source-pin/static-chain audit and stdout-only real-Godot runner.
- Python negative/regression contract tests.
- Godot in-memory profile/style parameter probe.
- Checkpoint documentation.

## What it proves

It verifies that the Producer grammar registry, frozen profile/prototype IDs, explicit `C11C_VISUAL_GRAMMAR` override, renderer style argument order, shader uniform and `field_harmonic_membrane` branch agree. With Godot 4.7.1, it evaluates four seeds through the frozen `C11CVariationProfile`, projects the 20 style parameter values in memory, confirms deterministic repeats, and requires the selected grammar to stay fixed while seed-derived visual parameters vary.

## What it does not prove

The probe does not instantiate the production prototype, renderer, material or shader; it does not create a D-owned grammar-specific payload, renderer-native input, receipt file, render job or media. The canonical C11-D authoring envelope remains family-level `geometric`; `exact_selector_payload_materialized=false` and `family_envelope_grammar_gap=OPEN` must remain unchanged.

## Run

From the repository root:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_visual_loop_grammar_binding_audit.py
python -B .\tools\c11d\d9\d_renderer_visual_loop_grammar_binding_audit.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120
```

The Python contract test is not a substitute for the runtime probe. The actual Windows Godot run must pass before this checkpoint can be closed.

## Governance

C11-C remains immutable. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 remains NO-GO and D10 remains blocked.
