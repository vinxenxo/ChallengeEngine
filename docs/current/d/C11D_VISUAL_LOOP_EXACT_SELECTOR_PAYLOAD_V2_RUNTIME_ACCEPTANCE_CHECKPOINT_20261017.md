# C11-D Visual Loop Exact-Selector Payload V2 — Active Windows Runtime Acceptance Checkpoint

**Date:** 2026-10-17  
**State:** `OPERATOR_CONFIRMED_WINDOWS_GODOT_RUNTIME_PASS_PREPARATION_ONLY_NO_RENDERER_INPUT`  
**Gate:** Canonical request planning → request-bound grammar parameter instance → exact-selector visual payload, in memory only.  
**Authority:** Scoped technical evidence only; not renderer admission, policy approval, D baseline approval/freeze, production or release.

## 1. Active-checkout acceptance evidence

The operator ran the acceptance block in the active Windows repository. Its preflight reported `Pinned source hashes verified: 7/7`. It resolved Python 3.13 and the Godot console executable, then verified Godot `4.7.1.stable.mono.official.a13da4feb`.

The audit exited `0` and emitted this exact summary:

```text
C11-D VISUAL LOOP EXACT SELECTOR PAYLOAD V2 AUDIT PASS | direct_source_pins=70/70 | request_plans=5/5 | parameter_instances_bound=5/5 | exact_selector_visual_payload_instances_materialized=5/5 | distinct_payload_instance_hashes=5/5 | deterministic_repeats=5/5 | authoring_envelopes=5/5 | shader_branch_selector_reviews=5/5 | policy_reference_pairs=45/45 | policy_values_consumed=false | renderer_inputs_emitted=0/5 | payload_files_written=false | approval_assertions_checked=19 | approvals_granted=0 | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE
```

## 2. Evidence fingerprints

| Evidence | SHA-256 / value |
|---|---|
| Godot version | `4.7.1.stable.mono.official.a13da4feb` |
| Exit code | `0` |
| Internal report self-hash | `55240ee0e34340bd860e4243f03d49ce777aa6ef87e5154443f5e2b1a9754d74` |
| stdout | `2b8a7bba0bf042c83d622c44ae5c3512c3ce5adc351c2c3f440008a2f7ca0b83` |
| stderr (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Saved report file | `ecdaac7e6155663ec13661427808c05f636874edb18ac0bb2c509bfa0499a03f` |
| Godot version stdout | `d1046084c2493a272b0b439dc2f6dc74b801cd74659c5010a67c1b2f3acc5866` |
| Evidence directory | `C:\Users\vinxe\AppData\Local\Temp\C11D_LOOP_EXACT_SELECTOR_V2_RUNTIME_20261017_104145` |

Source preflight hashes expected and confirmed by the operator:

| Path | SHA-256 |
|---|---|
| `release/C11C_FREEZE_PACKAGE_MANIFEST.json` | `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` |
| `tools/c11d/d9/d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py` | `76908c16d1b8fae5fa25aab4e35222259139954d6b25a1552ffc741eca8d22d0` |
| `tools/c11d/d9/materialize_visual_loop_grammar_parameter_matrix_v2_in_memory.gd` | `9d5a869d9db65a722bebd443acc9c90b8dc169ae3a5fada2e506ba7c1cee9cdb` |
| `definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_V2.json` | `f7c35fd5afbb593734aa340e838ef3081f86d9d971ef2bdcffe341a413494947` |
| `tools/c11d/d9/d_renderer_visual_loop_exact_selector_payload_v2.py` | `9d7d7c63d8c09e63bf8ef639c091d4a89f8cd48a5963beec734ca0ce37e32f33` |
| `tools/c11d/d9/materialize_visual_loop_exact_selector_payload_v2_in_memory.gd` | `52a9d26ae38298c2c955bb727f75324d6b87063032dcb8762e7d838cb2609641` |
| `definitions/c11d/production/D_RENDERER_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2.json` | `50379db3cd15dcae2ca8a39b6ddfc0d2e73835bea7d98983f81ed5c6ebcdd325` |

The values above are operator-supplied runtime evidence. The report and logs are at the Windows path above; they are not embedded in this documentation checkpoint.

## 3. Scope accepted

The fixed contract order is:

1. `harmonic_membrane` — index `0`, `field_harmonic_membrane`
2. `interference_plane` — index `1`, `field_interference_plane`
3. `parametric_ribbon` — index `2`, `field_parametric_ribbon`
4. `lattice_wave` — index `3`, `field_lattice_wave`
5. `orbital_wave` — index `4`, `field_orbital_wave`

All five are under `visual_loops / c11c_geometric_waves_v1`. The runtime built five request plans, five 20-style-value parameter instances, and five distinct in-memory visual payloads. The report says independent repeats passed `5/5`; the exact-selector audit and its parent binding audit were invoked as part of the runner.

## 4. Limits — do not overstate this gate

- It is not a shader/material execution or rendered-video test.
- It does not produce files for payloads or receipts, renderer-native input, dispatch, or media.
- It does not approve any of the 19 pending policy/authority assertions.
- It does not close the candidate I/O audit; latest prior recorded status remains `0/10 complete, 6 partial, 4 blocked` pending refresh on the active checkout.
- It does not establish seed sensitivity/orthogonality across these five grammars; the request chain used by this audit is not the seed-domain experiment.
- It covers only the five geometric grammars, not all Visual Loop grammars/families or all Challenge selectors.

## 5. Required next gate — new versioned Visual Loop seed-domain audit

Do not change `D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1` or its schema/runner. They are pinned to the V1 binder and bounded to one Challenge and one Loop representative. Do not label the five-grammar seed scope complete merely because selector payloads now bind.

Build a separate D-owned V2 seed audit over the five grammars above. The request planner and every downstream identity must be regenerated for each seed variant; do not mutate only the JSON receipt or reuse a stale request hash. Pin and validate the full canonical chain and independent Godot receipts.

For each of the five selectors, use a baseline seed pair and single-domain mutations:

| Variant | gameplay seed | music seed |
|---|---:|---:|
| Baseline | `12345` | `840001` |
| Gameplay-only mutation | `54321` | `840001` |
| Music-only mutation | `12345` | `840002` |

Repeat each variant in an independent Godot process: target `5 selectors × 3 variants × 2 repeats = 30` invocations. The implementation must derive request/plan/binding identity through canonical functions, not by hand-editing hashes. If canonical request construction or timing-reference joining cannot be regenerated for a seed mutation, fail closed and implement that request-bound extension first rather than weakening joins.

Expected behavior must be specified against the true data layers:

- Gameplay seed mutation: request identity changes and the bound gameplay/style/visual-content projection must show seed sensitivity for every selector; independent repeats match.
- Music seed mutation: request/binding identity changes, while the gameplay-derived parameter projection, variation recipe, palette and visual-spec projection remain identical when gameplay seed is unchanged.
- The outer V2 exact-selector payload includes full `request_identity`, including seed fields. Therefore the envelope/payload-instance digest may change when only `music_seed` changes. Do **not** incorrectly require the entire request-bound payload digest to remain identical; use explicit hashes of the visual-content subprojection to prove orthogonality.
- Invalid, missing, null, implicit/automatic, wrong-type, out-of-range and equal numeric cross-domain seeds remain negative pre-Godot cases. `master_seed=NOT_ADOPTED`; automatic/default generation stays disabled until a separately specified policy is approved and proven.

Only after the new audit passes should the candidate I/O seed group be re-evaluated with fresh source pins. Challenge seed coverage and the other four Visual Loop families remain separate populations.

## 6. Locked governance state

`renderer=OFF`; `candidate_input_admissible=false`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `D9.10=PREPARE_ONLY`; baseline approval missing; freeze eligibility false; `D9.17=BLOCKED_NO_GO`; D10 blocked. C11-C 2.19.12 and its manifest remain immutable. No cutover is authorized.
