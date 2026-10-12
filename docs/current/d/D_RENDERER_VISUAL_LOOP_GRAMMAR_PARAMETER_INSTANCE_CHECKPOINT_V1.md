# C11-D — Visual Loop Grammar Parameter Instance Checkpoint V1

**State:** `PREPARATION_ONLY_GRAMMAR_PARAMETER_INSTANCE_READY_FOR_WINDOWS_RUNTIME_GATE`

## Purpose

Close the narrow gap demonstrated by the Visual Loop grammar source audit: build a request-bound, grammar-specific *parameter instance* for `visual_loops / c11c_geometric_waves_v1 / harmonic_membrane`, using the canonical D9.9 request chain and a copy of frozen `C11CVariationProfile` output.

## What this proves if the Windows probe passes

- Each case is first accepted by the canonical D9.9 → D9.10 bridge/adapter/source-binding chain already implemented in `d_renderer_dynamic_request_payload_binding.py`.
- The explicit selector `harmonic_membrane` is bound to `grammar_mode=0` independently of the seed-derived family profile.
- Twenty ordered style parameters are assembled into a D-owned in-memory parameter structure. Source profile key `glow` maps to renderer style parameter `glow_strength`.
- Gameplay-seed change alters the parameter-instance/style digest. Changes to music seed, variation index, delivery profile, and editorial title leave the visual parameter-instance digest unchanged, while request binding hashes differ.

## Critical distinction

This is **not** the canonical family authoring envelope and is **not** renderer input. It does not update the upstream dynamic request contract's `exact_selector_payload_materialized=false`. That status continues to mean no exact selector-specific visual payload has been assembled and integrated through the Visual Loop authoring adapter. This checkpoint only proves the separate grammar-parameter instance exists in memory, request-bound by hashes.

## Runtime matrix

Six canonical requests: base seed 12345; gameplay-seed-only 54321; music-seed-only; variation-index-only; delivery-profile-only; editorial-title-only. The five non-gameplay metadata comparisons must keep the parameter-instance digest identical to BASE except for the gameplay-seed case; the request-binding digest must change for each altered request.

## Boundaries

- Reads and hashes only; request, payload and receipt are not persisted.
- Does not instantiate the prototype or renderer; does not create `ShaderMaterial`; does not execute the shader; does not emit native renderer input or media.
- Does not edit any C11-C source.
- `exact_grammar_parameter_instance_materialized=true` only for this separate parameter instance; `exact_selector_visual_payload_materialized=false` remains authoritative upstream.
- `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.14/D9.16 blocked, D9.17 NO-GO, D10 blocked.

## Windows gate

Run `test_d_renderer_visual_loop_grammar_parameter_instance.py`, then execute `d_renderer_visual_loop_grammar_parameter_instance.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120`. Runtime closure requires `cases=6/6`, `canonical_request_chain=6/6`, `exact_grammar_parameter_instance=6/6`, `style_parameters=20/20`, gameplay seed changes the actual style and instance digests, and `metadata_orthogonality=4/4`.

## Preparation validation note (2026-10-12)

- New contract test: `PASS 15/15` in the preparation tree.
- Existing Visual Loop grammar binding audit: `PASS 14/14`.
- Existing dynamic request payload binding contract: `PASS 12/12`.
- Existing request-scoped materialization binding contract: `PASS 9/9`.
- Existing candidate I/O contract: `PASS`.
- Existing unified content review: `PASS 36/36`.
- The preparation export does not include the locally reconciled legacy `c11d-control` quarantine ledger, so its lifecycle test cannot be relied upon here; rerun lifecycle and baseline in the full Windows checkout.
- **Actual Godot 4.7.1 execution of this new parameter-instance harness has not been performed in the preparation environment and remains a required Windows gate.** No runtime PASS is claimed here.
