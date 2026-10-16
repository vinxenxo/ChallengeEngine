# C11-D checkpoint — Request-scoped Visual Loop grammar parameter binding V2

**State:** preparation-only implementation candidate; Python contract tests pass in the isolated preparation tree. The new real-Godot 4.7.1 five-selector run must still pass in the active Windows checkout before runtime evidence can be recorded.

## Purpose

Extend the V2 request/source/reference matrix to produce one in-memory, selector-specific 20-field style-parameter instance per canonical Geometric Waves request. The runner binds the parameter-instance digest to the canonical D9.9 request and plan hashes, the D9.10 bridge and `PREPARE_ONLY` adapter hashes, the reused V1 source-binding digest, and the selector-specific timing/review envelope digest.

The fixed scope is only `visual_loops / c11c_geometric_waves_v1` with these ordered selector/index/shader mappings:

| Grammar | Index | Frozen shader branch |
|---|---:|---|
| `harmonic_membrane` | 0 | `field_harmonic_membrane` |
| `interference_plane` | 1 | `field_interference_plane` |
| `parametric_ribbon` | 2 | `field_parametric_ribbon` |
| `lattice_wave` | 3 | `field_lattice_wave` |
| `orbital_wave` | 4 | `field_orbital_wave` |

## Execution and data boundary

- The Godot harness builds the frozen `C11CVariationProfile` twice for each request seed, compares the raw profile results, deep-copies the profile dictionaries, then binds the explicit request grammar index/name to those local copies and projects the same 20 existing style fields.
- Each returned parameter instance is sealed with separate SHA-256 digests for style values and the complete parameter instance. The receipt adds a canonical request/plan/source binding and review-reference digest join.
- Timing/review values stay metadata-only. The harness receives only the selector-specific envelope digest, shared policy-reference-set digest, count `9`, and `policy_values_consumed=false`. It does not receive or consume policy bodies.
- The harness does not instantiate `GeometricWavesRenderer`, a `ShaderMaterial`, a shader, or a renderer-neutral frame program. It does not create a full Visual Loop payload, persist an input/receipt, emit renderer-native input, invoke rendering, or write media.
- Frozen C11-C source and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remain unchanged. The request's explicit selector only overrides `grammar_mode` and `grammar_name` on local copies of the profile values; it does not change gameplay/simulation code or C11-C source truth.

## Acceptance gates

The Python test suite verifies schema strictness, source lineage, request/plan/selector/ref joins, finite 20-field parameter shape, deterministic repeated profile values, integrity hashes, selector-to-index-to-branch parity, and fail-closed governance. It mocks the Godot subprocess by design; **the unit test is not runtime evidence**.

Runtime acceptance requires invoking the actual Godot console binary at `4.7.1.stable.mono.official.a13da4feb`. The runner runs `--version` first and then executes one in-memory probe per grammar. Only a complete pass may record `parameter_instances=5/5`, `request_parameter_bindings=5/5`, and `deterministic_repeats=5/5` in the active Windows evidence.

## Deliberately unresolved

`selected_grammar_parameter_instances_bound=5/5` is strictly about request-bound parameter dictionaries. It must not be substituted for `selected_grammar_payload_instances_bound`: that remains `0/5`. `exact_selector_visual_payload_materialized=false` remains mandatory, as do `approvals_granted=0/19`, `candidate_input_admissible=false`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, `D9.10=PREPARE_ONLY`, `D9.17=BLOCKED_NO_GO`, and `D10=BLOCKED`.

This checkpoint does not approve V2 binding, timing/review policy, editorial-to-visual consumption, temporal alignment, a renderer baseline, a renderer input contract, D9 closure, production, or release.
